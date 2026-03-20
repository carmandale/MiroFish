---
title: "Implementation Plan - Real Growth Research Foundation for Groove Jones"
date: 2026-03-20
bead: bd-7km
---

<!-- Codex Review: APPROVED after 3 rounds | model: gpt-5.4 | date: 2026-03-20 -->
<!-- Status: REVISED -->
<!-- Revisions: added immutable source snapshots and mandatory checksums; added explicit redaction boundary and corpus index; corrected chunk-survivability audit to use extracted text basis; split implementation-complete vs validation-complete -->

<!-- plan:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-20T15:42:28Z -->

# Implementation Plan: Real Growth Research Foundation for Groove Jones

> Planned 2026-03-20 by RedUnion with adversarial collaboration from YoungUnion and ZenQuartz.

## Overview

Build a bounded, spec-local research workspace that turns Groove Jones's raw internal operating data plus higher-quality external research into:

- mechanically transformed, provenance-bearing evidence documents
- clearly tiered external research documents
- a contradiction register and claim/evidence ledger
- a triage-first leadership package split into `30-90 day` and `6-24 month` horizons
- a curated MiroFish-ingestible corpus subset validated through the existing intake path

This plan deliberately avoids new MiroFish product work. The core implementation is a research-and-transformation workflow around existing inputs, not a new ingestion feature, ETL platform, or evidence graph product.

## Problem Statement

The current Strategy Lab work proved that MiroFish can preserve citations and generate comparative outputs, but it also showed that the evidence base was too narrow and too synthesized:

- the last live Strategy Lab corpus was only `3` files and `67` chunks
- MiroFish intake still only accepts `.pdf`, `.docx`, `.md`, `.markdown`, and `.txt`
- the richer Groove Jones operating truth lives in raw JSON-heavy QuickBooks, Pipedrive, and Forecast exports
- much of the existing `quickbooks/specs/009-market-intelligence/research` corpus is AI-mediated and cannot satisfy the new evidence-tier requirement by itself

The architectural gap is not UI or simulation behavior. It is the absence of a bounded, auditable way to move from raw operating evidence and primary external sources into a document corpus that leadership and MiroFish can both use honestly.

## Proposed Solution

1. Create a spec-local research workspace under `specs/004-real-growth-research/` as the canonical place for transformation tooling, evidence docs, research docs, contradiction tracking, and leadership deliverables.
2. Split transformation into two passes:
   - a mechanical pass that emits provenance-bearing markdown evidence docs from selected JSON inputs without relying on LLM summarization
   - a narrative pass that produces triage and strategy briefs, explicitly labeled as synthesis and linked back to the mechanical docs
3. Reuse the proven `quickbooks/specs/009-market-intelligence/source-appendix.md` verification-table pattern for source inventory and external research verification.
4. Keep the full research workspace larger than the ingest set, but enforce a curated MiroFish subset with an explicit file/chunk budget.
5. Validate the chosen subset by running it through the existing MiroFish intake path and confirming `corpus_manifest.json` plus `chunk_manifest.json` are produced without any code changes.

## Technical Approach

### Workspace Boundaries

Read-only sources:

- `~/dev/quickbooks/data-package/*`
- `~/dev/quickbooks/specs/009-market-intelligence/*`
- `~/dev/pipedrive/*` as needed for provenance or source confirmation
- `~/dev/forecast/*` as needed for provenance or source confirmation

Research outputs for this implementation live in the spec directory:

```text
specs/004-real-growth-research/
  source-inventory.md
  evidence-tier-rubric.md
  contradiction-register.md
  artifacts/
    transform/
    research/
    leadership/
    mirofish-corpus/
  tools/
```

The existing workflow artifacts (`plan.md`, `tasks.md`, `planning-transcript.md`) remain in the spec directory because `/plan` already created them, but they are not research deliverables produced by implementation. This is intentionally not a MiroFish backend feature branch. The transformation helper and its outputs are spec-local so the work stays bounded and auditable.

### Existing MiroFish Contracts To Reuse

Read-only validation targets:

- `backend/app/utils/file_parser.py`
- `backend/app/config.py`
- `backend/app/api/graph.py`
- `backend/app/services/strategy_lab_provenance.py`
- `backend/app/models/project.py`

These files already establish the non-negotiable v1 contract:

- document-style inputs only (`pdf`, `docx`, `md`, `markdown`, `txt`)
- project-scoped artifact storage under `backend/uploads/projects/<project>/strategy_lab/`
- provenance manifests via `corpus_manifest.json` and `chunk_manifest.json`

The plan treats those contracts as fixed. We adapt the evidence package to them rather than editing them.

### Two-Pass Transformation Contract

#### Pass 1: Mechanical Evidence Docs

Implement a bounded helper script under:

- `specs/004-real-growth-research/tools/build_research_bundle.py`

Outputs under:

- `specs/004-real-growth-research/artifacts/transform/*.md`

Pass 1 rules:

- no LLM summarization inside the transformer
- preserve reversible provenance from the source snapshot
- prefer direct tables for small/high-signal datasets
- use summary + appendix structure for large datasets
- make every transformed file independently inspectable
- emit a machine-readable snapshot manifest before any markdown transform is considered valid

Snapshot freeze contract:

- create `artifacts/transform/source-snapshots.json`
- for repo-backed sources, record the repo root plus the exact git commit SHA used for the source snapshot
- for exported files not safely pinned by git history, record the frozen artifact path actually read during the run
- record a mandatory SHA-256 checksum for every transformed input, with no `if practical` escape hatch
- record snapshot timestamp and record-count basis for each source
- treat this manifest as the canonical rerun/reversibility receipt for the whole workspace

Each transformed markdown file must contain both:

1. YAML frontmatter for tooling and auditability
2. an inline `## Provenance` block near the top of the markdown body so the metadata survives normal MiroFish chunking

Required provenance fields:

- `source_id`
- `source_path`
- `source_repo`
- `source_snapshot_ref`
- `snapshot_date`
- `record_count`
- `record_count_method`
- `transform_method`
- `selection_rule`
- `raw_sha256`
- `evidence_tier`
- `sensitivity_class`

Why inline provenance is required:

- current `chunk_manifest.json` rows do not carry source tier or original raw path
- current chunk-level fields are limited to things like `chunk_id`, `document_id`, `filename`, character offsets, locators, and `episode_uuid`
- frontmatter alone is too easy to lose at the chunk boundary

#### Pass 2: Narrative Deliverables

Outputs under:

- `specs/004-real-growth-research/artifacts/leadership/30-90-day-triage.md`
- `specs/004-real-growth-research/artifacts/leadership/6-24-month-strategy.md`

Optional synthesis docs under:

- `specs/004-real-growth-research/artifacts/research/*.md`

Pass 2 rules:

- clearly labeled as synthesis
- never treated as primary evidence
- every major claim links back to one or more Pass 1 evidence docs or verified external research docs
- triage deliverable ships before long-horizon strategy writing is considered complete

### Internal Evidence Selection Strategy

The workspace may transform more files than the first MiroFish bundle ingests, but even the workspace should be intentionally prioritized.

#### Tier A: Immediate triage transforms

Transform first:

- `08-qbo-financial-summary.json`
- `07-qbo-ar-aging.json`
- `01-pipedrive-open-pipeline.json`
- `05-forecast-active-projects.json`
- `06-forecast-team-capacity.json`
- `09-lost-deals-analysis.json`
- `10-notes-on-open-deals.json`

These answer the urgent questions around cash, collections, closeable work, delivery load, and failure modes.

#### Tier B: Secondary internal transforms

Transform next:

- `02-pipedrive-won-deals-2022-2026.json`
- `11-pipedrive-leads.json`

Potentially conditional:

- `03-client-relationship-profiles.json`
- `04-contacts-with-deal-history.json`

`03` and `04` are the largest and most PII-sensitive. The default should be summary transforms rather than raw-contact dumps, with explicit redaction rules.

### External Research Intake Strategy

The spec's quality bar only works if acquisition is concrete.

V1 external research approach:

- manual-first, bounded source intake
- agent assistance allowed for finding sources, but not for counting AI-mediated summaries as proof
- every external research doc must include named source references and verification status
- reuse the `source-appendix.md` verification-table pattern from spec 009

External research outputs live under:

- `specs/004-real-growth-research/artifacts/research/`

Priority research themes:

- immediate cash and buyer timing signals
- maintenance/support and recurring-revenue analogs
- healthcare/pharma training and buyer evidence
- defense/government procurement and adjacent timing signals
- competitor and category evidence strong enough to challenge existing assumptions

AI-mediated 009 files are allowed only as `context` or `ai-mediated` tier unless they are independently backed by named primary or attributable secondary sources in the new inventory.

### Sensitive Data Contract

The implementation must define the redaction boundary up front instead of deciding ad hoc while transforming files.

Allowlist for committed research outputs:

- company name
- account or opportunity identifier
- stage, service category, lane, and status fields
- aggregate financial values, aging buckets, revenue ranges, margin ranges, utilization/capacity summaries, and forecast ranges
- date ranges and quarter/month markers
- sanitized free-text excerpts only when they are needed to explain a sales or delivery risk and have been stripped of direct personal identifiers

Denylist for committed research outputs:

- personal emails
- personal phone numbers
- direct contact names unless they are already public executives and materially required for an external-source citation
- street addresses
- invoice-level identifiers that expose customer-specific billing details
- notes fields copied verbatim when they include personal context, staffing commentary, or negotiation details not needed for the claim
- raw contact exports or raw CRM history dumps

Artifact boundary:

- committed spec artifacts must be leadership-safe and conform to the allowlist above
- any analyst-only scratch files needed during transformation stay outside the repo in a local-only working directory and are not part of the deliverable set
- the transformer must prefer summarized markdown outputs over duplicated raw JSON content for all sensitive source sets
- `source-inventory.md` must record when a source was summarized-only, excluded, or transformed under redaction constraints

### Evidence Tier Contract

Define the rubric explicitly in:

- `specs/004-real-growth-research/evidence-tier-rubric.md`

Minimum tiers:

- `internal-primary`
- `external-primary`
- `external-attributable-secondary`
- `ai-mediated-context`
- `inference`

Rules:

- leadership recommendations cannot rest solely on `ai-mediated-context`
- contradiction register entries must show when a claim is backed only by `context` or `inference`
- MiroFish ingest bundle may include context-tier docs, but the source inventory and leadership briefs must label them honestly

### Source Inventory and Contradiction Ledger

Create:

- `specs/004-real-growth-research/source-inventory.md`
- `specs/004-real-growth-research/contradiction-register.md`
- `specs/004-real-growth-research/artifacts/mirofish-corpus/corpus-index.md`

`source-inventory.md` should follow the proven source-appendix pattern:

- source id
- source path or URL
- type
- evidence tier
- what it is used for
- verification status
- freshness notes

`contradiction-register.md` should track:

- claim
- supporting evidence
- contradicting evidence
- missing evidence
- current confidence
- implication for `30-90 day` vs `6-24 month` decisions

`artifacts/mirofish-corpus/corpus-index.md` should track, for every file selected into the first MiroFish bundle:

- filename
- source ids included
- evidence tier
- horizon relevance (`30-90 day`, `6-24 month`, or both)
- selection rationale
- estimated chunk count before upload
- actual chunk count after upload
- whether the required inline provenance tokens survived chunk reconstruction checks

### MiroFish Ingest Subset and Budget

The full research workspace is not the same thing as the first MiroFish ingest bundle.

Curated ingest bundle:

- assembled under `specs/004-real-growth-research/artifacts/mirofish-corpus/`
- copied from selected transform, research, and leadership docs
- initially targeted at roughly `12-15` files and `<=250` chunks for v1, but finalized by the smallest set that covers the triage and strategy claims cleanly

Budget rule:

- treat `<=250` chunks as the first validation ceiling, not a magic product limit
- estimate bundle size before upload, then confirm the actual chunk count from `chunk_manifest.json`
- if the curated bundle exceeds the ceiling, split it into multiple explicit corpus bundles rather than silently widening scope

Selection goals:

- strong triage signal first
- enough external evidence to challenge internal assumptions
- enough breadth to support future strategy work without blowing context budget

### Validation Path

Validation uses the existing MiroFish product path, not new code:

1. assemble the curated corpus subset in `artifacts/mirofish-corpus/`
2. create or reuse a research-validation project in MiroFish
3. upload the curated subset through the normal intake path
4. confirm `corpus_manifest.json` and `chunk_manifest.json` are produced
5. reconstruct sampled chunk text from the same normalized extracted-text basis that MiroFish actually chunks (`ExtractedDocument.text`, or a re-run of `FileParser.extract_document(...).text`), then apply `chunk_manifest.json` start/end offsets and prove that every selected file still exposes `source_id`, `source_path`, `record_count`, and `evidence_tier` inside retrievable chunk text
6. reconcile those results into `artifacts/mirofish-corpus/corpus-index.md`
7. record the validation result in the spec artifacts, including blocked-service notes if MiroFish dependencies are unavailable on the validation day

The validation goal is not to run a full strategy-lab project. The goal is to prove the chosen bundle is ingestible and provenance-bearing enough for future use.

## Implementation Phases

### Phase 0: Freeze Inputs and Artifact Contracts

- confirm exact source files, snapshot dates, and record counts
- create the spec-local workspace directories
- define the provenance schema and evidence-tier rubric
- create the source-inventory template and contradiction-register template
- freeze `source-snapshots.json` with commit SHAs or frozen source paths plus mandatory checksums before any transform work begins

### Phase 1: Build Triaged Internal Evidence Docs

- implement the mechanical transformer
- produce the highest-urgency internal docs first
- add inline provenance blocks and frontmatter to each output
- verify the generated docs are readable, auditable, and redacted appropriately
- add a mechanical validation mode that checks required provenance fields, checksum presence, and redaction-policy compliance on every generated markdown file

### Phase 2: Expand Internal Coverage and Curate Existing Research

- add secondary internal transforms
- classify 009 research docs by evidence tier
- carry forward only the useful subset, labeled honestly

### Phase 3: Acquire New External Sources

- collect a bounded set of named primary or attributable secondary sources
- create verified research docs and inventory entries
- add freshness notes and verification status

### Phase 4: Build the Decision Layer

- complete `contradiction-register.md`
- write `30-90 day` triage brief first
- write `6-24 month` strategy brief second
- ensure every major recommendation points back to evidence-tiered sources

### Phase 5: Assemble and Validate the MiroFish Corpus

- select the bounded ingest subset
- copy it into `artifacts/mirofish-corpus/`
- run the ingest smoke test through MiroFish
- audit provenance survivability for every file when a bundle has 12 or fewer files; for larger split bundles, audit at least the first chunk and one later chunk from every file, plus any file whose provenance block spans multiple chunks
- record manifest counts, chunk counts, and any ingestion problems

## Risks and Mitigations

### PII leakage from CRM/contact-heavy files

Mitigation:

- default to summary transforms rather than raw contact dumps
- enforce an explicit allowlist/denylist before transform work starts
- redact unnecessary personal contact details from leadership-facing artifacts
- keep raw-source references in provenance, not in duplicated body dumps
- keep analyst-only scratch material outside the repo and out of the committed artifact set

### Corpus bloat overwhelms MiroFish

Mitigation:

- explicit ingest budget
- workspace-superset / ingest-subset split
- validate estimated chunk count before upload and actual chunk count after upload
- split bundles if the first-pass ceiling is exceeded

### AI-mediated research contaminates evidence quality

Mitigation:

- explicit evidence-tier rubric
- reuse source-verification tables
- forbid AI-only claims from standing as proof in leadership recommendations

### Research goes stale too quickly

Mitigation:

- every source inventory row and transformed doc carries snapshot/freshness metadata
- triage brief is delivered first
- validation notes must state the snapshot window used

### Validation services are unavailable on ingest day

Mitigation:

- treat the corpus bundle, corpus index, and source snapshot manifest as the primary ready-state artifacts
- record blocked validation status explicitly instead of inventing a clean ingest result
- rerun only the bounded ingest-validation phase once MiroFish dependencies are available again
- if source snapshots have aged beyond the freshness window by the retry date, refresh `source-snapshots.json`, update freshness notes, and rerun affected transforms before claiming validation-complete

### Scope creep into ETL or product work

Mitigation:

- all helper code lives under the spec directory
- no changes to `backend/app/*` for v1
- any desire for ongoing automation beyond this bounded workflow becomes a separate spec/bead

## Done Criteria

### Implementation-Complete

Implementation is complete when the workspace can produce:

- a spec-local source inventory and evidence-tier rubric
- a `source-snapshots.json` receipt with mandatory checksums and immutable source references
- provenance-bearing internal evidence docs from selected JSON sources
- a verified external research set with named sources and status
- a contradiction register
- two leadership deliverables split by horizon
- a curated MiroFish corpus subset plus `artifacts/mirofish-corpus/corpus-index.md`

### Validation-Complete

Validation is complete when the implementation-complete artifacts also have:

- a successful ingest smoke test through the existing MiroFish path
- a chunk-reconstruction audit, based on normalized extracted text plus manifest offsets, that proves provenance tokens survive for the selected files

If MiroFish dependencies are unavailable on the validation day, the plan allows an honest temporary terminal state of `implementation-complete / validation-blocked`, with the blocked reason recorded in the spec artifacts and the bounded validation phase left as the only remaining step.

## Requirement Traceability

| Requirement | Planned mechanism |
|-------------|-------------------|
| R0 | Triage-first sequencing plus `30-90 day` leadership brief tied to cash/AR/pipeline/capacity evidence |
| R1 | Read-only raw source set remains canonical; mechanical transforms preserve direct provenance back to source files and frozen snapshot references |
| R2 | Frontmatter + inline provenance blocks + source inventory + `source-snapshots.json` + mandatory checksums + post-chunk survivability validation |
| R3 | Evidence-tier rubric + verified external-source intake + AI-mediated docs labeled as context only |
| R4 | Separate leadership deliverables and contradiction analysis by time horizon |
| R5 | Dedicated contradiction register and explicit confidence/unknown tracking |
| R6 | Leadership-facing markdown briefs linked back to mechanical evidence docs and verified source inventory |
| R7 | Curated `artifacts/mirofish-corpus/` bundle plus `corpus-index.md` validated through existing MiroFish intake with no code changes |
| R8 | Spec-local tooling only; no permanent warehouse, no new MiroFish ingest code, no evidence-graph platform work |

# Relevant Source Code Context

## backend/app/utils/file_parser.py

```python
class FileParser:
    """文件解析器"""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.md', '.markdown', '.txt'}
```

```python
        if suffix == '.pdf':
            text, segments = cls._extract_pdf_document(file_path)
        elif suffix == '.docx':
            text, segments = cls._extract_docx_document(file_path)
        elif suffix in {'.md', '.markdown'}:
            text, segments = cls._extract_text_document(
                file_path,
                extension=suffix,
            )
        elif suffix == '.txt':
            text, segments = cls._extract_text_document(
                file_path,
                extension=suffix,
            )
```

## backend/app/api/graph.py

```python
                document = FileParser.extract_document(
                    file_info["path"],
                    original_filename=file_info["original_filename"],
                    saved_filename=file_info["saved_filename"],
                )
                extracted_documents.append(document)
                document_texts.append(document.text)
                all_text += f"\n\n=== {file_info['original_filename']} ===\n{document.text}"
...
        ProjectManager.save_extracted_documents(project.project_id, extracted_documents)
        if workflow_mode == WorkflowMode.STRATEGY_LAB:
            corpus_manifest = StrategyLabProvenanceService.build_corpus_manifest(
                extracted_documents
            )
            ProjectManager.save_strategy_lab_artifact(
                project.project_id,
                'corpus_manifest.json',
                [entry.to_dict() for entry in corpus_manifest],
            )
```

## backend/app/services/strategy_lab_provenance.py

```python
    def build_corpus_manifest(
        documents: List[ExtractedDocument],
    ) -> List[DocumentManifestEntry]:
        return [
            DocumentManifestEntry(
                document_id=document.document_id,
                filename=document.original_filename,
                saved_filename=document.saved_filename,
                extension=document.extension,
                source_label=document.source_label,
                text_length=len(document.text),
                segment_count=len(document.segments),
            )
            for document in documents
        ]
```

```python
    def build_chunk_manifest(
        cls,
        documents: List[ExtractedDocument],
        chunk_size: int,
        overlap: int,
    ) -> List[ChunkManifestEntry]:
...
                entries.append(
                    ChunkManifestEntry(
                        chunk_id=f"{document.document_id}-chunk-{index:04d}",
                        document_id=document.document_id,
                        filename=document.original_filename,
                        text=chunk_text,
                        start_char=start_char,
                        end_char=end_char,
                        locator_start=locator_start,
                        locator_end=locator_end,
                    )
                )
```

## backend/app/models/project.py

```python
    def get_strategy_lab_artifact_path(cls, project_id: str, filename: str) -> str:
        """获取 Strategy Lab 工件路径"""
        strategy_lab_dir = cls.ensure_strategy_lab_dirs(project_id)
        return os.path.join(strategy_lab_dir, filename)

    @classmethod
    def save_strategy_lab_artifact(cls, project_id: str, filename: str, data: Any) -> None:
        """保存 Strategy Lab 工件"""
        artifact_path = cls.get_strategy_lab_artifact_path(project_id, filename)
        cls._atomic_write_json(artifact_path, data)
```

## quickbooks/specs/009-market-intelligence/source-appendix.md

```markdown
## Internal Data Sources

| # | Source | Location | Used In | Status |
|---|--------|----------|---------|--------|
| I1 | Pipedrive deals export | `specs/008-sales-diagnostic/deals.json` | B2.1 (R3), B1.1 (R1) | LOCAL — frozen 2026-03-17, 3,275 deals |
...
## Verification Summary

| Category | Verified | Not URL-Verified | Total |
|----------|----------|-----------------|-------|
| Internal | 5 (all local/committed) | 0 | 5 |
| External — Win-Back | 3 | 0 | 3 |
| External — Vertical | 2 | 0 | 2 |
| External — Competitive/Cases | 3 | 2 | 5 |
| **Total** | **13** | **2** | **15** |
```
