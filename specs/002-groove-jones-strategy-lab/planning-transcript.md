---
title: "Planning Transcript - Groove Jones Strategy Lab in MiroFish"
date: 2026-03-18
bead: bd-1cv
---

<!-- plan:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-18T22:51:24Z -->

# Planning Transcript

**Participants:** EpicZenith (`codex/gpt-5.4`, proposer) x GoldXenon (`crew-challenger`, adversary)  
**Date:** 2026-03-18  
**Spec:** `specs/002-groove-jones-strategy-lab/spec.md`

## Round 1: EpicZenith - Research and initial direction

### Research findings

- The current intake path only accepts `pdf`, `md`, and `txt`:
  - `frontend/src/views/Home.vue`
  - `backend/app/config.py`
  - `backend/app/utils/file_parser.py`
- `Project` state has no workflow discriminator and only stores `simulation_requirement`, graph info, and chunk settings:
  - `backend/app/models/project.py`
- Narrative simulation is still deeply platform-shaped:
  - `backend/app/services/ontology_generator.py`
  - `backend/app/services/simulation_manager.py`
  - `backend/app/services/simulation_config_generator.py`
  - `backend/app/services/simulation_runner.py`
- `ReportAgent` is built around `simulation_id`, and `/api/report/generate` requires a valid simulation before report generation can start:
  - `backend/app/api/report.py`
  - `backend/app/services/report_agent.py`
- Synthetic interviews require a live OASIS env:
  - `backend/app/services/zep_tools.py`
  - `backend/app/api/simulation.py`
- The frontend workflow is already split across hardcoded step routes:
  - `frontend/src/router/index.js`
  - `frontend/src/views/MainView.vue`
  - `frontend/src/views/SimulationRunView.vue`
  - `frontend/src/views/ReportView.vue`
  - `frontend/src/views/InteractionView.vue`

### Initial direction

- Reuse the graph path and narrative engine where honest.
- Add a report-agent-style private-analysis pass for lane scorecards.
- Extend the frontend and report path to present a strategy-lab workflow.

## Round 2: GoldXenon - Five challenges

```markdown
[PHASE:challenge]

I've read `spec.md`, `shaping-transcript.md`, and verified against the codebase. The spec and shaping are solid - Shape D was well-earned through adversarial shaping. But your technical direction still had five gaps:

1. `ReportAgent` is not actually reusable for private analysis because it is simulation-lifecycle-coupled. `backend/app/services/report_agent.py` requires `simulation_id`, and `backend/app/api/report.py` rejects missing simulations. You must explicitly choose a new service/class instead of implying light reuse.
2. Interviews require a live env. `backend/app/services/zep_tools.py` and `backend/app/api/simulation.py` both depend on `SimulationRunner.check_env_alive(...)`. The plan must choose interview timing instead of assuming transcripts can be fetched later.
3. Reusing twitter labels for public discourse creates semantic debt. The plan should add a workflow discriminator so strategy-lab runs are not mislabeled as default social runs.
4. Frontend workflow cannot be hand-waved. `frontend/src/views/MainView.vue` hardcodes `Step x/5`, `stepNames`, and `handleNextStep`, and the route tree is already split by step. The plan must choose a workflow strategy explicitly.
5. Sequence matters. Prototype the private-analysis surface before adapting the simulation layer, because that is the real net-new product contract.
```

## Round 3: EpicZenith - Revised decisions

```markdown
[PHASE:revise]

Accepted all 5 challenges. Revised planning decisions:

1. Private analysis becomes a new `PrivateAnalysisAgent` service for v1, not a `ReportAgent` refactor. It can reuse orchestration patterns, but not the `simulation_id` lifecycle.
2. Interviews will be captured before env teardown. V1 sequence: narrative sim completes -> curated batch interviews run while env is alive -> transcripts persist as artifacts -> later report/private-analysis steps read stored transcripts only.
3. Add `workflow_mode` metadata to project and simulation state so strategy-lab runs route and serialize separately from default/social runs.
4. Use a dedicated strategy-lab workflow shell/view instead of extending the existing 5-step `MainView.vue` path inline.
5. Resequence implementation to: (1) domain contracts + lane templates + workflow metadata, (2) private-analysis prototype on defense lane, (3) narrative adapter + prompt branching + interview capture, (4) comparative report composition + strategy-lab UI shell, (5) hardening/tests.
6. Add one more explicit Phase 1 prerequisite: verify the quickbooks corpus can enter the graph path cleanly, including `.docx` intake.
```

## Round 4: GoldXenon - Approved

```markdown
[PHASE:approved]

All five objections addressed. Verdict on each:

#1 (ReportAgent coupling) - Resolved. New PrivateAnalysisAgent operating on graph_id + lane template + stored narrative artifacts is correct. Option (b) - borrowing patterns, not lifecycle.

#2 (Interview timing) - Resolved. Pre-teardown batch capture is the right V1 tradeoff. Note in plan: Interview panel becomes a transcript viewer in V1, not interactive. Name this scope cut.

#3 (workflow_mode discriminator) - Resolved. On both project and simulation metadata is better than my suggestion. Clean routing at creation time plus disambiguation at state time.

#4 (Frontend workflow) - Resolved. Separate strategy-lab shell reusing primitives avoids blast radius.

#5 (Sequencing) - Resolved. Five phases correctly ordered with private analysis prototype before adapter.

Final note for plan.md: Phase 2 defense-lane prototype depends on research corpus in Zep graph. Validate graph_builder.py can ingest quickbooks corpus without strategy-specific changes, or add Phase 1 subtask.

Verdict: Plan direction approved. No remaining structural objections. Ship the plan.

[COMPLETE]
```
