"""
Strategy Lab 私有分析服务
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from ..models.project import ProjectManager
from ..models.strategy_lab import (
    AnalysisSourceLabel,
    ChunkManifestEntry,
    CitationRecord,
    LaneMetricResult,
    LaneScorecard,
    LaneTemplate,
)
from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger

logger = get_logger("mirofish.private_analysis")


PRIVATE_ANALYSIS_SYSTEM_PROMPT = """你是 Groove Jones Strategy Lab 的资深战略分析师。

你的任务不是预测社交媒体舆情，而是基于研究语料中的证据，为单条战略路径输出结构化评分卡。

严格要求：
1. 只能引用提供给你的 citation_id。
2. 只能输出 JSON，不要输出额外解释。
3. 每个 scorecard dimension 都必须出现。
4. 除 Monte Carlo attachment 外，每个维度至少引用 1 个 citation_id。
5. source_label 只能是：
   - research_citation
   - private_analysis
   - narrative_simulation
   - monte_carlo_attachment
6. judgment 必须是明确结论，不要只写“需要更多信息”。
"""


class PrivateAnalysisAgent:
    """基于 manifest-backed 证据生成路径评分卡"""

    MAX_EXCERPTS = 10

    def __init__(
        self,
        project_id: str,
        graph_id: str,
        llm_client: Optional[LLMClient] = None,
    ):
        self.project_id = project_id
        self.graph_id = graph_id
        self.llm_client = llm_client or LLMClient()

    def generate_scorecard(
        self,
        lane_template: LaneTemplate,
        interviews_markdown: Optional[str] = None,
        narrative_summary: Optional[str] = None,
        monte_carlo_attachment: Optional[str] = None,
        interview_source_path: Optional[str] = None,
        narrative_source_path: Optional[str] = None,
    ) -> Tuple[LaneScorecard, Dict[str, CitationRecord]]:
        chunk_manifest = ProjectManager.load_strategy_lab_artifact(
            self.project_id,
            "chunk_manifest.json",
        )
        if not chunk_manifest:
            raise ValueError("缺少 chunk_manifest.json，无法执行私有分析")

        chunks = [
            ChunkManifestEntry.from_dict(item)
            for item in chunk_manifest
            if item.get("episode_uuid")
        ]
        if not chunks:
            raise ValueError("chunk_manifest.json 中没有带 episode_uuid 的可引用证据")

        selected_chunks = self._select_relevant_chunks(lane_template, chunks)
        citation_index = {
            **self._build_research_citation_index(lane_template, selected_chunks),
            **self._build_narrative_citation_index(
                lane_template,
                interviews_markdown=interviews_markdown,
                narrative_summary=narrative_summary,
                interview_source_path=interview_source_path,
                narrative_source_path=narrative_source_path,
            ),
            **self._build_private_citation_index(lane_template),
        }

        prompt = self._build_prompt(
            lane_template=lane_template,
            citation_index=citation_index,
            interviews_markdown=interviews_markdown,
            narrative_summary=narrative_summary,
            monte_carlo_attachment=monte_carlo_attachment,
        )

        result = self.llm_client.chat_json(
            messages=[
                {"role": "system", "content": PRIVATE_ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=4096,
        )

        return (
            self._validate_scorecard_result(
                lane_template=lane_template,
                result=result,
                citation_index=citation_index,
                monte_carlo_attachment=monte_carlo_attachment,
                interviews_markdown=interviews_markdown,
                narrative_summary=narrative_summary,
            ),
            citation_index,
        )

    def scorecard_to_markdown(self, scorecard: LaneScorecard) -> str:
        lines = [
            f"# {scorecard.display_name}",
            "",
            scorecard.summary,
            "",
            "## Scorecard",
            "",
        ]

        for dimension, metric in scorecard.metrics.items():
            lines.append(f"### {dimension}")
            lines.append(f"- Score: {metric.score}")
            lines.append(f"- Judgment: {metric.judgment}")
            lines.append(f"- Source Label: {metric.source_label.value}")
            if metric.citation_ids:
                lines.append(f"- Citations: {', '.join(metric.citation_ids)}")
            if metric.monte_carlo_attachment:
                lines.append(f"- Monte Carlo Attachment: {metric.monte_carlo_attachment}")
            lines.append("")

        if scorecard.assumptions:
            lines.append("## Assumptions")
            lines.extend([f"- {item}" for item in scorecard.assumptions])
            lines.append("")

        if scorecard.caveats:
            lines.append("## Caveats")
            lines.extend([f"- {item}" for item in scorecard.caveats])
            lines.append("")

        return "\n".join(lines).strip() + "\n"

    def _build_prompt(
        self,
        *,
        lane_template: LaneTemplate,
        citation_index: Dict[str, CitationRecord],
        interviews_markdown: Optional[str],
        narrative_summary: Optional[str],
        monte_carlo_attachment: Optional[str],
    ) -> str:
        evidence_lines = []
        for citation_id, citation in citation_index.items():
            evidence_lines.append(
                "\n".join(
                    [
                        f"[{citation_id}] filename={citation.filename}",
                        f"locator={citation.locator}",
                        f"episode_uuid={citation.episode_uuid}",
                        citation.quote,
                    ]
                )
            )

        return f"""请基于下列 lane template 和 evidence bundle 输出 JSON。

lane_template:
{lane_template.to_dict()}

required_dimensions:
{lane_template.scorecard_dimensions}

monte_carlo_attachment:
{monte_carlo_attachment or "none"}

narrative_summary:
{narrative_summary or "none"}

interviews_markdown:
{interviews_markdown or "none"}

evidence_bundle:
{chr(10).join(evidence_lines)}

source_rules:
- 如果某个 metric 使用 research 开头的 citation_id，source_label 必须是 research_citation。
- 如果某个 metric 使用 narrative 开头的 citation_id，source_label 必须是 narrative_simulation。
- 如果某个 metric 使用 private 开头的 citation_id，source_label 必须是 private_analysis。
- narrative_summary 或 interviews_markdown 不为 none 时，至少 1 个维度必须使用 narrative citation。
- 至少 1 个维度必须使用 private citation。
- 至少 1 个维度必须使用 research citation。
- 只有 Monte Carlo attachment 可以不带 citation_ids。

输出格式：
{{
  "summary": "string",
  "assumptions": ["string"],
  "caveats": ["string"],
  "metrics": {{
    "<dimension>": {{
      "score": "High|Medium|Low|1-5|自定义也可以，但必须明确",
      "judgment": "string",
      "source_label": "research_citation|private_analysis|narrative_simulation|monte_carlo_attachment",
      "citation_ids": ["citation id"],
      "monte_carlo_attachment": "string|null"
    }}
  }}
}}
"""

    def _select_relevant_chunks(
        self,
        lane_template: LaneTemplate,
        chunks: List[ChunkManifestEntry],
    ) -> List[ChunkManifestEntry]:
        keyword_pool = " ".join(
            [
                lane_template.display_name,
                lane_template.hypothesis,
                lane_template.narrative_brief,
                " ".join(lane_template.public_actor_classes),
                " ".join(lane_template.public_event_classes),
                " ".join(lane_template.procurement_gates),
                " ".join(lane_template.capability_requirements),
            ]
        ).lower()
        keywords = {
            token
            for token in re.findall(r"[a-z0-9]{4,}", keyword_pool)
            if token not in {"groove", "jones", "lane", "with", "from", "that"}
        }

        scored = []
        for chunk in chunks:
            chunk_text = chunk.text.lower()
            score = sum(1 for keyword in keywords if keyword in chunk_text)
            scored.append((score, len(chunk.text), chunk))

        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
        selected = [item[2] for item in scored if item[0] > 0][: self.MAX_EXCERPTS]
        if selected:
            return selected
        return [item[2] for item in scored[: self.MAX_EXCERPTS]]

    def _build_research_citation_index(
        self,
        lane_template: LaneTemplate,
        chunks: List[ChunkManifestEntry],
    ) -> Dict[str, CitationRecord]:
        citation_index: Dict[str, CitationRecord] = {}
        for index, chunk in enumerate(chunks, start=1):
            citation_id = f"{lane_template.lane_id}:research:{index:02d}"
            citation_index[citation_id] = CitationRecord(
                chunk_id=chunk.chunk_id,
                filename=chunk.filename,
                locator=f"{chunk.locator_start} -> {chunk.locator_end}",
                quote=chunk.text[:600],
                episode_uuid=chunk.episode_uuid,
                source_label=AnalysisSourceLabel.RESEARCH_CITATION,
                source_kind="research_chunk",
            )
        return citation_index

    def _build_narrative_citation_index(
        self,
        lane_template: LaneTemplate,
        *,
        interviews_markdown: Optional[str],
        narrative_summary: Optional[str],
        interview_source_path: Optional[str],
        narrative_source_path: Optional[str],
    ) -> Dict[str, CitationRecord]:
        citation_index: Dict[str, CitationRecord] = {}

        if narrative_summary:
            citation_index[f"{lane_template.lane_id}:narrative:summary"] = CitationRecord(
                chunk_id=None,
                filename="narrative_summary.json",
                locator="summary_markdown",
                quote=narrative_summary[:600],
                source_label=AnalysisSourceLabel.NARRATIVE_SIMULATION,
                source_kind="narrative_summary",
                source_path=narrative_source_path,
            )

        if interviews_markdown:
            citation_index[f"{lane_template.lane_id}:narrative:interviews"] = CitationRecord(
                chunk_id=None,
                filename="interviews.json",
                locator="transcript_markdown",
                quote=interviews_markdown[:600],
                source_label=AnalysisSourceLabel.NARRATIVE_SIMULATION,
                source_kind="interview_transcript",
                source_path=interview_source_path,
            )

        return citation_index

    def _build_private_citation_index(
        self,
        lane_template: LaneTemplate,
    ) -> Dict[str, CitationRecord]:
        lane_template_path = ProjectManager.get_strategy_lab_artifact_path(
            self.project_id,
            "lane_templates.json",
        )
        quote = (
            f"Hypothesis: {lane_template.hypothesis}\n"
            f"Committee roles: {', '.join(lane_template.private_committee_roles)}\n"
            f"Procurement gates: {', '.join(lane_template.procurement_gates)}\n"
            f"Capability requirements: {', '.join(lane_template.capability_requirements)}\n"
            f"Required internal inputs: {', '.join(lane_template.required_internal_inputs)}"
        )
        return {
            f"{lane_template.lane_id}:private:template": CitationRecord(
                chunk_id=None,
                filename="lane_templates.json",
                locator=f"lane_template:{lane_template.lane_id}",
                quote=quote[:600],
                source_label=AnalysisSourceLabel.PRIVATE_ANALYSIS,
                source_kind="lane_template",
                source_path=lane_template_path,
            )
        }

    def _validate_scorecard_result(
        self,
        *,
        lane_template: LaneTemplate,
        result: Dict[str, object],
        citation_index: Dict[str, CitationRecord],
        monte_carlo_attachment: Optional[str],
        interviews_markdown: Optional[str],
        narrative_summary: Optional[str],
    ) -> LaneScorecard:
        metrics_payload = result.get("metrics")
        if not isinstance(metrics_payload, dict):
            raise ValueError("私有分析结果缺少 metrics 对象")

        metrics: Dict[str, LaneMetricResult] = {}
        for dimension in lane_template.scorecard_dimensions:
            metric_payload = metrics_payload.get(dimension)
            if not isinstance(metric_payload, dict):
                raise ValueError(f"缺少评分维度: {dimension}")

            source_label = AnalysisSourceLabel(
                metric_payload.get("source_label", AnalysisSourceLabel.PRIVATE_ANALYSIS.value)
            )
            citation_ids = metric_payload.get("citation_ids", [])
            if not isinstance(citation_ids, list):
                raise ValueError(f"{dimension} 的 citation_ids 必须是数组")

            resolved_citations = []
            inferred_sources = set()
            if source_label != AnalysisSourceLabel.MONTE_CARLO_ATTACHMENT:
                (
                    source_label,
                    citation_ids,
                    resolved_citations,
                ) = self._normalize_metric_citations(
                    dimension=dimension,
                    source_label=source_label,
                    citation_ids=citation_ids,
                    citation_index=citation_index,
                )
            elif not (metric_payload.get("monte_carlo_attachment") or monte_carlo_attachment):
                raise ValueError(f"{dimension} 使用 monte_carlo_attachment 但缺少附件内容")

            metrics[dimension] = LaneMetricResult(
                dimension=dimension,
                score=str(metric_payload.get("score", "")),
                judgment=str(metric_payload.get("judgment", "")),
                source_label=source_label,
                citation_ids=citation_ids,
                citations=resolved_citations,
                monte_carlo_attachment=metric_payload.get("monte_carlo_attachment") or monte_carlo_attachment,
            )

            if not metrics[dimension].score or not metrics[dimension].judgment:
                raise ValueError(f"{dimension} 缺少 score 或 judgment")

        assumptions = result.get("assumptions", [])
        caveats = result.get("caveats", [])
        self._validate_source_coverage(
            metrics,
            require_narrative=bool(interviews_markdown or narrative_summary),
        )
        return LaneScorecard(
            lane_id=lane_template.lane_id,
            display_name=lane_template.display_name,
            summary=str(result.get("summary", "")),
            metrics=metrics,
            assumptions=assumptions if isinstance(assumptions, list) else [],
            caveats=caveats if isinstance(caveats, list) else [],
        )

    def _normalize_metric_citations(
        self,
        *,
        dimension: str,
        source_label: AnalysisSourceLabel,
        citation_ids: List[str],
        citation_index: Dict[str, CitationRecord],
    ) -> Tuple[AnalysisSourceLabel, List[str], List[CitationRecord]]:
        if not citation_ids:
            raise ValueError(f"{dimension} 缺少 citation_ids")

        resolved_pairs: List[Tuple[str, CitationRecord]] = []
        grouped_pairs: Dict[AnalysisSourceLabel, List[Tuple[str, CitationRecord]]] = {}
        for citation_id in citation_ids:
            if citation_id not in citation_index:
                raise ValueError(f"{dimension} 使用了未知 citation_id: {citation_id}")
            citation = citation_index[citation_id]
            resolved_pairs.append((citation_id, citation))
            grouped_pairs.setdefault(citation.source_label, []).append((citation_id, citation))

        if len(grouped_pairs) == 1:
            inferred_source = next(iter(grouped_pairs))
            if source_label != inferred_source:
                logger.warning(
                    "scorecard metric source_label corrected: dimension=%s declared=%s inferred=%s",
                    dimension,
                    source_label.value,
                    inferred_source.value,
                )
                source_label = inferred_source
            normalized_pairs = grouped_pairs[inferred_source]
        else:
            normalized_pairs = grouped_pairs.get(source_label, [])
            if not normalized_pairs:
                inferred_labels = ", ".join(sorted(label.value for label in grouped_pairs))
                raise ValueError(
                    f"{dimension} 的 source_label={source_label.value} 与 citation_ids 的来源不一致: {inferred_labels}"
                )
            dropped_count = len(resolved_pairs) - len(normalized_pairs)
            if dropped_count > 0:
                logger.warning(
                    "scorecard metric dropped mixed-source citations: dimension=%s source_label=%s dropped=%s",
                    dimension,
                    source_label.value,
                    dropped_count,
                )

        normalized_ids = [citation_id for citation_id, _ in normalized_pairs]
        normalized_citations = [citation for _, citation in normalized_pairs]
        return source_label, normalized_ids, normalized_citations

    @staticmethod
    def _validate_source_coverage(
        metrics: Dict[str, LaneMetricResult],
        *,
        require_narrative: bool,
    ) -> None:
        labels = {metric.source_label for metric in metrics.values()}
        if require_narrative and AnalysisSourceLabel.NARRATIVE_SIMULATION not in labels:
            raise ValueError("scorecard 在存在 narrative artifacts 时至少需要 1 个 narrative_simulation 维度")
        if AnalysisSourceLabel.RESEARCH_CITATION not in labels:
            raise ValueError("scorecard 至少需要 1 个 research_citation 维度")
        if AnalysisSourceLabel.PRIVATE_ANALYSIS not in labels:
            raise ValueError("scorecard 至少需要 1 个 private_analysis 维度")
