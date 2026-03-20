from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
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
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            source = tmp_dir / "sample.json"
            source.write_text('{"a": 1}\n', encoding="utf-8")
            snapshot_path = tmp_dir / "source-snapshots.json"
            payload = [
                {
                    "source_id": "X-01",
                    "source_path": str(source),
                    "raw_sha256": MODULE.sha256_file(source),
                }
            ]
            snapshot_path.write_text(json.dumps(payload), encoding="utf-8")
            original = MODULE.SOURCE_SNAPSHOTS_PATH
            MODULE.SOURCE_SNAPSHOTS_PATH = snapshot_path
            try:
                MODULE.validate_snapshots_or_fail()
                source.write_text('{"a": 2}\n', encoding="utf-8")
                with self.assertRaises(SystemExit) as ctx:
                    MODULE.validate_snapshots_or_fail()
                self.assertIn("checksum drift", str(ctx.exception))
            finally:
                MODULE.SOURCE_SNAPSHOTS_PATH = original

    def test_transform_open_deal_notes_omits_raw_people_fields(self) -> None:
        data = [
            {
                "deal_id": 1,
                "content": "<p>Call Katie at katie@example.com or +1 (214) 555-1234 about $25,000 annual license.</p>",
                "org_name": "Init Labs",
                "person_name": "Katie Monk",
                "user": "William O'Donnell",
                "update_time": "2026-03-02 21:28:34",
            }
        ]
        sections = dict(MODULE.transform_open_deal_notes(data))
        text = "\n".join(sections.values())
        self.assertIn("Init Labs", text)
        self.assertIn("$25,000", text)
        self.assertNotIn("Katie Monk", text)
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


if __name__ == "__main__":
    unittest.main()
