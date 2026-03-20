# Corpus Index — Real Growth Research Foundation

| Filename | Source IDs | Tier | Horizon | Selection Rationale | Est. Chunks | Actual Chunks | Provenance Audit |
|----------|------------|------|---------|---------------------|-------------|---------------|------------------|
| `qbo_07.md` | `QBO-07` | `internal-primary` | `30-90 day` | AR concentration and collections proof | `4` | `4` | `PASS` |
| `qbo_08.md` | `QBO-08` | `internal-primary` | `30-90 day` | Cash, burn, runway, and margin reality | `7` | `7` | `PASS` |
| `pd_01.md` | `PD-01` | `internal-primary` | `30-90 day` | Pipeline stage/value mix and named late-stage opportunities | `4` | `4` | `PASS` |
| `pd_03.md` | `PD-03` | `internal-primary` | `both` | Existing-account relationship depth without raw contact leakage | `6` | `6` | `PASS` |
| `pd_04.md` | `PD-04` | `internal-primary` | `both` | Contact coverage and open-value rollups by organization | `7` | `7` | `PASS` |
| `pd_09.md` | `PD-09` | `internal-primary` | `30-90 day` | Lost-deal pattern and internal-cancellation signal | `5` | `5` | `PASS` |
| `pd_10.md` | `PD-10` | `internal-primary` | `30-90 day` | Sanitized note signals for live opportunity context | `7` | `7` | `PASS` |
| `ext-001-enterprise-training-signals.md` | `EXT-001..EXT-003` | `external-primary` | `both` | Verified training ROI and enterprise learning-demand signals | `12` | `12` | `PASS` |
| `ext-002-healthcare-medtech-signals.md` | `EXT-004..EXT-006` | `external-primary` | `6-24 month` | Verified healthcare and medtech deployment proof | `11` | `11` | `PASS` |
| `ext-003-defense-training-signals.md` | `EXT-007..EXT-009` | `external-primary` | `both` | Verified defense training-demand and entry-path proof | `12` | `12` | `PASS` |
| `30-90-day-triage.md` | `QBO-07,QBO-08,PD-01,PD-03,PD-04,PD-09,CAP-13` | `inference` | `30-90 day` | Leadership-readable synthesis for immediate operating action | `19` | `20` | `PASS` |
| `6-24-month-strategy.md` | `FC-05,PD-03,PD-04,PD-09,EXT-001..EXT-009,CAP-13` | `inference` | `6-24 month` | Leadership-readable strategy synthesis with explicit evidence-strength labeling | `19` | `20` | `PASS` |

## Notes

- Upload bundle excludes `corpus-index.md`; it is tracking metadata only, not part of the curated ingest subset.
- Live validation project: `proj_fb0d88a82d92`.
- `corpus_manifest.json` contains `12` entries and `chunk_manifest.json` contains `115` entries for the curated bundle.
- `Provenance Audit` reflects chunk reconstruction on the same extracted-text basis MiroFish uses via `FileParser.extract_document(...)` and `StrategyLabProvenanceService.build_chunk_manifest(..., chunk_size=500, overlap=50)`.
- Validation status: `implementation-complete / validation-blocked` beyond ingest. Ontology generation and manifest creation succeeded; downstream graph build failed on external Zep limit `429 Rate limit exceeded for FREE plan`.
