---
title: "Groove Jones Strategy Lab in MiroFish"
date: 2026-03-18
bead: bd-1cv
---

<!-- Codex Review: APPROVED after 2 rounds | model: gpt-5.4 | date: 2026-03-18 -->
<!-- Status: UNCHANGED -->
<!-- Revisions: none -->
<!-- issue:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-18T20:32:19Z -->

# Groove Jones Strategy Lab in MiroFish

## Problem

Groove Jones has two linked planning problems:

1. The immediate cash problem: the 30-day action plan identifies near-term revenue opportunities through maintenance, expansion, and warm introductions.
2. The structural path problem: the consolidated 2026 market-intelligence research shows Groove Jones is overexposed to shrinking brand-activation work and under-positioned in adjacent growth lanes such as healthcare/pharma training, defense/government, spatial enterprise, and selective partner-driven work.

The research is strong on diagnosis, but static. Groove Jones needs a decision aid that can compare strategic lanes without pretending that today’s MiroFish engine already models private procurement dynamics.

## Shaping Outcome

This spec is aligned to [shaping-transcript.md](/Users/dalecarman/Groove%20Jones%20Dropbox/Dale%20Carman/Projects/dev/MiroFish/specs/002-groove-jones-strategy-lab/shaping-transcript.md).

The selected shape is:

**Narrative Simulation + Structured Private Analysis**

V1 is explicitly two-layered:

1. **Narrative simulation layer**
   Reuse the current MiroFish engine only as a public-discourse and narrative-stress-testing system. It produces emergent interactions, framing pressure, competitor/partner signaling, and synthetic stakeholder interviews. It is explicitly **not** procurement prediction.
2. **Structured private analysis layer**
   Add a `report_agent`-style structured LLM synthesis pass over the research corpus plus lane-specific internal inputs. This produces cited lane scorecards for buying committees, procurement/compliance gates, capability load, investment needs, and failure modes. It is **not** a second simulation engine.

For v1, Monte Carlo integration is **side-by-side report composition**, not a deep behavioral coupling.

## Why This Shape

- It preserves the one thing MiroFish already does well for this problem: synthetic agents, emergent narrative behavior, and post-run interviews.
- It does not over-claim that Twitter/Reddit mechanics equal boardroom procurement.
- It creates a useful prototype path without forcing a full simulation-engine rewrite before anything can ship.
- It keeps every report dimension auditable by requiring an explicit source label.

## Strategic Lanes

The MVP must compare at least these five lanes:

| Lane | Why It Matters |
|------|----------------|
| Existing-client maintenance + expansion | Fastest path to cash and strongest win-rate evidence |
| Healthcare/pharma training growth | Strong enterprise XR activity with existing Groove Jones credibility |
| Defense/government entry | Strong long-duration upside with high compliance and BD friction |
| Spatial computing enterprise deployments | Strong fit with Apple Vision Pro and premium differentiation |
| Selective events / agency-partner work | Useful cash-flow channel, but must be filtered away from commoditized work |

## Requirements

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

## Selected Shape

| Part | Mechanism |
|------|-----------|
| D1 | Current MiroFish engine runs lane-specific narrative simulation packs only. The output is limited to framing pressure, competitor/partner signaling, emergent objections, and synthetic stakeholder interviews. It is explicitly not procurement prediction. |
| D2 | Private analysis layer = `report_agent`-driven structured LLM synthesis pass over the research corpus plus lane-specific internal inputs. Each lane uses a rubric covering committee roles, procurement/compliance gates, capability load, investment needs, and failure branches. Output is a cited lane scorecard, not a second simulation engine. |
| D3 | Every lane must declare a template before any run: public actors, public events, private inputs, private gates, required citations, expected outputs. |
| D4 | Comparative report merges D1 narrative outputs, D2 private scorecards, and explicit Monte Carlo attachments, with source labels per metric. |

## Lane Template Contract

Each lane template must define:

- Public actors
- Public events
- Private inputs
- Private gates
- Required citations
- Expected narrative outputs
- Expected final outputs

Canonical example: **Defense / Government Entry**

| Slot | Definition |
|------|------------|
| Public actors | Defense industry analyst; AFWERX/SBIR program manager; L3Harris BD director; Moth+Flame competitor rep; I/ITSEC conference organizer; National Guard training lead |
| Public events | SBIR topic release; I/ITSEC conference cycle; Disasterville press coverage; competitor contract award announcement; SAM.gov registration announcement |
| Private inputs | GJ defense proof point = Disasterville press/credibility; CMMC readiness = none; ITAR registration = none; GSA Schedule = none; dedicated federal BD headcount = 0; Year-1 compliance/BD investment = research-cited `$200K–$400K` |
| Private gates | SAM.gov + CAGE code -> basic federal eligibility; SBIR Phase I win -> Phase II path; CMMC Level 2 -> broader contract eligibility; prime introductions (L3Harris/SAIC/Leidos) -> subcontracting path |
| Research-cited outputs | Time-to-cash source = consolidated report `Year 1: $450K–$750K federal`; durability source = 18–36 month defense program framing; required investment source = ITAR/CMMC/GSA/BD cost block |
| Final outputs | Narrative plausibility findings; cited private scorecard; synthetic stakeholder interviews; failure mode inventory; Monte Carlo attachment = `not primary for this lane` unless linked later |

## Current vs Required Capability Map

| Workflow Step | Current MiroFish Capability | Selected Mechanism | Product Work Required |
|---------------|-----------------------------|--------------------|-----------------------|
| Ontology generation | `ontology_generator.py` exists but its system prompt is hardcoded for social-media public-opinion simulation | Override or branch the ontology prompt for strategy-lane narrative packs | Moderate |
| Research dossier ingestion | `graph_builder.py` + document pipeline | Reuse current graph build path | Minimal |
| Actor generation | `oasis_profile_generator.py` | Reuse for public-signal cast and interview personas | Moderate prompt/schema adaptation |
| Narrative simulation | `simulation_config_generator.py` + `simulation_runner.py` | Reuse current engine as a public discourse channel only | Moderate — requires `PlatformConfig` semantic reframing (`viral_threshold`, `echo_chamber_strength`, recommendation weights). V1 can reuse the `twitter` label while redefining it as public discourse, not literal Twitter. |
| Private lane analysis | No native capability today | New structured analysis pass using `report_agent` + lane rubric + internal-input schema | New product surface |
| Comparative report | `report_agent.py` + `zep_tools.py` | Extend to merge narrative outputs + private scorecards + Monte Carlo attachment | Moderate |
| Monte Carlo integration | None in MiroFish | Side-by-side report composition in v1 | Minimal |

## Acceptance Criteria

- A reader can explain the selected shape in one pass: narrative simulation for public discourse plus structured private analysis for procurement and capability gating.
- The spec names at least five strategic lanes and requires each to become a concrete lane template, not just a topic label.
- The narrative layer is explicitly described as public-discourse and narrative stress-testing, not procurement prediction.
- The private analysis layer is explicitly defined as a `report_agent`-style structured synthesis pass with named outputs and citations.
- Every comparative report metric must declare its source from `{narrative simulation | private analysis layer | research citation | Monte Carlo attachment}`.
- The current-vs-required capability map makes it obvious what can be prototyped now and what requires product work.
- V1 Monte Carlo integration is defined as side-by-side report composition when available.
- The defense lane template is concrete enough that a planner can derive implementation work from it without rediscovering the core problem.

## In Scope

- Turning the Groove Jones research package into a MiroFish-ready strategic comparison problem
- Defining the selected two-layer shape for this use case
- Defining the lane template contract and at least one concrete lane example
- Defining how comparative reports are sourced and labeled
- Defining current vs required capability boundaries
- Defining the v1 relationship to the Monte Carlo model

## Out of Scope

- Rewriting the core simulation engine into a full boardroom/procurement simulator for v1
- Treating MiroFish as the sole quantitative forecast engine
- Building a CRM, pipeline manager, or federal contracting operations system inside MiroFish
- Implementing SAM.gov, ITAR, CMMC, or GSA workflows directly in MiroFish
- Replacing human business development, sales judgment, or executive decision-making
- Designing the final UI in full fidelity; the breadboard in `shaping-transcript.md` is the current source of truth for affordances
