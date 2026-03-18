"""
Strategy Lab 相关数据模型
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class WorkflowMode(str, Enum):
    """项目工作流模式"""

    DEFAULT = "default"
    STRATEGY_LAB = "strategy_lab"


class LocatorType(str, Enum):
    """来源定位符类型"""

    PAGE = "page"
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    SECTION = "section"
    CHARACTER_RANGE = "character_range"


class SourceLabel(str, Enum):
    """文档来源标签"""

    PRIMARY = "primary"
    SUPPORTING = "supporting"


class AnalysisSourceLabel(str, Enum):
    """评分卡指标来源标签"""

    NARRATIVE_SIMULATION = "narrative_simulation"
    PRIVATE_ANALYSIS = "private_analysis"
    RESEARCH_CITATION = "research_citation"
    MONTE_CARLO_ATTACHMENT = "monte_carlo_attachment"


def _serialize(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _serialize(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


@dataclass
class DocumentSegment:
    """文档中的可引用片段"""

    locator_type: LocatorType
    locator: str
    start_char: int
    end_char: int
    text: str

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentSegment":
        locator_type = data.get("locator_type", LocatorType.CHARACTER_RANGE.value)
        return cls(
            locator_type=LocatorType(locator_type),
            locator=data.get("locator", ""),
            start_char=data.get("start_char", 0),
            end_char=data.get("end_char", 0),
            text=data.get("text", ""),
        )


@dataclass
class ExtractedDocument:
    """文档提取结果"""

    document_id: str
    original_filename: str
    saved_filename: str
    file_path: str
    extension: str
    text: str
    segments: List[DocumentSegment] = field(default_factory=list)
    source_label: SourceLabel = SourceLabel.PRIMARY

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractedDocument":
        return cls(
            document_id=data["document_id"],
            original_filename=data.get("original_filename", ""),
            saved_filename=data.get("saved_filename", ""),
            file_path=data.get("file_path", ""),
            extension=data.get("extension", ""),
            text=data.get("text", ""),
            segments=[
                DocumentSegment.from_dict(item)
                for item in data.get("segments", [])
            ],
            source_label=SourceLabel(data.get("source_label", SourceLabel.PRIMARY.value)),
        )


@dataclass
class DocumentManifestEntry:
    """语料清单条目"""

    document_id: str
    filename: str
    saved_filename: str
    extension: str
    source_label: SourceLabel
    text_length: int
    segment_count: int

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class ChunkManifestEntry:
    """切块清单条目"""

    chunk_id: str
    document_id: str
    filename: str
    text: str
    start_char: int
    end_char: int
    locator_start: str
    locator_end: str
    episode_uuid: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChunkManifestEntry":
        return cls(
            chunk_id=data["chunk_id"],
            document_id=data["document_id"],
            filename=data.get("filename", ""),
            text=data.get("text", ""),
            start_char=data.get("start_char", 0),
            end_char=data.get("end_char", 0),
            locator_start=data.get("locator_start", ""),
            locator_end=data.get("locator_end", ""),
            episode_uuid=data.get("episode_uuid"),
        )


@dataclass
class CitationRecord:
    """报告或评分卡中的引用记录"""

    chunk_id: str
    filename: str
    locator: str
    quote: str
    episode_uuid: Optional[str] = None
    source_label: AnalysisSourceLabel = AnalysisSourceLabel.RESEARCH_CITATION

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class LaneTemplate:
    """策略路径模板"""

    lane_id: str
    display_name: str
    hypothesis: str
    public_actor_classes: List[str] = field(default_factory=list)
    public_event_classes: List[str] = field(default_factory=list)
    narrative_brief: str = ""
    interview_personas: List[str] = field(default_factory=list)
    private_committee_roles: List[str] = field(default_factory=list)
    procurement_gates: List[str] = field(default_factory=list)
    capability_requirements: List[str] = field(default_factory=list)
    required_internal_inputs: List[str] = field(default_factory=list)
    scorecard_dimensions: List[str] = field(default_factory=list)
    monte_carlo_fields: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LaneTemplate":
        return cls(
            lane_id=data["lane_id"],
            display_name=data.get("display_name", data.get("title", "")),
            hypothesis=data.get("hypothesis", ""),
            public_actor_classes=data.get("public_actor_classes", []),
            public_event_classes=data.get("public_event_classes", []),
            narrative_brief=data.get("narrative_brief", ""),
            interview_personas=data.get("interview_personas", []),
            private_committee_roles=data.get("private_committee_roles", []),
            procurement_gates=data.get("procurement_gates", []),
            capability_requirements=data.get("capability_requirements", []),
            required_internal_inputs=data.get("required_internal_inputs", []),
            scorecard_dimensions=data.get("scorecard_dimensions", []),
            monte_carlo_fields=data.get("monte_carlo_fields", []),
        )


@dataclass
class LaneRunContext:
    """单条策略路径运行上下文"""

    lane_id: str
    workflow_mode: WorkflowMode
    template_path: str
    lane_context_path: str
    assumptions: List[str] = field(default_factory=list)
    display_name: str = ""
    narrative_brief: str = ""
    public_actor_classes: List[str] = field(default_factory=list)
    public_event_classes: List[str] = field(default_factory=list)
    interview_personas: List[str] = field(default_factory=list)
    procurement_gates: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class LaneMetricResult:
    """单个评分维度结果"""

    dimension: str
    score: str
    judgment: str
    source_label: AnalysisSourceLabel
    citation_ids: List[str] = field(default_factory=list)
    citations: List[CitationRecord] = field(default_factory=list)
    monte_carlo_attachment: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class LaneScorecard:
    """路径评分卡"""

    lane_id: str
    display_name: str
    summary: str
    metrics: Dict[str, LaneMetricResult]
    assumptions: List[str] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class LaneRunStatus:
    """单条路径运行状态"""

    project_id: str
    lane_id: str
    run_id: str
    workflow_mode: WorkflowMode
    status: str
    stage: str
    created_at: str
    updated_at: str
    artifact_paths: Dict[str, str] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class InterviewArtifact:
    """访谈纪要"""

    lane_id: str
    run_id: str
    transcript_markdown: str
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class ComparativeReport:
    """多路径对比报告"""

    project_id: str
    generated_at: str
    rows: List[Dict[str, Any]]
    markdown_summary: str
    citations: Dict[str, CitationRecord] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)
