import os
import threading

import pytest

from app.config import Config
from app.models.project import ProjectManager
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
    interview_path = os.path.join(run_dir, "interviews.json")
    narrative_summary_path = os.path.join(run_dir, "narrative_summary.json")
    template_path = ProjectManager.get_strategy_lab_artifact_path(project_id, "lane_templates.json")

    ProjectManager.save_strategy_lab_artifact(
        project_id,
        os.path.join("runs", lane_template.lane_id, run_status.run_id, "interviews.json"),
        {
            "lane_id": lane_template.lane_id,
            "run_id": run_status.run_id,
            "transcript_markdown": f"{lane_template.display_name} transcript",
            "created_at": run_status.created_at,
        },
    )
    ProjectManager.save_strategy_lab_artifact(
        project_id,
        os.path.join("runs", lane_template.lane_id, run_status.run_id, "narrative_summary.json"),
        {
            "lane_id": lane_template.lane_id,
            "run_id": run_status.run_id,
            "summary_markdown": f"{lane_template.display_name} narrative summary",
            "created_at": run_status.created_at,
        },
    )

    metrics = {}
    for dimension in lane_template.scorecard_dimensions:
        if dimension == "failure_modes":
            metrics[dimension] = LaneMetricResult(
                dimension=dimension,
                score="High",
                judgment=f"{dimension} judgment",
                source_label=AnalysisSourceLabel.NARRATIVE_SIMULATION,
                citation_ids=[f"{lane_template.lane_id}:narrative:summary"],
                citations=[
                    CitationRecord(
                        chunk_id=None,
                        filename="narrative_summary.json",
                        locator="summary_markdown",
                        quote=f"{lane_template.display_name} narrative summary",
                        source_label=AnalysisSourceLabel.NARRATIVE_SIMULATION,
                        source_kind="narrative_summary",
                        source_path=narrative_summary_path,
                    )
                ],
            )
        elif dimension in {"durability_12_24m", "capability_fit"}:
            metrics[dimension] = LaneMetricResult(
                dimension=dimension,
                score="Medium",
                judgment=f"{dimension} judgment",
                source_label=AnalysisSourceLabel.PRIVATE_ANALYSIS,
                citation_ids=[f"{lane_template.lane_id}:private:template"],
                citations=[
                    CitationRecord(
                        chunk_id=None,
                        filename="lane_templates.json",
                        locator=f"lane_template:{lane_template.lane_id}",
                        quote=lane_template.hypothesis,
                        source_label=AnalysisSourceLabel.PRIVATE_ANALYSIS,
                        source_kind="lane_template",
                        source_path=template_path,
                    )
                ],
            )
        else:
            metrics[dimension] = LaneMetricResult(
                dimension=dimension,
                score="Medium",
                judgment=f"{dimension} judgment",
                source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                citation_ids=[f"{lane_template.lane_id}:research:01"],
                citations=[
                    CitationRecord(
                        chunk_id=f"{lane_template.lane_id}-chunk-0001",
                        filename=f"{lane_template.lane_id}.md",
                        locator="paragraph:1 -> paragraph:1",
                        quote=f"Evidence for {lane_template.lane_id}",
                        episode_uuid=f"ep-{lane_template.lane_id}",
                        source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                        source_kind="research_chunk",
                    )
                ],
            )

    scorecard = LaneScorecard(
        lane_id=lane_template.lane_id,
        display_name=lane_template.display_name,
        summary=f"{lane_template.display_name} summary",
        metrics=metrics,
    )

    ProjectManager.save_strategy_lab_artifact(
        project_id,
        os.path.join("runs", lane_template.lane_id, run_status.run_id, "private_analysis.json"),
        scorecard.to_dict(),
    )

    run_status.status = "completed"
    run_status.artifact_paths = {
        "private_analysis_json": analysis_path,
        "status": status_path,
        "interviews": interview_path,
        "narrative_summary_json": narrative_summary_path,
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
    for template in templates:
        assert template.required_citations
        assert template.expected_narrative_outputs
        assert template.expected_final_outputs


def test_strategy_lab_service_composes_comparative_report_with_mixed_provenance(
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

    defense_row = next(row for row in report.rows if row["lane_id"] == "defense-government-entry")
    defense_labels = {metric["source_label"] for metric in defense_row["metrics"].values()}
    assert "research_citation" in defense_labels
    assert "private_analysis" in defense_labels
    assert "narrative_simulation" in defense_labels

    narrative_payload = StrategyLabService.inspect_source(
        project.project_id,
        "defense-government-entry:narrative:summary",
    )
    assert narrative_payload["source"]["kind"] == "narrative_summary"
    assert narrative_payload["source"]["artifact"]["lane_id"] == "defense-government-entry"

    research_payload = StrategyLabService.inspect_source(
        project.project_id,
        "defense-government-entry:research:01",
    )
    assert research_payload["source"]["chunk"]["episode_uuid"] == "ep-defense-government-entry"


def test_strategy_lab_service_requires_narrative_artifacts_before_private_analysis(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )
    template = next(
        item
        for item in StrategyLabService.seed_lane_templates(project.project_id)
        if item.lane_id == "defense-government-entry"
    )

    run_status, _ = StrategyLabService.prepare_lane_run(project.project_id, template.lane_id)

    with pytest.raises(ValueError, match="narrative"):
        StrategyLabService._execute_private_analysis(
            project.project_id,
            "graph-1",
            template.lane_id,
            run_status,
        )


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

    def fake_generate(
        self,
        lane_template,
        interviews_markdown=None,
        narrative_summary=None,
        monte_carlo_attachment=None,
        interview_source_path=None,
        narrative_source_path=None,
    ):
        return (
            LaneScorecard(
                lane_id=lane_template.lane_id,
                display_name=lane_template.display_name,
                summary="summary",
                metrics={
                    "time_to_cash": LaneMetricResult(
                        dimension="time_to_cash",
                        score="Medium",
                        judgment="time_to_cash judgment",
                        source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                        citation_ids=["defense-government-entry:research:01"],
                        citations=[
                            CitationRecord(
                                chunk_id="defense-government-entry-chunk-0001",
                                filename="defense.md",
                                locator="paragraph:1 -> paragraph:1",
                                quote="Defense buyers need partner access and evidence.",
                                episode_uuid="ep-defense",
                                source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                            )
                        ],
                    ),
                    "durability_12_24m": LaneMetricResult(
                        dimension="durability_12_24m",
                        score="Medium",
                        judgment="durability judgment",
                        source_label=AnalysisSourceLabel.PRIVATE_ANALYSIS,
                        citation_ids=["defense-government-entry:private:template"],
                        citations=[
                            CitationRecord(
                                chunk_id=None,
                                filename="lane_templates.json",
                                locator="lane_template:defense-government-entry",
                                quote="Selective government and defense work can diversify revenue while increasing compliance burden.",
                                source_label=AnalysisSourceLabel.PRIVATE_ANALYSIS,
                                source_kind="lane_template",
                                source_path=ProjectManager.get_strategy_lab_artifact_path(project.project_id, "lane_templates.json"),
                            )
                        ],
                    ),
                    "capability_fit": LaneMetricResult(
                        dimension="capability_fit",
                        score="Medium",
                        judgment="capability fit judgment",
                        source_label=AnalysisSourceLabel.PRIVATE_ANALYSIS,
                        citation_ids=["defense-government-entry:private:template"],
                        citations=[
                            CitationRecord(
                                chunk_id=None,
                                filename="lane_templates.json",
                                locator="lane_template:defense-government-entry",
                                quote="Selective government and defense work can diversify revenue while increasing compliance burden.",
                                source_label=AnalysisSourceLabel.PRIVATE_ANALYSIS,
                                source_kind="lane_template",
                                source_path=ProjectManager.get_strategy_lab_artifact_path(project.project_id, "lane_templates.json"),
                            )
                        ],
                    ),
                    "required_investment": LaneMetricResult(
                        dimension="required_investment",
                        score="Medium",
                        judgment="required investment judgment",
                        source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                        citation_ids=["defense-government-entry:research:01"],
                        citations=[
                            CitationRecord(
                                chunk_id="defense-government-entry-chunk-0001",
                                filename="defense.md",
                                locator="paragraph:1 -> paragraph:1",
                                quote="Defense buyers need partner access and evidence.",
                                episode_uuid="ep-defense",
                                source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                            )
                        ],
                    ),
                    "failure_modes": LaneMetricResult(
                        dimension="failure_modes",
                        score="High",
                        judgment="failure modes judgment",
                        source_label=AnalysisSourceLabel.NARRATIVE_SIMULATION,
                        citation_ids=["defense-government-entry:narrative:summary"],
                        citations=[
                            CitationRecord(
                                chunk_id=None,
                                filename="narrative_summary.json",
                                locator="summary_markdown",
                                quote="Narrative summary",
                                source_label=AnalysisSourceLabel.NARRATIVE_SIMULATION,
                                source_kind="narrative_summary",
                                source_path=narrative_source_path,
                            )
                        ],
                    ),
                    "evidence_strength": LaneMetricResult(
                        dimension="evidence_strength",
                        score="Medium",
                        judgment="evidence strength judgment",
                        source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                        citation_ids=["defense-government-entry:research:01"],
                        citations=[
                            CitationRecord(
                                chunk_id="defense-government-entry-chunk-0001",
                                filename="defense.md",
                                locator="paragraph:1 -> paragraph:1",
                                quote="Defense buyers need partner access and evidence.",
                                episode_uuid="ep-defense",
                                source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                            )
                        ],
                    ),
                },
            ),
            {},
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
    assert os.path.exists(
        os.path.join(
            ProjectManager.get_strategy_lab_artifact_path(project.project_id, "runs"),
            template.lane_id,
            analysis_run.run_id,
            "private_analysis.json",
        )
    )


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
