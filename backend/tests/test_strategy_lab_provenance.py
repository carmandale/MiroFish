from app.models.strategy_lab import (
    DocumentSegment,
    ExtractedDocument,
    LocatorType,
)
from app.services.strategy_lab_provenance import StrategyLabProvenanceService


def _build_document() -> ExtractedDocument:
    return ExtractedDocument(
        document_id="doc_lane",
        original_filename="lane-notes.md",
        saved_filename="lane.md",
        file_path="/tmp/lane-notes.md",
        extension="md",
        text="Alpha market.\n\nBeta motion.\n\nGamma lane.",
        segments=[
            DocumentSegment(
                locator_type=LocatorType.PARAGRAPH,
                locator="paragraph:1",
                start_char=0,
                end_char=13,
                text="Alpha market.",
            ),
            DocumentSegment(
                locator_type=LocatorType.PARAGRAPH,
                locator="paragraph:2",
                start_char=15,
                end_char=27,
                text="Beta motion.",
            ),
            DocumentSegment(
                locator_type=LocatorType.PARAGRAPH,
                locator="paragraph:3",
                start_char=29,
                end_char=40,
                text="Gamma lane.",
            ),
        ],
    )


def test_build_corpus_manifest_summarizes_documents():
    manifest = StrategyLabProvenanceService.build_corpus_manifest([_build_document()])

    assert len(manifest) == 1
    assert manifest[0].filename == "lane-notes.md"
    assert manifest[0].segment_count == 3


def test_build_chunk_manifest_preserves_filename_and_locator_ranges():
    entries = StrategyLabProvenanceService.build_chunk_manifest(
        [_build_document()],
        chunk_size=18,
        overlap=0,
    )

    assert len(entries) >= 2
    assert entries[0].chunk_id == "doc_lane-chunk-0001"
    assert entries[0].filename == "lane-notes.md"
    assert entries[0].locator_start == "paragraph:1"
    assert entries[-1].locator_end in {"paragraph:2", "paragraph:3"}
    assert all(entry.episode_uuid is None for entry in entries)
