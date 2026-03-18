"""
Strategy Lab 项目级编排服务
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..models.project import ProjectManager
from ..models.strategy_lab import (
    AnalysisSourceLabel,
    CitationRecord,
    ComparativeReport,
    InterviewArtifact,
    LaneMetricResult,
    LaneRunContext,
    LaneRunStatus,
    LaneScorecard,
    LaneTemplate,
    WorkflowMode,
)
from ..utils.logger import get_logger
from .private_analysis_agent import PrivateAnalysisAgent

logger = get_logger("mirofish.strategy_lab")


class StrategyLabService:
    """管理策略路径模板、运行状态和对比报告"""

    REQUIRED_LANE_IDS = [
        "existing-client-maintenance-expansion",
        "healthcare-pharma-training-growth",
        "defense-government-entry",
        "spatial-enterprise-enablement",
        "selective-events-agency-partners",
    ]

    DEFAULT_SCORECARD_DIMENSIONS = [
        "time_to_cash",
        "durability_12_24m",
        "capability_fit",
        "required_investment",
        "failure_modes",
        "evidence_strength",
    ]

    _lane_locks: Dict[str, threading.Lock] = {}

    @classmethod
    def load_lane_templates(cls, project_id: str) -> List[LaneTemplate]:
        data = ProjectManager.load_strategy_lab_artifact(project_id, "lane_templates.json")
        if not data:
            return cls.seed_lane_templates(project_id)
        return [LaneTemplate.from_dict(item) for item in data]

    @classmethod
    def save_lane_templates(
        cls,
        project_id: str,
        templates: List[Dict[str, Any] | LaneTemplate],
    ) -> List[LaneTemplate]:
        lane_templates = [
            template if isinstance(template, LaneTemplate) else LaneTemplate.from_dict(template)
            for template in templates
        ]
        cls._validate_lane_templates(lane_templates)
        ProjectManager.save_strategy_lab_artifact(
            project_id,
            "lane_templates.json",
            [template.to_dict() for template in lane_templates],
        )
        return lane_templates

    @classmethod
    def seed_lane_templates(cls, project_id: str) -> List[LaneTemplate]:
        templates = cls.default_lane_templates()
        cls.save_lane_templates(project_id, templates)
        return templates

    @classmethod
    def default_lane_templates(cls) -> List[LaneTemplate]:
        return [
            LaneTemplate(
                lane_id="existing-client-maintenance-expansion",
                display_name="Existing Client Maintenance + Expansion",
                hypothesis="Fastest path to cash comes from maintenance, expansion, and warm expansion motions inside current accounts.",
                public_actor_classes=["existing_clients", "procurement_watchers", "delivery_leads", "competitors"],
                public_event_classes=["renewal_signal", "case_study_release", "budget_freeze", "competitor_pitch"],
                narrative_brief="Model public market confidence and client-visible delivery signals around expanding existing relationships.",
                interview_personas=["existing_client_exec", "gj_account_lead", "delivery_director"],
                private_committee_roles=["buyer", "delivery", "finance"],
                procurement_gates=["budget_alignment", "renewal_timing", "scope_expansion"],
                capability_requirements=["account_growth_capacity", "delivery_margin_control", "case_study_evidence"],
                required_internal_inputs=["current_team_capacity", "top_accounts", "margin_floor"],
                scorecard_dimensions=cls.DEFAULT_SCORECARD_DIMENSIONS,
                monte_carlo_fields=["pipeline_size", "close_rate", "sales_cycle_days"],
            ),
            LaneTemplate(
                lane_id="healthcare-pharma-training-growth",
                display_name="Healthcare / Pharma Training Growth",
                hypothesis="Healthcare and pharma training work is a credible adjacent growth lane with enterprise-style buying cycles.",
                public_actor_classes=["healthcare_buyers", "training_partners", "industry_analysts", "competitors"],
                public_event_classes=["pilot_launch", "compliance_delay", "training_outcome_signal", "partner_announcement"],
                narrative_brief="Model market signaling and partner credibility pressure in healthcare and pharma training.",
                interview_personas=["healthcare_lnd_lead", "compliance_reviewer", "gj_delivery_lead"],
                private_committee_roles=["buyer", "legal", "delivery", "finance"],
                procurement_gates=["compliance_review", "pilot_scope", "reference_check"],
                capability_requirements=["regulated_content_delivery", "enterprise_procurement_readiness", "outcome_measurement"],
                required_internal_inputs=["existing_healthcare_cases", "delivery_capacity", "margin_floor"],
                scorecard_dimensions=cls.DEFAULT_SCORECARD_DIMENSIONS,
                monte_carlo_fields=["pipeline_size", "close_rate", "sales_cycle_days"],
            ),
            LaneTemplate(
                lane_id="defense-government-entry",
                display_name="Defense / Government Entry",
                hypothesis="Selective government and defense work can diversify revenue while increasing compliance burden.",
                public_actor_classes=["competitors", "prime_partners", "industry_analysts", "procurement_watchers"],
                public_event_classes=["award_announcement", "pilot_demo", "compliance_delay", "partner_signal"],
                narrative_brief="Model public market signaling and positioning pressure around the lane.",
                interview_personas=["procurement_officer", "prime_partner_exec", "internal_delivery_lead"],
                private_committee_roles=["buyer", "legal", "security", "delivery", "finance"],
                procurement_gates=["vehicle_access", "security_review", "past_performance", "cashflow_gap"],
                capability_requirements=["clearance_partner_strategy", "proposal_ops", "delivery_capacity"],
                required_internal_inputs=["current_team_capacity", "partner_list", "margin_floor"],
                scorecard_dimensions=cls.DEFAULT_SCORECARD_DIMENSIONS,
                monte_carlo_fields=["pipeline_size", "close_rate", "sales_cycle_days"],
            ),
            LaneTemplate(
                lane_id="spatial-enterprise-enablement",
                display_name="Spatial Enterprise Enablement",
                hypothesis="Spatial enterprise programs can compound Groove Jones strengths but require disciplined positioning and account selection.",
                public_actor_classes=["enterprise_buyers", "platform_partners", "industry_analysts", "competitors"],
                public_event_classes=["platform_launch", "pilot_case_study", "budget_shift", "partner_signal"],
                narrative_brief="Model public adoption and positioning signals around spatial enterprise enablement.",
                interview_personas=["enterprise_innovation_lead", "platform_partner", "gj_strategy_lead"],
                private_committee_roles=["buyer", "delivery", "it", "finance"],
                procurement_gates=["platform_fit", "deployment_readiness", "it_security"],
                capability_requirements=["enterprise_solution_packaging", "platform_partnerships", "deployment_capacity"],
                required_internal_inputs=["target_accounts", "partner_list", "team_capacity"],
                scorecard_dimensions=cls.DEFAULT_SCORECARD_DIMENSIONS,
                monte_carlo_fields=["pipeline_size", "close_rate", "sales_cycle_days"],
            ),
            LaneTemplate(
                lane_id="selective-events-agency-partners",
                display_name="Selective Events / Agency Partner Work",
                hypothesis="Selective event and agency partner work can support cash flow when filtered away from commoditized execution.",
                public_actor_classes=["agency_partners", "event_buyers", "competitors", "industry_watchers"],
                public_event_classes=["rfp_release", "festival_cycle", "partner_signal", "price_pressure"],
                narrative_brief="Model demand spikes, partner signaling, and price pressure in selective event or agency-partner work.",
                interview_personas=["agency_partner", "event_buyer", "gj_exec"],
                private_committee_roles=["buyer", "delivery", "finance"],
                procurement_gates=["margin_floor", "scope_control", "staffing_capacity"],
                capability_requirements=["partner_filtering", "rapid_delivery_capacity", "margin_discipline"],
                required_internal_inputs=["partner_list", "margin_floor", "team_capacity"],
                scorecard_dimensions=cls.DEFAULT_SCORECARD_DIMENSIONS,
                monte_carlo_fields=["pipeline_size", "close_rate", "sales_cycle_days"],
            ),
        ]

    @classmethod
    def build_lane_context(cls, project_id: str, lane_id: str) -> LaneRunContext:
        template = cls.get_lane_template(project_id, lane_id)
        template_path = ProjectManager.get_strategy_lab_artifact_path(project_id, "lane_templates.json")
        lane_context_path = cls._lane_run_root(project_id, lane_id)
        return LaneRunContext(
            lane_id=template.lane_id,
            workflow_mode=WorkflowMode.STRATEGY_LAB,
            template_path=template_path,
            lane_context_path=lane_context_path,
            display_name=template.display_name,
            narrative_brief=template.narrative_brief,
            public_actor_classes=template.public_actor_classes,
            public_event_classes=template.public_event_classes,
            interview_personas=template.interview_personas,
            procurement_gates=template.procurement_gates,
        )

    @classmethod
    def get_lane_template(cls, project_id: str, lane_id: str) -> LaneTemplate:
        templates = {template.lane_id: template for template in cls.load_lane_templates(project_id)}
        if lane_id not in templates:
            raise ValueError(f"未找到 lane template: {lane_id}")
        return templates[lane_id]

    @classmethod
    def run_private_analysis_async(cls, project_id: str, graph_id: str, lane_id: str) -> LaneRunStatus:
        cls.get_lane_template(project_id, lane_id)
        cls._acquire_lane_lock_or_raise(project_id, lane_id)

        run_status = cls._create_run_status(project_id, lane_id)

        def worker():
            try:
                cls._execute_private_analysis(project_id, graph_id, lane_id, run_status)
            except Exception as exc:  # pragma: no cover - defensive thread logging
                cls._mark_run_failed(project_id, lane_id, run_status, str(exc))
                logger.exception("Strategy Lab lane run failed: %s", exc)
            finally:
                cls._release_lane_lock(project_id, lane_id)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return run_status

    @classmethod
    def run_all_private_analysis_async(cls, project_id: str, graph_id: str) -> Dict[str, Any]:
        templates = cls.load_lane_templates(project_id)
        batch_id = f"batch_{uuid.uuid4().hex[:12]}"

        def worker():
            for template in templates:
                try:
                    cls._acquire_lane_lock_or_raise(project_id, template.lane_id)
                except ValueError:
                    logger.info("Lane already running, skipping duplicate batch launch: %s", template.lane_id)
                    continue

                run_status = cls._create_run_status(project_id, template.lane_id)
                try:
                    cls._execute_private_analysis(project_id, graph_id, template.lane_id, run_status)
                except Exception as exc:  # pragma: no cover - defensive thread logging
                    cls._mark_run_failed(project_id, template.lane_id, run_status, str(exc))
                    logger.exception("Strategy Lab batch lane failed: %s", exc)
                finally:
                    cls._release_lane_lock(project_id, template.lane_id)

        threading.Thread(target=worker, daemon=True).start()
        return {"batch_id": batch_id}

    @classmethod
    def list_lane_statuses(cls, project_id: str) -> Dict[str, Optional[Dict[str, Any]]]:
        result: Dict[str, Optional[Dict[str, Any]]] = {}
        for lane_id in cls.REQUIRED_LANE_IDS:
            status = cls.get_lane_status(project_id, lane_id)
            result[lane_id] = status.to_dict() if status else None
        return result

    @classmethod
    def get_lane_status(cls, project_id: str, lane_id: str) -> Optional[LaneRunStatus]:
        pointer_path = cls._current_pointer_path(project_id, lane_id)
        if not os.path.exists(pointer_path):
            return None
        pointer = cls._read_json(pointer_path)
        status_path = pointer.get("status_path")
        if not status_path or not os.path.exists(status_path):
            return None
        return cls._lane_status_from_dict(cls._read_json(status_path))

    @classmethod
    def load_interview_artifact(cls, project_id: str, lane_id: str) -> Optional[InterviewArtifact]:
        status = cls.get_lane_status(project_id, lane_id)
        if not status:
            return None
        interview_path = status.artifact_paths.get("interviews")
        if not interview_path or not os.path.exists(interview_path):
            return None
        data = cls._read_json(interview_path)
        if not data:
            return None
        return InterviewArtifact(
            lane_id=data.get("lane_id", lane_id),
            run_id=data.get("run_id", status.run_id),
            transcript_markdown=data.get("transcript_markdown", ""),
            created_at=data.get("created_at", status.created_at),
        )

    @classmethod
    def compose_comparative_report(cls, project_id: str) -> ComparativeReport:
        chunk_manifest = ProjectManager.load_strategy_lab_artifact(project_id, "chunk_manifest.json") or []
        valid_chunk_ids = {
            item["chunk_id"]: item
            for item in chunk_manifest
            if item.get("episode_uuid")
        }

        rows = []
        citations: Dict[str, CitationRecord] = {}

        for lane_id in cls.REQUIRED_LANE_IDS:
            status = cls.get_lane_status(project_id, lane_id)
            if not status or status.status != "completed":
                raise ValueError(f"lane 尚未完成: {lane_id}")

            analysis_path = status.artifact_paths.get("private_analysis_json")
            if not analysis_path or not os.path.exists(analysis_path):
                raise ValueError(f"lane 缺少 private analysis artifact: {lane_id}")

            scorecard = cls._scorecard_from_dict(cls._read_json(analysis_path))
            row = {
                "lane_id": scorecard.lane_id,
                "display_name": scorecard.display_name,
                "summary": scorecard.summary,
                "metrics": {},
            }

            for dimension in cls.DEFAULT_SCORECARD_DIMENSIONS:
                if dimension not in scorecard.metrics:
                    raise ValueError(f"{lane_id} 缺少评分维度: {dimension}")
                metric = scorecard.metrics[dimension]
                if not metric.source_label:
                    raise ValueError(f"{lane_id}/{dimension} 缺少 source_label")
                if metric.source_label != AnalysisSourceLabel.MONTE_CARLO_ATTACHMENT and not metric.citation_ids:
                    raise ValueError(f"{lane_id}/{dimension} 缺少 citation_ids")
                if metric.source_label != AnalysisSourceLabel.MONTE_CARLO_ATTACHMENT and len(metric.citation_ids) != len(metric.citations):
                    raise ValueError(f"{lane_id}/{dimension} 的 citation_ids 与 citations 数量不一致")

                resolved_citations = []
                for index, citation in enumerate(metric.citations, start=1):
                    if citation.chunk_id not in valid_chunk_ids:
                        raise ValueError(f"{lane_id}/{dimension} 引用了无 provenance 的 chunk: {citation.chunk_id}")
                    citation_id = metric.citation_ids[index - 1] if index - 1 < len(metric.citation_ids) else f"{lane_id}:{dimension}:{index:02d}"
                    citations[citation_id] = citation
                    resolved_citations.append(citation_id)

                row["metrics"][dimension] = {
                    "score": metric.score,
                    "judgment": metric.judgment,
                    "source_label": metric.source_label.value,
                    "citation_ids": resolved_citations,
                    "monte_carlo_attachment": metric.monte_carlo_attachment,
                }

            rows.append(row)

        report = ComparativeReport(
            project_id=project_id,
            generated_at=datetime.now().isoformat(),
            rows=rows,
            markdown_summary=cls._comparative_report_markdown(rows),
            citations=citations,
        )

        ProjectManager.save_strategy_lab_artifact(
            project_id,
            "comparative_report.json",
            report.to_dict(),
        )
        comparative_markdown_path = ProjectManager.get_strategy_lab_artifact_path(
            project_id,
            "comparative_report.md",
        )
        cls._atomic_write_text(comparative_markdown_path, report.markdown_summary)
        return report

    @classmethod
    def get_comparative_report(cls, project_id: str) -> Optional[Dict[str, Any]]:
        return ProjectManager.load_strategy_lab_artifact(project_id, "comparative_report.json")

    @classmethod
    def inspect_source(cls, project_id: str, citation_id: str) -> Dict[str, Any]:
        report = cls.get_comparative_report(project_id)
        if not report:
            raise ValueError("对比报告尚未生成")

        citation_payload = (report.get("citations") or {}).get(citation_id)
        if not citation_payload:
            raise ValueError(f"未找到 citation: {citation_id}")

        citation = cls._citation_from_dict(citation_payload)
        chunk_manifest = ProjectManager.load_strategy_lab_artifact(project_id, "chunk_manifest.json") or []
        matched_chunk = next(
            (item for item in chunk_manifest if item.get("chunk_id") == citation.chunk_id),
            None,
        )
        if not matched_chunk:
            raise ValueError(f"citation 缺少 manifest-backed provenance: {citation_id}")

        return {
            "citation_id": citation_id,
            "citation": citation.to_dict(),
            "chunk": matched_chunk,
        }

    @classmethod
    def project_overview(cls, project_id: str) -> Dict[str, Any]:
        return {
            "lane_templates": [template.to_dict() for template in cls.load_lane_templates(project_id)],
            "lane_statuses": cls.list_lane_statuses(project_id),
            "comparative_report": cls.get_comparative_report(project_id),
        }

    @classmethod
    def _execute_private_analysis(
        cls,
        project_id: str,
        graph_id: str,
        lane_id: str,
        run_status: LaneRunStatus,
    ) -> None:
        template = cls.get_lane_template(project_id, lane_id)
        run_dir = cls._run_dir(project_id, lane_id, run_status.run_id)
        os.makedirs(run_dir, exist_ok=True)

        interview_artifact = InterviewArtifact(
            lane_id=lane_id,
            run_id=run_status.run_id,
            transcript_markdown="No strategy-lab interview transcript captured yet.",
            created_at=datetime.now().isoformat(),
        )
        interview_path = os.path.join(run_dir, "interviews.json")
        cls._atomic_write_json(interview_path, interview_artifact.to_dict())

        agent = PrivateAnalysisAgent(project_id=project_id, graph_id=graph_id)
        scorecard, citation_index = agent.generate_scorecard(
            lane_template=template,
            interviews_markdown=interview_artifact.transcript_markdown,
        )

        private_analysis_json_path = os.path.join(run_dir, "private_analysis.json")
        private_analysis_md_path = os.path.join(run_dir, "private_analysis.md")
        status_path = os.path.join(run_dir, "status.json")

        cls._atomic_write_json(private_analysis_json_path, scorecard.to_dict())
        cls._atomic_write_text(private_analysis_md_path, agent.scorecard_to_markdown(scorecard))

        run_status.status = "completed"
        run_status.stage = "private_analysis"
        run_status.updated_at = datetime.now().isoformat()
        run_status.artifact_paths = {
            "private_analysis_json": private_analysis_json_path,
            "private_analysis_md": private_analysis_md_path,
            "interviews": interview_path,
            "status": status_path,
        }
        cls._atomic_write_json(status_path, run_status.to_dict())
        cls._atomic_write_json(
            cls._current_pointer_path(project_id, lane_id),
            {
                "lane_id": lane_id,
                "run_id": run_status.run_id,
                "status_path": status_path,
                "updated_at": run_status.updated_at,
            },
        )

        logger.info(
            "Strategy Lab lane completed: project=%s lane=%s run=%s citations=%s",
            project_id,
            lane_id,
            run_status.run_id,
            len(citation_index),
        )

        try:
            cls.compose_comparative_report(project_id)
        except ValueError:
            logger.info("Comparative report deferred until all lanes complete")

    @classmethod
    def _create_run_status(cls, project_id: str, lane_id: str) -> LaneRunStatus:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        now = datetime.now().isoformat()
        status = LaneRunStatus(
            project_id=project_id,
            lane_id=lane_id,
            run_id=run_id,
            workflow_mode=WorkflowMode.STRATEGY_LAB,
            status="running",
            stage="private_analysis",
            created_at=now,
            updated_at=now,
        )
        status_path = os.path.join(cls._run_dir(project_id, lane_id, run_id), "status.json")
        cls._atomic_write_json(status_path, status.to_dict())
        cls._atomic_write_json(
            cls._current_pointer_path(project_id, lane_id),
            {
                "lane_id": lane_id,
                "run_id": run_id,
                "status_path": status_path,
                "updated_at": now,
            },
        )
        return status

    @classmethod
    def _validate_lane_templates(cls, templates: List[LaneTemplate]) -> None:
        lane_ids = [template.lane_id for template in templates]
        if len(set(lane_ids)) != len(lane_ids):
            raise ValueError("lane template 不能包含重复 lane_id")
        missing_lane_ids = sorted(set(cls.REQUIRED_LANE_IDS) - set(lane_ids))
        if missing_lane_ids:
            raise ValueError(f"缺少必需 lane templates: {', '.join(missing_lane_ids)}")

        for template in templates:
            if not template.display_name or not template.hypothesis:
                raise ValueError(f"lane template 缺少 display_name 或 hypothesis: {template.lane_id}")
            required_lists = {
                "public_actor_classes": template.public_actor_classes,
                "public_event_classes": template.public_event_classes,
                "private_committee_roles": template.private_committee_roles,
                "procurement_gates": template.procurement_gates,
                "capability_requirements": template.capability_requirements,
                "required_internal_inputs": template.required_internal_inputs,
                "scorecard_dimensions": template.scorecard_dimensions,
            }
            for field_name, value in required_lists.items():
                if not value:
                    raise ValueError(f"{template.lane_id} 缺少 {field_name}")

    @classmethod
    def _lane_run_root(cls, project_id: str, lane_id: str) -> str:
        return ProjectManager.get_strategy_lab_artifact_path(project_id, os.path.join("runs", lane_id))

    @classmethod
    def _run_dir(cls, project_id: str, lane_id: str, run_id: str) -> str:
        return os.path.join(cls._lane_run_root(project_id, lane_id), run_id)

    @classmethod
    def _current_pointer_path(cls, project_id: str, lane_id: str) -> str:
        return ProjectManager.get_strategy_lab_artifact_path(
            project_id,
            os.path.join("current", f"{lane_id}.json"),
        )

    @classmethod
    def _lane_lock_key(cls, project_id: str, lane_id: str) -> str:
        return f"{project_id}:{lane_id}:{WorkflowMode.STRATEGY_LAB.value}"

    @classmethod
    def _acquire_lane_lock_or_raise(cls, project_id: str, lane_id: str) -> None:
        lock = cls._lane_locks.setdefault(cls._lane_lock_key(project_id, lane_id), threading.Lock())
        if not lock.acquire(blocking=False):
            raise ValueError(f"lane 正在运行中，拒绝重复提交: {lane_id}")

    @classmethod
    def _release_lane_lock(cls, project_id: str, lane_id: str) -> None:
        lock = cls._lane_locks.get(cls._lane_lock_key(project_id, lane_id))
        if lock and lock.locked():
            lock.release()

    @staticmethod
    def _atomic_write_json(path: str, data: Any) -> None:
        parent = Path(path).parent
        parent.mkdir(parents=True, exist_ok=True)
        temp_path = parent / f".{Path(path).name}.{uuid.uuid4().hex}.tmp"
        temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temp_path, path)

    @staticmethod
    def _atomic_write_text(path: str, content: str) -> None:
        parent = Path(path).parent
        parent.mkdir(parents=True, exist_ok=True)
        temp_path = parent / f".{Path(path).name}.{uuid.uuid4().hex}.tmp"
        temp_path.write_text(content, encoding="utf-8")
        os.replace(temp_path, path)

    @staticmethod
    def _read_json(path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _lane_status_from_dict(data: Dict[str, Any]) -> LaneRunStatus:
        return LaneRunStatus(
            project_id=data["project_id"],
            lane_id=data["lane_id"],
            run_id=data["run_id"],
            workflow_mode=WorkflowMode(data.get("workflow_mode", WorkflowMode.STRATEGY_LAB.value)),
            status=data.get("status", "unknown"),
            stage=data.get("stage", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            artifact_paths=data.get("artifact_paths", {}),
            error=data.get("error"),
        )

    @classmethod
    def _mark_run_failed(
        cls,
        project_id: str,
        lane_id: str,
        run_status: LaneRunStatus,
        error_message: str,
    ) -> None:
        status_path = os.path.join(cls._run_dir(project_id, lane_id, run_status.run_id), "status.json")
        run_status.status = "failed"
        run_status.error = error_message
        run_status.updated_at = datetime.now().isoformat()
        run_status.artifact_paths.setdefault("status", status_path)
        cls._atomic_write_json(status_path, run_status.to_dict())
        cls._atomic_write_json(
            cls._current_pointer_path(project_id, lane_id),
            {
                "lane_id": lane_id,
                "run_id": run_status.run_id,
                "status_path": status_path,
                "updated_at": run_status.updated_at,
            },
        )

    @staticmethod
    def _citation_from_dict(data: Dict[str, Any]) -> CitationRecord:
        return CitationRecord(
            chunk_id=data["chunk_id"],
            filename=data.get("filename", ""),
            locator=data.get("locator", ""),
            quote=data.get("quote", ""),
            episode_uuid=data.get("episode_uuid"),
            source_label=AnalysisSourceLabel(data.get("source_label", AnalysisSourceLabel.RESEARCH_CITATION.value)),
        )

    @classmethod
    def _scorecard_from_dict(cls, data: Dict[str, Any]) -> LaneScorecard:
        metrics = {}
        for dimension, payload in (data.get("metrics") or {}).items():
            citations = [
                cls._citation_from_dict(item)
                for item in payload.get("citations", [])
            ]
            metrics[dimension] = cls._metric_from_dict(dimension, payload, citations)
        return LaneScorecard(
            lane_id=data["lane_id"],
            display_name=data.get("display_name", ""),
            summary=data.get("summary", ""),
            metrics=metrics,
            assumptions=data.get("assumptions", []),
            caveats=data.get("caveats", []),
        )

    @staticmethod
    def _metric_from_dict(
        dimension: str,
        payload: Dict[str, Any],
        citations: List[CitationRecord],
    ) -> LaneMetricResult:
        return LaneMetricResult(
            dimension=dimension,
            score=payload.get("score", ""),
            judgment=payload.get("judgment", ""),
            source_label=AnalysisSourceLabel(
                payload.get("source_label", AnalysisSourceLabel.RESEARCH_CITATION.value)
            ),
            citation_ids=payload.get("citation_ids", []),
            citations=citations,
            monte_carlo_attachment=payload.get("monte_carlo_attachment"),
        )

    @staticmethod
    def _comparative_report_markdown(rows: List[Dict[str, Any]]) -> str:
        lines = [
            "# Groove Jones Strategy Lab Comparative Report",
            "",
            "| Lane | Time to Cash | Durability 12-24m | Capability Fit | Required Investment | Failure Modes | Evidence Strength |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]

        for row in rows:
            metrics = row["metrics"]
            lines.append(
                "| {lane} | {time_to_cash} | {durability} | {capability_fit} | {required_investment} | {failure_modes} | {evidence_strength} |".format(
                    lane=row["display_name"],
                    time_to_cash=metrics["time_to_cash"]["score"],
                    durability=metrics["durability_12_24m"]["score"],
                    capability_fit=metrics["capability_fit"]["score"],
                    required_investment=metrics["required_investment"]["score"],
                    failure_modes=metrics["failure_modes"]["score"],
                    evidence_strength=metrics["evidence_strength"]["score"],
                )
            )

        lines.append("")
        for row in rows:
            lines.append(f"## {row['display_name']}")
            lines.append(row["summary"])
            lines.append("")

        return "\n".join(lines).strip() + "\n"
