---
title: "Planning Transcript — Monte Carlo Revenue Scenario Model"
date: 2026-03-18
bead: bd-385
---

<!-- plan:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T19:20:42Z -->

# Planning Transcript

**Participants:** QuickUnion (pi/claude-opus-4-6, proposer) × YoungOwl (crew-challenger, adversary)
**Date:** 2026-03-18

---

## Round 1: QuickUnion — Research + Initial Plan

### Research Findings
- MiroFish backend uses uv + pyproject.toml (Python ≥3.11). numpy/matplotlib NOT in existing deps.
- Script is standalone — not part of Flask app. No dependency management needed beyond pip install.
- Existing scripts in backend/scripts/ are simulation runners (OASIS), not analysis tools. No patterns to follow.
- Derived p_convert values for all 12 revenue calls using a 70/30 weighted average of product-type and size-bucket CRM win rates, with warmth multipliers.

### Proposed Plan
- Single file architecture: simulate.py (~420 lines)
- 10 sequential tasks: CONFIG → Engine → Results → Survival → EV → Sensitivity → Calibration → Charts → Narrator → Main
- Burn rate placeholder of $150K/month
- 2 what-if scenarios: no_jj, maintenance_blitz

---

## Round 2: YoungOwl — Five Challenges

### Challenge 1: CRITICAL — Call #8 Invesco p_convert Wrong
Spec says "agency = use agency death rate directly" → p_convert should be 0.289, not 0.542. Plan applied warmth multiplier of 1.0× instead of the agency override. 25pp error on highest-value agency deal.

### Challenge 2: CRITICAL — 70/30 Blend Formula Has Simpson's Paradox
The $50–250K size bucket's 14.1% win rate is confounded with product type — it's driven by AR/AI deal failures, not deal size itself. A maintenance renewal to a 4-year client shouldn't be penalized by the bucket average. The 70/30 weights were invented (not from spec or data). Toyota's p_convert was being suppressed by 21.5pp.

### Challenge 3: SIGNIFICANT — Batch Calls #12 and #14 Modeled Wrong
"$25K–$100K ea." means per-unit pricing. NatGuard (3–5 PAOs) and Meta Spark (batch of 20, 3–4 conversions) should be modeled as multiple independent trials, not single trials. $67K EV swing (~3.5× company cash).

### Challenge 4: SIGNIFICANT — Tornado Symmetry Test Is Wrong
Non-linear model (Bernoulli × triangular × time-threshold) produces asymmetric output deltas for symmetric input perturbations. Symmetry assertion would pass for a broken engine. Better test: direction + completion.

### Challenge 5: MINOR — Missing p_convert Clamping
Tornado ±10pp and scenario overrides could push p_convert outside [0, 1]. Need max(0, min(1, p)) after every perturbation.

---

## Round 3: QuickUnion — All Five Fixed

1. **Invesco → 0.289** (agency override, not warmth multiplier)
2. **Killed 70/30 blend** — replaced with product-primary + documented per-call adjustments. Toyota went from 0.656 → 0.80. Much more defensible.
3. **Batch calls → multiple trials** — NatGuard ×4, Meta Spark ×4. batch_count config field. Total effective trials: 18.
4. **Tornado test → direction + completion** — no symmetry assertion.
5. **p_convert clamping added** — one line, defensive.

---

## Round 4: YoungOwl — Approved with One Minor Fix

All five fixes verified. One additional catch: Spirit Halloween cited "3D/VFX" (41.3% win rate) — this category doesn't exist in CRM data. Correct category is Web/WebGL (39.5%). Impact: 2pp adjustment (0.45 → 0.43). Non-blocking.

**Plan approved.** Proceeded to write plan.md + tasks.md.
