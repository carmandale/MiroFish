"""
Strategy Lab 语料与切块溯源服务
"""

from __future__ import annotations

from typing import List, Tuple

from ..models.strategy_lab import (
    ChunkManifestEntry,
    DocumentManifestEntry,
    DocumentSegment,
    ExtractedDocument,
)


class StrategyLabProvenanceService:
    """构建语料清单与 chunk 清单"""

    @staticmethod
    def build_corpus_manifest(
        documents: List[ExtractedDocument],
    ) -> List[DocumentManifestEntry]:
        return [
            DocumentManifestEntry(
                document_id=document.document_id,
                filename=document.original_filename,
                saved_filename=document.saved_filename,
                extension=document.extension,
                source_label=document.source_label,
                text_length=len(document.text),
                segment_count=len(document.segments),
            )
            for document in documents
        ]

    @classmethod
    def build_chunk_manifest(
        cls,
        documents: List[ExtractedDocument],
        chunk_size: int,
        overlap: int,
    ) -> List[ChunkManifestEntry]:
        entries: List[ChunkManifestEntry] = []

        for document in documents:
            for index, (chunk_text, start_char, end_char) in enumerate(
                cls.split_text_with_offsets(document.text, chunk_size, overlap),
                start=1,
            ):
                locator_start, locator_end = cls._resolve_locators(
                    document.segments,
                    start_char,
                    end_char,
                )
                entries.append(
                    ChunkManifestEntry(
                        chunk_id=f"{document.document_id}-chunk-{index:04d}",
                        document_id=document.document_id,
                        filename=document.original_filename,
                        text=chunk_text,
                        start_char=start_char,
                        end_char=end_char,
                        locator_start=locator_start,
                        locator_end=locator_end,
                    )
                )

        return entries

    @staticmethod
    def split_text_with_offsets(
        text: str,
        chunk_size: int,
        overlap: int,
    ) -> List[Tuple[str, int, int]]:
        if len(text) <= chunk_size:
            normalized = text.strip()
            return [(normalized, 0, len(text))] if normalized else []

        chunks: List[Tuple[str, int, int]] = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            if end < len(text):
                window = text[start:end]
                for separator in ['。', '！', '？', '.\n', '!\n', '?\n', '\n\n', '. ', '! ', '? ']:
                    last_sep = window.rfind(separator)
                    if last_sep != -1 and last_sep > chunk_size * 0.3:
                        end = start + last_sep + len(separator)
                        break

            raw_chunk = text[start:end]
            trimmed_chunk = raw_chunk.strip()
            if trimmed_chunk:
                left_padding = len(raw_chunk) - len(raw_chunk.lstrip())
                right_padding = len(raw_chunk) - len(raw_chunk.rstrip())
                chunk_start = start + left_padding
                chunk_end = end - right_padding
                chunks.append((trimmed_chunk, chunk_start, chunk_end))

            start = end - overlap if end < len(text) else len(text)

        return chunks

    @staticmethod
    def _resolve_locators(
        segments: List[DocumentSegment],
        start_char: int,
        end_char: int,
    ) -> Tuple[str, str]:
        if not segments:
            fallback = f"chars:{start_char}-{end_char}"
            return fallback, fallback

        overlapping = [
            segment
            for segment in segments
            if segment.end_char > start_char and segment.start_char < end_char
        ]

        if not overlapping:
            fallback = f"chars:{start_char}-{end_char}"
            return fallback, fallback

        return overlapping[0].locator, overlapping[-1].locator
