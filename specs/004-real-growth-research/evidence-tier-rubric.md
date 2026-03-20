# Evidence Tier Rubric — Real Growth Research Foundation

## Tier Definitions

| Tier | Meaning | Allowed Uses | Not Allowed |
|------|---------|--------------|-------------|
| `internal-primary` | Direct Groove Jones operating evidence from frozen local exports or committed first-party docs | Cash, pipeline, capacity, relationship, and delivery claims | Cannot be treated as externally validating market demand |
| `external-primary` | Named first-party external materials (filings, procurement notices, buyer announcements, investor materials, public earnings documents) | Highest-confidence market and buyer claims | None, as long as attribution and freshness are explicit |
| `external-attributable-secondary` | Named third-party reporting with attributable publisher and date | Supporting claims, triangulation, competitor/category context | Cannot override stronger conflicting primary evidence without explanation |
| `ai-mediated-context` | AI-produced syntheses, briefs, or mixed-source summaries that are not independently verified line-by-line | Orientation, question generation, candidate leads for deeper checking | Cannot stand alone as proof in leadership recommendations |
| `inference` | Reasoned conclusion drawn from multiple evidence points | Scenario framing, contradiction analysis, recommendation synthesis | Must never be presented as observed fact |

## Leadership Rules

- No recommendation in `30-90 day` or `6-24 month` deliverables may rely solely on `ai-mediated-context`.
- Every major recommendation must cite at least one `internal-primary`, `external-primary`, or `external-attributable-secondary` source.
- Contradiction entries must explicitly flag when a claim is supported only by `ai-mediated-context` or `inference`.

## Sensitive Internal Data Rules

- `internal-primary` does not mean raw-data dump. Sensitive internal evidence must still pass the committed-artifact allowlist.
- Summary-only transforms are acceptable for `crm-restricted` sources if the transform preserves provenance and record counts.

## Verification Status Labels

Use these statuses in `source-inventory.md`:

- `LOCAL — snapshot + checksum required`
- `COMMITTED`
- `VERIFIED (named source checked)`
- `PARTIALLY VERIFIED`
- `NEEDS VERIFICATION`

## Escalation

If a source cannot be placed confidently in one tier, default down, not up:

- unknown authorship -> `ai-mediated-context`
- unattributed aggregator summary -> `ai-mediated-context`
- mixed-source memo with some cited facts -> split the cited facts out and leave the memo as `ai-mediated-context`
