---
shaping: true
---

<!-- shape:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T21:24:32Z -->

# Strategic Path Simulation — Shaping

**Participants:** QuickUnion (pi/claude-opus-4-6, proposer) × RedArrow (crew-challenger, adversary)
**Date:** 2026-03-18
**Spec:** specs/003-strategic-path-simulation/spec.md
**Bead:** bd-2g4

---

## Source

670K words of market intelligence for Groove Jones — an XR agency at $7.1M revenue (declining from $9.2M), $19K cash, $397K/month burn. Research identifies 4 strategic paths: healthcare vertical, defense subcontracting, retainer conversion, phased hybrid. The question: which positioning generates the most market resonance?

---

## Problem

The research tells Dale WHAT the market looks like. It doesn't tell him how the market RESPONDS to different strategic moves. MiroFish can simulate market participant reactions — but its engine (OASIS) simulates Twitter/Reddit social media dynamics, not B2B procurement. Is this mismatch fatal, workable, or irrelevant?

## Outcome

A comparative simulation that reveals which strategic positioning LANGUAGE resonates most in industry discourse — not which market to enter (the research already answers that).

---

## Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| **R0** | Compare 4 strategic positioning scenarios by narrative resonance among simulated XR industry participants | Core goal |
| **R1** | Full 670K words of market intelligence in Zep knowledge graph — no silent truncation | Must-have |
| **R2** | Custom ontology designed for B2B market dynamics (manually crafted, not auto-generated from social media prompt) | Must-have |
| **R3** | Agent personas encode domain context (budget authority, procurement context, competitive position) in text fields — validated on 3 test entities before full run. Escalation: modify system prompt or manually override. | Must-have |
| **R4** | Concrete seed events per scenario (initial posts/announcements that trigger reactions) | Must-have |
| **R5** | Outputs interpreted as narrative resonance (engagement, amplification, competitive reaction) — NOT as procurement intent or market pull | Must-have |
| **R6** | Agent interviews post-simulation with honest caveat: "industry discourse persona, not procurement decision-maker" | Must-have |
| **R7** | Comparative report: engagement, amplification chains, competitive response intensity, sentiment distribution | Must-have |
| **R8** | US business hours, English-language discourse (not Chinese timezone defaults) | Must-have |
| **R9** | Deliverable scoped: helps choose positioning LANGUAGE for outreach, not which market to enter | Must-have |

---

## Shapes Explored

### Shape A: Vanilla MiroFish — Use As-Is (ELIMINATED)

Standard MiroFish pipeline with no customization.

| Part | Mechanism |
|------|-----------|
| A1 | Upload consolidated report via web UI |
| A2 | Auto-generated ontology (social media prompt, 10 types) |
| A3 | Auto-generated agent profiles (MBTI, follower counts) |
| A4 | Standard config (Chinese timezone, default events) |
| A5 | 4 simulation runs |
| A6 | Standard Report Agent |

**Why eliminated:** Fails every requirement. Auto-generated ontology is social-media-biased (R2), truncates to 50K chars for schema design (R1 partial), Chinese timezone (R8), no customization, no validation. Vanilla MiroFish is not fit for B2B market simulation.

### Shape B: Curated MiroFish — Custom Ontology + Enriched Profiles (SELECTED)

MiroFish's pipeline with manually curated key inputs. Full text through graph builder. Custom ontology. Validation gate on profile quality. Honest framing as narrative resonance.

| Part | Mechanism | Flag |
|------|-----------|:----:|
| **B1** | Feed ALL research docs to graph builder (full 670K words, chunked) | |
| **B2** | Manually craft ontology JSON: XRAgency, EnterpriseBuyer, DefenseContractor, HealthcareSystem, IndustryAnalyst, ConferenceOrganizer, PrimeContractor, VCFirm + Person + Organization (10 types) | |
| **B2.5** | Validation: generate 3 test profiles (J&J MedTech, Lockheed Martin, Publicis Sapient). Inspect for procurement-relevant context. If absent: (a) modify `_get_system_prompt()` in `oasis_profile_generator.py` or (b) manually override persona text for key agents. Gates full simulation. | ⚠️ |
| **B3** | Profile generator on graph entities with enrichment — 30+ agents minimum | |
| **B4** | Manually set simulation events: 4 scenario seed posts, US timezone, 20+ rounds | |
| **B5** | 4 simulation runs via web UI | |
| **B6** | Report Agent with custom comparison prompt | |
| **B7** | Agent interviews with caveat in report | |

### Shape C: Outside MiroFish — LLM Role-Play with B2B Actions (PRESERVED AS ESCALATION)

Custom multi-agent simulation reusing MiroFish's data pipeline but with B2B-native action space.

| Part | Mechanism |
|------|-----------|
| C1 | Reuse MiroFish graph builder for knowledge graph |
| C2 | Reuse profile generator for agent personas |
| C3 | Custom simulation loop (no OASIS) |
| C4 | Custom action space: REQUEST_BRIEFING, SHORTLIST_VENDOR, ISSUE_RFI, APPROVE_BUDGET, etc. |
| C5 | Track procurement-like actions per scenario |
| C6 | Summary comparing hypothetical procurement response patterns |

**Why preserved, not selected:** Outputs are closer to the decision Dale needs (procurement vocabulary), but with lower confidence — simulated APPROVE_BUDGET has no empirical grounding. Shape C is the natural escalation path if Shape B results feel too abstract. Requires custom development outside MiroFish.

---

## Fit Check

| Req | Requirement | Status | A | B | C |
|-----|-------------|--------|---|---|---|
| R0 | Compare 4 scenarios by narrative resonance | Core goal | ❌ | ✅ | ✅ |
| R1 | Full 670K words in graph | Must-have | ❌ | ✅ | ✅ |
| R2 | Custom ontology for B2B | Must-have | ❌ | ✅ | ✅ |
| R3 | Personas with domain context (validated) | Must-have | ❌ | ✅ | ✅ |
| R4 | Concrete seed events | Must-have | ❌ | ✅ | ✅ |
| R5 | Outputs = narrative resonance, not procurement | Must-have | ❌ | ✅ | ❌ |
| R6 | Interviews with caveat | Must-have | ❌ | ✅ | ✅ |
| R7 | Comparative report with metrics | Must-have | ❌ | ✅ | ✅ |
| R8 | US hours, English | Must-have | ❌ | ✅ | ✅ |
| R9 | Scoped: positioning language, not market choice | Must-have | ❌ | ✅ | ✅ |

**Notes:**
- A fails all: vanilla MiroFish is not configured for B2B
- B passes 10/10: curated inputs + honest framing
- C fails R5: claims to simulate procurement without procurement data. Outputs are in the right vocabulary but with no empirical grounding. Preserved as escalation.

**Selection: Shape B** — only shape that passes all requirements while remaining honest about limitations.

---

## Critical Adversarial Findings

### Round 1: RedArrow's Initial Challenge (7 findings)

1. **FATAL: Action space** — OASIS only has social media actions (CREATE_POST, LIKE, REPOST). No REQUEST_PROPOSAL, ISSUE_RFI, APPROVE_BUDGET. → Accepted. Narrowed claims to narrative resonance.
2. **FATAL: Ontology prompt hardcoded** for social media opinion simulation. → Accepted. Manual ontology crafting (B2).
3. **SEVERE: Agent profiles are social users** — MBTI, follower_count, no budget authority. → Accepted. Domain context via graph enrichment + validation gate (B2.5).
4. **SEVERE: Seed text truncation** to 50K chars. → Partially accepted. Graph builder processes full text; truncation only affects ontology schema design and config generation prompts, not agent knowledge.
5. **MODERATE: Chinese timezone hardcoded.** → Accepted. Config override (B4).
6. **MODERATE: Stance model too simplistic** for B2B buying committees. → Accepted. Sufficient for narrative resonance (narrowed claim).
7. **WORKABLE: "Public discourse proxy" framing** is dishonest if claims aren't narrowed. → Accepted. R5 + R9 narrow claims explicitly.

### Round 2: RedArrow's Refinement (3 concerns)

A. **R3 unverified** — profile generator system prompt actively steers away from procurement context. → Added validation step B2.5 with escalation path.
B. **Decision value unclear** — research already answers "where to go." → Added R9: simulation answers "how to talk about it," not "where to go."
C. **Shape C dismissed too fast** — its vocabulary is closer to Dale's needs. → Preserved as escalation path.

### Round 3: RedArrow Approves

All concerns addressed. Load-bearing requirements identified: R3 (validation) and R9 (scope). Shape B selected.

---

## Load-Bearing Requirements (from adversary)

**R3 and R9 are the requirements that prevent this from becoming misleading.** If R3 validation fails and nobody escalates, the simulation outputs social-media-flavored noise. If R9's scoping gets lost, Dale interprets narrative resonance as procurement prediction. These must survive into execution.
