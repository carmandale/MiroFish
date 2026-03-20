---
title: "Tasks - Real Growth Research Foundation for Groove Jones"
date: 2026-03-20
bead: bd-7km
---

<!-- Codex Review: APPROVED after 3 rounds | model: gpt-5.4 | date: 2026-03-20 -->
<!-- Status: RECONCILED -->
<!-- Revisions: reconciled tasks to require source snapshot receipts, explicit redaction rules, corpus index creation, extracted-text chunk audits, and split implementation vs validation completion states -->

<!-- plan:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-20T15:42:28Z -->

# Tasks: Real Growth Research Foundation for Groove Jones

## Prerequisites

- [x] **T0: Freeze the source set and scaffold the spec-local workspace**
  - Confirm the exact input files from `quickbooks/data-package/` and `quickbooks/specs/009-market-intelligence/`.
  - Freeze `artifacts/transform/source-snapshots.json` with snapshot dates, record counts, freshness caveats, and immutable source refs (repo commit SHA or frozen source path) plus mandatory SHA-256 checksums.
  - Create the working directories under `specs/004-real-growth-research/`:
    - `tools/`
    - `artifacts/transform/`
    - `artifacts/research/`
    - `artifacts/leadership/`
    - `artifacts/mirofish-corpus/`
  - **Verify:** source inventory seed list and `source-snapshots.json` exist, and no source-repo files were modified.

- [x] **T1: Define the provenance and evidence-tier contracts**
  - Create `source-inventory.md`.
  - Create `evidence-tier-rubric.md`.
  - Define the transformed-doc schema with frontmatter plus an inline `## Provenance` block, including `source_snapshot_ref`, `record_count_method`, and `sensitivity_class`.
  - Define the committed-artifact allowlist/denylist and the local-only analyst scratch boundary before any CRM/contact transforms.
  - Reuse the `source-appendix.md` verification-table pattern for external-source status.
  - Seed `artifacts/mirofish-corpus/corpus-index.md` with its required tracking columns.
  - **Verify:** one sample transformed doc can be traced back to source path, snapshot date, record count, transform method, and snapshot receipt entry.

## Internal Evidence Layer

- [x] **T2: Build mechanical transforms for the highest-urgency financial and collection signals**
  - Transform:
    - `08-qbo-financial-summary.json`
    - `07-qbo-ar-aging.json`
    - `09-lost-deals-analysis.json`
  - Emit provenance-bearing markdown docs under `artifacts/transform/`.
  - Run the mechanical validation mode to confirm required provenance fields, checksum presence, and redaction-policy compliance.
  - **Verify:** transformed docs preserve counts and remain readable without raw JSON access.
  - **Depends on:** T0, T1

- [x] **T3: Build mechanical transforms for near-term revenue and delivery signals**
  - Transform summary views for:
    - `01-pipedrive-open-pipeline.json`
    - `05-forecast-active-projects.json`
    - `06-forecast-team-capacity.json`
    - `10-notes-on-open-deals.json`
    - `11-pipedrive-leads.json`
  - Keep contact-heavy or verbose sections summarized rather than dumped raw.
  - **Verify:** each output includes provenance, the selection rule used to summarize large inputs, and passes the redaction allowlist/denylist checks.
  - **Depends on:** T2

- [x] **T4: Decide and implement the secondary CRM history transforms**
  - Evaluate whether to transform:
    - `02-pipedrive-won-deals-2022-2026.json`
    - `03-client-relationship-profiles.json`
    - `04-contacts-with-deal-history.json`
  - Default to PII-safe summaries instead of full exports.
  - **Verify:** the source inventory records which files were transformed, summarized only, intentionally excluded, or kept local-only because of sensitivity.
  - **Depends on:** T3

## Research Quality Layer

- [ ] **T5: Tier and curate the existing 009 research corpus**
  - Inventory the `009-market-intelligence/research` files.
  - Classify each file into the evidence-tier rubric.
  - Carry forward only the subset useful for v1, labeled honestly.
  - **Verify:** AI-mediated files are never mislabeled as primary or attributable secondary evidence.
  - **Depends on:** T1

- [ ] **T6: Add bounded, named external research beyond the current 009 bundle**
  - Acquire a bounded set of primary or attributable secondary sources for the highest-priority triage and strategy questions.
  - Create external research docs under `artifacts/research/`.
  - Add verification rows to `source-inventory.md`.
  - **Verify:** every new external document has named sources, URLs or source locations, and verification status.
  - **Depends on:** T5

## Decision Layer

- [ ] **T7: Build the contradiction register and claim/evidence ledger**
  - Create `contradiction-register.md`.
  - Map key strategic claims to supporting, contradicting, and missing evidence.
  - Flag freshness limits and confidence level.
  - **Verify:** each contradiction entry references specific internal or external evidence docs by path/id.
  - **Depends on:** T2, T3, T4, T6

- [ ] **T8: Draft the 30-90 day triage brief first**
  - Create `artifacts/leadership/30-90-day-triage.md`.
  - Focus on cash, AR, pipeline, capacity, and immediate moves.
  - **Verify:** every recommendation links back to evidence docs and does not rely solely on AI-mediated context.
  - **Depends on:** T2, T3, T7

- [ ] **T9: Draft the 6-24 month strategy brief second**
  - Create `artifacts/leadership/6-24-month-strategy.md`.
  - Focus on durable lanes, strategic constraints, and evidence-weighted opportunities.
  - **Verify:** the brief clearly distinguishes stronger evidence from directional inference.
  - **Depends on:** T4, T6, T7, T8

## MiroFish Validation Layer

- [ ] **T10: Assemble the bounded MiroFish ingest subset**
  - Select a curated subset from `artifacts/transform/`, `artifacts/research/`, and `artifacts/leadership/`.
  - Copy it into `artifacts/mirofish-corpus/`.
  - Keep the first validation pass near `12-15` files and `<=250` chunks, but shrink or split bundles if the estimate exceeds the ceiling.
  - Fill in `artifacts/mirofish-corpus/corpus-index.md` with source ids, evidence tier, horizon relevance, and selection rationale before upload.
  - **Verify:** selected files and estimated corpus size are recorded before upload.
  - **Depends on:** T5, T6, T8, T9

- [ ] **T11: Run the ingest smoke validation through the existing MiroFish path**
  - Upload the curated subset through the normal intake flow.
  - Confirm `corpus_manifest.json` and `chunk_manifest.json` are generated cleanly.
  - Reconstruct provenance-survivability samples from the normalized extracted text basis that MiroFish chunks (`ExtractedDocument.text` / `FileParser.extract_document(...).text`) and apply `chunk_manifest.json` offsets there.
  - Audit every file when the bundle has 12 or fewer files; for larger split bundles, audit at least the first chunk and one later chunk from every file, plus any file whose provenance block spans multiple chunks.
  - Record the resulting counts, audit results, and any ingestion issues in `corpus-index.md`.
  - **Verify:** validation output proves the bundle is ingestible without any new MiroFish code and that provenance tokens survive in retrievable chunk text.
  - **Depends on:** T10

## Final QA

- [ ] **T12: Finalize freshness, redaction, and packaging**
  - Review the workspace for unnecessary PII or raw sensitive detail.
  - Confirm freshness notes are present in the source inventory and leadership docs.
  - Ensure the final package separates:
    - raw/mechanical evidence
    - verified external research
    - synthesis/leadership documents
  - If validation was blocked, record the state as `implementation-complete / validation-blocked` and leave the bounded validation rerun as the only remaining step.
  - If validation is retried after the freshness window, refresh `source-snapshots.json`, update freshness notes, and rerun affected transforms before calling the work validation-complete.
  - **Verify:** the workspace is leadership-readable, evidence-traceable, and honest about unknowns.
  - **Depends on:** T11

## Dependency Graph

```text
T0 -> T1
T1 -> T2 -> T3 -> T4
T1 -> T5 -> T6
T2 + T3 + T4 + T6 -> T7
T2 + T3 + T7 -> T8
T4 + T6 + T7 + T8 -> T9
T5 + T6 + T8 + T9 -> T10 -> T11 -> T12
```
