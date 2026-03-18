---
title: "Tasks - Groove Jones Strategy Lab in MiroFish"
date: 2026-03-18
bead: bd-1cv
---

<!-- Codex Review: APPROVED after 2 rounds | model: gpt-5.4 | date: 2026-03-18 -->
<!-- Status: REVISED -->
<!-- Revisions: aligned tasks to manifest-backed provenance, all-five-lane completion, lane-context wiring, minimal StrategyLabView delivery, and safety controls for sanitization/CORS/locking/resume -->
<!-- plan:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-18T22:51:24Z -->

# Tasks: Groove Jones Strategy Lab in MiroFish

## Prerequisites

- [ ] **T0: Lock the canonical corpus and five lane fixtures**
  - Treat the quickbooks research package at the corrected `/Dale Carman/` path as the canonical source set for `002`.
  - Capture validated fixtures for all five strategic lanes, with the defense lane as the first proving fixture.
  - Verify the representative corpus sample can be extracted through the strategy-lab intake path.

- [x] **T0.5: Add workflow-mode and intake groundwork**
  - Add `workflow_mode` through `frontend/src/store/pendingUpload.js`, `frontend/src/views/Home.vue`, `backend/app/api/graph.py`, and `backend/app/models/project.py`.
  - Add `.docx` support in `frontend/src/views/Home.vue`, `backend/app/config.py`, `backend/app/utils/file_parser.py`, and `backend/pyproject.toml`.
  - Verify project JSON stores `workflow_mode` and `.docx` text reaches extraction output.

## Backend Foundation

- [x] **T1: Add strategy-lab artifact contracts and manifest storage**
  - Create models for `LaneTemplate`, `LaneRunContext`, `DocumentManifestEntry`, `ChunkManifestEntry`, `CitationRecord`, `LaneScorecard`, and `InterviewArtifact`.
  - Add project-directory helpers for `strategy_lab/` storage, run directories, and `current/<lane_id>.json` pointers.
  - **Verify:** validated fixtures save cleanly and artifact paths are created idempotently.
  - **Depends on:** T0.5

- [x] **T2: Implement provenance manifests at ingestion time**
  - Persist `corpus_manifest.json` from the per-file extraction path in `backend/app/api/graph.py`.
  - Persist `chunk_manifest.json` from `backend/app/services/graph_builder.py` and backfill `episode_uuid` after batch upload.
  - Ensure unresolved retrieval hits cannot become final citations.
  - **Verify:** a cited chunk can be traced to `filename + locator + chunk_id + episode_uuid`.
  - **Depends on:** T1

- [x] **T3: Add the strategy-lab API scaffold**
  - Register a new strategy-lab blueprint and create project-scoped endpoints for lane template save/load, lane run status, private-analysis launch/status, comparative-report fetch, and source inspection.
  - Keep existing `/api/report/*` endpoints simulation-centric.
  - **Verify:** missing project/lane artifacts return correct 4xx errors.
  - **Depends on:** T1

## Private Analysis and Comparative Core

- [x] **T4: Implement `PrivateAnalysisAgent` with manifest-backed citations**
  - Build a new service that runs on `project_id + graph_id + lane template + provenance-resolved excerpts + stored narrative artifacts`.
  - Emit markdown/json scorecards with required dimensions, per-metric `CitationRecord[]`, and explicit assumptions/caveats.
  - Do not require `simulation_id`.
  - **Verify:** one defense-lane scorecard generates with structured citations and no simulation-scoped report state.
  - **Depends on:** T2, T3

- [x] **T5: Expand private analysis and comparative composition to all five lanes**
  - Generalize `PrivateAnalysisAgent` across all five required lane IDs.
  - Build `comparative_report.json` and `comparative_report.md` so one project-scoped output includes every lane and every required dimension.
  - Reject unlabeled metrics and unverifiable citations.
  - **Verify:** five lane scorecards and one comparative report can be saved and reloaded.
  - **Depends on:** T4

## Narrative Adapter

- [ ] **T6: Wire lane context into ontology and simulation prep**
  - Propagate `workflow_mode`, `lane_id`, and `lane_context_path` into simulation state.
  - Extend `SimulationManager.prepare_simulation(...)`, `SimulationConfigGenerator.generate_config(...)`, and `OntologyGenerator.generate(...)` to accept `LaneRunContext`.
  - Treat the runtime as public-discourse simulation only, not procurement prediction.
  - **Verify:** strategy-lab simulation artifacts serialize with lane metadata and distinct prompt framing.
  - **Depends on:** T1, T3

- [ ] **T7: Add pre-teardown interview capture and persistence**
  - Trigger curated batch interviews while the environment is still alive.
  - Persist transcripts under project-scoped strategy-lab artifacts for each lane run.
  - Keep v1 as transcript review only.
  - **Verify:** success path stores transcripts; env-not-alive path fails clearly without corrupting artifacts.
  - **Depends on:** T6

## Delivery Surface

- [x] **T8: Build the minimal `StrategyLabView` and source inspector**
  - Route `strategy_lab` projects away from the existing 5-step shell.
  - Add a project-scoped `StrategyLabView` with lane template review, per-lane run status, comparative report display, transcript viewer, and source inspection.
  - Keep the default social flow unchanged.
  - **Verify:** default flow still routes as before, and strategy-lab projects land in the new surface.
  - **Depends on:** T3, T5, T7

- [x] **T9: Replace raw strategy-lab rendering with sanitized markdown**
  - Add a shared safe markdown utility for the new strategy-lab surface.
  - Do not reuse the current raw `v-html` helpers from `Step4Report.vue` / `Step5Interaction.vue` unchanged.
  - **Verify:** strategy-lab report/transcript content is sanitized before render.
  - **Depends on:** T8

## Hardening

- [ ] **T10: Add safety and operability controls**
  - Replace wildcard CORS with an environment-scoped allowlist, at minimum for non-dev mode.
  - Add atomic artifact writes, per-lane locking, resumable run state, and structured logging.
  - Preserve prior successful artifacts on rerun instead of overwriting in place.
  - **Verify:** duplicate overlapping lane runs are rejected or serialized, and reruns produce new run directories without corrupting `current/<lane_id>.json`.
  - **Depends on:** T2, T3, T5

- [ ] **T11: Add focused regression coverage**
  - Add parser coverage for `.docx`.
  - Add serialization coverage for `workflow_mode`, lane templates, manifests, and comparative completeness.
  - Add a test proving private analysis works without `simulation_id`.
  - Add coverage for citation validation and unchanged default workflow behavior.
  - **Verify:** relevant backend/frontend test targets pass.
  - **Depends on:** T5, T6, T9, T10

- [ ] **T12: Run the end-to-end five-lane proof**
  - Import the representative quickbooks corpus.
  - Create one strategy-lab project.
  - Run the five lane narrative packs.
  - Capture interviews.
  - Generate five lane scorecards.
  - Assemble the comparative report with labeled metrics and inspectable citations.
  - **Verify:** all artifacts exist in the project strategy-lab directory and render in the `StrategyLabView`.
  - **Depends on:** T8, T9, T10, T11

## Dependency Graph

```text
T0 -> T0.5
T0.5 -> T1 -> T2 -> T4 -> T5
T1 -> T3
T1 + T3 -> T6 -> T7
T3 + T5 + T7 -> T8 -> T9
T2 + T3 + T5 -> T10
T5 + T6 + T9 + T10 -> T11
T8 + T9 + T10 + T11 -> T12
```
