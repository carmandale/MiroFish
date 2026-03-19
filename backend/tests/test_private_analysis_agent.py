import json

import pytest

from app.models.project import ProjectManager
from app.models.strategy_lab import WorkflowMode
from app.services.private_analysis_agent import PrivateAnalysisAgent
from app.services.strategy_lab import StrategyLabService


class FakeLLMClient:
    def __init__(self, payload):
        self.payload = payload

    def chat_json(self, messages, temperature, max_tokens):
        return json.loads(json.dumps(self.payload))


def _create_project_with_manifest(monkeypatch, tmp_path):
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))
    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )
    StrategyLabService.seed_lane_templates(project.project_id)
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
    return project, lane_template


def test_private_analysis_agent_generates_mixed_source_scorecard_without_simulation_id(
    monkeypatch,
    tmp_path,
):
    project, lane_template = _create_project_with_manifest(monkeypatch, tmp_path)

    payload = {
        "summary": "Defense work is attractive but gated by compliance and access.",
        "assumptions": ["Groove Jones pursues selective partner-led entry."],
        "caveats": ["No Monte Carlo attachment in v1."],
        "metrics": {
            "time_to_cash": {
                "score": "Medium",
                "judgment": "time_to_cash judged from cited research.",
                "source_label": "research_citation",
                "citation_ids": ["defense-government-entry:research:01"],
                "monte_carlo_attachment": None,
            },
            "durability_12_24m": {
                "score": "Medium",
                "judgment": "durability judged from the lane template and internal gates.",
                "source_label": "private_analysis",
                "citation_ids": ["defense-government-entry:private:template"],
                "monte_carlo_attachment": None,
            },
            "capability_fit": {
                "score": "Medium",
                "judgment": "capability fit judged from the lane template and internal gates.",
                "source_label": "private_analysis",
                "citation_ids": ["defense-government-entry:private:template"],
                "monte_carlo_attachment": None,
            },
            "required_investment": {
                "score": "Medium",
                "judgment": "required investment judged from cited research.",
                "source_label": "research_citation",
                "citation_ids": ["defense-government-entry:research:02"],
                "monte_carlo_attachment": None,
            },
            "failure_modes": {
                "score": "High",
                "judgment": "failure modes surfaced in the narrative capture.",
                "source_label": "narrative_simulation",
                "citation_ids": ["defense-government-entry:narrative:summary"],
                "monte_carlo_attachment": None,
            },
            "evidence_strength": {
                "score": "Medium",
                "judgment": "evidence strength judged from cited research.",
                "source_label": "research_citation",
                "citation_ids": ["defense-government-entry:research:01"],
                "monte_carlo_attachment": None,
            },
        },
    }

    agent = PrivateAnalysisAgent(
        project_id=project.project_id,
        graph_id="graph-1",
        llm_client=FakeLLMClient(payload),
    )
    scorecard, citations = agent.generate_scorecard(
        lane_template,
        narrative_summary="Narrative summary from captured interviews.",
    )

    assert scorecard.lane_id == "defense-government-entry"
    assert scorecard.display_name == "Defense / Government Entry"
    assert scorecard.metrics["failure_modes"].source_label.value == "narrative_simulation"
    assert scorecard.metrics["capability_fit"].source_label.value == "private_analysis"
    assert citations["defense-government-entry:research:01"].episode_uuid == "ep-1"
    assert citations["defense-government-entry:private:template"].source_kind == "lane_template"


def test_private_analysis_agent_rejects_all_research_labels_when_narrative_exists(
    monkeypatch,
    tmp_path,
):
    project, lane_template = _create_project_with_manifest(monkeypatch, tmp_path)

    payload = {
        "summary": "All-research payload should fail when narrative inputs exist.",
        "assumptions": [],
        "caveats": [],
        "metrics": {
            dimension: {
                "score": "Medium",
                "judgment": f"{dimension} judged from cited research.",
                "source_label": "research_citation",
                "citation_ids": ["defense-government-entry:research:01"],
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

    with pytest.raises(ValueError, match="narrative_simulation"):
        agent.generate_scorecard(
            lane_template,
            narrative_summary="Narrative summary from captured interviews.",
        )


def test_private_analysis_agent_filters_mixed_citations_to_declared_source(
    monkeypatch,
    tmp_path,
):
    project, lane_template = _create_project_with_manifest(monkeypatch, tmp_path)

    payload = {
        "summary": "Mixed-source metrics should normalize to the declared source label.",
        "assumptions": [],
        "caveats": [],
        "metrics": {
            "time_to_cash": {
                "score": "Medium",
                "judgment": "time_to_cash judged from cited research.",
                "source_label": "research_citation",
                "citation_ids": ["defense-government-entry:research:01"],
                "monte_carlo_attachment": None,
            },
            "durability_12_24m": {
                "score": "Medium",
                "judgment": "durability judged from the lane template and internal gates.",
                "source_label": "private_analysis",
                "citation_ids": ["defense-government-entry:private:template"],
                "monte_carlo_attachment": None,
            },
            "capability_fit": {
                "score": "Medium",
                "judgment": "capability fit judged from the lane template and internal gates.",
                "source_label": "private_analysis",
                "citation_ids": ["defense-government-entry:private:template"],
                "monte_carlo_attachment": None,
            },
            "required_investment": {
                "score": "Medium",
                "judgment": "required investment judged from cited research.",
                "source_label": "research_citation",
                "citation_ids": ["defense-government-entry:research:02"],
                "monte_carlo_attachment": None,
            },
            "failure_modes": {
                "score": "High",
                "judgment": "failure modes surfaced in the narrative capture.",
                "source_label": "narrative_simulation",
                "citation_ids": ["defense-government-entry:narrative:summary"],
                "monte_carlo_attachment": None,
            },
            "evidence_strength": {
                "score": "Medium",
                "judgment": "evidence strength uses research as the cell source and should drop stray citations.",
                "source_label": "research_citation",
                "citation_ids": [
                    "defense-government-entry:research:01",
                    "defense-government-entry:private:template",
                    "defense-government-entry:narrative:summary",
                ],
                "monte_carlo_attachment": None,
            },
        },
    }

    agent = PrivateAnalysisAgent(
        project_id=project.project_id,
        graph_id="graph-1",
        llm_client=FakeLLMClient(payload),
    )

    scorecard, _ = agent.generate_scorecard(
        lane_template,
        narrative_summary="Narrative summary from captured interviews.",
    )

    assert scorecard.metrics["evidence_strength"].source_label.value == "research_citation"
    assert scorecard.metrics["evidence_strength"].citation_ids == [
        "defense-government-entry:research:01"
    ]
    assert len(scorecard.metrics["evidence_strength"].citations) == 1
