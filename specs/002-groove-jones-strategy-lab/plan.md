---
title: "Implementation Plan - Groove Jones Strategy Lab in MiroFish"
date: 2026-03-18
bead: bd-1cv
---

<!-- Codex Review: APPROVED after 2 rounds | model: gpt-5.4 | date: 2026-03-18 -->
<!-- Status: REVISED -->
<!-- Revisions: added manifest-backed provenance contract; made five-lane comparative output part of done; defined lane-template adapter path into simulation prep/config/ontology; reduced v1 UI scope to StrategyLabView; added sanitization, CORS, locking, atomic writes, and resumable-run controls -->
<!-- plan:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-18T22:51:24Z -->

# Implementation Plan: Groove Jones Strategy Lab in MiroFish

> Planned 2026-03-18 by EpicZenith x GoldXenon (adversarial), revised after Codex approval.

## Overview

Build Strategy Lab as a project-scoped, provenance-first workflow inside MiroFish that:

- reuses graph ingestion and the current simulation engine only for public narrative stress-testing
- adds a separate private-analysis surface for buying committees, capability load, compliance gates, and lane scorecards
- delivers a strategy-lab backend/API slice plus a minimal project-scoped review surface instead of stretching the current 5-step social workflow into a different product
- treats five-lane comparative output as part of done, not a post-v1 stretch goal

## Problem Statement

The current codebase is optimized around one end-to-end social simulation pipeline:

- Intake only accepts `pdf`, `md`, and `txt` in both the UI and backend, while the canonical Groove Jones research package includes `.docx` files.
- Project and simulation state only understand `simulation_requirement` plus twitter/reddit toggles.
- Runtime/config state is platform-hardcoded.
- Graph ingestion merges extracted files into a single text blob and chunk upload does not preserve a usable per-claim provenance contract.
- Report generation is simulation-scoped and cannot run without a known `simulation_id`.
- Synthetic interviews require a live OASIS environment.
- The frontend flow is split across a hardcoded 5-step route/view set.
- The current UI rendering path trusts generated HTML and backend CORS is wildcarded, which is too loose even for an internal decision tool.

The root architectural gap is workflow ownership plus evidence traceability. Strategy Lab needs project-scoped lane templates, provenance-aware corpus artifacts, private-analysis outputs, comparative reporting, and explicit workflow semantics. None of those are first-class in the current app.

## Proposed Solution

1. Introduce `workflow_mode` at project creation time and propagate it through project, simulation, and strategy-lab report state.
2. Add a provenance manifest layer at corpus-ingestion time so every reusable excerpt can be traced to `filename + locator + chunk_id + episode_uuid`, with page numbers where the source format supports them.
3. Keep the existing engine as a bounded narrative layer for public-signal packs only, but drive it through a validated `LaneTemplate` schema that maps into ontology, config, and interview generation.
4. Add a new `PrivateAnalysisAgent` service that runs on `project_id + graph_id + lane template + provenance-resolved excerpts + stored narrative artifacts`, not on `simulation_id`.
5. Capture strategy-lab interviews before environment teardown and persist them as artifacts for later report use.
6. Deliver a minimal strategy-lab API plus one project-scoped review surface in v1; defer a richer custom shell until after the five-lane comparative workflow is proven.
7. Add v1 safety controls: sanitized markdown rendering, constrained CORS, atomic artifact writes, per-lane locking, resumable run state, and structured observability.

## Technical Approach

### Project and Artifact Contracts

Touch:

- `backend/app/models/project.py`
- `backend/app/api/graph.py`
- `frontend/src/store/pendingUpload.js`
- `frontend/src/views/Home.vue`
- new `backend/app/models/strategy_lab.py`

Add `workflow_mode: "default" | "strategy_lab"` to `Project` and carry it from home upload to ontology generation, simulation state, and project JSON.

Add strategy-lab contracts:

- `LaneTemplate`
- `LaneRunContext`
- `PrivateInputSet`
- `DocumentManifestEntry`
- `ChunkManifestEntry`
- `CitationRecord`
- `SourceLabel`
- `LaneScorecard`
- `InterviewArtifact`
- `ComparativeReportSummary`

Store strategy-lab artifacts under the existing project directory so the workflow is project-scoped rather than simulation-scoped:

```text
backend/uploads/projects/<project_id>/strategy_lab/
  corpus_manifest.json
  chunk_manifest.json
  lane_templates.json
  runs/<lane_id>/<run_id>/narrative_summary.json
  runs/<lane_id>/<run_id>/interviews.json
  runs/<lane_id>/<run_id>/private_analysis.json
  runs/<lane_id>/<run_id>/status.json
  current/<lane_id>.json
  comparative_report.md
  comparative_report.json
```

`current/<lane_id>.json` is a pointer file to the latest successful run for that lane. Reruns create a new `<run_id>` directory instead of overwriting prior artifacts in place.

### Provenance Model

Touch:

- `backend/app/api/graph.py`
- `backend/app/services/graph_builder.py`
- new `backend/app/services/strategy_lab_provenance.py`
- `backend/app/models/strategy_lab.py`

Current intake concatenates document text with filename headers in `api/graph.py`, and `graph_builder.py` currently uploads bare `EpisodeData(data=chunk, type="text")`. For strategy lab, that is not enough.

Add a local-first provenance layer:

- `DocumentManifestEntry`
  - `document_id`
  - `filename`
  - `sha256`
  - `mime_type`
  - `source_format`
  - `locator_type` (`page`, `heading_paragraph`, `line_range`)
- `ChunkManifestEntry`
  - `chunk_id`
  - `document_id`
  - `filename`
  - `page_start`
  - `page_end`
  - `section_path`
  - `paragraph_start`
  - `paragraph_end`
  - `char_start`
  - `char_end`
  - `chunk_sha256`
  - `episode_uuid`
- `CitationRecord`
  - `metric_id`
  - `source_label`
  - `document_id`
  - `filename`
  - `locator_display`
  - `chunk_id`
  - `episode_uuid`
  - `snippet`

Implementation rules:

- `api/graph.py` still saves `all_text` for ontology generation, but also persists per-document extraction metadata into `corpus_manifest.json`.
- `graph_builder.py` writes `chunk_manifest.json` before upload, then backfills `episode_uuid` from `add_batch(...)` results after each batch completes.
- PDF ingestion records page ranges; `.docx`, `.md`, and `.txt` record heading/paragraph or line locators when true page numbers do not exist.
- `PrivateAnalysisAgent` and the comparative composer must resolve every citation through `chunk_manifest.json`. If a retrieval hit cannot be mapped back to a manifest row, it cannot appear as a cited claim in the final scorecard.
- Strategy-lab report output exposes citations as structured objects, not the current report-agent pattern of echoing tool query strings as `sources`.

### Corpus Intake and Graph Readiness

Touch:

- `backend/app/config.py`
- `backend/app/utils/file_parser.py`
- `backend/pyproject.toml`
- `frontend/src/views/Home.vue`

Add `.docx` intake because the canonical quickbooks research corpus currently cannot enter MiroFish untouched.

Use a backend parser such as `python-docx`, widen accepted extension lists in both the UI and API, and verify the extracted text path still feeds `graph_builder.py`.

Extend extraction to emit locator-friendly metadata:

- PDF -> page spans
- DOCX -> heading path + paragraph ranges
- Markdown/text -> line ranges or section headers

Validate ingestion against the actual quickbooks research files under:

- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/research.md`
- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/Groove_Jones_Consolidated_Market_Intelligence_2026.docx`
- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/Groove_Jones_30Day_Revenue_Action_Plan.docx`

This is a Phase 1 prerequisite, not optional cleanup.

### Lane Template Schema and Engine Mapping

Touch:

- `backend/app/services/ontology_generator.py`
- `backend/app/services/simulation_manager.py`
- `backend/app/services/simulation_config_generator.py`
- `backend/app/services/simulation_runner.py`
- `backend/app/api/simulation.py`
- new `backend/app/api/strategy_lab.py`

Define a concrete `LaneTemplate` schema that can be validated before any run:

```json
{
  "lane_id": "defense-government-entry",
  "display_name": "Defense / Government Entry",
  "hypothesis": "Selective government and defense work can diversify revenue while increasing compliance burden.",
  "public_actor_classes": ["competitors", "prime_partners", "industry_analysts", "procurement_watchers"],
  "public_event_classes": ["award_announcement", "pilot_demo", "compliance_delay", "partner_signal"],
  "narrative_brief": "Model public market signaling and positioning pressure around the lane.",
  "interview_personas": ["procurement_officer", "prime_partner_exec", "internal_delivery_lead"],
  "private_committee_roles": ["buyer", "legal", "security", "delivery", "finance"],
  "procurement_gates": ["vehicle_access", "security_review", "past_performance", "cashflow_gap"],
  "capability_requirements": ["clearance_partner_strategy", "proposal_ops", "delivery_capacity"],
  "required_internal_inputs": ["current_team_capacity", "partner_list", "margin_floor"],
  "scorecard_dimensions": ["time_to_cash", "durability_12_24m", "capability_fit", "required_investment", "failure_modes", "evidence_strength"],
  "monte_carlo_fields": ["pipeline_size", "close_rate", "sales_cycle_days"]
}
```

Concrete adapter path:

- Persist `lane_templates.json` per project and load it through strategy-lab API endpoints.
- Generate a `LaneRunContext` from the saved template and attach `lane_id`, `workflow_mode`, and `lane_context_path` to `SimulationState`.
- Extend `SimulationManager.prepare_simulation(...)` with optional `lane_context`.
- Extend `SimulationConfigGenerator.generate_config(...)` with optional `lane_context`.
- `_build_context(...)` merges `simulation_requirement` with `LaneRunContext.narrative_brief`, public actor seeds, event seeds, and interview persona hints.
- `OntologyGenerator.generate(...)` receives `additional_context` containing `workflow_mode`, `lane_id`, actor/event seeds, and explicit "public discourse only" framing.
- Runtime keeps the existing twitter/reddit engine for v1, but strategy-lab code treats those as public-discourse channels, not literal procurement simulators.

Do not attempt a boardroom-engine rewrite in v1.

### Interview Capture Before Teardown

Touch:

- `backend/app/api/simulation.py`
- `backend/app/services/zep_tools.py`
- new `backend/app/services/strategy_lab_interviews.py`

After a strategy-lab narrative run finishes, auto-execute a curated batch interview set while the OASIS environment is still alive, then persist transcripts to project-scoped artifacts.

The v1 interview surface is read-only transcript review. Do not promise reopen/reinterview after teardown because the current APIs require `SimulationRunner.check_env_alive(...)`.

### Private Analysis Layer

Add a new service: `backend/app/services/private_analysis_agent.py`

Inputs:

- `project_id`
- `graph_id`
- `lane_template`
- canonical research corpus excerpts / graph references
- optional stored narrative/interview artifacts
- optional Monte Carlo attachment metadata
- provenance-resolved excerpt references from `chunk_manifest.json`

Outputs:

- a cited scorecard per lane with required dimensions:
  - time-to-cash
  - 12-24 month durability
  - capability fit
  - required investment
  - failure modes
  - evidence strength
- per-metric source labels from `{narrative simulation | private analysis layer | research citation | Monte Carlo attachment}`
- a machine-readable citation list per metric using `CitationRecord[]`
- an assumptions/caveats block that explicitly calls out narrative-only vs private-analysis-derived judgments

Reuse `ReportAgent` patterns where useful:

- staged generation
- structured logs
- markdown/json outputs

Do not reuse `ReportAgent` lifecycle or its `simulation_id` contract.

Execution contract:

- Defense lane is the first fixture used to validate the abstraction.
- The implementation is not done at one lane. The agent/service must run across all five required lanes before exit.
- Comparative scoring is project-scoped: one lane may fail independently, but the final comparative report is not complete until all five lanes have a successful scorecard or an explicit blocking error status.

### Comparative Report Composition

Add new project-scoped strategy-lab endpoints, for example `backend/app/api/strategy_lab.py`, and register them in:

- `backend/app/api/__init__.py`
- `backend/app/__init__.py`

Responsibilities:

- CRUD/load lane templates
- launch private analysis for a lane
- fetch narrative/interview artifacts for a lane
- assemble the comparative report markdown + JSON for the full strategy lab
- reject report generation if any required metric lacks `source_label` or any citation lacks manifest-backed provenance
- expose a source-inspection payload so the UI can drill from report rows to filenames, locators, chunk IDs, and episode IDs

Keep the existing `/api/report/*` endpoints simulation-centric instead of forcing mixed semantics into them.

Comparative output contract:

- one row per strategic lane
- required columns: time-to-cash, 12-24 month durability, capability fit, required investment, failure modes, evidence strength
- each cell carries:
  - score / judgment
  - `source_label`
  - `citation_ids[]`
  - optional Monte Carlo attachment pointer

### Frontend Delivery Surface

Touch:

- `frontend/src/router/index.js`
- new `frontend/src/api/strategyLab.js`
- `frontend/src/store/pendingUpload.js`
- `frontend/src/views/Home.vue`
- new `frontend/src/views/StrategyLabView.vue`
- new strategy-lab components
- new `frontend/src/utils/safeMarkdown.js`

Add workflow selection at project creation and route `strategy_lab` projects away from the existing 5-step shell.

For v1, prefer one new project-scoped `StrategyLabView.vue` plus supporting components instead of a full multi-step custom shell.

Reuse shared primitives where they already fit:

- graph/workbench shell layout
- existing cards/tables/progress patterns

Do not reuse the current raw `v-html` markdown helpers unchanged; strategy-lab surfaces must use a sanitized renderer.

V1 review surface:

- lane template review
- per-lane run status
- comparative report table and narrative summary
- transcript viewer
- source inspector for citations and attached excerpts

### Safety and Operability

Touch:

- `backend/app/__init__.py`
- strategy-lab API/service modules
- new frontend markdown utility

Add concrete safety controls in the plan:

- Replace wildcard CORS with environment-configured allowed origins, at minimum for non-dev mode.
- Sanitize all strategy-lab markdown/HTML before rendering. Do not introduce new raw `v-html` paths.
- Use atomic artifact writes (`.tmp` then rename) for manifests, per-lane status, and comparative reports.
- Add a per-lane lock keyed by `project_id + lane_id + workflow_mode` to reject duplicate overlapping runs.
- Persist run status so failed lanes can be retried without corrupting prior successful artifacts.
- Emit structured logs with `project_id`, `lane_id`, `run_id`, and workflow stage for ingestion, narrative run, interview capture, private analysis, and report composition.
- Treat auth/ACL as an explicit product gap outside this spec. Until that exists, v1 deployment target is internal/single-team usage only. Even so, CORS tightening and output sanitization are mandatory.

## Implementation Phases

### Phase 1: Workflow Metadata, Provenance, Corpus Intake, and Lane Contracts

- Add `workflow_mode` to project/simulation state and frontend pending-upload state.
- Add `.docx` parsing support and verify the quickbooks corpus can populate the Zep graph path.
- Add `corpus_manifest.json` and `chunk_manifest.json` generation plus `episode_uuid` backfill after upload.
- Add strategy-lab contract models and project-scoped artifact paths.
- Seed and validate all five required lane templates, with the defense lane used as the first fixture to prove the schema.

### Phase 2: Private-Analysis Backbone and Five-Lane Comparative Composer

- Implement `PrivateAnalysisAgent` against manifest-backed provenance, first on the defense lane and then generalized to the other four lanes before phase exit.
- Emit one cited `LaneScorecard` per lane with the required labeled dimensions and per-metric `CitationRecord[]`.
- Build the comparative composer that assembles all five lane outputs into `comparative_report.json` and `comparative_report.md`.
- Prove that private analysis and comparative composition can run without `simulation_id`.

### Phase 3: Narrative Adapter and Interview Capture

- Branch ontology/config prompts for `strategy_lab`.
- Inject `LaneRunContext` into simulation prep/config generation.
- Generate lane-specific narrative packs using the existing simulation engine for all five lanes.
- Capture and persist the interview bundle before environment teardown for each lane.
- Attach narrative/interview artifacts to each lane scorecard and comparative row with explicit source labels.

### Phase 4: Minimal Strategy-Lab Delivery Surface

- Add the strategy-lab API slice.
- Add a project-scoped `StrategyLabView` route and supporting components.
- Render per-lane status, comparative report, transcripts, and source inspection from stored artifacts.
- Keep the legacy report and interaction routes unchanged; they remain simulation-centric.

### Phase 5: Hardening and Proof

- Tighten CORS and add sanitized markdown rendering.
- Add artifact locking, atomic writes, retry/resume semantics, and structured status transitions.
- Add focused regression tests for provenance, lane validation, comparative completeness, and unchanged default workflow behavior.
- Run an end-to-end proof against the representative quickbooks corpus and verify that all five lanes produce a comparative output.

## Acceptance Criteria

- A strategy-lab project can be created with `workflow_mode=strategy_lab`.
- The canonical research corpus can be ingested through the supported document pipeline, including `.docx`.
- `corpus_manifest.json` and `chunk_manifest.json` are generated for strategy-lab projects, and each cited claim in a scorecard/report can be traced to `filename + locator + chunk_id + episode_uuid`.
- All five strategic lanes are validated and saved as project-scoped `LaneTemplate` artifacts.
- Narrative simulation can run in strategy-lab mode without pretending to be a procurement simulator.
- Interviews are captured before teardown and later rendered as stored transcripts for each lane.
- `PrivateAnalysisAgent` can generate a cited lane scorecard for each of the five lanes without requiring `simulation_id`.
- The comparative report rejects unlabeled metrics and preserves the spec's source-label contract.
- The comparative report includes all five lanes and all required dimensions in one project-scoped output.
- The UI can inspect report citations back to manifest-backed provenance records.
- Strategy-lab rendering uses sanitized markdown/HTML, not the current raw `v-html` helpers.
- Duplicate overlapping lane runs are rejected or serialized through the per-lane lock, and reruns do not destroy prior successful artifacts.
- The default social workflow still routes and behaves as before.

## Requirement-to-Change Traceability

- R0 -> Five validated lane templates + five narrative packs + five interview bundles + five private-analysis scorecards + one comparative report composer
- R1 -> `.docx` intake, `corpus_manifest.json`, `chunk_manifest.json`, and manifest-backed citations in scorecard/report outputs
- R2 -> `PrivateAnalysisAgent` plus lane rubric/schema and stored private inputs
- R3 -> Source-labeled scorecards, explicit assumptions/caveats sections in report output, no interactive post-teardown claims
- R4 -> `LaneScorecard` and `CitationRecord` contracts with required labeled dimensions and report-level validation
- R5 -> `strategy_lab` workflow mode and backend/API slice without rewriting the simulation engine
- R6 -> Workflow metadata + project-scoped artifact map + explicit separation between narrative layer and private-analysis layer
- R7 -> Comparative report field for Monte Carlo attachments, treated as side-by-side evidence rather than hidden coupling
- R8 -> `LaneTemplate` validator, explicit lane-to-engine adapter path, and five-lane template coverage

## Alternative Approaches Considered

### Reuse `ReportAgent` Directly

Rejected. `ReportAgent` and `/api/report/generate` are built around `simulation_id`, report lookup by simulation, and simulation-scoped chat/log flows. Reusing them directly would either create fake simulation state or hide coupling behind conditionals.

### Full Custom Strategy-Lab Shell Immediately

Deferred. The current UI assumptions are rigid enough that strategy lab should not be jammed into them, but v1 does not need a large bespoke shell. One project-scoped review surface is lower risk and gets the comparative workflow proven sooner.

### Keep Citations as Free-Text Footnotes Only

Rejected. The current code already shows how easy it is to degrade into query-string "sources". Strategy lab needs machine-readable, manifest-backed citation objects so report rows can be validated and inspected.

### Full Boardroom / Procurement Engine Rewrite

Rejected by the selected shape. It is not required for a credible v1 and would delay the one thing MiroFish can already contribute: public narrative stress-testing and synthetic interviews.

## Dependencies and Prerequisites

- `python-docx` (or equivalent) for `.docx` extraction
- existing Zep graph build path remains the canonical research-ingestion mechanism
- the quickbooks research corpus at the corrected `/Dale Carman/` path
- one validated lane-template fixture for each of the five strategic lanes
- backend test harness expansion beyond the current `backend/scripts/test_profile_format.py`

## Risk Analysis and Mitigation

- Social semantics leak into strategy-lab outputs.
  - Mitigation: explicit `workflow_mode`, prompt branching, and clear report copy about narrative-layer boundaries.
- Canonical corpus extraction is lossy or inconsistent.
  - Mitigation: Phase 1 ingestion validation on the actual quickbooks material plus manifest-level locator checks.
- Comparative report drifts into unlabeled or unverifiable assertions.
  - Mitigation: schema validation rejects missing `source_label`, and report generation rejects citations without manifest-backed provenance.
- Lane templates become descriptive documents instead of executable inputs.
  - Mitigation: `LaneRunContext` adapter and simulation-config injection are part of the plan, not follow-up cleanup.
- Monte Carlo data is not available when the comparative report runs.
  - Mitigation: explicit attachment slot with an absent/not-provided state rather than silent omission.
- Frontend blast radius breaks default flow.
  - Mitigation: one new project-scoped strategy-lab view instead of mutating the standard 5-step shell.
- Unsafe generated HTML or loose API exposure.
  - Mitigation: sanitized markdown plus environment-scoped CORS allowlist.
- Concurrent reruns corrupt artifacts.
  - Mitigation: per-lane lock, run-scoped directories, and atomic `current/<lane_id>.json` pointer updates.

## References and Research

### Internal References

- `specs/002-groove-jones-strategy-lab/spec.md`
- `specs/002-groove-jones-strategy-lab/shaping-transcript.md`
- `backend/app/models/project.py`
- `backend/app/api/graph.py`
- `backend/app/services/graph_builder.py`
- `backend/app/services/ontology_generator.py`
- `backend/app/services/simulation_manager.py`
- `backend/app/services/simulation_config_generator.py`
- `backend/app/services/simulation_runner.py`
- `backend/app/services/report_agent.py`
- `backend/app/services/zep_tools.py`
- `backend/app/api/report.py`
- `frontend/src/router/index.js`
- `frontend/src/views/Home.vue`
- `frontend/src/views/MainView.vue`
- `frontend/src/views/SimulationRunView.vue`
- `frontend/src/views/ReportView.vue`
- `frontend/src/views/InteractionView.vue`

### External / Adjacent Inputs

- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/research.md`
- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/Groove_Jones_Consolidated_Market_Intelligence_2026.docx`
- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/Groove_Jones_30Day_Revenue_Action_Plan.docx`
