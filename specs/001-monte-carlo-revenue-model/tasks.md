---
title: "Tasks — Monte Carlo Revenue Scenario Model"
date: 2026-03-18
bead: bd-385
---

<!-- Codex Review: APPROVED after 3 rounds | model: codex/gpt-5.4 | date: 2026-03-18 -->
<!-- Status: RECONCILED — added T0.5 gitignore, effort_hours in T1, min_conversions in T5, R2.3 fallback in T2, call_id traceability, requirements.txt in T0.5 -->
<!-- plan:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T19:20:42Z -->

# Tasks: Monte Carlo Revenue Scenario Model

## Prerequisites

- [x] **T0: Get burn rate from Dale** — **$397,456/month** (QuickBooks snapshot, March 17, 2026). ✅ Resolved.
- [ ] **T0.5: Data governance + reproducibility setup**
  - Add `specs/001-monte-carlo-revenue-model/` to `.gitignore` (entire dir is confidential)
  - Create `specs/001-monte-carlo-revenue-model/requirements.txt` with `numpy>=1.24` and `matplotlib>=3.7`
  - **This task MUST complete before any code is written.**

## Implementation Tasks

All work happens in `specs/001-monte-carlo-revenue-model/simulate.py`.

- [ ] **T1: Write CONFIG section** (~140 lines)
  - 12 revenue call entries using **original 14-call IDs** (gaps at #10, #13), each with:
    - `call_id`, `name`, `pitch`, `tier`
    - `crm_base` (float or null), `crm_category`, `crm_citation` — empirical inputs
    - `crm_override` (for agency: 0.289) — if set, bypasses crm_base
    - `analyst_warmth`, `analyst_warmth_rationale` — judgment inputs
    - `analyst_size_adj`, `analyst_size_rationale` — judgment inputs (0 if none)
    - `p_convert` (computed), `p_convert_method` (human-readable)
    - `value_min`, `value_mode` (default: min + (max−min)/3), `value_max`
    - `close_days_min`, `close_days_max`
    - `client_type`, `batch_count` (default 1; NatGuard=4, Meta Spark=4), `batch_note`
    - `effort_hours` (analyst estimate: prep + call + follow-up + proposal)
  - `EXCLUDED_CALLS` list: call_id #10 (HSBC/IBM) and #13 (Publicis) with reasons
  - `BASELINE_P = 0.40` (R2.3 no-match fallback)
  - `BURN_RATE = 397_456` (QuickBooks, 2026-03-17)
  - `N_SIMULATIONS = 10_000`
  - `CALIBRATION_TARGET = (200_000, 500_000)`
  - `SCENARIOS` dict: `"no_jj"` (call #2 → p=0), `"maintenance_blitz"` (calls #1,2,5,7 → p=0.73)
  - Script header: `# CONFIDENTIAL`, Python 3.11+, deps, invocation
  - **Verify:** 12 entries. call_ids match spec. batch_count=4 for #12, #14. p_convert matches plan table.

- [ ] **T2: Write Engine** (~40 lines)
  - `run_simulation(calls, n, seed=42)` → numpy array
    - Expand calls with batch_count > 1 into repeated trial entries (total: 18)
    - p_convert computation with R2.3 fallback: `crm_override → crm_base × warmth + size_adj → BASELINE_P`
    - Clamp: `p = max(0.0, min(1.0, p))`
    - Per trial: Bernoulli(p), triangular(min, mode, max), uniform(close_min, close_max)
    - Scenario override: deep-copy calls, merge scenario params, then run
  - **Verify:** n=100, output shape (100, 18, 3). All values ≥ 0. Won values are 0 or 1.
  - **Depends on:** T1

- [ ] **T3: Write Results** (~25 lines)
  - `aggregate(raw, [30, 60, 90])` → {30: array(n), 60: array(n), 90: array(n)}
  - `percentiles(agg, [10, 25, 50, 75, 90])` → nested dict
  - **Verify:** agg_90 ≥ agg_60 ≥ agg_30 (monotonic). P90 > P50 > P10.
  - **Depends on:** T2

- [ ] **T4: Write Survival** (~15 lines)
  - `survival_curve({30: agg30, 60: agg60, 90: agg90}, burn_rate)` → survival data
  - P(survive 1mo) = frac(agg_30 ≥ 1×burn). P(2mo) = frac(agg_60 ≥ 2×burn). P(3mo) = frac(agg_90 ≥ 3×burn).
  - **Verify:** P(survive) = 1.0 when burn = 0. Monotonically decreasing with months.
  - **Depends on:** T3

- [ ] **T5: Write EV + Min Conversions** (~30 lines)
  - `ev_ranking(calls)` → sorted by total EV and by EV/hour
    - EV = p_convert × E[triangular] × batch_count
    - EV/hour = EV / effort_hours
  - `min_conversions_to_survive(raw, burn_rate, horizon)` → min K where cumulative P(survive | ≥K wins) > 50%
    - Use cumulative bins (≥K), not exact-K, for stability
  - **Verify:** Sum EVs > 0. Batch calls have multiplied EV. Min K is between 1 and 18.
  - **Depends on:** T2

- [ ] **T6: Write Sensitivity/Tornado** (~45 lines)
  - `tornado(calls, n)` → list of (call_name, param, direction, delta_median)
    - p_convert ±10pp (clamped) AND value_mode ±30%
    - 48 total runs. Sort by |delta| descending.
  - **Verify:** All 48 complete. +p → higher median. −p → lower. No NaN/inf.
  - **Depends on:** T2

- [ ] **T7: Write Calibration** (~15 lines)
  - `calibrate(p25, p75, 200_000, 500_000)` → {status, details}
  - Pass if overlap. Warn if P25 < 140K or P75 > 650K. Fail if no overlap.
  - **Depends on:** T3

- [ ] **T8: Write Charts** (~80 lines)
  - `plot_distributions(agg)` → distributions.png (3 histograms, P25/P50/P75 lines)
  - `plot_survival(surv)` → survival.png (with burn rate markers)
  - `plot_tornado(tornado_data)` → tornado.png (color-coded p_convert vs value_mode)
  - `plot_ev(ev_data)` → ev_ranking.png (grouped by total EV and EV/hour)
  - **Depends on:** T3, T4, T5, T6

- [ ] **T9: Write Narrator** (~70 lines)
  - `write_narrative(...)` → narrative.md with `⚠️ CONFIDENTIAL` header
  - Sections: Executive Summary, Key Numbers, Survival Outlook (with placeholder warning if applicable), Where to Focus (EV/hour), Minimum Conversions, What Matters Most (tornado top 3), What-If Scenarios, Calibration Note, Methodology Note, Excluded Calls
  - **Depends on:** T3, T4, T5, T6, T7

- [ ] **T10: Write Main** (~35 lines)
  - CLI: `--scenario`, `--output-dir` (default output/), `--n-simulations`, `--burn-rate`, `--seed`
  - Print ⚠️ if burn_rate not overridden
  - Run: base sim → aggregate → percentiles → survival → EV → min_conversions → tornado → calibration → charts → narrative → raw JSON
  - **Depends on:** All above

## Integration Verification

- [ ] **T11: Full integration test**
  - Run: `python simulate.py --output-dir output/`
  - Verify 6 output files exist and non-empty
  - Run with `--scenario no_jj`
  - Edge: set one call p=0.98, run tornado — verify no crash (clamping)
  - Verify: 10K sims in <10 seconds
  - Spot-check narrative.md: calibration reported, excluded calls listed, CONFIDENTIAL banner present
  - **Depends on:** T10

## Dependency Graph

```
T0 (burn rate — async)
T0.5 (gitignore + requirements.txt — FIRST)
  ↓
T1 (config)
  ↓
T2 (engine)
  ↓
T3 (results) ─── T4 (survival)
 │                 │
 ├── T5 (EV + min_conversions)
 ├── T6 (tornado)
 ├── T7 (calibration)
 │                 │
 └───── T8 (charts) ←──┘
          │
          T9 (narrator)
          │
          T10 (main)
          │
          T11 (integration test)
```
