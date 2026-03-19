---
title: "Implementation Plan — Monte Carlo Revenue Scenario Model"
date: 2026-03-18
bead: bd-385
---

<!-- Codex Review: APPROVED after 3 rounds | model: codex/gpt-5.4 | date: 2026-03-18 -->
<!-- Status: REVISED — R2.3 fallback, source separation, data governance, EV/hour, min_conversions, call ID traceability, batch as spec-level, reproducibility -->
<!-- Revisions: (1) requirements.txt + seed control, (2) batch expansion as spec-level not hidden, (3) original 14-call IDs preserved, (4) burn rate CLI warning + metadata, (5) crm_base vs analyst separation, (6) effort_hours + min_conversions_to_survive, (7) full spec dir gitignored, (8) R2.3 BASELINE_P=0.40 fallback, (9) spec internal consistency rewrite, (10) cumulative P for min_conversions stability -->
<!-- plan:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T19:20:42Z -->

# Implementation Plan: Monte Carlo Revenue Scenario Model

> Planned 2026-03-18 by QuickUnion × YoungOwl (adversarial). Codex-reviewed 2026-03-18 (3 rounds, gpt-5.4).

## Architecture

**File:** `specs/001-monte-carlo-revenue-model/simulate.py`
**Dependencies:** `specs/001-monte-carlo-revenue-model/requirements.txt` (numpy>=1.24, matplotlib>=3.7)
**Install:** `pip install -r specs/001-monte-carlo-revenue-model/requirements.txt`
**Run:** `python specs/001-monte-carlo-revenue-model/simulate.py`
**Output:** `specs/001-monte-carlo-revenue-model/output/` (gitignored)

### Data Governance (enforced — Codex finding #7)

- `specs/001-monte-carlo-revenue-model/` added to `.gitignore` — the ENTIRE directory is confidential
- `simulate.py` header: `# CONFIDENTIAL — Groove Jones sales intelligence`
- `narrative.md` header: `⚠️ CONFIDENTIAL`
- Task T0.5 applies the .gitignore change BEFORE any code is written

### Reproducibility

- `requirements.txt` with pinned deps
- `np.random.seed(42)` default, overridable via `--seed`
- Python 3.11+ documented in script header

---

## Conversion Probability Methodology

### Source Separation (Codex finding #5)

Each call config explicitly labels empirical vs analyst inputs:

```python
{
    "call_id": 1,                    # Original 14-call numbering
    "name": "Toyota",
    # Empirical (CRM-derived)
    "crm_base": 0.792,              # or null if no CRM match → BASELINE_P
    "crm_category": "Maintenance",
    "crm_citation": "research-brief.md, Maintenance row: 20.8% death",
    # Analyst adjustments (judgment, not data)
    "analyst_warmth": 1.1,
    "analyst_warmth_rationale": "4-year repeat client with $1.1M history",
    "analyst_size_adj": -0.07,
    "analyst_size_rationale": "Expansion portion requires more approval",
    # Computed
    "p_convert": 0.80,
    # Effort
    "effort_hours": 8,
}
```

### Computation Path (includes R2.3 no-match fallback)

```python
BASELINE_P = 0.40  # R2.3: midpoint of action plan's 30–50%

if call.get("crm_override"):
    p = call["crm_override"]                          # Agency override (R2.4)
elif call["crm_base"] is not None:
    p = call["crm_base"] * call["analyst_warmth"]     # CRM + warmth (R2.1/R2.2)
    p += call.get("analyst_size_adj", 0)              # + size adjustment
else:
    p = BASELINE_P                                     # R2.3: no CRM match
p = max(0.0, min(0.85, p))                            # Cap + clamp
```

### p_convert Table (Original 14-Call IDs — Codex finding #3)

| ID | Call | crm_base | CRM Cat | warmth | size_adj | p_convert |
|----|------|----------|---------|--------|----------|-----------|
| 1 | Toyota | 0.792 | Maintenance | 1.1× | −0.07 | **0.80** |
| 2 | J&J MedTech | 0.792 | Maintenance | 1.0× | −0.10 | **0.69** |
| 3 | Be Pro Be Proud | 0.328 | VR App/CGI | 1.1× | — | **0.36** |
| 4 | Ideal Industries | 0.328 | VR App/CGI | 1.1× | — | **0.36** |
| 5 | Amgen | 0.792 | Maintenance | 1.0× | — | **0.79** |
| 6 | Spirit Halloween | 0.395 | Web/WebGL | 1.1× | — | **0.43** |
| 7 | Angelo State | 0.792 | Maintenance | 1.0× | — | **0.79** |
| 8 | Invesco/160over90 | override | Agency | — | — | **0.29** |
| 9 | Salesforce | 0.714 | Live Action | 0.7× | — | **0.50** |
| 11 | Cosm (Dallas) | 0.328 | VR App/CGI | 0.7× | — | **0.23** |
| 12 | NatGuard PAOs | 0.328 | VR App/CGI | 0.5× | — | **0.16** |
| 14 | Meta Spark | 0.257 | WebAR | 0.5× | — | **0.13** |

Gaps at #10 and #13 are intentional (non-revenue calls).

### Batch Calls

- **#12 NatGuard:** 4 independent trials at $25K–$100K each
- **#14 Meta Spark:** 4 independent trials at $30K–$75K each
- Total effective trials per iteration: **18**

---

## Burn Rate (R8 — Codex finding #4)

`BURN_RATE = 397_456` (from QuickBooks snapshot, March 17, 2026). CLI `--burn-rate` override still available. JSON: `burn_rate_source: "quickbooks_2026-03-17"`. No placeholder warning needed — this is the real number.

**Implication:** The action plan's optimistic $500K 30-day revenue barely covers 1.26 months of burn. The $200K low end covers only 0.50 months. The survival curve will show that **even strong conversion rates may not cover operating costs from these 14 calls alone.** This is critical context for the CEO narrative — the 14-call plan buys time but likely does not fully cover the burn.

## Effort-Normalized Ranking (R3 — Codex finding #6)

Config includes `effort_hours` per call. EV ranking outputs both total EV and EV/hour columns.

## Minimum Conversion Count (Codex finding #6)

`min_conversions_to_survive(raw, burn_rate, horizon)`: for each K (1..18), compute cumulative P(survive | ≥K wins) — using cumulative bins, not exact-K, for stability against sparse samples.

## What-If Scenarios (R5)

- `"no_jj"`: Call #2 p_convert = 0
- `"maintenance_blitz"`: Calls #1, #2, #5, #7 p_convert = 0.73

## Requirement → Implementation Traceability

| Req | Implementation |
|-----|---------------|
| R0 | Engine + Results.aggregate([30,60,90]) + Charts |
| R1.1–R1.3 | CONFIG with call_id, batch_count, excluded calls |
| R2.1–R2.4 | crm_base/analyst separation + BASELINE_P fallback + agency override |
| R3 | ev_ranking() with EV/hour (effort_hours) |
| R4 | tornado() — 48 runs (p_convert ±10pp, value_mode ±30%) |
| R5 | SCENARIOS config |
| R6 | CONFIG section at top |
| R7 | write_narrative() with CONFIDENTIAL banner |
| R8 | BURN_RATE + CLI warning + JSON metadata |
| R9 | calibrate() vs $200K/$500K |
| NEW | min_conversions_to_survive() — cumulative P for stability |
| NEW | EV/hour ranking |

## Adversarial Findings Addressed

| Source | Round | Finding | Resolution |
|--------|-------|---------|------------|
| YoungOwl | Plan | 70/30 blend Simpson's paradox | Product-primary + documented adjustments |
| YoungOwl | Plan | Invesco agency override | p=0.289 direct |
| YoungOwl | Plan | Batch calls as single trials | ×4 each, spec-level |
| YoungOwl | Plan | Tornado symmetry test wrong | Direction + completion |
| YoungOwl | Plan | Missing p_convert clamping | max(0, min(1, p)) |
| YoungOwl | Plan | Spirit Halloween phantom category | Web/WebGL 39.5% |
| Codex | R1 | Not reproducible | requirements.txt + seed |
| Codex | R1 | Batch = spec drift | Spec-level, not hidden |
| Codex | R1 | Call ID renumbering | Original 14-call IDs |
| Codex | R1 | Burn rate misrepresented | CLI warning + banner + JSON |
| Codex | R1 | Warmth/size unlabeled | crm_base vs analyst separation |
| Codex | R1 | Missing EV/hour, min conversions | effort_hours + cumulative min_conversions |
| Codex | R1 | Data governance | Full dir gitignored |
| Codex | R2 | Spec internal inconsistency | Canonical model rewritten inline |
| Codex | R2 | R2.3 not implemented | BASELINE_P = 0.40 fallback path |
| Codex | R2 | Gitignore not applied | T0.5 enforces before code |
