import json
from types import SimpleNamespace

import pytest

import app.services.graph_builder as graph_builder_module
from app.models.strategy_lab import ChunkManifestEntry
from app.services.graph_builder import GraphBuilderService


class FakeGraph:
    def __init__(self, uuid_batches):
        self.uuid_batches = uuid_batches
        self.calls = 0

    def add_batch(self, graph_id, episodes):
        uuids = self.uuid_batches[self.calls]
        self.calls += 1
        return [SimpleNamespace(uuid_=value) for value in uuids]


def _build_service(uuid_batches):
    service = GraphBuilderService.__new__(GraphBuilderService)
    service.client = SimpleNamespace(graph=FakeGraph(uuid_batches))
    return service


def test_add_text_batches_backfills_manifest_and_writes_atomically(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(graph_builder_module.time, "sleep", lambda _: None)
    manifest_path = tmp_path / "chunk_manifest.json"
    chunk_entries = [
        ChunkManifestEntry(
            chunk_id="chunk-1",
            document_id="doc-1",
            filename="market.docx",
            text="alpha",
            start_char=0,
            end_char=5,
            locator_start="paragraph:1",
            locator_end="paragraph:1",
        ),
        ChunkManifestEntry(
            chunk_id="chunk-2",
            document_id="doc-1",
            filename="market.docx",
            text="beta",
            start_char=6,
            end_char=10,
            locator_start="paragraph:2",
            locator_end="paragraph:2",
        ),
    ]

    service = _build_service([["ep-1", "ep-2"]])
    episode_uuids = service.add_text_batches(
        "graph-1",
        ["alpha", "beta"],
        batch_size=2,
        chunk_entries=chunk_entries,
        manifest_path=str(manifest_path),
    )

    saved_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert episode_uuids == ["ep-1", "ep-2"]
    assert [entry["episode_uuid"] for entry in saved_manifest] == ["ep-1", "ep-2"]


def test_add_text_batches_fails_closed_when_batch_count_mismatches(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(graph_builder_module.time, "sleep", lambda _: None)
    manifest_path = tmp_path / "chunk_manifest.json"
    chunk_entries = [
        ChunkManifestEntry(
            chunk_id="chunk-1",
            document_id="doc-1",
            filename="market.docx",
            text="alpha",
            start_char=0,
            end_char=5,
            locator_start="paragraph:1",
            locator_end="paragraph:1",
        ),
        ChunkManifestEntry(
            chunk_id="chunk-2",
            document_id="doc-1",
            filename="market.docx",
            text="beta",
            start_char=6,
            end_char=10,
            locator_start="paragraph:2",
            locator_end="paragraph:2",
        ),
    ]

    service = _build_service([["ep-1"]])

    with pytest.raises(ValueError, match="返回数量异常"):
        service.add_text_batches(
            "graph-1",
            ["alpha", "beta"],
            batch_size=2,
            chunk_entries=chunk_entries,
            manifest_path=str(manifest_path),
        )

    saved_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert [entry["episode_uuid"] for entry in saved_manifest] == [None, None]
