import os
import threading

from app.models.project import ProjectManager
from app.config import Config
from app.models.strategy_lab import (
    AnalysisSourceLabel,
    CitationRecord,
    LaneMetricResult,
    LaneScorecard,
    WorkflowMode,
)
from app.services.private_analysis_agent import PrivateAnalysisAgent
from app.services.strategy_lab import StrategyLabService


def _write_completed_scorecard(project_id, lane_template):
    run_status = StrategyLabService._create_run_status(project_id, lane_template.lane_id)
    run_dir = StrategyLabService._run_dir(project_id, lane_template.lane_id, run_status.run_id)
    status_path = os.path.join(run_dir, "status.json")
    analysis_path = os.path.join(run_dir, "private_analysis.json")

    citation_id = f"{lane_template.lane_id}:citation:01"
    scorecard = LaneScorecard(
        lane_id=lane_template.lane_id,
        display_name=lane_template.display_name,
        summary=f"{lane_template.display_name} summary",
        metrics={
            dimension: LaneMetricResult(
                dimension=dimension,
                score="Medium",
                judgment=f"{dimension} judgment",
                source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                citation_ids=[citation_id],
                citations=[
                    CitationRecord(
                        chunk_id=f"{lane_template.lane_id}-chunk-0001",
                        filename=f"{lane_template.lane_id}.md",
                        locator="paragraph:1 -> paragraph:1",
                        quote=f"Evidence for {lane_template.lane_id}",
                        episode_uuid=f"ep-{lane_template.lane_id}",
                        source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                    )
                ],
            )
            for dimension in lane_template.scorecard_dimensions
        },
    )

    ProjectManager.save_strategy_lab_artifact(
        project_id,
        os.path.join(
            "runs",
            lane_template.lane_id,
            run_status.run_id,
            "private_analysis.json",
        ),
        scorecard.to_dict(),
    )

    run_status.status = "completed"
    run_status.artifact_paths = {
        "private_analysis_json": analysis_path,
        "status": status_path,
    }
    StrategyLabService._atomic_write_json(status_path, run_status.to_dict())


def test_strategy_lab_service_seeds_required_templates(monkeypatch, tmp_path):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )

    templates = StrategyLabService.seed_lane_templates(project.project_id)

    assert len(templates) == 5
    assert {template.lane_id for template in templates} == set(StrategyLabService.REQUIRED_LANE_IDS)


def test_strategy_lab_service_composes_comparative_report_with_provenance(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    monkeypatch.setattr(Config, "LLM_API_KEY", "test-key")
    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )

    templates = StrategyLabService.seed_lane_templates(project.project_id)
    ProjectManager.save_strategy_lab_artifact(
        project.project_id,
        "chunk_manifest.json",
        [
            {
                "chunk_id": f"{template.lane_id}-chunk-0001",
                "document_id": f"doc-{index}",
                "filename": f"{template.lane_id}.md",
                "text": f"Evidence for {template.display_name}",
                "start_char": 0,
                "end_char": 24,
                "locator_start": "paragraph:1",
                "locator_end": "paragraph:1",
                "episode_uuid": f"ep-{template.lane_id}",
            }
            for index, template in enumerate(templates, start=1)
        ],
    )

    for template in templates:
        _write_completed_scorecard(project.project_id, template)

    report = StrategyLabService.compose_comparative_report(project.project_id)

    assert len(report.rows) == 5
    assert "Defense / Government Entry" in report.markdown_summary

    first_citation_id = next(iter(report.citations))
    source_payload = StrategyLabService.inspect_source(project.project_id, first_citation_id)
    assert source_payload["chunk"]["episode_uuid"].startswith("ep-")


def test_strategy_lab_service_reuses_active_run_and_creates_new_rerun_dir(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    monkeypatch.setattr(Config, "LLM_API_KEY", "test-key")
    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )

    templates = StrategyLabService.seed_lane_templates(project.project_id)
    template = next(item for item in templates if item.lane_id == "defense-government-entry")
    ProjectManager.save_strategy_lab_artifact(
        project.project_id,
        "chunk_manifest.json",
        [
            {
                "chunk_id": "defense-government-entry-chunk-0001",
                "document_id": "doc-1",
                "filename": "defense.md",
                "text": "Defense buyers need partner access and evidence.",
                "start_char": 0,
                "end_char": 48,
                "locator_start": "paragraph:1",
                "locator_end": "paragraph:1",
                "episode_uuid": "ep-defense",
            }
        ],
    )

    def fake_generate(self, lane_template, interviews_markdown=None, narrative_summary=None, monte_carlo_attachment=None):
        citation_id = f"{lane_template.lane_id}:citation:01"
        return (
            LaneScorecard(
                lane_id=lane_template.lane_id,
                display_name=lane_template.display_name,
                summary="summary",
                metrics={
                    dimension: LaneMetricResult(
                        dimension=dimension,
                        score="Medium",
                        judgment=f"{dimension} judgment",
                        source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                        citation_ids=[citation_id],
                        citations=[
                            CitationRecord(
                                chunk_id="defense-government-entry-chunk-0001",
                                filename="defense.md",
                                locator="paragraph:1 -> paragraph:1",
                                quote="Defense buyers need partner access and evidence.",
                                episode_uuid="ep-defense",
                            )
                        ],
                    )
                    for dimension in lane_template.scorecard_dimensions
                },
            ),
            {
                citation_id: CitationRecord(
                    chunk_id="defense-government-entry-chunk-0001",
                    filename="defense.md",
                    locator="paragraph:1 -> paragraph:1",
                    quote="Defense buyers need partner access and evidence.",
                    episode_uuid="ep-defense",
                )
            },
        )

    monkeypatch.setattr(PrivateAnalysisAgent, "generate_scorecard", fake_generate)
    monkeypatch.setattr(PrivateAnalysisAgent, "scorecard_to_markdown", lambda self, scorecard: "# scorecard\n")

    run_status, lane_context = StrategyLabService.prepare_lane_run(project.project_id, template.lane_id)
    StrategyLabService.attach_simulation(
        project.project_id,
        template.lane_id,
        run_status.run_id,
        "sim-1",
    )
    StrategyLabService.attach_interview_artifacts(
        project.project_id,
        template.lane_id,
        run_status.run_id,
        os.path.join(os.path.dirname(lane_context.lane_context_path), "interviews.json"),
        os.path.join(os.path.dirname(lane_context.lane_context_path), "narrative_summary.json"),
    )
    ProjectManager.save_strategy_lab_artifact(
        project.project_id,
        os.path.join("runs", template.lane_id, run_status.run_id, "interviews.json"),
        {
            "lane_id": template.lane_id,
            "run_id": run_status.run_id,
            "transcript_markdown": "Real interview transcript",
            "created_at": run_status.created_at,
        },
    )
    ProjectManager.save_strategy_lab_artifact(
        project.project_id,
        os.path.join("runs", template.lane_id, run_status.run_id, "narrative_summary.json"),
        {
            "lane_id": template.lane_id,
            "run_id": run_status.run_id,
            "summary_markdown": "Narrative summary",
            "created_at": run_status.created_at,
        },
    )

    analysis_run = StrategyLabService._analysis_run_status(project.project_id, template.lane_id)
    assert analysis_run.run_id == run_status.run_id

    StrategyLabService._execute_private_analysis(
        project.project_id,
        "graph-1",
        template.lane_id,
        analysis_run,
    )

    rerun = StrategyLabService._analysis_run_status(project.project_id, template.lane_id)
    assert rerun.run_id != analysis_run.run_id
    assert os.path.exists(os.path.join(ProjectManager.get_strategy_lab_artifact_path(project.project_id, "runs"), template.lane_id, analysis_run.run_id, "private_analysis.json"))


def test_strategy_lab_service_rejects_duplicate_overlapping_lane_runs(monkeypatch, tmp_path):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )

    key = StrategyLabService._lane_lock_key(project.project_id, "defense-government-entry")
    lock = StrategyLabService._lane_locks.setdefault(key, threading.Lock())
    acquired = lock.acquire(blocking=False)
    assert acquired is True
    try:
        try:
            StrategyLabService._acquire_lane_lock_or_raise(project.project_id, "defense-government-entry")
        except ValueError as exc:
            assert "拒绝重复提交" in str(exc)
        else:  # pragma: no cover - defensive
            raise AssertionError("expected duplicate lane run rejection")
    finally:
        if lock.locked():
            lock.release()
