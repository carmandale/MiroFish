import json

from app.models.project import ProjectManager
from app.models.strategy_lab import WorkflowMode
from app.services.private_analysis_agent import PrivateAnalysisAgent
from app.services.strategy_lab import StrategyLabService


class FakeLLMClient:
    def __init__(self, payload):
        self.payload = payload

    def chat_json(self, messages, temperature, max_tokens):
        return json.loads(json.dumps(self.payload))


def test_private_analysis_agent_generates_scorecard_without_simulation_id(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )

    ProjectManager.save_strategy_lab_artifact(
        project.project_id,
        "chunk_manifest.json",
        [
            {
                "chunk_id": "chunk-1",
                "document_id": "doc-1",
                "filename": "defense.docx",
                "text": "Defense buyers require past performance and vehicle access.",
                "start_char": 0,
                "end_char": 58,
                "locator_start": "paragraph:1",
                "locator_end": "paragraph:1",
                "episode_uuid": "ep-1",
            },
            {
                "chunk_id": "chunk-2",
                "document_id": "doc-1",
                "filename": "defense.docx",
                "text": "Federal entry often needs up-front BD investment and partner strategy.",
                "start_char": 59,
                "end_char": 125,
                "locator_start": "paragraph:2",
                "locator_end": "paragraph:2",
                "episode_uuid": "ep-2",
            },
        ],
    )

    lane_template = next(
        template
        for template in StrategyLabService.default_lane_templates()
        if template.lane_id == "defense-government-entry"
    )

    payload = {
        "summary": "Defense work is attractive but gated by compliance and access.",
        "assumptions": ["Groove Jones pursues selective partner-led entry."],
        "caveats": ["No Monte Carlo attachment in v1."],
        "metrics": {
            dimension: {
                "score": "Medium",
                "judgment": f"{dimension} judged from cited research.",
                "source_label": "research_citation",
                "citation_ids": ["defense-government-entry:citation:01"],
                "monte_carlo_attachment": None,
            }
            for dimension in lane_template.scorecard_dimensions
        },
    }

    agent = PrivateAnalysisAgent(
        project_id=project.project_id,
        graph_id="graph-1",
        llm_client=FakeLLMClient(payload),
    )
    scorecard, citations = agent.generate_scorecard(lane_template)

    assert scorecard.lane_id == "defense-government-entry"
    assert scorecard.display_name == "Defense / Government Entry"
    assert "time_to_cash" in scorecard.metrics
    assert citations["defense-government-entry:citation:01"].episode_uuid == "ep-1"
