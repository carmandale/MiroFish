---
shaping: true
---

<!-- shape:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T18:34:52Z -->

# Monte Carlo Revenue Scenario Model — Shaping

**Participants:** QuickUnion (pi/claude-opus-4-6, proposer) × TrueMoon (crew-challenger, adversary)
**Date:** 2026-03-18
**Spec:** specs/001-monte-carlo-revenue-model/spec.md
**Bead:** bd-385

---

## Source

The 30-Day Revenue Action Plan for Groove Jones — a triage plan identifying 14 priority sales calls derived from 26 research documents and CRM analysis of 1,902 deals. Groove Jones has $19K cash and zero months runway. The plan provides qualitative prioritization but lacks quantified probability distributions.

Source documents in `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/`:
- `Groove_Jones_30Day_Revenue_Action_Plan.docx` — the 14-call action plan
- `research-brief.md` — CRM cancellation analysis (death rates by product, size, client type)
- `Groove Jones Market Intelligence Brief 01.md` — external market data
- `external-market-research.md` — market sizing and competitive landscape

---

## Problem

The action plan says "call Toyota, estimated $25K–$150K" but doesn't answer:
- What's the probability of closing ≥$100K in 30 days?
- Which calls give the highest risk-adjusted expected value?
- What's the minimum conversion count to survive 60 days?
- How sensitive is the outcome to one large deal falling through?

This is a decision-under-uncertainty problem. Monte Carlo simulation models it well.

## Outcome

A Python CLI tool that runs 10K Monte Carlo scenarios over the 14-call action plan and produces probability distributions, survival curves, sensitivity analysis, and a plain-language narrative for the CEO.

---

## Critical Data Corrections (from TrueMoon's adversarial review)

### 1. The 14-Call Table Was Wrong

The original spec's calls 8–14 did not match the actual action plan document (Table 9). Princess Cruises, Pfizer, Stryker, and Medtronic were hallucinated from body text mentions — they are NOT in the official 14-call summary table.

**Corrected 14 calls (from docx Table 9):**

| # | Who | What to Pitch | Est. Value | Time to Close |
|---|-----|--------------|-----------|---------------|
| 1 | Toyota | Maintenance + 2027 WebGL refresh | $25K–$150K | 2–4 weeks |
| 2 | J&J MedTech | Maintenance + Stryker intro | $17K–$400K | 2–6 weeks |
| 3 | Be Pro Be Proud | New state expansion | $100K–$200K | 3–6 weeks |
| 4 | Ideal Industries | New VR safety module | $100K–$200K | 3–6 weeks |
| 5 | Amgen | visionOS update + maintenance | $17K–$75K | 2–4 weeks |
| 6 | Spirit Halloween | 2026 FOOH campaign | $80K–$150K | 3–8 weeks |
| 7 | Angelo State | Curriculum update + new labs | $17K–$50K | 2–4 weeks |
| 8 | Invesco/160over90 | Fall activation scoping | $100K–$300K | 4–8 weeks |
| 9 | Salesforce | Dreamforce 2026 activation | $100K–$300K | 4–8 weeks |
| 10 | HSBC/IBM | Referrals to financial services | Referral value | 2–3 weeks |
| 11 | Cosm (Dallas) | Immersive venue content | $50K–$200K | 4–8 weeks |
| 12 | 3–5 NatGuard PAOs | Modified Disasterville | $25K–$100K ea. | 4–8 weeks |
| 13 | Publicis Sapient | Preferred vendor application | Pipeline access | 60–90 days |
| 14 | Meta Spark orphans | WebAR rebuilds (batch of 20) | $30K–$75K ea. | 4–8 weeks |

### 2. Value Range Corrections

| Call | Spec Had | Actual (Table 9) |
|------|----------|-----------------|
| Amgen (#5) | $17K–$150K | $17K–$75K |
| Angelo State (#7) | $50K–$100K | $17K–$50K |

### 3. Maintenance Win Rate Discrepancy

- CRM data: Died=25, Won=95 → death rate 20.8%, win rate **79.2%**
- Action plan header says "73% win rate" — likely uses larger denominator including open/other-status deals
- Decision: use conservative 73% from action plan; document both figures

### 4. Non-Revenue Calls

Calls #10 (HSBC/IBM: "Referral value") and #13 (Publicis Sapient: "Pipeline access") are not dollar-value Bernoulli trials. They are pipeline-building activities excluded from dollar simulation.

### 5. Call #8 Is an Agency Deal

Invesco/160over90 is the only agency-sourced call in the 14. Agency death rate is 71.1% vs 59.7% for direct. Flagged in model inputs.

---

## Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| **R0** | **Produce probability distributions for total revenue at 30, 60, and 90 days from the 14-call action plan** | Core goal |
| **R1** | **Per-call parameterization** | Must-have |
| R1.1 | Revenue calls (12 of 14): conversion probability, value distribution (triangular), time-to-close (uniform, from action plan's subjective tier estimates — NOT CRM-derived) | Must-have |
| R1.2 | Non-revenue calls (#10 HSBC/IBM, #13 Publicis Sapient): excluded from dollar simulation, documented in report | Must-have |
| R1.3 | Bimodal calls (~4 calls where max/min > 5× and pitch contains distinct components): MAY use multi-outcome with independent sub-outcomes. Sub-outcome parameters are analyst estimates, documented as such. | Nice-to-have |
| **R2** | **Conversion probabilities: CRM-derived with fallback hierarchy** | Must-have |
| R2.1 | CRM product×size×client match → use direct rate | Must-have |
| R2.2 | Partial match → closest category + documented assumption | Must-have |
| R2.3 | No match → 30–50% baseline from action plan | Must-have |
| R2.4 | Call #8 (Invesco/160over90) flagged as agency deal (71.1% death rate) | Must-have |
| **R3** | **Per-call expected value ranking for effort prioritization** | Must-have |
| **R4** | **Sensitivity analysis: tornado chart identifying top assumptions that swing 30-day median revenue most. Vary both p_convert ±10pp AND value_mode ±30% per call.** | Must-have |
| **R5** | **At least 2 conditional what-if scenarios configurable without code changes (config-driven)** | Must-have |
| **R6** | **All input parameters in a single editable config dict/YAML at top of script** | Must-have |
| **R7** | **Plain-language CEO narrative (markdown file)** | Must-have |
| **R8** | **Monthly burn rate as configurable input (default TBD — requires user input). Used to compute survival probability: P(revenue_Nd ≥ ceil(N/30) × burn_rate)** | Must-have |
| **R9** | **Calibration check: model's base-case 30-day P25–P75 should approximately overlap with action plan's $200K–$500K estimate. Flag if outside ±30%.** | Must-have |

**9 top-level requirements. Within chunking limit.**

---

## Shapes Explored

### Shape A: Flat Monte Carlo — Independent Trials (SELECTED)

All 12 revenue calls modeled as independent Bernoulli trials. Non-revenue calls excluded. Simple: one config dict, one loop, numpy vectorized.

| Part | Mechanism |
|------|-----------|
| **A1** | Config dict: 12 revenue calls × {p_convert, p_convert_method, value_min, value_mode, value_max, close_days_min, close_days_max, product_type, client_type, crm_citation} + burn_rate + n_simulations |
| **A2** | Calls #10 (HSBC/IBM) and #13 (Publicis) excluded — noted in output report |
| **A3** | For each of 10K iterations: Bernoulli(p) per call → if won, triangular(min, mode, max) for value, uniform(min, max) for close_days |
| **A4** | Aggregate: cumulative revenue at day 30, 60, 90. Percentile table (P10/P25/P50/P75/P90). |
| **A5** | Survival curve: wire aggregated_30, aggregated_60, aggregated_90 into survival. P(revenue_30d ≥ 1×burn), P(revenue_60d ≥ 2×burn), P(revenue_90d ≥ 3×burn). |
| **A6** | Per-call EV: p_convert × E[triangular]. Sort descending. |
| **A7** | Tornado: vary each call's p_convert ±10pp AND value_mode ±30%. 12 calls × 2 params × 2 directions = 48 runs. |
| **A8** | What-if scenarios in config: named parameter overrides (e.g., "no_jj": {call_2: {p_convert: 0}}) |
| **A9** | Calibration: compare base-case P25/P75 at 30 days against $200K/$500K. Flag if outside ±30%. |
| **A10** | Output: matplotlib PNGs + narrative.md + raw_results.json |

### Shape B: Staged Pipeline — Tier-Based with Dependencies (KILLED)

Models 5 tiers as sequential stages with dependency DAG.

**Why killed:** GJ is making all calls simultaneously regardless of tier outcomes. Tier dependencies are speculative — no calibration data exists for boost factors. B3's "probability of opening N pipeline opportunities" from referral calls is completely uncalibrated. Adds complexity without data to back it.

### Shape C: Spreadsheet Decision Model — No Simulation (ELIMINATED)

Deterministic expected-value calculation. No distributions, no percentiles, no time dimension.

**Why eliminated:** Fails core goal (R0) — no probability distributions. Also fails R1 (no distributions), R4 (no simulation-driven sensitivity), R5 (no what-if scenarios). Useful as a sanity check on the simulation, not as the deliverable.

---

## Fit Check

| Req | Requirement | Status | A | C |
|-----|-------------|--------|---|---|
| R0 | Probability distributions at 30/60/90 days | Core goal | ✅ | ❌ |
| R1 | Per-call parameterization (value dist, time-to-close, non-revenue exclusion, bimodal) | Must-have | ✅ | ❌ |
| R2 | CRM-derived probabilities with fallback hierarchy | Must-have | ✅ | ✅ |
| R3 | Per-call EV ranking | Must-have | ✅ | ✅ |
| R4 | Sensitivity/tornado (p_convert ±10pp AND value_mode ±30%) | Must-have | ✅ | ❌ |
| R5 | Config-driven what-if scenarios | Must-have | ✅ | ❌ |
| R6 | Single editable config | Must-have | ✅ | ✅ |
| R7 | CEO narrative | Must-have | ✅ | ✅ |
| R8 | Burn rate for survival curve | Must-have | ✅ | ✅ |
| R9 | Calibration check against $200K–$500K | Must-have | ✅ | ✅ |

**Notes:**
- C fails R0: no probability distributions (core goal disqualifier)
- C fails R1: no distributions, no time-to-close
- C fails R4, R5: no simulation engine for sensitivity or what-ifs
- A passes all 10 requirements
- Shape B not shown (killed — see rationale above)

**Selection: Shape A** — the only shape that passes the fit check.

---

## Breadboard: Shape A

### UI Affordances (CLI + output files)

| Place | Affordance | Type | Wires Out |
|-------|-----------|------|-----------|
| Config (top of script) | `CALLS` dict: 12 revenue calls with per-call params | Data | → Engine |
| Config | `BURN_RATE` monthly operating cost | Data | → Survival |
| Config | `N_SIMULATIONS` (default 10000) | Data | → Engine |
| Config | `SCENARIOS` dict: named what-if overrides | Data | → Engine |
| Config | `CALIBRATION_TARGET` ($200K, $500K) | Data | → Calibration |
| CLI invocation | `python simulate.py` or `python simulate.py --scenario no_jj` | Action | → Engine |
| Output dir | `distributions.png` — histograms at 30/60/90 days | Display | ← Engine |
| Output dir | `survival.png` — P(revenue ≥ X) curve at 30/60/90 | Display | ← Survival |
| Output dir | `tornado.png` — sensitivity chart (p_convert AND value_mode) | Display | ← Sensitivity |
| Output dir | `ev_ranking.png` — per-call EV bar chart | Display | ← EV |
| Output dir | `narrative.md` — plain-language summary | Display | ← Narrator |
| Output dir | `raw_results.json` — full simulation data | Data | ← Engine |

### Non-UI Affordances

| Place | Affordance | Type | Wires Out |
|-------|-----------|------|-----------|
| **Engine** | `run_simulation(calls, n)` — main Monte Carlo loop | Handler | → Results |
| Engine | Per-call trial: `Bernoulli(p) → if won: triangular(min, mode, max), uniform(close_min, close_max)` | Logic | — |
| Engine | Scenario override: merge scenario params into base calls before run | Logic | — |
| **Results** | `aggregate(raw, [30, 60, 90])` — cumulative revenue at day thresholds | Transform | → Charts, Survival |
| Results | `percentiles(aggregated, [10, 25, 50, 75, 90])` — percentile table | Transform | → Narrator |
| **Survival** | `survival_curve({30: agg30, 60: agg60, 90: agg90}, burn_rate)` — P(revenue_Nd ≥ ceil(N/30) × burn) | Transform | → Charts |
| **Sensitivity** | `tornado(calls, n, base_median)` — vary p_convert ±10pp AND value_mode ±30% per call (48 runs) | Analysis | → Charts |
| **EV** | `ev_ranking(calls)` — p × E[triangular] per call, sorted | Analysis | → Charts |
| **Calibration** | `calibrate(p25_30d, p75_30d, target_min, target_max)` — check overlap, flag if outside ±30% | Check | → Narrator |
| **Narrator** | `write_narrative(percentiles, ev_rank, tornado_top3, calibration_result, scenarios)` — plain English | Output | → narrative.md |
| **Charts** | `plot_distributions()`, `plot_survival()`, `plot_tornado()`, `plot_ev()` — matplotlib | Output | → PNGs |

### Wiring

```
Config
  ├─ CALLS ──────────────→ Engine.run_simulation()
  ├─ N_SIMULATIONS ──────→ Engine.run_simulation()
  ├─ SCENARIOS ──────────→ Engine (scenario override merge)
  ├─ BURN_RATE ──────────→ Survival.survival_curve()
  └─ CALIBRATION_TARGET ─→ Calibration.calibrate()

Engine
  ├─ raw results ────────→ Results.aggregate([30, 60, 90])
  └─ scenario results ───→ Results.aggregate() (per scenario)

Results
  ├─ aggregated arrays ──→ Charts.plot_distributions()
  ├─ percentile table ───→ Narrator.write_narrative()
  ├─ aggregated_30 ──────→ Survival (1-month: ≥ 1×burn)
  ├─ aggregated_60 ──────→ Survival (2-month: ≥ 2×burn)
  └─ aggregated_90 ──────→ Survival (3-month: ≥ 3×burn)

Survival
  └─ survival data ──────→ Charts.plot_survival()

Sensitivity (48 runs: 12 calls × 2 params × 2 directions)
  └─ tornado deltas ─────→ Charts.plot_tornado()
                          → Narrator (top 3)

EV
  └─ ranked list ────────→ Charts.plot_ev()
                          → Narrator

Calibration
  └─ pass/fail + details → Narrator

Narrator
  └─ narrative.md ───────→ Output dir

Charts
  └─ *.png ──────────────→ Output dir
```

---

## Implementation Notes

1. **p_convert blending rule (must be repeatable and auditable):**
   - Use the most specific CRM rate available (product-type win rate)
   - Adjust for deal size bucket if rate differs significantly
   - Apply documented relationship warmth multiplier (4-year repeat = 1.1×, new direct = 0.7×, agency = use agency death rate)
   - Record the formula as `p_convert_method` string in each call's config

2. **value_mode default:** `min + (max - min) / 3` (conservative skew toward lower end). Overridable per call.

3. **Multi-outcome (R1.3, nice-to-have):** If implemented, a call has `outcomes: [{p, min, mode, max}, ...]` instead of flat params. Each outcome is an independent sub-trial. Not needed for MVP.

4. **Dependencies:** numpy, matplotlib. scipy optional (numpy.random.triangular exists natively).

5. **Total file count:** 1 Python file (`simulate.py`) + output directory.

---

## Open Blocker

**Monthly burn rate must come from Dale.** No source document contains it. The survival curve (R8) is gated on this input. Need a number or range for monthly operating costs.

---

## Conversation Log

### Round 1: TrueMoon's Initial Challenge

**5 concrete problems found:**

1. **CRITICAL: 14-call table wrong.** Calls 8–14 didn't match the actual action plan document. Princess Cruises and Pfizer don't appear anywhere in the docx. Stryker/Medtronic are body-text mentions, not in the 14-call summary table. Verified by programmatic docx parsing.

2. **Value range discrepancies.** Amgen upper bound doubled ($75K → $150K). Angelo State both bounds inflated (min 3×, max 2×). Verified against Table 9.

3. **Maintenance win rate inconsistency.** 73% (action plan prose) vs 79.2% (CRM calculation: 95/(95+25)). Mathematically incompatible — different denominators.

4. **Non-revenue calls break Bernoulli model.** HSBC/IBM ("Referral value") and Publicis ("Pipeline access") can't be sampled from a dollar distribution.

5. **Independence assumption contradicts data.** J&J intro → Stryker/Medtronic dependency (though moot since they're not in the 14 calls).

### Round 2: QuickUnion Revises — Requirements + Shapes Proposed

All 5 corrections applied. Proposed R0–R9 requirements (chunked to 9 top-level). Three shapes: A (flat MC), B (staged pipeline), C (spreadsheet). Initial fit check.

### Round 3: TrueMoon's Second Challenge

**6 issues found:**

1. **Missing burn rate.** Survival curve P(revenue ≥ X) has no anchor without monthly operating cost. → Added R8 (burn rate as configurable input).

2. **Time-to-close has no CRM data.** Zero temporal data in research-brief. Action plan's "2–4 weeks" is subjective. → R1 amended to note subjective source.

3. **R2 partial CRM coverage.** 4 of 12 revenue calls lack clean CRM product-type mappings. Government (NatGuard) has no CRM client-type. Call #8 is agency deal. → R2 amended with fallback hierarchy.

4. **R4 narrow applicability.** Only 4 calls have multi-outcome descriptions. Combined value ranges, not per-sub-outcome. → R4 narrowed to nice-to-have.

5. **Shape B should be killed.** GJ makes all calls simultaneously. Tier dependencies speculative and uncalibrated. → Shape B killed.

6. **Missing calibration requirement.** Action plan says $200K–$500K at 30–50% conversion. Free sanity check. → Added R9.

### Round 4: QuickUnion Revises — Shape A Selected, Breadboard Proposed

All 6 issues addressed. R0–R9 finalized. Shape A selected (only shape passing fit check). Breadboard with UI/Non-UI affordances and wiring diagram.

### Round 5: TrueMoon's Breadboard Challenge

**3 issues found:**

1. **BUG: Survival curve only wired to 30-day data.** Needs aggregated_30/60/90 for proper multi-horizon survival. → Fixed wiring.

2. **CRITICAL: p_convert blending formula undefined.** Example showed 0.52 for Toyota but no reproducible formula. → Defined repeatable blending rule (most-specific CRM rate → size adjustment → warmth multiplier → documented method string).

3. **Tornado only varies p_convert.** value_mode is also an analyst guess. → Expanded to vary both p_convert ±10pp AND value_mode ±30% (48 runs total).

### Round 6: TrueMoon Approves

All issues resolved. Shape A approved with R0–R9. Burn rate from user is the remaining blocker.
