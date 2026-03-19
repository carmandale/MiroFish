import json
import os

from app import create_app
from app.config import Config
from app.models.project import ProjectManager
from app.models.strategy_lab import LaneRunContext, WorkflowMode
from app.services.simulation_config_generator import SimulationConfigGenerator, SimulationParameters
from app.services.simulation_manager import SimulationManager
from app.services.strategy_lab import StrategyLabService
from app.services.zep_entity_reader import FilteredEntities


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    LLM_API_KEY = "test-key"
    ZEP_API_KEY = "test-zep"
    CORS_ALLOWED_ORIGINS = ["https://allowed.example"]


class FakeEntity:
    def __init__(self, uuid, name, entity_type, summary):
        self.uuid = uuid
        self.name = name
        self._entity_type = entity_type
        self.summary = summary

    def get_entity_type(self):
        return self._entity_type


class FakeProfileGenerator:
    def __init__(self, graph_id=None):
        self.graph_id = graph_id

    def generate_profiles_from_entities(self, entities, **kwargs):
        return [
            {
                "agent_id": index,
                "entity_uuid": entity.uuid,
                "entity_name": entity.name,
                "entity_type": entity.get_entity_type(),
                "influence_weight": 2.0 - (index * 0.1),
                "activity_level": 0.7,
            }
            for index, entity in enumerate(entities)
        ]

    def save_profiles(self, profiles, file_path, platform):
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(profiles, handle, ensure_ascii=False, indent=2)


class FakeConfigGenerator:
    def generate_config(
        self,
        simulation_id,
        project_id,
        graph_id,
        simulation_requirement,
        document_text,
        entities,
        enable_twitter=True,
        enable_reddit=True,
        progress_callback=None,
        lane_context=None,
    ):
        return SimulationParameters(
            simulation_id=simulation_id,
            project_id=project_id,
            graph_id=graph_id,
            simulation_requirement=simulation_requirement,
            workflow_mode=lane_context.workflow_mode.value if lane_context else WorkflowMode.DEFAULT.value,
            lane_id=lane_context.lane_id if lane_context else None,
            lane_context_path=lane_context.lane_context_path if lane_context else None,
            prompt_framing=(
                f"strategy_lab:{lane_context.lane_id}:public_discourse_only"
                if lane_context
                else "default_social_discourse"
            ),
        )


def _create_app_with_tmp_dirs(monkeypatch, tmp_path):
    projects_dir = tmp_path / "projects"
    simulations_dir = tmp_path / "simulations"
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(projects_dir))
    monkeypatch.setattr(SimulationManager, "SIMULATION_DATA_DIR", str(simulations_dir))
    monkeypatch.setattr(Config, "OASIS_SIMULATION_DATA_DIR", str(simulations_dir))
    app = create_app(TestConfig)
    return app, projects_dir, simulations_dir


def test_default_workflow_create_simulation_still_allows_no_lane_id(monkeypatch, tmp_path):
    app, _, _ = _create_app_with_tmp_dirs(monkeypatch, tmp_path)
    client = app.test_client()

    project = ProjectManager.create_project(name="Default")
    project.graph_id = "graph-default"
    ProjectManager.save_project(project)

    response = client.post(
        "/api/simulation/create",
        json={"project_id": project.project_id},
    )

    payload = response.get_json()
    assert response.status_code == 200
    assert payload["data"]["workflow_mode"] == "default"
    assert payload["data"]["lane_id"] is None


def test_strategy_lab_create_simulation_requires_lane_id_and_persists_metadata(monkeypatch, tmp_path):
    app, _, _ = _create_app_with_tmp_dirs(monkeypatch, tmp_path)
    client = app.test_client()

    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )
    project.graph_id = "graph-1"
    ProjectManager.save_project(project)
    StrategyLabService.seed_lane_templates(project.project_id)

    missing_lane = client.post(
        "/api/simulation/create",
        json={"project_id": project.project_id},
    )
    assert missing_lane.status_code == 400

    response = client.post(
        "/api/simulation/create",
        json={
            "project_id": project.project_id,
            "lane_id": "defense-government-entry",
        },
    )

    payload = response.get_json()["data"]
    assert response.status_code == 200
    assert payload["workflow_mode"] == "strategy_lab"
    assert payload["lane_id"] == "defense-government-entry"
    assert payload["lane_context_path"].endswith("lane_context.json")
    assert os.path.exists(payload["lane_context_path"])

    lane_status = StrategyLabService.get_lane_status(project.project_id, "defense-government-entry")
    assert lane_status.artifact_paths["simulation_id"] == payload["simulation_id"]


def test_simulation_prepare_serializes_strategy_lab_metadata(monkeypatch, tmp_path):
    _app, _, simulations_dir = _create_app_with_tmp_dirs(monkeypatch, tmp_path)
    monkeypatch.setattr("app.services.simulation_manager.ZepEntityReader", type("FakeReader", (), {
        "filter_defined_entities": lambda self, graph_id, defined_entity_types=None, enrich_with_edges=True: FilteredEntities(
            entities=[FakeEntity("ent-1", "Prime Partner", "Organization", "Partner signal")],
            entity_types={"Organization"},
            total_count=1,
            filtered_count=1,
        )
    }))
    monkeypatch.setattr("app.services.simulation_manager.OasisProfileGenerator", FakeProfileGenerator)
    monkeypatch.setattr("app.services.simulation_manager.SimulationConfigGenerator", FakeConfigGenerator)

    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )
    project.graph_id = "graph-1"
    project.simulation_requirement = "Compare strategic lanes."
    ProjectManager.save_project(project)
    StrategyLabService.seed_lane_templates(project.project_id)

    run_status, lane_context = StrategyLabService.prepare_lane_run(
        project.project_id,
        "defense-government-entry",
    )
    manager = SimulationManager()
    state = manager.create_simulation(
        project_id=project.project_id,
        graph_id="graph-1",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
        lane_id="defense-government-entry",
        lane_context_path=lane_context.lane_context_path,
    )
    StrategyLabService.attach_simulation(project.project_id, "defense-government-entry", run_status.run_id, state.simulation_id)

    result = manager.prepare_simulation(
        simulation_id=state.simulation_id,
        simulation_requirement=project.simulation_requirement,
        document_text="Defense lane public discourse source text.",
        lane_context=lane_context,
    )

    config_path = simulations_dir / state.simulation_id / "simulation_config.json"
    saved = json.loads(config_path.read_text(encoding="utf-8"))
    assert result.status.value == "ready"
    assert saved["workflow_mode"] == "strategy_lab"
    assert saved["lane_id"] == "defense-government-entry"
    assert saved["lane_context_path"] == lane_context.lane_context_path
    assert "public_discourse_only" in saved["prompt_framing"]


def test_strategy_lab_close_env_captures_interviews_before_teardown(monkeypatch, tmp_path):
    app, _, simulations_dir = _create_app_with_tmp_dirs(monkeypatch, tmp_path)
    client = app.test_client()

    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )
    project.graph_id = "graph-1"
    ProjectManager.save_project(project)
    StrategyLabService.seed_lane_templates(project.project_id)

    create_response = client.post(
        "/api/simulation/create",
        json={"project_id": project.project_id, "lane_id": "defense-government-entry"},
    )
    simulation_payload = create_response.get_json()["data"]
    simulation_id = simulation_payload["simulation_id"]
    lane_context_path = simulation_payload["lane_context_path"]
    run_id = os.path.basename(os.path.dirname(lane_context_path))

    sim_dir = simulations_dir / simulation_id
    sim_dir.mkdir(parents=True, exist_ok=True)
    (sim_dir / "simulation_config.json").write_text(
        json.dumps(
            {
                "agent_configs": [
                    {"agent_id": 3, "entity_name": "Prime Partner", "entity_type": "Organization", "influence_weight": 2.0, "activity_level": 0.8},
                    {"agent_id": 4, "entity_name": "Analyst", "entity_type": "Person", "influence_weight": 1.8, "activity_level": 0.7},
                    {"agent_id": 5, "entity_name": "Competitor", "entity_type": "Organization", "influence_weight": 1.6, "activity_level": 0.6},
                ]
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("app.api.simulation.SimulationRunner.check_env_alive", lambda simulation_id: True)
    monkeypatch.setattr(
        "app.api.simulation.SimulationRunner.interview_agents_batch",
        lambda simulation_id, interviews, platform=None, timeout=180.0: {
            "success": True,
            "result": {
                "results": {
                    "twitter_3": {"response": "Twitter says partner access matters."},
                    "reddit_3": {"response": "Reddit says award timing matters."},
                    "twitter_4": {"response": "Twitter says analysts watch public traction."},
                    "reddit_4": {"response": "Reddit says analysts watch risk."},
                    "twitter_5": {"response": "Twitter says incumbents will challenge."},
                    "reddit_5": {"response": "Reddit says incumbents can squeeze margin."},
                }
            },
        },
    )
    monkeypatch.setattr(
        "app.api.simulation.SimulationRunner.close_simulation_env",
        lambda simulation_id, timeout=30: {"success": True, "message": "closed"},
    )

    response = client.post(
        "/api/simulation/close-env",
        json={"simulation_id": simulation_id},
    )

    payload = response.get_json()["data"]
    assert response.status_code == 200
    assert payload["interview_captured"] is True

    lane_status = StrategyLabService.get_lane_status(project.project_id, "defense-government-entry")
    assert lane_status.stage == "narrative_captured"
    interviews_path = lane_status.artifact_paths["interviews"]
    with open(interviews_path, "r", encoding="utf-8") as handle:
        interviews_payload = json.load(handle)
    assert interviews_payload["interview_count"] == 3
    assert "Prime Partner" in interviews_payload["transcript_markdown"]
    assert os.path.exists(lane_status.artifact_paths["narrative_summary_json"])
    assert os.path.basename(os.path.dirname(interviews_path)) == run_id


def test_strategy_lab_close_env_fails_cleanly_when_env_not_alive(monkeypatch, tmp_path):
    app, _, simulations_dir = _create_app_with_tmp_dirs(monkeypatch, tmp_path)
    client = app.test_client()

    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )
    project.graph_id = "graph-1"
    ProjectManager.save_project(project)
    StrategyLabService.seed_lane_templates(project.project_id)

    create_response = client.post(
        "/api/simulation/create",
        json={"project_id": project.project_id, "lane_id": "defense-government-entry"},
    )
    simulation_payload = create_response.get_json()["data"]
    simulation_id = simulation_payload["simulation_id"]
    lane_context_path = simulation_payload["lane_context_path"]
    sim_dir = simulations_dir / simulation_id
    sim_dir.mkdir(parents=True, exist_ok=True)
    (sim_dir / "simulation_config.json").write_text(json.dumps({"agent_configs": []}), encoding="utf-8")

    lane_status_before = StrategyLabService.get_lane_status(project.project_id, "defense-government-entry")

    monkeypatch.setattr("app.api.simulation.SimulationRunner.check_env_alive", lambda simulation_id: False)

    response = client.post(
        "/api/simulation/close-env",
        json={"simulation_id": simulation_id},
    )

    assert response.status_code == 400
    lane_status_after = StrategyLabService.get_lane_status(project.project_id, "defense-government-entry")
    assert lane_status_after.stage == lane_status_before.stage
    assert not os.path.exists(os.path.join(os.path.dirname(lane_context_path), "interviews.json"))


def test_strategy_lab_prompt_context_includes_public_discourse_framing():
    generator = object.__new__(SimulationConfigGenerator)
    generator.MAX_CONTEXT_LENGTH = 50000
    generator.ENTITIES_PER_TYPE_DISPLAY = 20
    generator.ENTITY_SUMMARY_LENGTH = 300

    lane_context = LaneRunContext(
        lane_id="defense-government-entry",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
        template_path="/tmp/lane_templates.json",
        lane_context_path="/tmp/lane_context.json",
        display_name="Defense / Government Entry",
        narrative_brief="Model public positioning pressure.",
        public_actor_classes=["prime_partners", "analysts"],
        public_event_classes=["award_announcement"],
        interview_personas=["procurement_officer"],
        procurement_gates=["vehicle_access"],
    )

    context = generator._build_context(
        simulation_requirement="Compare lanes",
        document_text="Source text",
        entities=[FakeEntity("ent-1", "Prime Partner", "Organization", "Summary")],
        lane_context=lane_context,
    )

    assert "public_discourse_only: true" in context
    assert "do not simulate procurement committees" in context
    assert "defense-government-entry" in context
