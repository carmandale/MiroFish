# Spec 009 Corpus Tiering

> Scope: `~/dev/quickbooks/specs/009-market-intelligence/research/`
>
> Classification date: 2026-03-20
>
> Rule: if authorship or live verification is unclear, tier down instead of up.

## Summary

- Total files reviewed: `30`
- Markdown files classified: `26`
- Binary files held as local reference only: `4`
- Carry-forward set for v1 workspace: `6`
- Mixed / needs-review files kept as leads only: `8`
- `ai-mediated-context` files: `14`
- Process prompts/tasks excluded from evidence use: `2` (counted inside `ai-mediated-context`)

## Carry-Forward Set

These are the only spec-009 research files worth carrying into the v1 workspace as reusable leads. Even here, they do not become primary evidence automatically; they remain bounded by the tier column below.

| File | Tier | Carry Forward | Why |
|------|------|---------------|-----|
| `Groove Jones Market Intelligence Brief 01.md` | `mixed-needs-review` | `yes` | Large, source-cited synthesis with useful buyer, competitor, and procurement leads, but still requires spot-checking before leadership use. |
| `q1_active_xr_spenders.md` | `external-attributable-secondary` | `yes` | Best reusable buyer list with named sources and dates. |
| `q2_competing_agencies.md` | `external-attributable-secondary` | `yes` | Useful competitor baseline with named agencies and traceable public references. |
| `q4_scaling_examples.md` | `external-attributable-secondary` | `yes` | Best reusable scaling-case baseline; good for long-horizon strategy comparisons. |
| `q5_cancellation_research.md` | `mixed-needs-review` | `yes` | Honest about the lack of direct XR cancellation studies and useful for contradiction analysis. |
| `research-brief.md` | `internal-primary` | `yes` | Internal CRM-grounded context from spec 009; useful as a bridge between spec 008 and this workspace. |

## Full Markdown Classification

| File | Tier | Status | Carry Forward | Notes |
|------|------|--------|---------------|-------|
| `Gemini-market-research.md` | `ai-mediated-context` | local context only | `no` | Model-written synthesis with source links, but no proof of line-by-line live verification. |
| `Groove Jones Market Intelligence Brief 01.md` | `mixed-needs-review` | reusable with spot-checking | `yes` | High-value synthesis; use for leads, not standalone proof. |
| `Market-Research-Prompt.md` | `ai-mediated-context` | process input only | `no` | Prompt, not evidence. |
| `Perplexity-market-research.md` | `ai-mediated-context` | local context only | `no` | Strong narrative, but still AI-mediated synthesis. |
| `deep-research-results.md` | `ai-mediated-context` | local context only | `no` | Explicitly says Perplexity sonar-pro plus supplemental analysis. |
| `deep-research-tasks.md` | `ai-mediated-context` | process input only | `no` | Task brief, not evidence. |
| `external-market-research.md` | `mixed-needs-review` | leads only | `no` | Web-augmented swarm output with useful framing, but still synthesized and broad. |
| `groove-jones-market-intelligence.pplx.md` | `mixed-needs-review` | leads only | `no` | Better than pure context because it cites named sources, but still Perplexity-mediated. |
| `q1_active_xr_spenders.md` | `external-attributable-secondary` | reusable | `yes` | Best current buyer list from the 009 bundle. |
| `q2_competing_agencies.md` | `external-attributable-secondary` | reusable | `yes` | Most concrete peer-agency baseline in the folder. |
| `q3_government_contracts.md` | `mixed-needs-review` | leads only | `no` | Useful defense pathfinder, but contains market-size claims from weaker third-party sources. |
| `q4_scaling_examples.md` | `external-attributable-secondary` | reusable | `yes` | Scaling examples are attributable and directionally useful. |
| `q5_cancellation_research.md` | `mixed-needs-review` | reusable with caution | `yes` | Valuable because it explicitly separates direct evidence from analogy. |
| `research-ai-xr-convergence.md` | `ai-mediated-context` | local context only | `no` | Strategic thesis doc; not directly verified. |
| `research-angle-5-xr-competitive-landscape.md` | `ai-mediated-context` | local context only | `no` | Explicitly labeled training-data synthesis and draft. |
| `research-angle-6-growth-strategies.md` | `mixed-needs-review` | leads only | `no` | Good strategy heuristics, but mixes named sources with uncited operating conclusions. |
| `research-brief.md` | `internal-primary` | reusable | `yes` | Internal CRM-based input; not external proof, but valid internal evidence. |
| `research-fortune500-xr-2024-2025.md` | `ai-mediated-context` | local context only | `no` | Explicitly says training knowledge and no live web search. |
| `research-military-xr-contracts-2025.md` | `ai-mediated-context` | local context only | `no` | Useful orientation, but not enough direct verification status to carry forward. |
| `research-pharma-healthcare-xr-2025.md` | `ai-mediated-context` | local context only | `no` | Explicitly training-knowledge synthesis. |
| `research-spatial-computing-2025.md` | `ai-mediated-context` | local context only | `no` | Broad market framing with mixed source quality. |
| `research-xr-agency-landscape-2025.md` | `ai-mediated-context` | local context only | `no` | Explicitly says live web search unavailable. |
| `research-xr-automotive-sports-2024-2025.md` | `ai-mediated-context` | local context only | `no` | No verification status or source table. |
| `research-xr-who-is-spending-2025.md` | `mixed-needs-review` | leads only | `no` | Useful company list, but estimates and source quality vary too much for direct carry-forward. |
| `research.md` | `mixed-needs-review` | leads only | `no` | Helpful strategic bridge doc, but not an evidence artifact by itself. |
| `xr-market-angle1.md` | `ai-mediated-context` | local context only | `no` | Market-size framing with mixed-source aggregation and no verification table. |

## Binary Files

| File | Status | Notes |
|------|--------|-------|
| `GrooveJones_MarketResearch_2026.pdf` | local reference only | Content not independently re-tiered in this workspace yet. |
| `groove-jones-30-day-strike-list.pdf` | local reference only | Leadership support doc, not evidence baseline. |
| `Groove_Jones_30Day_Revenue_Action_Plan.docx` | local reference only | Internal planning context; not external proof. |
| `Groove_Jones_Consolidated_Market_Intelligence_2026.docx` | local reference only | Internal synthesis; already known to be a compressed evidence layer. |

## Working Rule For Spec 004

- The carry-forward set above can be copied into the bounded MiroFish bundle later only if each file is labeled with its current tier and limitations.
- No `ai-mediated-context` file from spec 009 should appear in a leadership recommendation as if it were observed market fact.
- Any claim reused from the `mixed-needs-review` files should be re-backed by a named external source in this workspace before it drives a recommendation.
