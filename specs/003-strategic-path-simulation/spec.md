---
title: "MiroFish Strategic Path Simulation for GJ Market Pivot"
date: 2026-03-18
bead: bd-2g4
shaped: true
---

<!-- Codex Review: APPROVED after 4 rounds (fresh session) | model: codex/gpt-5.4 | date: 2026-03-18 -->
<!-- Status: REVISED — R7 sentiment narrowed to qualitative (no structured metric in OASIS), B6 and acceptance criteria aligned -->
<!-- issue:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T21:49:47Z -->

# MiroFish Strategic Path Simulation

## Problem

Groove Jones has $7.1M revenue (down from $9.2M), $19K cash, $397K/month burn, and 670K words of market intelligence identifying 4 strategic paths forward. The research answers "where to go" — healthcare is growing 38.7%, defense is $14–19B, every XR firm that crossed $15M solved churn via retainers first. What the research can't answer: **which positioning language resonates most with the market when you get there.**

Dale has 50 NatGuard PAO emails to write this week. He needs to know whether to lead with "disaster response training specialist" or "XR production studio that did an Army project." The market intelligence says both are valid strategies. The simulation tests which narrative frame generates the most organic traction.

## What This Delivers (R9 — Load-Bearing Scope)

> **This simulation helps choose positioning LANGUAGE for outreach — it does NOT determine which market to enter.** The market growth data from the research already answers "where to go." The simulation answers "how to talk about it when you get there."

## Selected Shape: B — Curated MiroFish

> Shaped 2026-03-18 by QuickUnion × RedArrow (adversarial). Full transcript: `shaping-transcript.md`

MiroFish's existing pipeline with manually curated key inputs: custom ontology, validated agent profiles, concrete seed events, US timezone. Full 670K words through graph builder. Outputs honestly interpreted as **narrative resonance** — not procurement intent.

**Shapes explored and eliminated:**
- **Shape A (Vanilla MiroFish):** Eliminated — fails every requirement. Auto-generated ontology is social-media-biased, truncates input, uses Chinese timezone, no B2B customization.
- **Shape C (LLM Role-Play with B2B Actions):** Preserved as escalation path — outputs are in procurement vocabulary (REQUEST_BRIEFING, SHORTLIST_VENDOR, ISSUE_RFI) but with no empirical grounding. Build this if Shape B results feel too abstract. Requires custom development.

---

## The B2B / Social Media Mismatch (Honestly Stated)

MiroFish simulates Twitter/Reddit social media interactions via the OASIS engine. Enterprise B2B procurement happens in boardrooms, not on social media.

**What this MEANS (from adversarial review of actual code):**
- **Action space is limited:** OASIS agents can only CREATE_POST, LIKE, REPOST, COMMENT, FOLLOW, DO_NOTHING. No REQUEST_PROPOSAL, ISSUE_RFI, or APPROVE_BUDGET. (`config.py` lines 47-55)
- **Ontology prompt is social-media-focused:** System prompt says "design entity types suitable for social media opinion simulation." (`ontology_generator.py` line 8) → We bypass this with manual ontology.
- **Agent profiles default to social metrics:** MBTI, follower_count, karma — not budget authority or procurement power. (`oasis_profile_generator.py` lines 22-50) → Domain context injected via graph enrichment, validated before full run.

**What this IS still good for:** Narrative resonance. Which positioning statement generates the most organic discussion, amplification, and competitive reaction among simulated industry participants. This maps to LinkedIn/conference/industry-press dynamics — which IS how B2B buyers signal intent.

**What this CANNOT reveal:** Actual procurement timelines, contract values, internal budget approvals, buying committee dynamics. Those remain the Monte Carlo model's domain (spec 001).

---

## Scenarios to Simulate

### Scenario A: Healthcare Vertical Specialization
**Seed event:** "Groove Jones announces dedicated Healthcare XR Practice, anchored by J&J MedTech surgical training ($907K) and AHA CPR VR (Auggie Award). Targeting pharma Medical Affairs teams for ASCO congress activations."

### Scenario B: Defense Pivot via Disasterville
**Seed event:** "Groove Jones wins Army SBIR Phase I ($250K) for expanded Disasterville disaster response training. Registers on SAM.gov. Hires defense BD lead. Targets 10 state National Guard units."

### Scenario C: Retainer-First Revenue Model
**Seed event:** "Groove Jones launches Annual Platform Support program, converting project relationships to monthly retainers ($15–40K/month). Toyota, J&J, Spirit Halloween, Ideal Industries sign year-one retainers."

### Scenario D: Phased Hybrid
**Seed event:** "Groove Jones simultaneously launches retainer program (5 clients), submits Army SBIR Phase I, and packages healthcare case studies for ASCO congress outreach. Three-front push with existing proof points."

---

## Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| **R0** | **Compare 4 strategic positioning scenarios by narrative resonance among simulated XR industry participants** | Core goal |
| **R1** | **Full 670K words of market intelligence in Zep knowledge graph — no silent truncation of agent knowledge** | Must-have |
| **R2** | **Custom ontology designed for B2B market dynamics (manually crafted, not auto-generated)** | Must-have |
| **R3** | **Agent personas encode domain context (budget authority, procurement context, competitive position) in text fields — validated on 3 test entities (J&J, Lockheed, Publicis) before full run. Escalation: modify profile generator system prompt or manually override persona text.** | Must-have |
| **R4** | **Concrete seed events per scenario (initial posts/announcements)** | Must-have |
| **R5** | **Outputs interpreted as narrative resonance (engagement, amplification, competitive reaction) — NOT as procurement intent or market pull** | Must-have |
| **R6** | **Agent interviews post-simulation with honest caveat: "industry discourse persona, not procurement decision-maker"** | Must-have |
| **R7** | **Comparative report: engagement volume, amplification ratio, competitive response count, buyer engagement count. Sentiment via ReportAgent qualitative analysis (no structured sentiment data in OASIS).** | Must-have |
| **R8** | **US business hours, English-language discourse** | Must-have |
| **R9** | **Deliverable scoped: helps choose positioning LANGUAGE for outreach, not which market to enter** | Must-have |

---

## Fit Check (Shape B vs. eliminated A and preserved C)

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

- A fails 10/10. B passes 10/10. C fails R5 (claims procurement without data).
- Shape C preserved as escalation — build if B feels too abstract.

---

## Shape B — Parts

| Part | Mechanism | Flag |
|------|-----------|:----:|
| **B1** | Feed ALL research docs to graph builder (full 670K words, chunked). Priority: consolidated report, research-brief, external-market-research. Secondary: q1–q5, market intelligence brief. | |
| **B2** | Manually craft ontology JSON with 10 B2B entity types: XRAgency, EnterpriseBuyer, DefenseContractor, HealthcareSystem, IndustryAnalyst, ConferenceOrganizer, PrimeContractor, VCFirm + Person + Organization. Edge types: COMPETES_WITH, COLLABORATES_WITH, SUPPLIES_TO, EVALUATES, REPORTS_ON, PARTNERS_WITH. | |
| **B2.5** | **Validation gate:** Generate 3 test profiles (J&J MedTech, Lockheed Martin, Publicis Sapient). Inspect for procurement-relevant context. If absent: (a) modify `_get_system_prompt()` in `oasis_profile_generator.py` to include domain instructions, or (b) manually override persona text for key agents. **Gates full simulation commitment.** | ⚠️ |
| **B3** | Profile generator on graph entities with enrichment — 30+ agents spanning: Fortune 500 buyers, competitor agencies, industry analysts, government procurement, conference organizers. | |
| **B4** | Manually set simulation events: 4 scenario seed posts (one per scenario), US business hours timezone config, 20+ rounds per scenario on both Twitter and Reddit. | |
| **B5** | 4 simulation runs via MiroFish web UI, one per scenario. | |
| **B6** | Report Agent with custom comparison prompt: compare engagement volume, amplification ratio, competitive response count, buyer engagement. Sentiment via ReportAgent qualitative analysis across all 4 scenarios. | |
| **B7** | Agent interviews with caveat in every report: "These represent industry discourse personas, not procurement decision-makers." | |

---

## Acceptance Criteria

- [ ] Market intelligence docs ingested into Zep graph (at minimum: consolidated report + research-brief + external-market-research — full text, not truncated)
- [ ] Custom ontology JSON with 10 B2B entity types created and loaded
- [ ] B2.5 validation: 3 test profiles inspected for procurement-relevant context. Pass/fail documented. If fail, escalation executed.
- [ ] 30+ agent personas generated spanning buyers, competitors, analysts, government
- [ ] 4 scenario simulations run with 20+ rounds each
- [ ] Comparative report with metrics: engagement volume, amplification ratio, competitive response count, buyer engagement. Sentiment via qualitative analysis
- [ ] At least 3 agent interviews conducted post-simulation
- [ ] Every output document states: "narrative resonance measurement, not procurement prediction"
- [ ] All simulation configs use US business hours

---

## Constraints

- MiroFish requires: LLM API key (OpenAI-compatible), Zep Cloud API key
- API cost: ~4,800+ LLM calls across 4 simulations. Start with 10-round test run to validate before full 20+ round runs.
- MiroFish accepts: PDF, MD, TXT files for seed text. The .docx files need conversion to MD/TXT first.
- The ontology generator's 50K char truncation affects schema DESIGN only — the graph builder processes full text in chunks. Agent knowledge is not truncated.

## Load-Bearing Requirements (from adversary)

**R3 and R9 must survive from spec into execution.** If R3 validation fails and nobody escalates, the output is social-media noise. If R9's scope gets lost, Dale interprets narrative resonance as procurement prediction. These are the requirements that prevent this from becoming actively misleading.

## Relationship to Other Specs

| Spec | What it answers | Horizon |
|------|----------------|---------|
| 001 (Monte Carlo) | Financial probabilities for 14-call triage | 30/60/90 days |
| **003 (This)** | **Which positioning language resonates in market discourse** | **6–18 months** |

They're complementary. The Monte Carlo tells you if the 14 calls buy enough time. This simulation tells you how to position yourself during that time.

## Source Materials

All in `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/`:

| File | Priority | Content |
|------|----------|---------|
| `Groove_Jones_Consolidated_Market_Intelligence_2026.docx` | Primary | Full consolidated report — all sections |
| `research-brief.md` | Primary | CRM pipeline analysis |
| `external-market-research.md` | Primary | Market sizing, 27 F500 spenders, competitors |
| `Groove Jones Market Intelligence Brief 01.md` | Secondary | Source-cited intelligence (5 questions) |
| `q1–q5_*.md` | Tertiary | Individual research queries |
| `groove-jones-market-intelligence.pplx.md` | Tertiary | Perplexity deep research |
