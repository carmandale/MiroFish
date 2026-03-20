---
title: "Real Growth Research Foundation for Groove Jones"
date: 2026-03-19
bead: bd-7km
shaped: true
---

<!-- Codex Review: APPROVED after 3 rounds | model: gpt-5.4 | date: 2026-03-20 -->
<!-- Status: UNCHANGED -->
<!-- Revisions: none -->

<!-- issue:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-19T21:50:12Z -->

# Spec 004 — Real Growth Research Foundation

## Problem

The current MiroFish Strategy Lab work proved that the product can preserve citations and produce structured comparative outputs, but it also exposed a deeper input problem: the analysis was driven mostly by already-synthesized Groove Jones research documents rather than a genuinely broad evidence base.

For the live Strategy Lab run, the corpus was only three files:

- `Groove_Jones_Consolidated_Market_Intelligence_2026.docx`
- `Groove_Jones_30Day_Revenue_Action_Plan.docx`
- `research.md`

That corpus produced 67 chunked research segments, of which 41 came from the consolidated market-intelligence doc, 21 came from the 30-day action plan, and only 5 came from `research.md`. The resulting comparative report cited those same documents heavily, plus MiroFish-generated lane templates and interview artifacts. This means the system was mostly reorganizing existing strategic thinking rather than discovering new truth from raw finance, sales, production, and primary external research.

At the same time, Groove Jones already has materially richer internal evidence available across:

- `~/dev/quickbooks`
- `~/dev/pipedrive`
- `~/dev/forecast`

Those repos already contain usable operating data and packaged extracts, including:

- cash position, AR aging, and financial summaries from QuickBooks
- won deals, open pipeline, lost-deal analysis, contacts, and relationship profiles from Pipedrive
- active projects and team capacity from Forecast
- prior market-intelligence research in `quickbooks/specs/009-market-intelligence`

The real missing work is to build a stronger research foundation that combines raw internal operating data with higher-quality external research, preserves provenance, separates raw evidence from synthesis, and produces a decision-grade evidence bundle for leadership and for future MiroFish runs.

## Why This Is Distinct Work

This is not the same as:

- `specs/002-groove-jones-strategy-lab/`, which shaped how MiroFish should compare strategic lanes
- `specs/003-strategic-path-simulation/`, which scoped narrative-resonance simulations
- `quickbooks/specs/009-market-intelligence/`, which asked where the market is growing

Those efforts answer strategy and modeling questions. This work answers a prior question:

**What evidence base should exist before Groove Jones trusts strategic recommendations or simulation outputs?**

## Goal

Produce a real, decision-grade research foundation for Groove Jones that:

1. uses raw internal operating evidence from QuickBooks, Pipedrive, and Forecast,
2. incorporates stronger, fresher, named external research sources,
3. preserves source lineage from raw evidence through synthesis,
4. makes contradictions and unknowns explicit, and
5. leaves behind a research bundle that MiroFish can ingest without collapsing everything into one summary document.

## Selected Shape

**Selected Shape: D — Timeboxed Hybrid Bundle**

Shaping selected a hybrid approach rather than a pure dossier, pure transformation pipeline, or evidence graph. The chosen shape combines:

- a bounded, provenance-preserving transformation layer,
- a human-readable leadership package split between immediate triage and longer-horizon strategy,
- a contradiction register,
- and a MiroFish-ingestible markdown corpus that works with the current product constraints.

This shape was selected because it is the only one that satisfies both the crisis-driven business need and the current MiroFish ingest limitations without expanding into permanent platform work.

## Current Technical Context

MiroFish already has the basic infrastructure to preserve research provenance once the inputs are good enough:

- graph ingest writes `corpus_manifest.json` and `chunk_manifest.json`
- Strategy Lab persists `lane_templates.json`, per-lane artifacts, and `comparative_report.json`
- private analysis requires citation-backed chunk manifests and fails if the evidence layer is missing
- current file ingest only supports `.pdf`, `.docx`, `.md`, `.markdown`, and `.txt`

So the immediate product gap is not “build more report UI.” It is “give the system a better, wider, more trustworthy evidence bundle.” It also means the raw JSON operating data cannot be fed directly into MiroFish in v1; a provenance-preserving transformation layer is required.

## Available Evidence Surfaces

### Internal Operating Data

From the currently accessible repos:

- `quickbooks/data-package/08-qbo-financial-summary.json`
- `quickbooks/data-package/07-qbo-ar-aging.json`
- `quickbooks/data-package/01-pipedrive-open-pipeline.json`
- `quickbooks/data-package/02-pipedrive-won-deals-2022-2026.json`
- `quickbooks/data-package/03-client-relationship-profiles.json`
- `quickbooks/data-package/04-contacts-with-deal-history.json`
- `quickbooks/data-package/05-forecast-active-projects.json`
- `quickbooks/data-package/06-forecast-team-capacity.json`
- `quickbooks/data-package/09-lost-deals-analysis.json`
- `quickbooks/data-package/10-notes-on-open-deals.json`
- `quickbooks/data-package/11-pipedrive-leads.json`

### Existing Syntheses

- `quickbooks/data-package/12-market-intelligence-synthesis.md`
- `quickbooks/specs/009-market-intelligence/` and its research folder
- prior MiroFish Strategy Lab artifacts under `backend/uploads/projects/*/strategy_lab/`

These are useful context, but shaping explicitly treats many of them as synthesized artifacts rather than clean source-of-truth evidence.

### Needed External Research

This work explicitly calls for higher-quality external inputs than the current strategy-lab bundle, using named and preferably primary or near-primary sources such as:

- earnings calls, annual reports, and investor presentations
- press releases and buyer announcements
- SAM.gov / defense / government procurement sources
- analyst reports with attributable publishers
- industry publications with named examples and dates
- event sponsor, exhibitor, and conference program data

## Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | Produce a research package that directly supports an actual leadership decision in the current cash crisis, not just a better archive. | Core goal |
| R1 | Raw internal operating evidence from QuickBooks, Pipedrive, and Forecast must remain first-class source material, even if a transformed view is created for MiroFish ingestion. | Must-have |
| R2 | Any transformation from raw JSON/data into MiroFish-ingestible documents must preserve reversible provenance: source file, extraction date, row or record counts, and transformation method. | Must-have |
| R3 | External research must be tiered by evidence quality. Major claims may only rely on named primary or attributable secondary sources; AI syntheses can provide context but cannot stand alone as proof. | Must-have |
| R4 | The package must clearly separate 30–90 day survival or triage questions from 6–24 month strategic positioning questions. | Must-have |
| R5 | Contradictions, unsupported beliefs, and freshness limits must be explicit and easy to inspect. | Must-have |
| R6 | The human-readable deliverable must be strong enough that leadership can act without opening raw JSON, while still linking back to evidence. | Must-have |
| R7 | The final corpus must be ingestible by current MiroFish without requiring product changes in v1. | Must-have |
| R8 | v1 must stay bounded: no permanent warehouse, no new MiroFish ingest code, and no pretending this research is already a long-term data platform. | Must-have |

## What This Must Answer

The shaped work must support questions like:

- what Groove Jones should do in the next 30–90 days to survive,
- which AR, pipeline, and active-project signals matter immediately,
- which strategic lanes hold up when internal evidence is combined with stronger external evidence,
- where current market beliefs are actually unsupported or contradicted,
- and what evidence is strong enough to feed into future MiroFish strategy work.

## Expected Deliverables

At minimum, this work should yield:

- a source inventory covering internal datasets, existing syntheses, and new external research
- an evidence-tier rubric that distinguishes primary, attributable secondary, and AI-mediated/context-only sources
- a provenance-preserving transformation layer that turns selected raw operating data into MiroFish-ingestible markdown without losing source identity
- a contradiction register explaining what supports, contradicts, or remains unknown
- a leadership package split into:
  - `30–90 day triage`
  - `6–24 month strategy`
- a MiroFish-ready corpus bundle and corpus index that preserve provenance across files

Exact filenames and packaging should be decided in shaping and planning.

## Acceptance Criteria

- [ ] Internal data sources from QuickBooks, Pipedrive, and Forecast are inventoried with enough detail to understand what they can answer
- [ ] Existing synthesized artifacts are separated from raw operating evidence and labeled by evidence tier
- [ ] New external research is added from named, attributable, high-quality sources beyond the current `009-market-intelligence` bundle
- [ ] Any selected raw JSON/data is transformed into MiroFish-ingestible markdown with source path, extraction date, and record-count metadata preserved
- [ ] Major strategic claims are backed by citations to internal or external evidence, with AI syntheses never standing alone as proof
- [ ] Contradictions, blind spots, and freshness limits are documented explicitly in a dedicated contradiction register or equivalent artifact
- [ ] The outputs are useful to Groove Jones leadership without requiring MiroFish to interpret them first
- [ ] The leadership package clearly separates `30–90 day triage` from `6–24 month strategy`
- [ ] The final research package can be ingested into MiroFish as a multi-file corpus with provenance intact and without new MiroFish ingest code

## Constraints

- This work may read sensitive financial, sales, and production data; outputs must avoid leaking credentials, tokens, or unnecessary personal information.
- Access exists across multiple repos, but the immediate need is research quality, not building a permanent cross-repo data warehouse.
- MiroFish is currently strongest when ingesting document-style evidence bundles with citations; that should shape the output format.
- Existing internal syntheses are useful context, but they cannot stand in for the underlying evidence base.
- Raw JSON cannot be ingested directly by current MiroFish, so any v1 workflow must transform selected internal data into supported document formats.
- The current cash crisis is load-bearing context, not background flavor; the research package must help with urgent decisions, not just future reflection.

## Scope

### In Scope

- inventorying and evaluating available internal operating datasets
- incorporating existing Groove Jones research artifacts as context
- adding higher-quality external market, buyer, competitor, and procurement research
- producing a bounded transformation layer from selected raw data into provenance-bearing markdown evidence docs
- producing a stronger evidence foundation for leadership triage, leadership strategy, and future MiroFish analysis
- defining the research package that future modeling should rely on

### Out of Scope

- implementing a permanent production ETL or BI stack
- adding new MiroFish ingest code in v1
- rewriting MiroFish’s simulation engine
- building a full evidence graph as part of v1
- committing to a single strategic recommendation without first improving the evidence base
- creating plan.md or tasks.md in this step

## Shaping Outcome

The selected shape and fit check are captured in [shaping-transcript.md](/Users/dalecarman/Groove%20Jones%20Dropbox/Dale%20Carman/Projects/dev/MiroFish/specs/004-real-growth-research/shaping-transcript.md). The key decision is that v1 should ship a **timeboxed hybrid bundle**, not a pure one-off memo and not a long-term data platform.
