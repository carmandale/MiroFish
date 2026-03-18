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

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class LaneTemplate:
    """策略路径模板"""

    lane_id: str
    title: str
    hypothesis: str
    target_accounts: List[str] = field(default_factory=list)
    key_capabilities: List[str] = field(default_factory=list)
    evaluation_dimensions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class LaneRunContext:
    """单条策略路径运行上下文"""

    lane_id: str
    workflow_mode: WorkflowMode
    template_path: str
    lane_context_path: str
    assumptions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return _serialize(self)


@dataclass
class LaneScorecard:
    """路径评分卡"""

    lane_id: str
    summary: str
    metrics: Dict[str, Any]
    caveats: List[str] = field(default_factory=list)

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
