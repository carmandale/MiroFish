---
title: "Tasks — MiroFish Strategic Path Simulation"
date: 2026-03-18
bead: bd-2g4
---

<!-- Codex Review: APPROVED after 4 rounds (fresh session) | model: codex/gpt-5.4 | date: 2026-03-18 -->
<!-- Status: RECONCILED — direct source edits, wholesale template translations, R7 sentiment narrowed -->
<!-- plan:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T22:02:28Z -->

# Tasks: Strategic Path Simulation

## Phase 0: Setup

- [ ] **T0: Convert .docx files to markdown**
  - `pandoc -f docx -t markdown -o Groove_Jones_Consolidated_Market_Intelligence_2026.md Groove_Jones_Consolidated_Market_Intelligence_2026.docx`
  - `pandoc -f docx -t markdown -o Groove_Jones_30Day_Revenue_Action_Plan.md Groove_Jones_30Day_Revenue_Action_Plan.docx`
  - Verify: tables preserved as pipe tables, text structure intact, images lost (acceptable)
  - Source dir: `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/`

- [ ] **T1: Create MiroFish project via web UI**
  - Start MiroFish: `npm run dev` (frontend :3000, backend :5001)
  - Upload ALL .md/.txt research files through the web UI
  - Set `simulation_requirement` to: "Simulate XR industry discourse reactions to Groove Jones strategic positioning announcements. Agents represent enterprise buyers, competitor agencies, defense contractors, healthcare systems, industry analysts, and conference organizers. English language, US market focus."
  - Record the `project_id` returned
  - **Verify:** `total_text_length` in response ≥ 500K chars (confirms most research ingested)

- [ ] **T2a: Design custom B2B ontology JSON**
  - Write `specs/003-strategic-path-simulation/ontology.json` following the schema in plan.md
  - 10 entity types: XRAgency, EnterpriseBuyer, DefenseContractor, HealthcareSystem, IndustryAnalyst, ConferenceOrganizer, PrimeContractor, VCFirm, Person, Organization
  - 8 edge types: COMPETES_WITH, COLLABORATES_WITH, SUPPLIES_TO, EVALUATES, REPORTS_ON, PARTNERS_WITH, INVESTS_IN, PROCURES_FROM
  - Constraints: attribute names ≠ {name, uuid, group_id, created_at, summary}. Descriptions ≤100 chars. Last 2 types = Person + Organization.
  - **Verify:** JSON is valid. source_targets for each edge type cover the intended entity pairings.

- [ ] **T2b: Inject custom ontology into project**
  - Locate project file: `backend/uploads/projects/{project_id}/project.json`
  - Replace `ontology` field with contents of `ontology.json`
  - Ensure `status` remains `"ontology_generated"`
  - **Verify:** Read back project.json, confirm ontology has 10 entity types and 8 edge types
  - **Depends on:** T1, T2a

- [ ] **T3: Build knowledge graph**
  - Call `POST /api/graph/build` with the project_id via web UI
  - Wait for completion (may take several minutes for 670K words)
  - Record the `graph_id` returned
  - **Verify:** Graph has ≥50 nodes and ≥30 edges. Entity types include XRAgency and EnterpriseBuyer.
  - **Depends on:** T2b

- [ ] **T4: Create English prompt override module**
  - Write `backend/gj_config.py` (~150 lines) that monkey-patches:
    - `OasisProfileGenerator._get_system_prompt()` → English system prompt including "professional context: role, budget authority, procurement influence"
    - `OasisProfileGenerator._build_individual_persona_prompt()` → English persona generation instructions
    - `OasisProfileGenerator._build_group_persona_prompt()` → English group persona instructions
    - `PLAN_USER_PROMPT_TEMPLATE` → full English reassignment (not replace() — Codex R5)
    - `SECTION_USER_PROMPT_TEMPLATE` → full English reassignment (not replace() — Codex R5)
    - `CHAT_SYSTEM_PROMPT_TEMPLATE` → full English reassignment (not replace() — Codex R5)
    - `ReportAgent.plan_outline()` → wrap to catch/translate Chinese fallback outline
  - Add `import gj_config` to `backend/run.py` (THE single MiroFish source modification — document this clearly)
  - Restart backend: `npm run backend`
  - **Verify:** Backend starts without import errors

- [ ] **T5: Extend individual entity type list**
  - Edit `backend/app/services/oasis_profile_generator.py` line ~68
  - Add `"enterprisebuyer", "industryanalyst", "conferenceorganizer"` to `INDIVIDUAL_ENTITY_TYPES`
  - **Verify:** `_is_individual_entity("enterprisebuyer")` returns True

- [ ] **T6: B2.5 Validation Gate — test 3 profiles** ⚠️ GATES ALL SUBSEQUENT WORK
  - Write `specs/003-strategic-path-simulation/validate_profiles.py`
  - Script reads 3 entities from graph by name: J&J MedTech, Lockheed Martin, Publicis Sapient
  - Calls `OasisProfileGenerator.generate_profile_from_entity()` for each
  - Prints full persona text
  - **INSPECT:** Do personas contain procurement-relevant context? (budget authority, competitive position, industry knowledge)
  - **If PASS:** Proceed to Phase 1
  - **If FAIL:** Escalate per spec: (a) modify gj_config.py system prompt to be more explicit, or (b) manually write persona text for key agents
  - **Depends on:** T3, T4, T5

## Phase 1: Test Run (Scenario A — Healthcare, 10 rounds)

- [ ] **T7: Create test simulation**
  - Edit `project.json` → set `simulation_requirement` to Scenario A healthcare description
  - Call `POST /api/simulation/create` with project_id and graph_id
  - Record `simulation_id`
  - **Depends on:** T6 (passed)

- [ ] **T8: Prepare test simulation**
  - Call `POST /api/simulation/{id}/prepare`
  - Wait for profile generation + config generation to complete
  - **Verify:** ~30+ agent profiles generated. simulation_config.json exists.

- [ ] **T9: Configure test simulation for scenario**
  - Edit `uploads/simulations/{sim_id}/simulation_config.json`:
    - Replace `initial_posts` with Scenario A healthcare seed event (from plan.md)
    - Replace `hot_topics` with: ["healthcare XR", "surgical training VR", "pharma Medical Affairs", "ASCO congress"]
    - Set timezone config to US business hours (peak: 9-12, 14-17 ET)
    - Set `total_simulation_hours` to match 10-round test scope
  - **Verify:** JSON is valid after edits

- [ ] **T10: Run 10-round test**
  - Call `POST /api/simulation/{id}/start` with `enable_graph_memory_update: false`
  - Monitor progress via web UI
  - **Verify:** Agents produce English-language posts. Discourse is coherent (not random social media noise). At least 3 different entity types participate.

- [ ] **T11: Test run gate — pass/fail**
  - Review simulation logs in `uploads/simulations/{sim_id}/`
  - **PASS criteria:** Agents reference XR industry context from the knowledge graph. Posts are in English. Multiple agent types interact meaningfully. Competitive dynamics visible (at least 1 agent references competitor positioning).
  - **If PASS:** Proceed to Phase 2
  - **If FAIL:** Diagnose — is it prompt quality? Ontology design? Graph sparsity? Fix and re-run test.

## Phase 2: Full Simulation Runs

For each scenario (A through D), repeat T12-T15:

- [ ] **T12: Scenario A — Healthcare (20+ rounds, full run)**
  - Edit project.json simulation_requirement → Scenario A
  - Create simulation → prepare → edit config (seed event A, US timezone) → start (20+ rounds)
  - **Depends on:** T11 (passed)

- [ ] **T13: Scenario B — Defense (20+ rounds)**
  - Edit project.json simulation_requirement → Scenario B
  - Create → prepare → edit config (seed event B) → start

- [ ] **T14: Scenario C — Retainer (20+ rounds)**
  - Edit project.json simulation_requirement → Scenario C
  - Create → prepare → edit config (seed event C) → start

- [ ] **T15: Scenario D — Hybrid (20+ rounds)**
  - Edit project.json simulation_requirement → Scenario D
  - Create → prepare → edit config (seed event D) → start

- [ ] **T16a: Run ReportAgent for each scenario**
  - Call `POST /api/report/generate` for each of the 4 simulation_ids
  - 4 separate reports generated
  - **Depends on:** T12-T15

- [ ] **T16b: Write cross-scenario comparison**
  - Read all 4 ReportAgent reports + simulation action logs
  - Compare metrics: total engagement volume, amplification chain length, competitive response count, sentiment distribution
  - Produce comparative summary document
  - **Every output document states:** "narrative resonance measurement, not procurement prediction"
  - **Depends on:** T16a

## Phase 3: Interviews + Deliverable

- [ ] **T17: Conduct agent interviews**
  - For each scenario, interview 3+ key agents via MiroFish web UI
  - Priority agents: EnterpriseBuyer (healthcare/defense context), competitor XRAgency, IndustryAnalyst
  - Test positioning pitches: "How would you describe Groove Jones to a colleague?"
  - **Caveat in all interview notes:** "industry discourse persona, not procurement decision-maker"
  - **Depends on:** T12-T15

- [ ] **T18: Produce comparative summary**
  - Synthesize T16b comparison + T17 interview insights
  - Structure: which scenario generated (1) most buyer engagement, (2) strongest amplification, (3) most competitive reaction, (4) best sentiment
  - Include narrative resonance caveat (R5, R9)
  - **Depends on:** T16b, T17

- [ ] **T19: Write positioning recommendation**
  - Based on T18, recommend specific language for:
    - NatGuard PAO outreach emails (this week)
    - Healthcare buyer outreach (ASCO timing)
    - Defense BD conversations (DFW primes)
    - Client retainer proposals
  - Scope: "how to talk about it" — NOT "which market to enter"
  - **Depends on:** T18

## Dependency Graph

```
T0 (docx → md)
  ↓
T1 (create project, upload files)
  ↓
T2a (design ontology JSON)
  ↓
T2b (inject ontology) ←── T1
  ↓
T3 (build graph)
  ↓
T4 (English prompts) ──── T5 (entity type list)
  ↓                         ↓
T6 (B2.5 VALIDATION GATE) ←┘
  ↓
T7-T11 (test run — 10 rounds Scenario A)
  ↓ (pass)
T12-T15 (4 full scenario runs, 20+ rounds each)
  ↓
T16a (4 ReportAgent runs) → T16b (cross-scenario comparison)
  ↓                           ↓
T17 (agent interviews)        │
  ↓                           ↓
T18 (comparative summary) ←──┘
  ↓
T19 (positioning recommendation)
```

## Gates

| Gate | Task | Criteria | Escalation |
|------|------|----------|------------|
| B2.5 | T6 | 3 test profiles contain procurement-relevant context | Modify system prompt or manually override personas |
| Test run | T11 | English discourse, graph context visible, multi-type interaction | Diagnose and fix prompts/ontology/graph |
