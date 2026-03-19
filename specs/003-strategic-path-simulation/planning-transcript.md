---
title: "Planning Transcript — MiroFish Strategic Path Simulation"
date: 2026-03-18
bead: bd-2g4
---

<!-- plan:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T22:02:28Z -->

# Planning Transcript

**Participants:** QuickUnion (pi/claude-opus-4-6, proposer) × UltraQuartz (crew-challenger, adversary)
**Date:** 2026-03-18

---

## Round 1: UltraQuartz — 8 Implementation Risks

### Findings (from codebase research)

1. **CRITICAL: No API path to inject manual ontology.** `/ontology/generate` is monolithic: uploads files → auto-generates → saves. `/build` requires `status == ONTOLOGY_GENERATED`. No endpoint accepts pre-built ontology. Three paths identified: (a) file overwrite, (b) manual project creation, (c) new endpoint.

2. **CRITICAL: `simulation_requirement` is project-level.** Stored on Project model, not Simulation. Each `prepare_simulation()` reads from project. For 4 scenarios: either 4 projects (4× graph cost) or 1 project with manual edits between prepares.

3. **SEVERE: Entity types → wrong persona template.** `INDIVIDUAL_ENTITY_TYPES` hardcoded list doesn't include `enterprisebuyer`, `industryanalyst`, `conferenceorganizer`. These 3 get group persona prompts instead of individual.

4. **SEVERE: Chinese-language prompts pervasive.** Profile generator, config generator, persona prompts all in Chinese. 5+ methods need translation.

5. **MODERATE: B2.5 validation can't happen inside prepare.** `prepare_simulation()` is monolithic — generates ALL profiles. Need standalone script for 3-entity test.

6. **MODERATE: .docx conversion details missing.** `ALLOWED_EXTENSIONS = {pdf, md, txt, markdown}`. Need pandoc command + table/image handling decision.

7. **MODERATE: Cost model underspecified.** Need test run as explicit task.

8. **LOW: Graph memory contamination.** `enable_graph_memory_update` defaults to `False` — non-issue.

---

## Round 2: QuickUnion — Decisions for All 8

1. Path (a) — overwrite project.json after auto-generation. Linear flow, no re-entry risk.
2. 1 project, 4 simulations. Edit project.json between prepares. Edit simulation_config.json for seed events.
3. Add 3 words to `INDIVIDUAL_ENTITY_TYPES`. Minimal blast radius.
4. Create `gj_config.py` monkey-patch module. Load via `import gj_config` in `run.py`. Don't modify MiroFish core prompts.
5. Standalone `validate_profiles.py` script. ~3 LLM calls.
6. `pandoc -f docx -t markdown`. Tables preserved. Images lost (acceptable).
7. 10-round Scenario A test run before full 20+ round runs.
8. Confirmed off by default.

---

## Round 3: UltraQuartz — 5 Remaining Gaps

A. **Ontology JSON design is real work** — not just "overwrite project.json." Need explicit task with format constraints (10 types max, reserved attribute names, ≤100 char descriptions, source_targets completeness). → Added T2a.

B. **ReportAgent is per-simulation** — no cross-scenario comparison mode. → Split T16 into T16a (4 individual reports) + T16b (manual cross-scenario comparison).

C. **Profile cost 4× redundant** — each prepare regenerates all 30 profiles. → Accepted: ~$3-5 extra, simplicity > optimization.

D. **gj_config.py loading mechanism** — "wrapper script" doesn't work for web UI triggers. → Path (a): `import gj_config` in `run.py` (1 line, the ONLY source modification).

E. **Test run should be separate simulation** (withdrawn — current plan already does this correctly).

---

## Round 4: UltraQuartz Approves

All 4 conditions met. Load-bearing reminders: R3 gate must actually block, R9 scope caveat in every deliverable, run.py import documented as single source modification.
