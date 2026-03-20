# Source Inventory — Real Growth Research Foundation

> Verification pattern adapted from `quickbooks/specs/009-market-intelligence/source-appendix.md`.
>
> Snapshot window starts with the March 18, 2026 operating-data pull and will be refreshed only if validation slips past the agreed freshness window.

## Internal Data Sources

| ID | Source | Location | Used For | Tier | Verification | Notes |
|----|--------|----------|----------|------|--------------|-------|
| QBO-07 | QBO AR aging | `~/dev/quickbooks/data-package/07-qbo-ar-aging.json` | Collections triage and cash recovery | `internal-primary` | LOCAL — snapshot + checksum required | 12 customer rows |
| QBO-08 | QBO financial summary | `~/dev/quickbooks/data-package/08-qbo-financial-summary.json` | Cash/runway triage | `internal-primary` | LOCAL — snapshot + checksum required | 6-key summary dict |
| PD-01 | Open pipeline export | `~/dev/quickbooks/data-package/01-pipedrive-open-pipeline.json` | Near-term revenue and close timing | `internal-primary` | LOCAL — snapshot + checksum required | 267 open deals |
| PD-02 | Won-deal history | `~/dev/quickbooks/data-package/02-pipedrive-won-deals-2022-2026.json` | Historical buyer pattern analysis | `internal-primary` | LOCAL — snapshot + checksum required | 380 won deals |
| PD-03 | Client relationship profiles | `~/dev/quickbooks/data-package/03-client-relationship-profiles.json` | Reactivation and relationship depth | `internal-primary` | LOCAL — summary-only transform | 304 org-level profiles with nested contacts |
| PD-04 | Contacts with deal history | `~/dev/quickbooks/data-package/04-contacts-with-deal-history.json` | Relationship coverage analysis | `internal-primary` | LOCAL — summary-only transform | 286 contact rows; direct PII present |
| FC-05 | Forecast active projects | `~/dev/quickbooks/data-package/05-forecast-active-projects.json` | Delivery load and budget context | `internal-primary` | LOCAL — snapshot + checksum required | 37 active/opportunity projects |
| FC-06 | Forecast team capacity | `~/dev/quickbooks/data-package/06-forecast-team-capacity.json` | Capacity and staffing constraints | `internal-primary` | LOCAL — snapshot + checksum required | 44 team rows |
| PD-09 | Lost-deal analysis | `~/dev/quickbooks/data-package/09-lost-deals-analysis.json` | Failure-pattern analysis | `internal-primary` | LOCAL — snapshot + checksum required | 6-key summary dict |
| PD-10 | Open-deal notes | `~/dev/quickbooks/data-package/10-notes-on-open-deals.json` | Timing/risk signal extraction | `internal-primary` | LOCAL — sanitized signal extraction only | 11 note records with free text |
| PD-11 | Leads export | `~/dev/quickbooks/data-package/11-pipedrive-leads.json` | New-business timing signals | `internal-primary` | LOCAL — snapshot + checksum required | 9 active leads |
| SYN-12 | Market-intelligence synthesis | `~/dev/quickbooks/data-package/12-market-intelligence-synthesis.md` | Context only | `ai-mediated-context` | LOCAL — existing synthesis | Not primary evidence for leadership claims |
| CAP-13 | Groove Jones capabilities brief | `~/dev/quickbooks/data-package/13-groove-jones-capabilities.md` | Capability context | `internal-primary` | LOCAL — markdown source | Use to ground strategy/positioning claims |

## Existing Research Corpus (Spec 009)

| Prefix | Source Set | Location | Tier Default | Verification Status | Notes |
|--------|------------|----------|--------------|---------------------|-------|
| R-009 | Research folder | `~/dev/quickbooks/specs/009-market-intelligence/research/` | mixed | Needs per-file classification | 30 research files; many are AI-mediated or mixed-source |
| R-APP | Source appendix | `~/dev/quickbooks/specs/009-market-intelligence/source-appendix.md` | verification helper | COMMITTED | Reuse table pattern for current work |

## External Research Intake

| ID | Source | URL / Location | Used For | Tier | Verification | Notes |
|----|--------|----------------|----------|------|--------------|-------|
| EXT-001 | Pending | _to be filled during T6_ | Buyer timing / market proof | `external-primary` or `external-attributable-secondary` | NEEDS VERIFICATION | Add only named, attributable sources |

## Sensitivity Rules

- `PD-03`, `PD-04`, and `PD-10` are `crm-restricted` and must never be committed as raw dumps.
- Committed artifacts may keep org/account names, deal ids, values, dates, and role/category labels.
- Personal names, personal emails, phone numbers, and raw free-text notes are excluded from committed outputs.

## Freshness Notes

- `source-snapshots.json` is the mechanical source of truth for exact checksums and snapshot refs.
- If validation is retried outside the freshness window, refresh snapshots first and update this file before claiming validation-complete.
