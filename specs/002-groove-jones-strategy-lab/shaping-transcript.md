---
shaping: true
---

<!-- shape:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-18T21:40:37Z -->

# Groove Jones Strategy Lab — Shaping Transcript

**Participants:** EpicZenith (`codex/gpt-5.4`, proposer) × NiceArrow (`crew-challenger` / `claude-opus-4-6`, adversary)  
**Date:** 2026-03-18  
**Spec:** `specs/002-groove-jones-strategy-lab/spec.md`  
**Bead:** `bd-1cv`

## Source

> "We're going to shape this properly. Not a quick brainstorm, not 'ask 3 questions and write a plan.' The real thing — requirements, shapes, fit checks, the works."

> "The problem: specs/002-groove-jones-strategy-lab"

> "Shaping means:
> - R — numbered requirements
> - S — multiple shapes
> - Fit check
> - A selected shape
> - Breadboard"

Additional source material:
- `specs/002-groove-jones-strategy-lab/spec.md`
- `README.md`
- `specs/001-monte-carlo-revenue-model/shaping-transcript.md`
- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/research.md`
- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/Groove_Jones_30Day_Revenue_Action_Plan.docx`
- `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/Groove_Jones_Consolidated_Market_Intelligence_2026.docx`

## Problem

Groove Jones needs more than a static strategy memo, but MiroFish’s current engine is structurally social-platform-native. The shaping problem is not “how do we stuff five strategic paths into today’s simulation?” It is: what is the honest product shape for using MiroFish to compare Groove Jones strategic lanes without pretending the current engine can simulate boardroom procurement dynamics it does not model?

## Outcome

A shape that lets MiroFish help Groove Jones choose among five strategic lanes by combining what MiroFish can credibly do now with explicit handling of what must live outside or beyond the current engine.

## Transcript

### NiceArrow — Review

```markdown
[PHASE:review]

I've read all six documents and performed concrete verification against the MiroFish codebase. Here's my assessment.

## 1. My Understanding of the Real Problem

Groove Jones has $19K cash and zero months runway. The 30-day action plan is triage. The consolidated market intelligence identifies five strategic lanes. The Monte Carlo model (001) handles the quantitative "how much revenue might close?" question. This spec (002) proposes MiroFish become a "Strategic Futures Lab" that complements Monte Carlo by simulating multi-actor scenario dynamics across those five lanes to answer "which lane creates the strongest future position?"

## 2. Concrete Verification: The Social-Platform Gap Is Far Worse Than the Spec Admits

I grepped the MiroFish codebase for the hardcoded platform assumptions:

- `simulation_runner.py`: 146 occurrences of twitter/reddit/social. The `SimulationRunState` dataclass has hardcoded fields: `twitter_current_round`, `reddit_current_round`, `twitter_running`, `reddit_running`, `twitter_completed`, `reddit_completed`. The `platform` field is typed as `str` with comment `# twitter / reddit`.
- `simulation_config_generator.py`: 65 occurrences. `PlatformConfig` is hardcoded with `platform: str # twitter or reddit`. The `generate_config()` method takes `enable_twitter: bool` and `enable_reddit: bool` parameters. There are separate `twitter_config` and `reddit_config` fields.
- Enterprise/B2B concept count across ALL of `backend/app/services/`: The terms "account", "procurement", "buyer", "committee", "stakeholder" appear a total of 4 times — all in `oasis_profile_generator.py`.

The spec says "the current simulation framing is social-platform-native, not B2B account-native" and "the semantic model must shift." That's a dramatic understatement. This isn't a semantic shift — it's a structural rewrite of the simulation engine's core abstractions. Every run loop, every state tracker, every config generator assumes Twitter/Reddit platforms.

## 3. Biggest Weaknesses and Ambiguities

### A. This Is Not a Shaped Spec — It's a Pre-Shape Problem Definition

Compare to `specs/001-monte-carlo-revenue-model/shaping-transcript.md`: that went through 6 adversarial rounds, proposed 3 concrete shapes (A/B/C), killed Shape B with evidence, eliminated Shape C on fit check, produced a detailed breadboard with UI/non-UI affordances, and wired everything together. It defined exactly 48 tornado runs (12 calls × 2 params × 2 directions).

This spec proposes a "six-part workflow" but:
- No shapes explored.
- No breadboard.
- No fit check.

### B. The Strategic Paths Are Named But Not Operationalized

The spec says "Encode the five major Groove Jones paths as scenarios, not just topics." But it doesn't explain what a "scenario" means in MiroFish terms.

### C. The Comparative Report (R5) Has No Defined Metrics Pipeline

- How does MiroFish produce "near-term cash impact" from a multi-agent simulation?
- "Evidence strength" is a meta-metric with no defined mechanism.
- "Downside risk" needs counterfactual handling that the spec never defines.

### D. R7 (Distinguish Current vs. Required Adaptations) Is Unmet By the Spec Itself

The spec says this distinction is required, but it never creates the explicit workflow-step-to-capability map.

### E. The "Complement Monte Carlo" Framing Is Underdefined

If "integration" just means "a human reads both reports," that's coexistence, not integration.

## Summary

The problem framing is strong — I agree MiroFish-as-strategy-lab is a better use case than a generic social prediction engine for Groove Jones. But this spec is a problem definition, not a shaped solution. The five paths are topics, not scenarios. The report metrics are labels, not pipelines. And the codebase gap is far larger than "the semantic model must shift" implies.

I need to see shapes, not just requirements.
```

### EpicZenith — Revise Round 1

```markdown
[PHASE:revise]

Accepted. You're right that `specs/002-groove-jones-strategy-lab/spec.md` is still pre-shape. I am not treating that doc as the shaped answer anymore. I am resetting the work as an actual shaping draft.

## Source

- User problem statement: shape `specs/002-groove-jones-strategy-lab` properly with requirements, multiple shapes, fit check, selected shape, breadboard.
- Research corpus: Groove Jones consolidated 2026 market-intelligence report plus 30-day action plan.
- Codebase reality: current MiroFish engine is deeply Twitter/Reddit-oriented and cannot honestly be described as “almost B2B-ready.”

## Problem

Groove Jones needs more than a static strategy memo, but MiroFish’s current engine is structurally social-platform-native. The shaping problem is not “how do we stuff five strategic paths into today’s simulation?” It is: what is the honest product shape for using MiroFish to compare Groove Jones strategic lanes without pretending the current engine can simulate boardroom procurement dynamics it does not model?

## Outcome

A shape that lets MiroFish help Groove Jones choose among five strategic lanes by combining what MiroFish can credibly do now with explicit handling of what must live outside or beyond the current engine.

## Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | Compare at least five Groove Jones strategic lanes through multi-actor scenario behavior, not just a static memo, so leadership can decide where to focus next. | Core goal |
| R1 | Use the quickbooks research corpus as the canonical evidence base and preserve traceability from source material to assumptions and report claims. | Must-have |
| R2 | Model B2B/private go-to-market dynamics honestly: internal Groove Jones roles, buyers, committees, partners, competitors, procurement/compliance gates, and timing events must appear somewhere in the solution without pretending today’s social engine natively handles them. | Must-have |
| R3 | Produce scenario guidance rather than fake certainty; assumptions, caveats, and system boundaries must be visible to the reader. | Must-have |
| R4 | Produce a comparative decision output with a defined evaluation frame: time-to-cash, 12-24 month durability, capability fit, required investment, path-specific failure modes, and evidence strength. | Must-have |
| R5 | Deliver a credible v1 inside the existing MiroFish codebase without requiring a full simulation-engine rewrite before anything useful exists. | Must-have |
| R6 | Explicitly separate current MiroFish capabilities from required product work so the team can see what is prototype-ready, what needs adaptation, and what belongs outside MiroFish. | Must-have |
| R7 | Define Monte Carlo integration concretely rather than vaguely: either a specific data handoff or explicit side-by-side report composition. | Must-have |
| R8 | Operationalize each lane as a scenario template with named actor classes, event classes, and outputs. Topic labels alone do not count. | Must-have |

## A: Public-Discourse Proxy Packs

| Part | Mechanism |
|------|-----------|
| A1 | One strategy pack per lane: shared dossier plus lane-specific seed packet flows through current graph builder, profile generator, and config generator with minimal engine changes. |
| A2 | Agent cast limited to actors with plausible public voice: analysts, conference organizers, partner BD leads, competitor agencies, public-facing buyer voices. |
| A3 | Event library limited to public signaling: launch announcements, conference deadlines, analyst notes, vendor applications, referrals, media chatter. |
| A4 | Comparative report ranks lanes on narrative pull, partner interest, competitor response, and interview takeaways; Monte Carlo remains a sidecar for cash. |

## B: Boardroom Mode Rewrite

| Part | Mechanism |
|------|-----------|
| B1 | Replace platform abstraction with accounts, buying committees, procurement stages, internal GJ capacity, and contract/compliance gates. |
| B2 | Replace Twitter/Reddit event flow with budget cycles, RFP releases, champion loss, compliance milestones, partner introductions, and fiscal timing. |
| B3 | Model lanes as interventions inside a shared strategy world competing for the same internal resources and market actors. |
| B4 | Comparative report reads directly from boardroom-mode state and event outcomes. |

## C: Strategy Workshop Companion

| Part | Mechanism |
|------|-----------|
| C1 | Use graph builder plus report-agent tooling to create actor cards, lane dossiers, and evidence-backed scenario narratives, but no live multi-agent simulation loop. |
| C2 | For each lane, create structured scenario canvases with named actors, event timelines, success/failure triggers, and synthetic interviews. |
| C3 | Comparative report synthesizes lane canvases plus Monte Carlo outputs into a strategy memo. |

## D: Two-Layer Strategy Lab

| Part | Mechanism |
|------|-----------|
| D1 | Use the current MiroFish engine only for the public narrative layer: market pull, analyst chatter, partner signaling, competitor reaction, recruiting/pipeline resonance. |
| D2 | Add a separate private strategy layer outside the social engine for buying committees, procurement/compliance gates, internal capability load, and failure branches. |
| D3 | Define a required lane template for every lane before any run: actor classes, public events, private gates, success/failure triggers, evidence citations, and report outputs. |
| D4 | Comparative report merges D1 narrative signals, D2 private scorecards, and explicit Monte Carlo attachments; it also ships with a current-vs-required capability map. |

## Fit Check

| Req | Requirement | Status | A | B | C | D |
|-----|-------------|--------|---|---|---|---|
| R0 | Compare at least five Groove Jones strategic lanes through multi-actor scenario behavior, not just a static memo, so leadership can decide where to focus next. | Core goal | ✅ | ✅ | ❌ | ✅ |
| R1 | Use the quickbooks research corpus as the canonical evidence base and preserve traceability from source material to assumptions and report claims. | Must-have | ✅ | ✅ | ✅ | ✅ |
| R2 | Model B2B/private go-to-market dynamics honestly: internal Groove Jones roles, buyers, committees, partners, competitors, procurement/compliance gates, and timing events must appear somewhere in the solution without pretending today’s social engine natively handles them. | Must-have | ❌ | ✅ | ✅ | ✅ |
| R3 | Produce scenario guidance rather than fake certainty; assumptions, caveats, and system boundaries must be visible to the reader. | Must-have | ❌ | ✅ | ✅ | ✅ |
| R4 | Produce a comparative decision output with a defined evaluation frame: time-to-cash, 12-24 month durability, capability fit, required investment, path-specific failure modes, and evidence strength. | Must-have | ❌ | ✅ | ✅ | ✅ |
| R5 | Deliver a credible v1 inside the existing MiroFish codebase without requiring a full simulation-engine rewrite before anything useful exists. | Must-have | ✅ | ❌ | ✅ | ✅ |
| R6 | Explicitly separate current MiroFish capabilities from required product work so the team can see what is prototype-ready, what needs adaptation, and what belongs outside MiroFish. | Must-have | ✅ | ✅ | ✅ | ✅ |
| R7 | Define Monte Carlo integration concretely rather than vaguely: either a specific data handoff or explicit side-by-side report composition. | Must-have | ✅ | ✅ | ✅ | ✅ |
| R8 | Operationalize each lane as a scenario template with named actor classes, event classes, and outputs. Topic labels alone do not count. | Must-have | ✅ | ✅ | ✅ | ✅ |

Tentative selection: D.
```

### NiceArrow — Challenge

```markdown
[PHASE:challenge]

Major improvement from the original spec. Four shapes, a fit check, kill rationale — this is now real shaping.

## Attack 1: Does D Really Satisfy R2?

No. D gets a ✅ on R2 by moving the unsolved problem into a box labeled "New product surface" and calling it done.

D2 is either:
- A second simulation engine with different abstractions.
- A structured scorecard/form that a human fills in.
- An LLM-driven analysis pass over research documents with structured output.

Until you specify the mechanism for D2, the fit check is unfalsifiable. My read: the honest mechanism for D2 is a structured LLM synthesis pass using `report_agent` tooling with lane-specific evaluation rubrics.

## Attack 2: Should C Beat D?

No, but for a different reason than you think.

C throws away the one thing MiroFish actually does well: generating synthetic agents from research and running them through scenarios to produce emergent behavior and synthetic interviews.

D beats C only if D's public layer is honest about what it provides: narrative stress-testing and synthetic stakeholder interviews, not market-signal detection or procurement prediction.

## Attack 3: Which Requirements Are Still Vague, Tautological, or Non-Testable?

- R0: "multi-actor scenario behavior" is undefined.
- R2: "must appear somewhere in the solution" is a loophole.
- R4: report headings have no production methods.
- R8: needs at least one concrete lane template.

## Additional Finding

`backend/app/services/ontology_generator.py` is also social-platform-hardcoded:
- line 12: `社交媒体舆论模拟`
- line 18: `社交媒体舆论模拟系统`

## Bottom Line

D is the right shape direction, but it needs three fixes before approval:
1. Name D2's mechanism explicitly.
2. Tighten R0, R2, R4.
3. Provide one concrete lane template.
```

### EpicZenith — Revise Round 2

```markdown
[PHASE:revise]

Accepted. Your R2 objection was right: D2 was a disguised placeholder. I’ve fixed the mechanism, tightened the loophole requirements, and grounded the shape with one concrete lane template.

## Revised Requirements (changes marked)

| ID | Requirement | Status |
|----|-------------|--------|
| 🟡 R0 | 🟡 Compare at least five Groove Jones strategic lanes by running lane-specific scenario packs that produce: (a) synthetic stakeholder interviews, (b) emergent narrative dynamics across agents, and (c) structured lane scorecards with cited evidence. | Core goal |
| R1 | Use the quickbooks research corpus as the canonical evidence base and preserve traceability from source material to assumptions and report claims. | Must-have |
| 🟡 R2 | 🟡 B2B/private go-to-market dynamics must be modeled in a defined **private analysis layer** with an explicit mechanism and named outputs per lane. For the selected shape, that mechanism is **structured LLM synthesis using `report_agent`-style tooling plus lane-specific evaluation rubrics**, not social simulation. | Must-have |
| R3 | Produce scenario guidance rather than fake certainty; assumptions, caveats, and system boundaries must be visible to the reader. | Must-have |
| 🟡 R4 | 🟡 Produce a comparative decision output where every evaluation dimension declares its source: `{narrative simulation | private analysis layer | research citation | Monte Carlo attachment}`. No unlabeled dimensions. Required dimensions: time-to-cash, 12-24 month durability, capability fit, required investment, path-specific failure modes, and evidence strength. | Must-have |
| R5 | Deliver a credible v1 inside the existing MiroFish codebase without requiring a full simulation-engine rewrite before anything useful exists. | Must-have |
| R6 | Explicitly separate current MiroFish capabilities from required product work so the team can see what is prototype-ready, what needs adaptation, and what belongs outside MiroFish. | Must-have |
| R7 | Define Monte Carlo integration concretely rather than vaguely: either a specific data handoff or explicit side-by-side report composition. | Must-have |
| R8 | Operationalize each lane as a scenario template with named actor classes, event classes, and outputs. Topic labels alone do not count. | Must-have |

## Revised Selected Shape

## 🟡 D: Narrative Simulation + Structured Private Analysis

| Part | Mechanism |
|------|-----------|
| 🟡 D1 | 🟡 Current MiroFish engine runs lane-specific **narrative simulation packs** only. The output is limited to framing pressure, competitor/partner signaling, emergent objections, and synthetic stakeholder interviews. It is explicitly **not** procurement prediction. |
| 🟡 D2 | 🟡 Private analysis layer = `report_agent`-driven structured LLM synthesis pass over the research corpus plus lane-specific internal inputs. Each lane uses a rubric covering committee roles, procurement/compliance gates, capability load, investment needs, and failure branches. Output is a cited lane scorecard, not a second simulation engine. |
| 🟡 D3 | 🟡 Every lane must declare a template before any run: public actors, public events, private inputs, private gates, required citations, expected outputs. |
| 🟡 D4 | 🟡 Comparative report merges D1 narrative outputs, D2 private scorecards, and explicit Monte Carlo attachments, with source labels per metric. |

## Updated Current-vs-Required Capability Map

| Workflow Step | Current MiroFish Capability | Selected Mechanism | Product Work Required |
|---------------|-----------------------------|--------------------|-----------------------|
| 🟡 Ontology generation | 🟡 `ontology_generator.py` exists but its system prompt is hardcoded for `社交媒体舆论模拟` / social-media public-opinion simulation (`backend/app/services/ontology_generator.py:12,18`) | 🟡 Override/branch ontology prompt for strategy-lane narrative packs | Moderate |
| Research dossier ingestion | `graph_builder.py` + document pipeline | Reuse current graph build path | Minimal |
| Actor generation | `oasis_profile_generator.py` | Reuse for public-signal cast and interview personas | Moderate prompt/schema adaptation |
| Narrative simulation | `simulation_config_generator.py` + `simulation_runner.py` | Reuse as narrative-simulation layer only | Moderate constraints + lane adapter |
| 🟡 Private lane analysis | 🟡 No native capability today | 🟡 New structured analysis pass using `report_agent` + lane rubric + internal-input schema | New product surface |
| Comparative report | `report_agent.py` + `zep_tools.py` | Extend to merge narrative outputs + private scorecards + Monte Carlo attachment | Moderate |
| Monte Carlo integration | None in MiroFish | Side-by-side report composition in v1 | Minimal |

## Concrete Lane Template Example: Defense / Government Entry

| Slot | Definition |
|------|------------|
| Lane | Defense / Government Entry |
| Public actors | Defense industry analyst; AFWERX/SBIR program manager; L3Harris BD director; Moth+Flame competitor rep; I/ITSEC conference organizer; National Guard training lead |
| Public events | SBIR topic release; I/ITSEC conference cycle; Disasterville press coverage; competitor contract award announcement; SAM.gov registration announcement |
| Private inputs | GJ defense proof point = Disasterville press/credibility; CMMC readiness = none; ITAR registration = none; GSA Schedule = none; dedicated federal BD headcount = 0; Year-1 compliance/BD investment = research-cited `$200K–$400K` |
| Private gates | SAM.gov + CAGE code -> basic federal eligibility; SBIR Phase I win -> Phase II path; CMMC Level 2 -> broader contract eligibility; prime introductions (L3Harris/SAIC/Leidos) -> subcontracting path |
| Research-cited outputs | Time-to-cash source = consolidated report `Year 1: $450K–$750K federal`; durability source = 18–36 month defense program framing; required investment source = ITAR/CMMC/GSA/BD cost block |
| Narrative outputs | Emergent objections, positioning resonance, competitor framing, partner-signaling patterns, synthetic interviews |
| Final outputs | Narrative plausibility findings; cited private scorecard; synthetic stakeholder interviews; failure mode inventory; Monte Carlo attachment = `not primary for this lane` unless linked later |
```

### NiceArrow — Approved

```markdown
[PHASE:approved]

Your three fixes land.

1. Renaming D2 fixes the loophole. The mechanism is explicit, with named inputs and outputs.
2. The Defense lane template makes R8 concrete enough.
3. The structural over-claim is gone. D1 explicitly says "not procurement prediction." D4's source labeling makes the report auditable.

One flagged risk that does not block approval:
- `PlatformConfig` has social-media-specific semantics (`viral_threshold`, `echo_chamber_strength`, `recency_weight`, `popularity_weight`, `relevance_weight`).
- The capability map should note that narrative simulation needs semantic reframing for strategy-lane context.

Summary: The shape is approved. D is now honest about what each layer does. This is ready for `/plan`.
```

### EpicZenith — Revise Round 3

````markdown
[PHASE:revise]

One more required shaping piece before I freeze the artifact: the breadboard for the selected shape, plus your flagged narrative-layer caveat folded into the capability map.

## Capability Map Adjustment

| Workflow Step | Current MiroFish Capability | Selected Mechanism | Product Work Required |
|---------------|-----------------------------|--------------------|-----------------------|
| Narrative simulation | `simulation_config_generator.py` + `simulation_runner.py` | Reuse current engine as a **public discourse channel** only | **Moderate** — requires `PlatformConfig` semantic reframing (`viral_threshold`, `echo_chamber_strength`, recommendation weights) for strategy-lane context. V1 can reuse the `twitter` platform label while explicitly redefining it as public discourse rather than literal Twitter. |

## Detail D: Breadboard

### UI Affordances

| Place | Affordance | Type | Wires Out |
|-------|------------|------|-----------|
| Research workspace | Canonical corpus picker / uploaded source set | Input | → Graph build, Private analysis |
| Lane template editor | Per-lane template fields: public actors, public events, private inputs, private gates, metric sources | Form | → Template store |
| Narrative run controls | Run a lane’s narrative pack with a discourse-tuning preset | Action | → Narrative simulation |
| Interview panel | Interview generated public-layer stakeholders after a run | Interaction | → Interview notes, Report builder |
| Comparative strategy report | Side-by-side lane cards with source-labeled metrics and citations | Display | ← Report builder |
| Capability map panel | Current vs required adaptation table | Display | ← Capability gap map |

### Non-UI Affordances

| Place | Affordance | Type | Wires Out |
|-------|------------|------|-----------|
| Corpus | Zep graph build from canonical research corpus | Service | → Template suggestions, Narrative pack adapter, Private analysis |
| Template store | `LaneTemplate` schema `{lane_id, public_actors, public_events, private_inputs, private_gates, rubric, metric_sources}` | Data | → Narrative pack adapter, Private analysis, Report builder |
| Ontology | Strategy-ontology prompt override for narrative packs | Transform | → Graph build, Profile generation |
| Narrative layer | `NarrativePackAdapter` maps a lane template into current simulation config plus discourse-tuned `PlatformConfig` | Transform | → Simulation runner |
| Narrative layer | Narrative simulation runner produces logs, emergent interactions, and interviewable agents | Service | → Interview panel, Report builder |
| Private analysis | `LaneRubric` schema for committee, gate, capability, investment, and failure-mode evaluation | Data | → Private analysis pass |
| Private analysis | Structured private analysis pass (`report_agent` + lane rubric + citations + internal inputs) | Service | → Report builder |
| Reporting | `MetricSourceMap` declaring source per dimension | Data | → Report builder |
| Reporting | Monte Carlo attachment loader | Service | → Report builder |
| Reporting | Capability gap map generator | Service | → Capability map panel, Report builder |
| Reporting | Comparative strategy report builder merging narrative outputs, private scorecards, citations, and Monte Carlo attachment | Service | → Comparative strategy report |

### Wiring

```text
Canonical corpus
  -> Graph build
  -> Template suggestions
  -> Private analysis pass

Lane template editor
  -> Template store
  -> Ontology override
  -> Narrative pack adapter
  -> Lane rubric

Ontology override
  -> Graph build
  -> Profile generation

Narrative pack adapter
  -> Narrative simulation runner
  -> Interview panel
  -> Report builder

Lane rubric + internal inputs + canonical corpus
  -> Structured private analysis pass
  -> Report builder

Metric source map + Monte Carlo attachment + capability gap map
  -> Report builder
  -> Comparative strategy report
```
````

### NiceArrow — Complete

```markdown
[COMPLETE]

Final approval. The breadboard closes the loop.

The shaping artifact is now complete with:
- Problem statement
- Requirements R0–R8
- Four shapes explored
- Fit check matrix with kill rationale
- Selected shape D with explicit layer mechanisms
- Current-vs-required capability map
- Concrete Defense lane template
- Breadboard with UI/Non-UI affordances and wiring

Verified capabilities that the breadboard depends on:
- `report_agent.py` -> `interview_agents` tool
- `zep_tools.py` -> `interview_agents()` accepting `simulation_id`, `interview_requirement`, `custom_questions`
- `ontology_generator.py` -> `generate()` accepting `document_texts + simulation_requirement`
```

## Final Shaped Artifact

## Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | Compare at least five Groove Jones strategic lanes by running lane-specific scenario packs that produce: (a) synthetic stakeholder interviews, (b) emergent narrative dynamics across agents, and (c) structured lane scorecards with cited evidence. | Core goal |
| R1 | Use the quickbooks research corpus as the canonical evidence base and preserve traceability from source material to assumptions and report claims. | Must-have |
| R2 | B2B/private go-to-market dynamics must be modeled in a defined private analysis layer with an explicit mechanism and named outputs per lane. For the selected shape, that mechanism is structured LLM synthesis using `report_agent`-style tooling plus lane-specific evaluation rubrics, not social simulation. | Must-have |
| R3 | Produce scenario guidance rather than fake certainty; assumptions, caveats, and system boundaries must be visible to the reader. | Must-have |
| R4 | Produce a comparative decision output where every evaluation dimension declares its source: `{narrative simulation | private analysis layer | research citation | Monte Carlo attachment}`. No unlabeled dimensions. Required dimensions: time-to-cash, 12-24 month durability, capability fit, required investment, path-specific failure modes, and evidence strength. | Must-have |
| R5 | Deliver a credible v1 inside the existing MiroFish codebase without requiring a full simulation-engine rewrite before anything useful exists. | Must-have |
| R6 | Explicitly separate current MiroFish capabilities from required product work so the team can see what is prototype-ready, what needs adaptation, and what belongs outside MiroFish. | Must-have |
| R7 | Define Monte Carlo integration concretely rather than vaguely: either a specific data handoff or explicit side-by-side report composition. | Must-have |
| R8 | Operationalize each lane as a scenario template with named actor classes, event classes, and outputs. Topic labels alone do not count. | Must-have |

## A: Public-Discourse Proxy Packs

| Part | Mechanism |
|------|-----------|
| A1 | One strategy pack per lane: shared dossier plus lane-specific seed packet flows through current graph builder, profile generator, and config generator with minimal engine changes. |
| A2 | Agent cast limited to actors with plausible public voice: analysts, conference organizers, partner BD leads, competitor agencies, public-facing buyer voices. |
| A3 | Event library limited to public signaling: launch announcements, conference deadlines, analyst notes, vendor applications, referrals, media chatter. |
| A4 | Comparative report ranks lanes on narrative pull, partner interest, competitor response, and interview takeaways; Monte Carlo remains a sidecar for cash. |

## B: Boardroom Mode Rewrite

| Part | Mechanism |
|------|-----------|
| B1 | Replace platform abstraction with accounts, buying committees, procurement stages, internal GJ capacity, and contract/compliance gates. |
| B2 | Replace Twitter/Reddit event flow with budget cycles, RFP releases, champion loss, compliance milestones, partner introductions, and fiscal timing. |
| B3 | Model lanes as interventions inside a shared strategy world competing for the same internal resources and market actors. |
| B4 | Comparative report reads directly from boardroom-mode state and event outcomes. |

## C: Strategy Workshop Companion

| Part | Mechanism |
|------|-----------|
| C1 | Use graph builder plus report-agent tooling to create actor cards, lane dossiers, and evidence-backed scenario narratives, but no live multi-agent simulation loop. |
| C2 | For each lane, create structured scenario canvases with named actors, event timelines, success/failure triggers, and synthetic interviews. |
| C3 | Comparative report synthesizes lane canvases plus Monte Carlo outputs into a strategy memo. |

## D: Narrative Simulation + Structured Private Analysis

| Part | Mechanism |
|------|-----------|
| D1 | Current MiroFish engine runs lane-specific narrative simulation packs only. The output is limited to framing pressure, competitor/partner signaling, emergent objections, and synthetic stakeholder interviews. It is explicitly not procurement prediction. |
| D2 | Private analysis layer = `report_agent`-driven structured LLM synthesis pass over the research corpus plus lane-specific internal inputs. Each lane uses a rubric covering committee roles, procurement/compliance gates, capability load, investment needs, and failure branches. Output is a cited lane scorecard, not a second simulation engine. |
| D3 | Every lane must declare a template before any run: public actors, public events, private inputs, private gates, required citations, expected outputs. |
| D4 | Comparative report merges D1 narrative outputs, D2 private scorecards, and explicit Monte Carlo attachments, with source labels per metric. |

## Fit Check

| Req | Requirement | Status | A | B | C | D |
|-----|-------------|--------|---|---|---|---|
| R0 | Compare at least five Groove Jones strategic lanes by running lane-specific scenario packs that produce: (a) synthetic stakeholder interviews, (b) emergent narrative dynamics across agents, and (c) structured lane scorecards with cited evidence. | Core goal | ✅ | ✅ | ❌ | ✅ |
| R1 | Use the quickbooks research corpus as the canonical evidence base and preserve traceability from source material to assumptions and report claims. | Must-have | ✅ | ✅ | ✅ | ✅ |
| R2 | B2B/private go-to-market dynamics must be modeled in a defined private analysis layer with an explicit mechanism and named outputs per lane. For the selected shape, that mechanism is structured LLM synthesis using `report_agent`-style tooling plus lane-specific evaluation rubrics, not social simulation. | Must-have | ❌ | ✅ | ✅ | ✅ |
| R3 | Produce scenario guidance rather than fake certainty; assumptions, caveats, and system boundaries must be visible to the reader. | Must-have | ❌ | ✅ | ✅ | ✅ |
| R4 | Produce a comparative decision output where every evaluation dimension declares its source: `{narrative simulation | private analysis layer | research citation | Monte Carlo attachment}`. No unlabeled dimensions. Required dimensions: time-to-cash, 12-24 month durability, capability fit, required investment, path-specific failure modes, and evidence strength. | Must-have | ❌ | ✅ | ✅ | ✅ |
| R5 | Deliver a credible v1 inside the existing MiroFish codebase without requiring a full simulation-engine rewrite before anything useful exists. | Must-have | ✅ | ❌ | ✅ | ✅ |
| R6 | Explicitly separate current MiroFish capabilities from required product work so the team can see what is prototype-ready, what needs adaptation, and what belongs outside MiroFish. | Must-have | ✅ | ✅ | ✅ | ✅ |
| R7 | Define Monte Carlo integration concretely rather than vaguely: either a specific data handoff or explicit side-by-side report composition. | Must-have | ✅ | ✅ | ✅ | ✅ |
| R8 | Operationalize each lane as a scenario template with named actor classes, event classes, and outputs. Topic labels alone do not count. | Must-have | ✅ | ✅ | ✅ | ✅ |

**Notes:**
- A fails R2 because it keeps private procurement dynamics outside the solution and still tempts the report to over-read public chatter as account behavior.
- A fails R3 and R4 because the report would smuggle private business judgments out of public-discourse proxies.
- B fails R5 because it requires replacing the engine’s core platform abstraction before a useful prototype exists.
- C fails R0 because it becomes a structured memo workshop rather than a true multi-actor scenario system.
- D passes because it keeps MiroFish’s simulation strengths, names a falsifiable private-analysis mechanism, and makes report sources auditable.

**Selected Shape:** `D: Narrative Simulation + Structured Private Analysis`

**Rationale:** D is the only shape that both respects the current engine’s limits and still produces honest comparative scenario behavior. It keeps MiroFish’s current strengths where they are real, does not lie about the procurement gap, and defines a credible v1 that does not wait on a greenfield engine rewrite.

## Current-vs-Required Capability Map

| Workflow Step | Current MiroFish Capability | Selected Mechanism | Product Work Required |
|---------------|-----------------------------|--------------------|-----------------------|
| Ontology generation | `ontology_generator.py` exists but its system prompt is hardcoded for `社交媒体舆论模拟` / social-media public-opinion simulation (`backend/app/services/ontology_generator.py:12,18`) | Override/branch ontology prompt for strategy-lane narrative packs | Moderate |
| Research dossier ingestion | `graph_builder.py` + document pipeline | Reuse current graph build path | Minimal |
| Actor generation | `oasis_profile_generator.py` | Reuse for public-signal cast and interview personas | Moderate prompt/schema adaptation |
| Narrative simulation | `simulation_config_generator.py` + `simulation_runner.py` | Reuse current engine as a public discourse channel only | Moderate — requires `PlatformConfig` semantic reframing (`viral_threshold`, `echo_chamber_strength`, recommendation weights) for strategy-lane context. V1 can reuse the `twitter` label while explicitly redefining it as public discourse rather than literal Twitter. |
| Private lane analysis | No native capability today | New structured analysis pass using `report_agent` + lane rubric + internal-input schema | New product surface |
| Comparative report | `report_agent.py` + `zep_tools.py` | Extend to merge narrative outputs + private scorecards + Monte Carlo attachment | Moderate |
| Monte Carlo integration | None in MiroFish | Side-by-side report composition in v1 | Minimal |

## Lane Template Example: Defense / Government Entry

| Slot | Definition |
|------|------------|
| Lane | Defense / Government Entry |
| Public actors | Defense industry analyst; AFWERX/SBIR program manager; L3Harris BD director; Moth+Flame competitor rep; I/ITSEC conference organizer; National Guard training lead |
| Public events | SBIR topic release; I/ITSEC conference cycle; Disasterville press coverage; competitor contract award announcement; SAM.gov registration announcement |
| Private inputs | GJ defense proof point = Disasterville press/credibility; CMMC readiness = none; ITAR registration = none; GSA Schedule = none; dedicated federal BD headcount = 0; Year-1 compliance/BD investment = research-cited `$200K–$400K` |
| Private gates | SAM.gov + CAGE code -> basic federal eligibility; SBIR Phase I win -> Phase II path; CMMC Level 2 -> broader contract eligibility; prime introductions (L3Harris/SAIC/Leidos) -> subcontracting path |
| Research-cited outputs | Time-to-cash source = consolidated report `Year 1: $450K–$750K federal`; durability source = 18–36 month defense program framing; required investment source = ITAR/CMMC/GSA/BD cost block |
| Narrative outputs | Emergent objections, positioning resonance, competitor framing, partner-signaling patterns, synthetic interviews |
| Final outputs | Narrative plausibility findings; cited private scorecard; synthetic stakeholder interviews; failure mode inventory; Monte Carlo attachment = `not primary for this lane` unless linked later |

## Detail D: Breadboard

### UI Affordances

| Place | Affordance | Type | Wires Out |
|-------|------------|------|-----------|
| Research workspace | Canonical corpus picker / uploaded source set | Input | → Graph build, Private analysis |
| Lane template editor | Per-lane template fields: public actors, public events, private inputs, private gates, metric sources | Form | → Template store |
| Narrative run controls | Run a lane’s narrative pack with a discourse-tuning preset | Action | → Narrative simulation |
| Interview panel | Interview generated public-layer stakeholders after a run | Interaction | → Interview notes, Report builder |
| Comparative strategy report | Side-by-side lane cards with source-labeled metrics and citations | Display | ← Report builder |
| Capability map panel | Current vs required adaptation table | Display | ← Capability gap map |

### Non-UI Affordances

| Place | Affordance | Type | Wires Out |
|-------|------------|------|-----------|
| Corpus | Zep graph build from canonical research corpus | Service | → Template suggestions, Narrative pack adapter, Private analysis |
| Template store | `LaneTemplate` schema `{lane_id, public_actors, public_events, private_inputs, private_gates, rubric, metric_sources}` | Data | → Narrative pack adapter, Private analysis, Report builder |
| Ontology | Strategy-ontology prompt override for narrative packs | Transform | → Graph build, Profile generation |
| Narrative layer | `NarrativePackAdapter` maps a lane template into current simulation config plus discourse-tuned `PlatformConfig` | Transform | → Simulation runner |
| Narrative layer | Narrative simulation runner produces logs, emergent interactions, and interviewable agents | Service | → Interview panel, Report builder |
| Private analysis | `LaneRubric` schema for committee, gate, capability, investment, and failure-mode evaluation | Data | → Private analysis pass |
| Private analysis | Structured private analysis pass (`report_agent` + lane rubric + citations + internal inputs) | Service | → Report builder |
| Reporting | `MetricSourceMap` declaring source per dimension | Data | → Report builder |
| Reporting | Monte Carlo attachment loader | Service | → Report builder |
| Reporting | Capability gap map generator | Service | → Capability map panel, Report builder |
| Reporting | Comparative strategy report builder merging narrative outputs, private scorecards, citations, and Monte Carlo attachment | Service | → Comparative strategy report |

### Wiring

```text
Canonical corpus
  -> Graph build
  -> Template suggestions
  -> Private analysis pass

Lane template editor
  -> Template store
  -> Ontology override
  -> Narrative pack adapter
  -> Lane rubric

Ontology override
  -> Graph build
  -> Profile generation

Narrative pack adapter
  -> Narrative simulation runner
  -> Interview panel
  -> Report builder

Lane rubric + internal inputs + canonical corpus
  -> Structured private analysis pass
  -> Report builder

Metric source map + Monte Carlo attachment + capability gap map
  -> Report builder
  -> Comparative strategy report
```

## Decision

Selected shape: **D: Narrative Simulation + Structured Private Analysis**

This shape passed the fit check, survived adversarial review, and now has a concrete breadboard. It is the foundation for planning.
