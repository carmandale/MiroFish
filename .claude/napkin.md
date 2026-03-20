# Napkin

## Corrections
| Date | Source | What Went Wrong | What To Do Instead |
|------|--------|----------------|-------------------|
| 2026-03-19 | code-verify follow-up | I described the March 18 Strategy Lab proof artifacts as if they demonstrated a fresh live simulation run. | Treat `backend/uploads/projects/proj_85bec7582332/strategy_lab/` as a proof harness using real corpus extraction plus synthetic interview/private-analysis artifacts (`proof-sim-0N` IDs), not a live post-fix OASIS+LLM rerun. |
| 2026-03-19 | live rerun attempt | I assumed wiring `OPENAI_API_KEY` into `LLM_API_KEY` plus a real `ZEP_API_KEY` would be sufficient to complete a fresh Strategy Lab rerun. | Shell wiring is now correct, but the first live ontology call fails with OpenAI `429 insufficient_quota`; the next real rerun needs working model credits or an alternate OpenAI-compatible provider, not more shell changes. |
| 2026-03-19 | live rerun attempt | I recommended `gpt-5-mini` before proving this repo’s current OpenAI call patterns were fully compatible with it. | For now, use `gpt-4.1` as the practical live-run default; GPT-5 support needs further hardening beyond token/temperature compatibility because ontology generation still returned empty JSON on the live path. |
| 2026-03-20 | user correction on mesh stalls | I treated non-speaking `crew-challenger` spawns as a collaborator health/path issue. | Treat it as the current spawn-command liveness-heuristic bug tracked by `pi-messenger-35k` / `specs/009-deterministic-spawn-liveness/`; do not debug `crew-challenger`, and if retrying mesh in MiroFish, use `.pi/messenger/crew/config.json` with `{\"collaboration\":{\"stallThresholdMs\":600000}}`. |

## User Preferences
- (accumulate as you learn them)
- Fully ground the repo before starting implementation work; honor the ground-cache gate instead of skimming.
- If shaping materially changes the solution, update the spec to match the selected shape before planning or implementation.
- Spec-local workflow artifacts are critical assets here; commit them instead of leaving them untracked just because they look like metadata.
- Do not debug `crew-challenger` stalls in MiroFish right now; the tracked bug is spawn-command liveness detection, and the approved local workaround is a 10-minute `stallThresholdMs` override under `.pi/messenger/crew/config.json`.

## Patterns That Work
- (approaches that succeeded)
- Backend is organized around thin Flask blueprints over service-layer orchestration; read `backend/app/api/*` with `backend/app/services/*` together.
- Frontend mirrors the product pipeline directly: route views host `Step1-5*` components plus a shared `GraphPanel`, so user flow is easiest to follow from `frontend/src/views/*`.

## Patterns That Don't Work
- (approaches that failed and why)
- Assuming repo-local agent rules exist; this repo currently has no local `AGENTS.md`, `.claude/CLAUDE.md`, or `.cursor/rules/*`, so global instructions apply.

## Domain Notes
- MiroFish is a multi-agent swarm intelligence prediction engine (Python Flask backend + Vue.js frontend)
- Built on OASIS simulation engine (CAMEL-AI) for running Twitter/Reddit-like social platform simulations
- Uses Zep Cloud for knowledge graph (GraphRAG) and agent memory
- LLM calls use OpenAI-compatible API format (configurable provider)
- 5-step pipeline: Graph Build → Env Setup → Simulation → Report → Interaction
- Backend uses `uv` for Python package management, not pip
- Project language is primarily Chinese with bilingual docs
- Backend persists project/simulation/report state under `backend/uploads`; long-running graph builds use `TaskManager`, while simulations/reports persist their own JSON/JSONL artifacts.
- Recent code focus is `report_agent` robustness/formatting plus Zep graph pagination.
- Backend now has a focused Python regression suite under `backend/tests/` plus `backend/scripts/test_profile_format.py`; prefer `UV_CACHE_DIR=/tmp/uv-cache uv run pytest` in sandboxed Codex shells because the default `~/.cache/uv` path may be unreadable.
- Existing Strategy Lab proof artifacts under `backend/uploads/projects/proj_85bec7582332/strategy_lab/` are useful for artifact-flow validation, but they are not evidence of a fresh live model-backed rerun; the JSONs themselves call out synthetic interviews and fake `proof-sim-*` IDs.
- A failed live rerun on 2026-03-19 hit OpenAI `429 insufficient_quota` for `proj_96a1497b6ddd`, but that is no longer the current blocker state after credits were restored.
- As of 2026-03-19, `gpt-4.1` is the safer model for live MiroFish runs. GPT-5 now clears token/temperature parameter issues after patches, but ontology generation still failed on a live run with empty JSON content.
- Proven live rerun: `proj_720421fb9a44` on graph `mirofish_19d4a269b27d4815` completed all five Strategy Lab lanes and wrote `backend/uploads/projects/proj_720421fb9a44/strategy_lab/comparative_report.json` at 2026-03-19 12:31 local time.
- For live reruns in Codex shells, explicitly `source ~/.zprofile`, bridge `LLM_API_KEY` from `OPENAI_API_KEY` if needed, and force `LLM_MODEL_NAME=gpt-4.1` before invoking the backend runner scripts.
- No `thoughts/shared/handoffs/current.md` exists yet in this repo.
