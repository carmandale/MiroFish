---
title: "Monte Carlo Revenue Scenario Model for 30-Day Action Plan"
date: 2026-03-18
bead: bd-385
shaped: true
---

<!-- Codex Review: APPROVED after 3 rounds | model: codex/gpt-5.4 | date: 2026-03-18 -->
<!-- Status: REVISED — batch expansion (12→18 trials), R2.3 no-match fallback, effort_hours, min_conversions, data governance -->
<!-- issue:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T19:07:43Z -->

# Monte Carlo Revenue Scenario Model

## Problem

Groove Jones has $19K cash and zero months of runway. A 30-day revenue action plan identifies 14 priority sales calls across 5 tiers, derived from 26 research documents and CRM analysis of 1,902 deals. The plan provides qualitative prioritization and estimated value ranges but lacks quantified probability distributions.

The action plan says "call Toyota, estimated $25K–$150K" — but it doesn't answer:

- What's the probability of closing ≥$100K in 30 days?
- Which calls give the highest risk-adjusted expected value per hour of effort?
- What's the minimum conversion count needed to survive 60 days?
- How sensitive is the outcome to one large deal falling through?

This is a decision-under-uncertainty problem that Monte Carlo simulation solves well.

## Selected Shape: A — Flat Monte Carlo with Independent Trials

> Shaped 2026-03-18 by QuickUnion × TrueMoon (adversarial). Full transcript: `shaping-transcript.md`

12 revenue call configs producing 18 effective Bernoulli trials (10 single-trial calls + NatGuard ×4 + Meta Spark ×4). 2 non-revenue calls excluded. Runs 10K scenarios, produces probability distributions at 30/60/90 days, survival curves against burn rate, effort-normalized EV ranking, minimum conversion count analysis, sensitivity analysis, and plain-language CEO narrative.

**Shapes explored and eliminated:**
- **Shape B (Staged Pipeline):** Killed — GJ makes all calls simultaneously regardless of tier outcomes. Tier dependencies were speculative with no calibration data.
- **Shape C (Spreadsheet Decision Model):** Eliminated — fails core goal (R0). No probability distributions, no time dimension, no sensitivity analysis.

---

## The 14 Calls (Corrected — from docx Table 9)

> ⚠️ The original spec's calls 8–14 were wrong — hallucinated from body text mentions, not from the actual summary table. Corrected by adversarial review with programmatic docx verification.

| # | Who | What to Pitch | Est. Value | Time to Close | Call Class |
|---|-----|--------------|-----------|---------------|------------|
| 1 | Toyota | Maintenance + 2027 WebGL refresh | $25K–$150K | 2–4 weeks | Revenue |
| 2 | J&J MedTech | Maintenance + Stryker intro | $17K–$400K | 2–6 weeks | Revenue |
| 3 | Be Pro Be Proud | New state expansion | $100K–$200K | 3–6 weeks | Revenue |
| 4 | Ideal Industries | New VR safety module | $100K–$200K | 3–6 weeks | Revenue |
| 5 | Amgen | visionOS update + maintenance | $17K–$75K | 2–4 weeks | Revenue |
| 6 | Spirit Halloween | 2026 FOOH campaign | $80K–$150K | 3–8 weeks | Revenue |
| 7 | Angelo State | Curriculum update + new labs | $17K–$50K | 2–4 weeks | Revenue |
| 8 | Invesco/160over90 | Fall activation scoping | $100K–$300K | 4–8 weeks | Revenue (Agency) |
| 9 | Salesforce | Dreamforce 2026 activation | $100K–$300K | 4–8 weeks | Revenue |
| 10 | HSBC/IBM | Referrals to financial services | Referral value | 2–3 weeks | **Non-revenue** |
| 11 | Cosm (Dallas) | Immersive venue content | $50K–$200K | 4–8 weeks | Revenue |
| 12 | 3–5 NatGuard PAOs | Modified Disasterville | $25K–$100K ea. | 4–8 weeks | Revenue (batch ×4) |
| 13 | Publicis Sapient | Preferred vendor application | Pipeline access | 60–90 days | **Non-revenue** |
| 14 | Meta Spark orphans | WebAR rebuilds (batch of 20) | $30K–$75K ea. | 4–8 weeks | Revenue (batch ×4) |

**12 revenue call configs → 18 effective Bernoulli trials** (calls #12 and #14 each expand to 4 independent trials per action plan batch counts). **2 non-revenue calls** (#10, #13) excluded from dollar simulation, documented in output report.

---

## CRM Data Available (from `research-brief.md`)

| Parameter | Value | Source |
|-----------|-------|--------|
| Total pipeline deals analyzed | 1,902 | CRM pipeline_id=1 |
| Maintenance death rate | 20.8% (win rate: 79.2% by CRM calc, 73% per action plan) | R3, tagged subset |
| Live Action death rate | 28.6% | R3, tagged subset |
| Web/WebGL death rate | 60.5% | R3, tagged subset |
| VR App/CGI death rate | 67.2% | R3, tagged subset |
| AR Social/WebAR death rate | 74.3% | R3, tagged subset |
| AI/Web App death rate | 85.9% | R3, tagged subset |
| AR App death rate | 91.3% | R3, tagged subset |
| Deals <$50K death rate | 47.8% | R3, valued subset |
| Deals $50–250K death rate | 85.9% | R3, valued subset |
| Deals >$250K death rate | 86.5% | R3, valued subset |
| Agency-sourced death rate | 71.1% | R3, tagged subset |
| Direct brand death rate | 59.7% | R3, tagged subset |

**Maintenance win rate discrepancy:** CRM says 79.2% (95 won / 120 total). Action plan header says 73% — likely uses a larger denominator including open/other-status deals (~130 total). Model uses conservative 73% from the action plan. Both figures documented.

**Time-to-close:** NOT CRM-derived. The action plan's "2–4 weeks" and "4–8 weeks" are subjective tier-level estimates by the plan author. Modeled as uniform distributions with wide bounds.

---

## Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| **R0** | **Produce probability distributions for total revenue at 30, 60, and 90 days from the 14-call action plan** | Core goal |
| **R1** | **Per-call parameterization** | Must-have |
| R1.1 | Revenue calls (12 of 14): conversion probability, value distribution (triangular), time-to-close (uniform, subjective) | Must-have |
| R1.2 | Non-revenue calls (#10 HSBC/IBM, #13 Publicis Sapient): excluded from dollar simulation, documented in report | Must-have |
| R1.3 | Batch calls #12 (NatGuard ×4) and #14 (Meta Spark ×4): modeled as 4 independent trials each, per action plan batch counts | Must-have |
| **R2** | **Conversion probabilities: CRM-derived with fallback hierarchy** | Must-have |
| R2.1 | CRM product×size×client match → use direct rate | Must-have |
| R2.2 | Partial match → closest category + documented assumption | Must-have |
| R2.3 | No match → BASELINE_P = 0.40 (midpoint of action plan's 30–50%) | Must-have |
| R2.4 | Call #8 (Invesco/160over90) flagged as agency deal (71.1% death rate) | Must-have |
| **R3** | **Per-call EV ranking with EV/hour (effort_hours in config)** | Must-have |
| **R4** | **Sensitivity analysis: tornado chart. Vary both p_convert ±10pp AND value_mode ±30% per call (48 runs total).** | Must-have |
| **R5** | **At least 2 conditional what-if scenarios configurable without code changes (config-driven)** | Must-have |
| **R6** | **All input parameters in a single editable config dict/YAML at top of script** | Must-have |
| **R7** | **Plain-language CEO narrative (markdown file)** | Must-have |
| **R8** | **Monthly burn rate = $397,456 (from QuickBooks, March 17 2026). Survival: P(revenue_30d ≥ 1×burn), P(revenue_60d ≥ 2×burn), P(revenue_90d ≥ 3×burn).** | Must-have |
| **R9** | **Calibration check: base-case 30-day P25–P75 should overlap action plan's $200K–$500K estimate. Flag if outside ±30%.** | Must-have |

9 top-level requirements.

---

## Fit Check (Shape A vs. eliminated Shape C)

| Req | Requirement | Status | A | C |
|-----|-------------|--------|---|---|
| R0 | Probability distributions at 30/60/90 days | Core goal | ✅ | ❌ |
| R1 | Per-call parameterization (value dist, time-to-close, non-revenue exclusion) | Must-have | ✅ | ❌ |
| R2 | CRM-derived probabilities with fallback hierarchy | Must-have | ✅ | ✅ |
| R3 | Per-call EV ranking | Must-have | ✅ | ✅ |
| R4 | Sensitivity/tornado (p_convert ±10pp AND value_mode ±30%) | Must-have | ✅ | ❌ |
| R5 | Config-driven what-if scenarios | Must-have | ✅ | ❌ |
| R6 | Single editable config | Must-have | ✅ | ✅ |
| R7 | CEO narrative | Must-have | ✅ | ✅ |
| R8 | Burn rate for survival curve | Must-have | ✅ | ✅ |
| R9 | Calibration check against $200K–$500K | Must-have | ✅ | ✅ |

- C fails R0 (core goal), R1, R4, R5. Disqualified.
- A passes 10/10.

---

## Shape A — Parts

| Part | Mechanism |
|------|-----------|
| **A1** | Config dict: 12 revenue calls × {p_convert, p_convert_method, value_min, value_mode, value_max, close_days_min, close_days_max, product_type, client_type, crm_citation} + burn_rate + n_simulations |
| **A2** | Calls #10 and #13 excluded — noted in output report |
| **A3** | Per iteration: Bernoulli(p) per call → if won, triangular(min, mode, max) for value, uniform(min, max) for close_days |
| **A4** | Aggregate: cumulative revenue at day 30, 60, 90. Percentile table (P10/P25/P50/P75/P90). |
| **A5** | Survival curve: aggregated_30/60/90 → P(revenue_Nd ≥ ceil(N/30) × burn) |
| **A6** | Per-call EV: p_convert × E[triangular(min,mode,max)]. Sort descending. |
| **A7** | Tornado: vary p_convert ±10pp AND value_mode ±30% per call (48 simulation runs) |
| **A8** | What-if scenarios: named config overrides (e.g., "no_jj": {call_2: {p_convert: 0}}) |
| **A9** | Calibration: compare base-case P25/P75 at 30 days against $200K/$500K. Flag if outside ±30%. |
| **A10** | Output: matplotlib PNGs (distributions, survival, tornado, EV ranking) + narrative.md + raw_results.json |

---

## Breadboard

### UI Affordances (CLI + output files)

| Place | Affordance | Type | Wires Out |
|-------|-----------|------|-----------|
| Config | `CALLS` dict: 12 revenue calls with per-call params | Data | → Engine |
| Config | `BURN_RATE` monthly operating cost | Data | → Survival |
| Config | `N_SIMULATIONS` (default 10000) | Data | → Engine |
| Config | `SCENARIOS` dict: named what-if overrides | Data | → Engine |
| Config | `CALIBRATION_TARGET` ($200K, $500K) | Data | → Calibration |
| CLI | `python simulate.py` or `python simulate.py --scenario no_jj` | Action | → Engine |
| Output | `distributions.png` | Display | ← Engine |
| Output | `survival.png` | Display | ← Survival |
| Output | `tornado.png` | Display | ← Sensitivity |
| Output | `ev_ranking.png` | Display | ← EV |
| Output | `narrative.md` | Display | ← Narrator |
| Output | `raw_results.json` | Data | ← Engine |

### Non-UI Affordances

| Place | Affordance | Type | Wires Out |
|-------|-----------|------|-----------|
| **Engine** | `run_simulation(calls, n)` — main Monte Carlo loop | Handler | → Results |
| **Results** | `aggregate(raw, [30, 60, 90])` — cumulative revenue at thresholds | Transform | → Charts, Survival |
| **Results** | `percentiles(aggregated, [10, 25, 50, 75, 90])` | Transform | → Narrator |
| **Survival** | `survival_curve({30: agg30, 60: agg60, 90: agg90}, burn_rate)` | Transform | → Charts |
| **Sensitivity** | `tornado(calls, n, base_median)` — 48 runs | Analysis | → Charts, Narrator |
| **EV** | `ev_ranking(calls)` — p × E[triangular] | Analysis | → Charts, Narrator |
| **Calibration** | `calibrate(p25_30d, p75_30d, target_min, target_max)` | Check | → Narrator |
| **Narrator** | `write_narrative(...)` — plain English | Output | → narrative.md |
| **Charts** | matplotlib plotting functions | Output | → PNGs |

### Wiring

```
Config
  ├─ CALLS ──────────────→ Engine.run_simulation()
  ├─ N_SIMULATIONS ──────→ Engine.run_simulation()
  ├─ SCENARIOS ──────────→ Engine (scenario override merge)
  ├─ BURN_RATE ──────────→ Survival.survival_curve()
  └─ CALIBRATION_TARGET ─→ Calibration.calibrate()

Engine → Results.aggregate([30, 60, 90])

Results
  ├─ aggregated arrays ──→ Charts.plot_distributions()
  ├─ percentile table ───→ Narrator
  ├─ aggregated_30 ──────→ Survival (1-month)
  ├─ aggregated_60 ──────→ Survival (2-month)
  └─ aggregated_90 ──────→ Survival (3-month)

Survival → Charts.plot_survival()
Sensitivity → Charts.plot_tornado() + Narrator (top 3)
EV → Charts.plot_ev() + Narrator
Calibration → Narrator
Narrator → narrative.md
Charts → *.png
```

---

## Implementation Rules

### p_convert Blending (must be repeatable and auditable)

1. Use the most specific CRM product-type win rate available
2. Adjust for deal size bucket if rate differs significantly from product-type rate
3. Apply documented relationship warmth multiplier: 4-year repeat = 1.1×, new direct = 0.7×, agency = use agency death rate directly
4. Record the formula as `p_convert_method` string in each call's config

### value_mode Default

`min + (max - min) / 3` — conservative skew toward lower end. Overridable per call. The action plan provides only min and max; no most-likely value is available.

### Multi-outcome (R1.3, nice-to-have)

Calls with bimodal ranges MAY use `outcomes: [{p, min, mode, max}, ...]` instead of flat params. Each outcome is an independent sub-trial. Not required for MVP — the combined range already captures blended expected value.

---

## Constraints

- Python 3.11+
- Dependencies: numpy, matplotlib. scipy optional (numpy.random.triangular exists natively).
- Single Python file (`simulate.py`) + output directory
- Output directory: `specs/001-monte-carlo-revenue-model/output/`

## Open Blocker

**Monthly burn rate: $397,456/month** (from QuickBooks snapshot, March 17, 2026). Blocker resolved.

## Source Materials

All in `/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/`:

| File | What It Contains |
|------|-----------------|
| `Groove_Jones_30Day_Revenue_Action_Plan.docx` | The 14-call action plan with value ranges (Table 9 is authoritative) |
| `research-brief.md` | CRM-derived cancellation analysis (death rates by product, size, client type) |
| `Groove Jones Market Intelligence Brief 01.md` | External market data with verified sources |
| `external-market-research.md` | Market sizing, competitive landscape, growth strategies |
