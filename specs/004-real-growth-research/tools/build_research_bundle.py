#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any, Callable


SPEC_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = SPEC_DIR / "artifacts"
TRANSFORM_DIR = ARTIFACTS_DIR / "transform"
SOURCE_SNAPSHOTS_PATH = TRANSFORM_DIR / "source-snapshots.json"

HOME = Path.home()
QUICKBOOKS_ROOT = HOME / "dev" / "quickbooks"
QUICKBOOKS_DATA = QUICKBOOKS_ROOT / "data-package"
QUICKBOOKS_RESEARCH = QUICKBOOKS_ROOT / "specs" / "009-market-intelligence" / "research"


EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\$)(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b")
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
CURRENCY_RE = re.compile(r"\$[\d,]+(?:\.\d+)?")
INLINE_PROVENANCE_MAX_CHARS = 320
SAFE_NOTE_KEYWORDS = {
    "budget",
    "close",
    "closing",
    "contract",
    "demo",
    "discount",
    "expansion",
    "followup",
    "forecast",
    "launch",
    "license",
    "maintenance",
    "meeting",
    "milestone",
    "pricing",
    "procurement",
    "proposal",
    "renewal",
    "review",
    "risk",
    "scope",
    "security",
    "signature",
    "support",
    "timeline",
}
REQUIRED_FRONTMATTER_KEYS = [
    "title",
    "source_id",
    "source_path",
    "source_repo",
    "source_snapshot_ref",
    "snapshot_date",
    "record_count",
    "record_count_method",
    "transform_method",
    "selection_rule",
    "raw_sha256",
    "evidence_tier",
    "sensitivity_class",
    "generated_at",
]
REQUIRED_INLINE_TOKENS = [
    "source_id=",
    "source_path=",
    "records=",
    "tier=",
    "snapshot=",
    "method=",
]


@dataclass(frozen=True)
class SourceConfig:
    source_id: str
    filename: str
    evidence_tier: str
    sensitivity_class: str
    transform_method: str
    selection_rule: str
    summary: str
    upstream_system: str
    group: str
    pii_mode: str = "structured-safe"

    @property
    def path(self) -> Path:
        return QUICKBOOKS_DATA / self.filename


def _source_configs() -> list[SourceConfig]:
    return [
        SourceConfig(
            source_id="QBO-07",
            filename="07-qbo-ar-aging.json",
            evidence_tier="internal-primary",
            sensitivity_class="financial-internal",
            transform_method="qbo_ar_aging_v1",
            selection_rule="tier-a-triage",
            summary="Accounts receivable aging buckets for immediate collections work.",
            upstream_system="QuickBooks",
            group="tier-a",
        ),
        SourceConfig(
            source_id="QBO-08",
            filename="08-qbo-financial-summary.json",
            evidence_tier="internal-primary",
            sensitivity_class="financial-internal",
            transform_method="qbo_financial_summary_v1",
            selection_rule="tier-a-triage",
            summary="Cash position, runway, burn, and concentration metrics.",
            upstream_system="QuickBooks",
            group="tier-a",
        ),
        SourceConfig(
            source_id="PD-01",
            filename="01-pipedrive-open-pipeline.json",
            evidence_tier="internal-primary",
            sensitivity_class="sales-sensitive",
            transform_method="open_pipeline_rollup_v1",
            selection_rule="tier-a-triage",
            summary="Open pipeline rollup emphasizing stage, value, and near-term timing.",
            upstream_system="Pipedrive",
            group="tier-a",
        ),
        SourceConfig(
            source_id="FC-05",
            filename="05-forecast-active-projects.json",
            evidence_tier="internal-primary",
            sensitivity_class="delivery-internal",
            transform_method="forecast_active_projects_v1",
            selection_rule="tier-a-triage",
            summary="Active-project budget and timing rollup for delivery load.",
            upstream_system="Forecast",
            group="tier-a",
        ),
        SourceConfig(
            source_id="FC-06",
            filename="06-forecast-team-capacity.json",
            evidence_tier="internal-primary",
            sensitivity_class="delivery-internal",
            transform_method="forecast_team_capacity_v1",
            selection_rule="tier-a-triage",
            summary="Team capacity by role and department.",
            upstream_system="Forecast",
            group="tier-a",
        ),
        SourceConfig(
            source_id="PD-09",
            filename="09-lost-deals-analysis.json",
            evidence_tier="internal-primary",
            sensitivity_class="sales-sensitive",
            transform_method="lost_deals_analysis_v1",
            selection_rule="tier-a-triage",
            summary="Failure-pattern analysis for lost deals and recent high-value losses.",
            upstream_system="Pipedrive",
            group="tier-a",
        ),
        SourceConfig(
            source_id="PD-10",
            filename="10-notes-on-open-deals.json",
            evidence_tier="internal-primary",
            sensitivity_class="crm-restricted",
            transform_method="open_deal_notes_signals_v1",
            selection_rule="tier-a-triage",
            summary="Sanitized signal extraction from open-deal notes; no raw notes committed.",
            upstream_system="Pipedrive",
            group="tier-a",
            pii_mode="free-text-signal",
        ),
        SourceConfig(
            source_id="PD-02",
            filename="02-pipedrive-won-deals-2022-2026.json",
            evidence_tier="internal-primary",
            sensitivity_class="sales-sensitive",
            transform_method="won_deals_history_v1",
            selection_rule="tier-b-history",
            summary="Won-deal trend and concentration rollup across years.",
            upstream_system="Pipedrive",
            group="tier-b",
        ),
        SourceConfig(
            source_id="PD-11",
            filename="11-pipedrive-leads.json",
            evidence_tier="internal-primary",
            sensitivity_class="sales-sensitive",
            transform_method="leads_rollup_v1",
            selection_rule="tier-b-history",
            summary="Inbound lead rollup emphasizing timing, value, and source signals.",
            upstream_system="Pipedrive",
            group="tier-b",
        ),
        SourceConfig(
            source_id="PD-03",
            filename="03-client-relationship-profiles.json",
            evidence_tier="internal-primary",
            sensitivity_class="crm-restricted",
            transform_method="client_relationship_rollup_v1",
            selection_rule="tier-b-summary-only",
            summary="Org-level relationship rollup with contact counts only; no named contacts committed.",
            upstream_system="Pipedrive",
            group="tier-b",
            pii_mode="nested-contacts-summary",
        ),
        SourceConfig(
            source_id="PD-04",
            filename="04-contacts-with-deal-history.json",
            evidence_tier="internal-primary",
            sensitivity_class="crm-restricted",
            transform_method="contact_history_org_rollup_v1",
            selection_rule="tier-b-summary-only",
            summary="Organization-level contact coverage summary; names, emails, and phones excluded.",
            upstream_system="Pipedrive",
            group="tier-b",
            pii_mode="contact-rollup",
        ),
    ]


SOURCE_INDEX = {cfg.source_id: cfg for cfg in _source_configs()}
DENYLIST_KEYS = {"name", "email", "phone", "person_name", "user", "contacts"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def record_count(data: Any) -> tuple[int, str]:
    if isinstance(data, list):
        return len(data), "list_length"
    if isinstance(data, dict):
        return len(data), "dict_keys"
    return 1, "scalar"


def git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return None


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def strip_html(text: str) -> str:
    return WHITESPACE_RE.sub(" ", unescape(TAG_RE.sub(" ", text or ""))).strip()


def redact_text(text: str) -> str:
    value = strip_html(text)
    value = EMAIL_RE.sub("[redacted-email]", value)
    value = PHONE_RE.sub("[redacted-phone]", value)
    return value


def extract_safe_note_keywords(text: str) -> list[str]:
    normalized = text.lower().replace("-", "")
    found = {keyword for keyword in SAFE_NOTE_KEYWORDS if keyword in normalized}
    return sorted(found)[:6]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise SystemExit("missing yaml frontmatter header")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise SystemExit("missing yaml frontmatter terminator")
    frontmatter = {}
    for line in parts[0].splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def build_source_snapshots() -> list[dict[str, Any]]:
    repo_sha = git_head(QUICKBOOKS_ROOT)
    snapshots = []
    for cfg in _source_configs():
        if not cfg.path.exists():
            raise FileNotFoundError(f"Missing source file: {cfg.path}")
        data = load_json(cfg.path)
        count, count_method = record_count(data)
        snapshots.append(
            {
                "source_id": cfg.source_id,
                "filename": cfg.filename,
                "source_path": str(cfg.path),
                "source_repo": str(QUICKBOOKS_ROOT),
                "source_snapshot_ref": repo_sha or str(cfg.path),
                "snapshot_date": datetime.fromtimestamp(cfg.path.stat().st_mtime, tz=timezone.utc)
                .date()
                .isoformat(),
                "record_count": count,
                "record_count_method": count_method,
                "raw_sha256": sha256_file(cfg.path),
                "evidence_tier": cfg.evidence_tier,
                "sensitivity_class": cfg.sensitivity_class,
                "transform_method": cfg.transform_method,
                "selection_rule": cfg.selection_rule,
                "upstream_system": cfg.upstream_system,
                "summary": cfg.summary,
                "pii_mode": cfg.pii_mode,
                "frozen_at": now_iso(),
            }
        )
    return snapshots


def load_snapshots() -> list[dict[str, Any]]:
    if not SOURCE_SNAPSHOTS_PATH.exists():
        raise FileNotFoundError("source-snapshots.json does not exist; run freeze first")
    return json.loads(SOURCE_SNAPSHOTS_PATH.read_text(encoding="utf-8"))


def validate_snapshots_or_fail() -> list[dict[str, Any]]:
    snapshots = load_snapshots()
    errors: list[str] = []
    for item in snapshots:
        path = Path(item["source_path"])
        if not path.exists():
            errors.append(f"{item['source_id']}: missing {path}")
            continue
        actual = sha256_file(path)
        if actual != item["raw_sha256"]:
            errors.append(
                f"{item['source_id']}: checksum drift for {path.name} "
                f"(expected {item['raw_sha256']}, got {actual})"
            )
    if errors:
        raise SystemExit("Snapshot validation failed:\n- " + "\n- ".join(errors))
    return snapshots


def compact_provenance_line(snapshot: dict[str, Any]) -> str:
    snapshot_ref = Path(snapshot["source_snapshot_ref"]).name
    source_path = Path(snapshot["source_path"]).name
    line = (
        f"`source_id={snapshot['source_id']}` "
        f"`source_path={source_path}` "
        f"`records={snapshot['record_count']}` "
        f"`tier={snapshot['evidence_tier']}` "
        f"`snapshot={snapshot_ref}` "
        f"`method={snapshot['transform_method']}`"
    )
    if len(line) > INLINE_PROVENANCE_MAX_CHARS:
        raise ValueError(
            f"Inline provenance exceeds budget ({len(line)} > {INLINE_PROVENANCE_MAX_CHARS}) for {snapshot['source_id']}"
        )
    return line


def yaml_frontmatter(snapshot: dict[str, Any], title: str) -> str:
    fields = {
        "title": title,
        "source_id": snapshot["source_id"],
        "source_path": snapshot["source_path"],
        "source_repo": snapshot["source_repo"],
        "source_snapshot_ref": snapshot["source_snapshot_ref"],
        "snapshot_date": snapshot["snapshot_date"],
        "record_count": snapshot["record_count"],
        "record_count_method": snapshot["record_count_method"],
        "transform_method": snapshot["transform_method"],
        "selection_rule": snapshot["selection_rule"],
        "raw_sha256": snapshot["raw_sha256"],
        "evidence_tier": snapshot["evidence_tier"],
        "sensitivity_class": snapshot["sensitivity_class"],
        "generated_at": now_iso(),
    }
    lines = ["---"]
    for key, value in fields.items():
        lines.append(f'{key}: "{str(value).replace(chr(34), chr(39))}"')
    lines.append("---")
    return "\n".join(lines)


def render_markdown(title: str, snapshot: dict[str, Any], sections: list[tuple[str, str]]) -> str:
    body = [
        yaml_frontmatter(snapshot, title),
        "",
        f"# {title}",
        "",
        "## Provenance",
        "",
        compact_provenance_line(snapshot),
        "",
    ]
    for heading, content in sections:
        body.extend([f"## {heading}", "", content.strip(), ""])
    return "\n".join(body).strip() + "\n"


def currency(value: Any) -> str:
    try:
        return f"${float(value):,.0f}"
    except (TypeError, ValueError):
        return "n/a"


def top_lines(pairs: list[tuple[str, Any]], limit: int = 5, formatter: Callable[[Any], str] | None = None) -> str:
    if formatter is None:
        formatter = lambda value: str(value)
    lines = []
    for key, value in pairs[:limit]:
        lines.append(f"- {key}: {formatter(value)}")
    return "\n".join(lines) if lines else "- none"


def transform_qbo_financial_summary(data: dict[str, Any]) -> list[tuple[str, str]]:
    overview = data.get("overview_kpis", {})
    sections = [
        (
            "Key Signals",
            "\n".join(
                [
                    f"- Cash position: {currency(data.get('cash_position'))}",
                    f"- Runway months: {data.get('runway_months', 'n/a')}",
                    f"- Monthly burn: {currency(data.get('monthly_burn'))}",
                    f"- Snapshot date: {data.get('snapshot_date', 'n/a')}",
                ]
            ),
        ),
        (
            "Overview KPIs",
            "\n".join(f"- {key}: {value}" for key, value in overview.items()) or "- none",
        ),
        (
            "Concentration",
            json.dumps(data.get("concentration", {}), indent=2, ensure_ascii=False),
        ),
    ]
    return sections


def transform_qbo_ar_aging(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    totals = defaultdict(float)
    for row in data:
        for key in ["current", "1_30", "31_60", "61_90", "91_over", "total"]:
            totals[key] += float(row.get(key, 0) or 0)
    top_customers = sorted(data, key=lambda row: float(row.get("total", 0) or 0), reverse=True)
    sections = [
        (
            "Aging Totals",
            "\n".join(
                [
                    f"- Current: {currency(totals['current'])}",
                    f"- 1-30: {currency(totals['1_30'])}",
                    f"- 31-60: {currency(totals['31_60'])}",
                    f"- 61-90: {currency(totals['61_90'])}",
                    f"- 91+: {currency(totals['91_over'])}",
                    f"- Total AR: {currency(totals['total'])}",
                ]
            ),
        ),
        (
            "Largest Balances",
            top_lines([(row["customer"], row["total"]) for row in top_customers], formatter=currency),
        ),
    ]
    return sections


def transform_lost_deals(data: dict[str, Any]) -> list[tuple[str, str]]:
    top_reasons = data.get("top_reasons", {})
    if isinstance(top_reasons, dict):
        reason_pairs = sorted(top_reasons.items(), key=lambda pair: pair[1], reverse=True)
    else:
        reason_pairs = [
            (item.get("reason", "unknown"), item.get("count", 0))
            for item in top_reasons
            if isinstance(item, dict)
        ]
    sections = [
        (
            "Loss Summary",
            "\n".join(
                [
                    f"- Total lost deals: {data.get('total_lost_deals', 'n/a')}",
                    f"- Total lost value: {currency(data.get('total_lost_value'))}",
                    f"- Died internally count: {data.get('died_internally_count', 'n/a')}",
                    f"- Died internally value: {currency(data.get('died_internally_value'))}",
                ]
            ),
        ),
        (
            "Top Reasons",
            top_lines(reason_pairs),
        ),
        (
            "Recent High-Value Losses",
            "\n".join(
                f"- {item.get('org', item.get('org_name', 'unknown'))} — {currency(item.get('value'))} — {item.get('reason', 'no reason')}"
                for item in data.get("recent_high_value_losses", [])[:5]
            )
            or "- none",
        ),
    ]
    return sections


def transform_open_pipeline(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    by_stage = defaultdict(float)
    close_windows = Counter()
    top_deals = []
    for item in data:
        by_stage[item.get("stage_name", "Unknown")] += float(item.get("value", 0) or 0)
        date = item.get("expected_close_date")
        if date:
            close_windows[date[:7]] += 1
        top_deals.append(
            (
                f"{item.get('org_name', 'Unknown')} — {item.get('title', 'Untitled')}",
                item.get("value", 0),
            )
        )
    top_deals.sort(key=lambda pair: float(pair[1] or 0), reverse=True)
    sections = [
        ("Stage Value Rollup", top_lines(sorted(by_stage.items(), key=lambda pair: pair[1], reverse=True), formatter=currency)),
        ("Expected Close Windows", top_lines(close_windows.most_common())),
        ("Largest Pipeline Deals", top_lines(top_deals, formatter=currency)),
    ]
    return sections


def transform_forecast_active_projects(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    by_stage = Counter(item.get("stage", "Unknown") for item in data)
    budget_total = sum(float(item.get("budget", 0) or 0) for item in data)
    sections = [
        (
            "Portfolio Summary",
            "\n".join(
                [
                    f"- Active projects: {len(data)}",
                    f"- Total budget: {currency(budget_total)}",
                ]
            ),
        ),
        ("Stage Mix", top_lines(by_stage.most_common())),
        (
            "Largest Projects",
            top_lines(
                sorted(
                    [(f"{item.get('client', 'Unknown')} — {item.get('name', 'Untitled')}", item.get("budget", 0)) for item in data],
                    key=lambda pair: float(pair[1] or 0),
                    reverse=True,
                ),
                formatter=currency,
            ),
        ),
    ]
    return sections


def transform_team_capacity(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    by_role = Counter(item.get("role", "Unknown") for item in data)
    by_department = Counter(item.get("department", "Unknown") for item in data)
    weekly_capacity = sum(float(item.get("weekly_capacity", 0) or 0) for item in data)
    sections = [
        (
            "Capacity Summary",
            "\n".join(
                [
                    f"- Team members: {len(data)}",
                    f"- Weekly capacity: {weekly_capacity:,.1f} hours",
                ]
            ),
        ),
        ("Role Mix", top_lines(by_role.most_common())),
        ("Department Mix", top_lines(by_department.most_common())),
    ]
    return sections


def transform_open_deal_notes(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    rows = []
    for item in data:
        clean = redact_text(item.get("content", ""))
        values = ", ".join(CURRENCY_RE.findall(clean)[:3]) or "none"
        keywords = extract_safe_note_keywords(clean)
        rows.append(
            {
                "deal_id": item.get("deal_id"),
                "org_name": item.get("org_name"),
                "signals": values,
                "keywords": ", ".join(keywords) or "none",
                "updated": item.get("update_time"),
            }
        )
    sections = [
        (
            "Sanitized Note Signals",
            "\n".join(
                f"- Deal {row['deal_id']} / {row['org_name']}: amounts={row['signals']}; keywords={row['keywords']}; updated={row['updated']}"
                for row in rows[:10]
            )
            or "- none",
        ),
        (
            "Redaction Rules Applied",
            "\n".join(
                [
                    "- Omitted `person_name`, `user`, raw HTML, and raw note bodies from committed output.",
                    "- Emails and phone patterns are redacted before keyword extraction.",
                    "- Output carries only organization, deal id, timing, currency signals, and neutral keywords.",
                ]
            ),
        ),
    ]
    return sections


def transform_won_deals(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    by_year = Counter(str(item.get("year", "Unknown")) for item in data)
    revenue_by_org = defaultdict(float)
    for item in data:
        revenue_by_org[item.get("org_name", "Unknown")] += float(item.get("value", 0) or 0)
    sections = [
        ("Wins by Year", top_lines(sorted(by_year.items()), formatter=lambda value: str(value))),
        (
            "Top Revenue Orgs",
            top_lines(sorted(revenue_by_org.items(), key=lambda pair: pair[1], reverse=True), formatter=currency),
        ),
    ]
    return sections


def transform_leads(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    sections = [
        ("Lead Count", f"- Active leads: {len(data)}"),
        (
            "Lead Value Signals",
            top_lines(
                sorted(
                    [
                        (
                            item.get("title", f"Lead {item.get('id')}"),
                            item.get("value", 0),
                        )
                        for item in data
                    ],
                    key=lambda pair: float(pair[1] or 0),
                    reverse=True,
                ),
                formatter=currency,
            ),
        ),
    ]
    return sections


def transform_client_profiles(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    status_counts = Counter(item.get("status", "Unknown") for item in data)
    high_value = sorted(data, key=lambda row: float(row.get("total_revenue", 0) or 0), reverse=True)
    sections = [
        ("Status Mix", top_lines(status_counts.most_common())),
        (
            "Top Relationship Accounts",
            "\n".join(
                f"- {item.get('org_name')}: total_revenue={currency(item.get('total_revenue'))}; deals={item.get('deal_count')}; open_value={currency(item.get('open_deal_value'))}; contact_count={len(item.get('contacts', []))}"
                for item in high_value[:10]
            ),
        ),
        (
            "PII Handling",
            "- Contact names from the nested `contacts` field are counted but never emitted in committed artifacts.",
        ),
    ]
    return sections


def transform_contact_history(data: list[dict[str, Any]]) -> list[tuple[str, str]]:
    by_org: dict[str, dict[str, Any]] = {}
    for item in data:
        org = item.get("org_name", "Unknown")
        bucket = by_org.setdefault(org, {"contacts": 0, "won_value": 0.0, "open_value": 0.0, "total_deals": 0})
        bucket["contacts"] += 1
        bucket["won_value"] += float(item.get("won_deal_value", 0) or 0)
        bucket["open_value"] += float(item.get("open_deal_value", 0) or 0)
        bucket["total_deals"] += int(item.get("total_deals", 0) or 0)
    ranked = sorted(by_org.items(), key=lambda pair: pair[1]["won_value"] + pair[1]["open_value"], reverse=True)
    sections = [
        (
            "Organization Contact Coverage",
            "\n".join(
                f"- {org}: contacts={stats['contacts']}; won_value={currency(stats['won_value'])}; open_value={currency(stats['open_value'])}; total_deals={stats['total_deals']}"
                for org, stats in ranked[:12]
            )
            or "- none",
        ),
        (
            "PII Handling",
            "\n".join(
                [
                    "- Personal names, emails, phone numbers, and job titles are excluded entirely.",
                    "- Output is organization-level only, preserving relationship depth without leaking contact details.",
                ]
            ),
        ),
    ]
    return sections


TRANSFORMS: dict[str, Callable[[Any], list[tuple[str, str]]]] = {
    "QBO-07": transform_qbo_ar_aging,
    "QBO-08": transform_qbo_financial_summary,
    "PD-01": transform_open_pipeline,
    "FC-05": transform_forecast_active_projects,
    "FC-06": transform_team_capacity,
    "PD-09": transform_lost_deals,
    "PD-10": transform_open_deal_notes,
    "PD-02": transform_won_deals,
    "PD-11": transform_leads,
    "PD-03": transform_client_profiles,
    "PD-04": transform_contact_history,
}


def transform_one(source_id: str, snapshot: dict[str, Any]) -> Path:
    cfg = SOURCE_INDEX[source_id]
    data = load_json(Path(snapshot["source_path"]))
    title = f"{source_id} — {cfg.summary}"
    sections = TRANSFORMS[source_id](data)
    output = TRANSFORM_DIR / f"{source_id.lower().replace('-', '_')}.md"
    output.write_text(render_markdown(title, snapshot, sections), encoding="utf-8")
    return output


def validate_markdown(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    missing_fields = [field for field in REQUIRED_FRONTMATTER_KEYS if field not in frontmatter]
    if missing_fields:
        raise SystemExit(f"{path.name}: missing frontmatter fields {missing_fields}")
    missing = [token for token in REQUIRED_INLINE_TOKENS if token not in text]
    if missing:
        raise SystemExit(f"{path.name}: missing inline provenance tokens {missing}")
    if EMAIL_RE.search(text):
        raise SystemExit(f"{path.name}: email address leaked into committed output")
    if PHONE_RE.search(text):
        raise SystemExit(f"{path.name}: phone number leaked into committed output")
    lowered = text.lower()
    for denied in ["email:", "phone:", "person_name:", "contacts:", "user:"]:
        if denied in lowered:
            raise SystemExit(f"{path.name}: denylist token leaked: {denied}")


def cmd_freeze(_: argparse.Namespace) -> int:
    snapshots = build_source_snapshots()
    write_json(SOURCE_SNAPSHOTS_PATH, snapshots)
    print(f"Wrote {len(snapshots)} source snapshots to {SOURCE_SNAPSHOTS_PATH}")
    return 0


def cmd_validate(_: argparse.Namespace) -> int:
    snapshots = validate_snapshots_or_fail()
    print(f"Validated {len(snapshots)} source snapshots with no drift")
    return 0


def cmd_transform(args: argparse.Namespace) -> int:
    snapshots = {item["source_id"]: item for item in validate_snapshots_or_fail()}
    selected = _source_configs()
    if args.group != "all":
        selected = [cfg for cfg in selected if cfg.group == args.group]
    if args.source_id:
        selected = [SOURCE_INDEX[args.source_id]]
    outputs = []
    for cfg in selected:
        output = transform_one(cfg.source_id, snapshots[cfg.source_id])
        validate_markdown(output)
        outputs.append(output.name)
    print("Rendered transforms:")
    for name in outputs:
        print(f"- {name}")
    return 0


def cmd_validate_outputs(_: argparse.Namespace) -> int:
    count = 0
    for path in sorted(TRANSFORM_DIR.glob("*.md")):
        if path.name == "source-snapshots.json":
            continue
        validate_markdown(path)
        count += 1
    print(f"Validated {count} transform documents")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build spec-local research bundle artifacts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    freeze = subparsers.add_parser("freeze", help="Write source snapshot manifest")
    freeze.set_defaults(func=cmd_freeze)

    validate = subparsers.add_parser("validate-snapshots", help="Fail closed on source drift")
    validate.set_defaults(func=cmd_validate)

    transform = subparsers.add_parser("transform", help="Render markdown transforms")
    transform.add_argument("--group", choices=["tier-a", "tier-b", "all"], default="all")
    transform.add_argument("--source-id", choices=sorted(SOURCE_INDEX), default=None)
    transform.set_defaults(func=cmd_transform)

    validate_outputs = subparsers.add_parser("validate-outputs", help="Run mechanical validation on rendered markdown")
    validate_outputs.set_defaults(func=cmd_validate_outputs)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
