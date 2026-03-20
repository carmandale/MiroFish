from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "tools" / "build_research_bundle.py"
SPEC = importlib.util.spec_from_file_location("build_research_bundle", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class BuildResearchBundleTests(unittest.TestCase):
    def test_compact_provenance_line_stays_within_budget(self) -> None:
        snapshot = {
            "source_id": "QBO-08",
            "source_path": "/tmp/08-qbo-financial-summary.json",
            "source_snapshot_ref": "206fb5787e8f92886d3b26ae94dc4539ab9be5a2",
            "record_count": 6,
            "evidence_tier": "internal-primary",
            "transform_method": "qbo_financial_summary_v1",
        }
        line = MODULE.compact_provenance_line(snapshot)
        self.assertIn("source_id=QBO-08", line)
        self.assertIn("source_path=08-qbo-financial-summary.json", line)
        self.assertIn("records=6", line)
        self.assertIn("tier=internal-primary", line)
        self.assertLessEqual(len(line), MODULE.INLINE_PROVENANCE_MAX_CHARS)

    def test_validate_snapshots_or_fail_detects_drift(self) -> None:
        source = Path(__file__)
        payload = [
            {
                "source_id": "X-01",
                "source_path": str(source),
                "raw_sha256": MODULE.sha256_file(source),
            }
        ]
        MODULE.validate_snapshot_payload_or_fail(payload)
        payload[0]["raw_sha256"] = "deadbeef"
        with self.assertRaises(SystemExit) as ctx:
            MODULE.validate_snapshot_payload_or_fail(payload)
        self.assertIn("checksum drift", str(ctx.exception))

    def test_transform_open_deal_notes_omits_raw_people_fields_and_names(self) -> None:
        data = [
            {
                "deal_id": 1,
                "content": "<p>Call Katherine at katie@example.com or +1 (214) 555-1234 about $25,000 annual license renewal.</p>",
                "org_name": "Init Labs",
                "person_name": "Katherine Monk",
                "user": "William O'Donnell",
                "update_time": "2026-03-02 21:28:34",
            }
        ]
        sections = dict(MODULE.transform_open_deal_notes(data))
        text = "\n".join(sections.values())
        self.assertIn("Init Labs", text)
        self.assertIn("$25,000", text)
        self.assertIn("license", text)
        self.assertIn("renewal", text)
        self.assertNotIn("Katherine", text)
        self.assertNotIn("Katherine Monk", text)
        self.assertNotIn("William O'Donnell", text)
        self.assertNotIn("katie@example.com", text)
        self.assertNotIn("214", text)

    def test_transform_contact_history_rolls_up_to_org_level(self) -> None:
        data = [
            {
                "name": "Dan McGowan",
                "email": "dmcgowan@teamwass.com",
                "phone": "214-555-1212",
                "org_name": "Wasserman",
                "won_deal_value": 1000,
                "open_deal_value": 500,
                "total_deals": 3,
            },
            {
                "name": "Nick Marello",
                "email": "nick@example.com",
                "phone": None,
                "org_name": "Wasserman",
                "won_deal_value": 2000,
                "open_deal_value": 0,
                "total_deals": 1,
            },
        ]
        sections = dict(MODULE.transform_contact_history(data))
        text = "\n".join(sections.values())
        self.assertIn("Wasserman: contacts=2", text)
        self.assertNotIn("Dan McGowan", text)
        self.assertNotIn("nick@example.com", text)
        self.assertNotIn("214-555-1212", text)

    def test_validate_markdown_requires_full_contract(self) -> None:
        sample_text = "\n".join(
            [
                "---",
                'title: "Sample"',
                'source_id: "X-01"',
                'source_path: "/tmp/source.json"',
                'source_repo: "/tmp"',
                'source_snapshot_ref: "abc123"',
                'snapshot_date: "2026-03-20"',
                'record_count: "1"',
                'record_count_method: "list_length"',
                'transform_method: "sample_v1"',
                'selection_rule: "tier-a"',
                'raw_sha256: "deadbeef"',
                'evidence_tier: "internal-primary"',
                'sensitivity_class: "restricted"',
                'generated_at: "2026-03-20T17:00:00+00:00"',
                "---",
                "",
                "## Provenance",
                "",
                "`source_id=X-01` `source_path=source.json` `records=1` `tier=internal-primary` `snapshot=abc123` `method=sample_v1`",
            ]
        )
        MODULE.validate_markdown_text(sample_text, "sample.md")
        broken = sample_text.replace('raw_sha256: "deadbeef"\n', "")
        with self.assertRaises(SystemExit) as ctx:
            MODULE.validate_markdown_text(broken, "broken.md")
        self.assertIn("missing frontmatter fields", str(ctx.exception))

    def test_all_transforms_render_and_validate_with_live_snapshots(self) -> None:
        snapshots = {item["source_id"]: item for item in MODULE.validate_snapshots_or_fail()}
        validated = 0
        for source_id, transform in MODULE.TRANSFORMS.items():
            snapshot = snapshots[source_id]
            data = MODULE.load_json(Path(snapshot["source_path"]))
            title = f"{source_id} — {MODULE.SOURCE_INDEX[source_id].summary}"
            text = MODULE.render_markdown(title, snapshot, transform(data))
            MODULE.validate_markdown_text(text, f"{source_id}.md")
            validated += 1
        self.assertEqual(validated, len(MODULE.TRANSFORMS))


if __name__ == "__main__":
    unittest.main()
