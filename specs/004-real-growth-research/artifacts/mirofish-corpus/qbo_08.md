---
title: "QBO-08 — Cash position, runway, burn, and concentration metrics."
source_id: "QBO-08"
source_path: "/Users/dalecarman/dev/quickbooks/data-package/08-qbo-financial-summary.json"
source_repo: "/Users/dalecarman/dev/quickbooks"
source_snapshot_ref: "636270bfc38682401d5ac1f60cc87cea03f13b3d"
snapshot_date: "2026-03-18"
record_count: "6"
record_count_method: "dict_keys"
transform_method: "qbo_financial_summary_v1"
selection_rule: "tier-a-triage"
raw_sha256: "b46bebefbfddcc50e244b7af5740e3a6069f342967ae5aebb960c4c22e6978bf"
evidence_tier: "internal-primary"
sensitivity_class: "financial-internal"
generated_at: "2026-03-20T17:06:14+00:00"
---

# QBO-08 — Cash position, runway, burn, and concentration metrics.

## Provenance

`source_id=QBO-08` `source_path=08-qbo-financial-summary.json` `records=6` `tier=internal-primary` `snapshot=636270bfc38682401d5ac1f60cc87cea03f13b3d` `method=qbo_financial_summary_v1`

## Key Signals

- Cash position: $19,455
- Runway months: 0
- Monthly burn: $397,456
- Snapshot date: 2026-03-17T10:00:00Z

## Overview KPIs

- revenue: 7068679.48
- netIncome: -608991.8
- grossProfit: 3681559.27
- cogs: 3387120.21
- totalExpenses: 3860379.57
- grossMarginPct: 52.1
- netMarginPct: -8.6
- cashPosition: 19454.91
- runwayMonths: 0
- runwayNetPositive: False
- arOutstanding: 242641

## Concentration

{
  "hhi": 552,
  "level": "low",
  "clients": [
    {
      "name": "25025 Disasterville VR",
      "revenue": 900000,
      "share": 12.1
    },
    {
      "name": "25031 Ottava Surgical Robotic Holistic XR",
      "revenue": 823793.88,
      "share": 11.1
    },
    {
      "name": "25062 ASU STEM Innovation Lab Apps",
      "revenue": 650000,
      "share": 8.8
    },
    {
      "name": "25069 Drone Racing",
      "revenue": 523900,
      "share": 7.1
    },
    {
      "name": "25059 AT&T Fiber App VR and iOS",
      "revenue": 376500,
      "share": 5.1
    },
    {
      "name": "25015 Honda AVP",
      "revenue": 314878.2,
      "share": 4.2
    },
    {
      "name": "25047 SWA Getaways Portal",
      "revenue": 288291.46,
      "share": 3.9
    },
    {
      "name": "25066 Mission Ready AI",
      "revenue": 268383.15,
      "share": 3.6
    },
    {
      "name": "24077 Engineering Data Visualization and Digital Art Service Agreement",
      "revenue": 265465.73,
      "share": 3.6
    },
    {
      "name": "25036 FIFA Scanner - NJ Finals",
      "revenue": 245181.41,
      "share": 3.3
    }
  ]
}
