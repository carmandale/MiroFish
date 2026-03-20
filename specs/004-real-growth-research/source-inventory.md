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

| ID | Source | Location | Used For | Tier | Verification | Notes |
|----|--------|----------|----------|------|--------------|-------|
| R-009 | Spec-009 research corpus | `~/dev/quickbooks/specs/009-market-intelligence/research/` | Lead generation only | mixed | REVIEWED — see `artifacts/research/009-corpus-tiering.md` | 30 files total; 26 markdown files classified |
| R-009-Q1 | Active spenders research | `~/dev/quickbooks/specs/009-market-intelligence/research/q1_active_xr_spenders.md` | Buyer-target seeding | `external-attributable-secondary` | COMMITTED — carry forward with attribution | Good carry-forward file for named spender examples |
| R-009-Q2 | Competitor landscape research | `~/dev/quickbooks/specs/009-market-intelligence/research/q2_competing_agencies.md` | Competitive baseline | `external-attributable-secondary` | COMMITTED — carry forward with attribution | Use as market map, not final proof |
| R-009-Q4 | Scaling examples research | `~/dev/quickbooks/specs/009-market-intelligence/research/q4_scaling_examples.md` | Long-horizon strategic comparisons | `external-attributable-secondary` | COMMITTED — carry forward with attribution | Useful for platform-vs-services cases |
| R-009-Q5 | Cancellation research | `~/dev/quickbooks/specs/009-market-intelligence/research/q5_cancellation_research.md` | Contradiction and risk analysis | `mixed-needs-review` | COMMITTED — use with spot-checking | Strongest because it explicitly states evidence limits |
| R-009-BRIEF | Market intelligence brief 01 | `~/dev/quickbooks/specs/009-market-intelligence/research/Groove Jones Market Intelligence Brief 01.md` | Lead bundle for cross-checking | `mixed-needs-review` | COMMITTED — spot-check before reuse | Valuable synthesis, not standalone proof |
| R-APP | Source appendix | `~/dev/quickbooks/specs/009-market-intelligence/source-appendix.md` | verification helper | `external-attributable-secondary` | COMMITTED | Reused table pattern for current work |

## External Research Intake

| ID | Source | URL / Location | Used For | Tier | Verification | Notes |
|----|--------|----------------|----------|------|--------------|-------|
| EXT-001 | PwC VR soft-skills training study | `artifacts/research/ext-001-enterprise-training-signals.md` | Training ROI and speed proof | `external-primary` | VERIFIED (named source checked) | Official PwC study page |
| EXT-002 | Accenture Nth Floor enterprise VR use | `artifacts/research/ext-001-enterprise-training-signals.md` | Large-enterprise onboarding and learning signal | `external-primary` | VERIFIED (named source checked) | Official Accenture page |
| EXT-003 | Accenture investment in Praxis Labs | `artifacts/research/ext-001-enterprise-training-signals.md` | Enterprise services investment signal for immersive learning | `external-primary` | VERIFIED (named source checked) | Strategic demand signal, not buyer deployment |
| EXT-004 | GE HealthCare + MediView OmnifyXR installation | `artifacts/research/ext-002-healthcare-medtech-signals.md` | Healthcare/medtech deployment proof | `external-primary` | VERIFIED (named source checked) | Live clinical deployment |
| EXT-005 | Stryker + IRCAD NA training center agreement | `artifacts/research/ext-002-healthcare-medtech-signals.md` | Training-center and medtech education investment signal | `external-primary` | VERIFIED (named source checked) | Multi-year agreement |
| EXT-006 | Stryker Blueprint MR first surgeries | `artifacts/research/ext-002-healthcare-medtech-signals.md` | Mixed-reality procedural-use proof | `external-primary` | VERIFIED (named source checked) | Clinical workflow evidence |
| EXT-007 | Army PD SAI VAST classroom deployment | `artifacts/research/ext-003-defense-training-signals.md` | Defense immersive-training deployment proof | `external-primary` | VERIFIED (named source checked) | Operational Army deployment |
| EXT-008 | Army SBIR JETT XR training award | `artifacts/research/ext-003-defense-training-signals.md` | Small-business-accessible defense entry proof | `external-primary` | VERIFIED (named source checked) | Official SBIR award record |
| EXT-009 | Army Synthetic Training Environment operational use | `artifacts/research/ext-003-defense-training-signals.md` | Broader modernization context | `external-primary` | VERIFIED (named source checked) | Official Army article |

## Sensitivity Rules

- `PD-03`, `PD-04`, and `PD-10` are `crm-restricted` and must never be committed as raw dumps.
- Committed artifacts may keep org/account names, deal ids, values, dates, and role/category labels.
- Personal names, personal emails, phone numbers, and raw free-text notes are excluded from committed outputs.

## Freshness Notes

- `source-snapshots.json` is the mechanical source of truth for exact checksums and snapshot refs.
- If validation is retried outside the freshness window, refresh snapshots first and update this file before claiming validation-complete.
