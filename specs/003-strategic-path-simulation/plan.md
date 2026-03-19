---
title: "Implementation Plan — MiroFish Strategic Path Simulation"
date: 2026-03-18
bead: bd-2g4
---

<!-- Codex Review: APPROVED after 4 rounds | model: codex/gpt-5.4 | date: 2026-03-18 -->
<!-- Status: REVISED — direct source edits (dropped monkey-patch), wholesale template translations, R7 sentiment narrowed, JSON schema contract preserved, entity routing corrected, metric lookup via simulation_config.json -->
<!-- plan:complete:v1 | harness: pi/claude-opus-4-6 | date: 2026-03-18T22:02:28Z -->

# Plan (Implementation) — Complete Standalone Document

## Architecture: 5 Projects (4 prod + 1 test), Graph-Memory Enabled, Direct Source Edits

Direct source edits on the MiroFish fork. No monkey-patch module. No run.py modification. Each edit is surgical.

5 isolated MiroFish projects. `enable_graph_memory_update: true`. Test project abandoned after validation.

## Task T0: Convert .docx to Markdown

```bash
cd "/Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/quickbooks/specs/009-market-intelligence/research/"
pandoc -f docx -t markdown -o Groove_Jones_Consolidated_Market_Intelligence_2026.md Groove_Jones_Consolidated_Market_Intelligence_2026.docx
pandoc -f docx -t markdown -o Groove_Jones_30Day_Revenue_Action_Plan.md Groove_Jones_30Day_Revenue_Action_Plan.docx
```

Tables preserved as pipe tables. Images lost (acceptable). Verify output before upload.

## Complete Source Edit List

### File 1: `backend/app/services/oasis_profile_generator.py` (~12 edits)

- Line ~169: Add to `INDIVIDUAL_ENTITY_TYPES`: `"enterprisebuyer", "industryanalyst", "conferenceorganizer"`
- Line ~175: Add to `GROUP_ENTITY_TYPES`: `"xragency", "defensecontractor", "healthcaresystem", "primecontractor", "vcfirm"`
- Line ~163: Replace `COUNTRIES` with `["United States"]`
- Line ~673: Replace Chinese system prompt with English B2B version (preserving `is_individual` parameter)
- Lines ~713, ~720: Translate individual persona instructions to English
- Lines ~762, ~769: Translate group persona instructions to English
- Lines ~816, ~828: Replace hardcoded `"中国"` with `"United States"`
- Line ~1174: Replace fallback `"中国"` with `"United States"`

### File 2: `backend/app/services/report_agent.py` (~8 template replacements)

**PLAN_SYSTEM_PROMPT (lines 551-588):** Full English replacement. MUST include JSON schema contract:
```
Output a JSON report outline:
{
    "title": "Report title",
    "summary": "One-sentence summary",
    "sections": [{"title": "Section title", "description": "Section description"}]
}
Note: sections array must have 2-5 elements.
```
This JSON schema is read by `plan_outline()` at line 1176 via `chat_json()`. Dropping it breaks outline generation.

**PLAN_USER_PROMPT_TEMPLATE (lines 590-612):** Full English replacement. Preserves: `{simulation_requirement}`, `{total_nodes}`, `{total_edges}`, `{entity_types}`, `{total_entities}`, `{related_facts_json}`.

**SECTION_SYSTEM_PROMPT_TEMPLATE (lines 614-766):** Wholesale English replacement preserving entire ReACT protocol: tool-call grammar, 3-5 tool calls/section, formatting rules, workflow. ~153-line English equivalent.

**SECTION_USER_PROMPT_TEMPLATE (lines 768-793):** Full English replacement. Preserves: `{previous_content}`, `{section_title}`.

**REACT_OBSERVATION_TEMPLATE (lines 795-805):** Translate Chinese instructions. Preserves: `{tool_name}`, `{result}`, `{tool_calls_count}`, `{max_tool_calls}`, `{used_tools_str}`, `{unused_hint}`.

**REACT_INSUFFICIENT_TOOLS_MSG (lines 807-810):** Translate. Preserves: `{tool_calls_count}`, `{min_tool_calls}`, `{unused_hint}`.

**CHAT_SYSTEM_PROMPT_TEMPLATE (lines 828-856):** Full English replacement. Preserves: `{simulation_requirement}`, `{report_content}`, `{tools_description}`.

**Tool descriptions in _get_tools_dict() (lines 920-950):** Translate Chinese parameter descriptions to English.

**Fallback outline (lines 1210-1218):** Replace Chinese fallback strings with English equivalents.

### File 3: `backend/app/services/zep_tools.py` (~8 edits)

- Lines 374-410: `InterviewResult.to_text()` — translate headers: "深度采访报告"→"In-Depth Interview Report", "采访主题"→"Interview Topic", "采访人数"→"Interviewees", "采访对象选择理由"→"Selection Rationale"
- Line 1574: `"未知"` → `"Unknown"`
- Lines 1580-1603: `_select_agents_for_interview()` system prompt — full English translation
- Lines 1644-1662: `_generate_interview_questions()` — full English translation
- Lines 1698-1719: `_generate_interview_summary()` — full English translation

### File 4: `backend/app/services/zep_graph_memory_updater.py` (~10 edits)

- Lines 63-140: All `_describe_*()` methods — translate action descriptions: "发布了一条帖子"→"Posted", "点赞了"→"Liked", "转发了"→"Reposted", etc.

### File 5: `backend/app/api/simulation.py` (~1 edit)

- Lines 23-31: `INTERVIEW_PROMPT_PREFIX` — translate to English + add narrative-resonance caveat

## Comparison Metrics (R7)

Data: `uploads/simulations/{sim_id}/twitter/actions.jsonl` and `reddit/actions.jsonl`
Agent types: `simulation_config.json` → `agent_configs[].entity_type` (NOT profile exports)

| Metric | Formula |
|--------|---------|
| Total engagement | count(CREATE_POST + LIKE_POST + CREATE_COMMENT + REPOST + QUOTE_POST) |
| Amplification ratio | (REPOST + QUOTE_POST) / CREATE_POST |
| Competitive response | count(actions by XRAgency agents) |
| Buyer engagement | count(actions by EnterpriseBuyer + HealthcareSystem + DefenseContractor agents) |
| Sentiment | ReportAgent qualitative analysis (no structured classifier in OASIS) |

## Entity Routing (authoritative)

| Type | Route | Why |
|------|-------|-----|
| EnterpriseBuyer | INDIVIDUAL | Person: VP Medical Ed, Head of L&D |
| IndustryAnalyst | INDIVIDUAL | Person: tech journalist, analyst |
| ConferenceOrganizer | INDIVIDUAL | Person: event producer |
| XRAgency | GROUP | Org: Groove Jones, Trigger XR |
| DefenseContractor | GROUP | Org: Lockheed Martin |
| HealthcareSystem | GROUP | Org: J&J MedTech |
| PrimeContractor | GROUP | Org: Boeing |
| VCFirm | GROUP | Org: a16z |
| Person | INDIVIDUAL | Fallback |
| Organization | GROUP | Fallback |

## Requirement Traceability

| Req | How | Files |
|-----|-----|-------|
| R0 | 5 projects × graph-memory × compare_scenarios.py | — |
| R1 | T0 pandoc conversion + upload .md | Task T0 |
| R2 | Custom ontology JSON into project.json | ontology.json |
| R3 | English profile prompts + entity routing + ALL-profile validation | oasis_profile_generator.py |
| R4 | poster_agent_id in simulation_config.json | — |
| R5 | ALL report templates English + narrative-resonance framing | report_agent.py |
| R6 | Interviews + caveat in INTERVIEW_PROMPT_PREFIX + CHAT template | simulation.py, zep_tools.py |
| R7 | compare_scenarios.py (engagement, amplification, competitive, buyer) + ReportAgent qualitative | New file |
| R8 | Direct source edits on ALL Chinese strings across 5 files + manual US timezone config | 5 files |
| R9 | All report prompts enforce "narrative resonance, not procurement prediction" | report_agent.py |

## Data Handling

- Research → external LLM/Zep services: requires Dale's explicit approval
- Test project: delete after validation
- Production projects: retain for reports, delete after final deliverable

## Total Edit Count

| File | Edits |
|------|-------|
| oasis_profile_generator.py | ~12 |
| report_agent.py | ~8 templates + tool descriptions + fallback |
| zep_tools.py | ~8 |
| zep_graph_memory_updater.py | ~10 |
| simulation.py | ~1 |
| compare_scenarios.py (NEW) | ~80 lines |
