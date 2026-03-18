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
        citation_index = self._build_citation_index(lane_template, selected_chunks)

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

    def _build_citation_index(
        self,
        lane_template: LaneTemplate,
        chunks: List[ChunkManifestEntry],
    ) -> Dict[str, CitationRecord]:
        citation_index: Dict[str, CitationRecord] = {}
        for index, chunk in enumerate(chunks, start=1):
            citation_id = f"{lane_template.lane_id}:citation:{index:02d}"
            citation_index[citation_id] = CitationRecord(
                chunk_id=chunk.chunk_id,
                filename=chunk.filename,
                locator=f"{chunk.locator_start} -> {chunk.locator_end}",
                quote=chunk.text[:600],
                episode_uuid=chunk.episode_uuid,
                source_label=AnalysisSourceLabel.RESEARCH_CITATION,
            )
        return citation_index

    def _validate_scorecard_result(
        self,
        *,
        lane_template: LaneTemplate,
        result: Dict[str, object],
        citation_index: Dict[str, CitationRecord],
        monte_carlo_attachment: Optional[str],
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
            if source_label != AnalysisSourceLabel.MONTE_CARLO_ATTACHMENT:
                if not citation_ids:
                    raise ValueError(f"{dimension} 缺少 citation_ids")
                for citation_id in citation_ids:
                    if citation_id not in citation_index:
                        raise ValueError(f"{dimension} 使用了未知 citation_id: {citation_id}")
                    resolved_citations.append(citation_index[citation_id])

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
        return LaneScorecard(
            lane_id=lane_template.lane_id,
            display_name=lane_template.display_name,
            summary=str(result.get("summary", "")),
            metrics=metrics,
            assumptions=assumptions if isinstance(assumptions, list) else [],
            caveats=caveats if isinstance(caveats, list) else [],
        )
