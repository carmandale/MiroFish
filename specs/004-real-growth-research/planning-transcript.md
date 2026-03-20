---
title: "Planning Transcript - Real Growth Research Foundation for Groove Jones"
date: 2026-03-20
bead: bd-7km
---

<!-- plan:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-20T15:42:28Z -->

# Planning Transcript

**Participants:** RedUnion (`codex/gpt-5.4`, proposer) x YoungUnion (`crew-challenger`, adversary) x ZenQuartz (`crew-challenger`, approval after respawn)  
**Date:** 2026-03-20  
**Spec:** `specs/004-real-growth-research/spec.md`

## Round 1: RedUnion - Research and initial direction

### Research findings

- MiroFish ingest still only supports `.pdf`, `.docx`, `.md`, `.markdown`, and `.txt`:
  - `backend/app/utils/file_parser.py`
  - `backend/app/config.py`
- Existing provenance and artifact patterns already exist in the current product path:
  - `backend/app/api/graph.py`
  - `backend/app/services/strategy_lab_provenance.py`
  - `backend/app/models/project.py`
- `quickbooks/data-package` is the raw internal evidence surface:
  - `11` JSON files
- `quickbooks/specs/009-market-intelligence/research` is the current synthesized external context:
  - `26` markdown files
- `quickbooks/specs/009-market-intelligence/source-appendix.md` already provides a useful verification-table pattern for source inventory.
- The prior live Strategy Lab corpus was only `3` files and `67` chunks, so any new research bundle must be intentionally curated.

### Initial direction

- Keep MiroFish code unchanged in v1.
- Build a bounded provenance-preserving transformation layer outside product code.
- Produce a tiered research bundle plus leadership deliverables.
- Validate the final subset through existing MiroFish intake instead of changing the intake path.

## Round 2: YoungUnion - Structural challenge

```markdown
[PHASE:challenge]

I've read spec.md and shaping-transcript.md end-to-end and independently verified 14 files across MiroFish, quickbooks/data-package, and 009-market-intelligence. Here is my adversarial challenge of the implementation approach before you write plan.md.

---

## 1) MISSING RISKS AND BLIND SPOTS

### 1A. The "transformation layer" is underspecified in a way that will bite you during planning

The spec says "provenance-preserving transformation layer" 6 times but never defines:
- **Who/what does the transforming?** A Python script? An LLM agent? A human copy-paste session? Each has completely different provenance characteristics.
- **Which of the 11 JSON files actually need transformation?**
- **The provenance metadata format is undefined.**

### 1B. MiroFish chunk_manifest provenance has a lossy gap you're not seeing

I checked the actual `chunk_manifest.json` for proj_720421fb9a44. Each chunk carries `chunk_id`, `document_id`, `filename`, `text`, `start_char`, `end_char`, `locator_start`, `locator_end`, `episode_uuid`. Notice: **there is no field for source-tier, extraction date, or original-raw-source-path.**

### 1C. The "new external research" requirement (R3) has no acquisition plan

The spec lists the *types* of external sources wanted but has zero plan for how they get acquired.

### 1D. The 30-file research corpus will overwhelm MiroFish's current Strategy Lab

The existing Strategy Lab run used 3 docs -> 67 chunks. The spec envisions ~30 files.

### 1E. No freshness guarantee

All 11 JSON files have a `snapshot_date` of `2026-03-17` or `2026-03-18`. The spec says nothing about whether the transformation preserves this, or whether the research bundle becomes stale in 2 weeks.

---

## 2) BETTER AND WORSE IMPLEMENTATION OPTIONS

### BETTER: Two-pass transformation with mechanical + narrative layers

Instead of one ambiguous "transformation layer":

**Pass 1 — Mechanical (script-driven, zero-loss):** emit provenance-bearing markdown docs from JSON.

**Pass 2 — Narrative (LLM-driven, explicitly labeled):** synthesize findings across the mechanical extracts.

### OPTION: Reuse source-appendix.md's verification pattern

The `source-appendix.md` from 009 has a genuinely useful pattern: every source gets a row in a verification table with URL, status, and the specific claim it supports.

---

## 3) CONCRETE FILE-LEVEL INSERTION POINTS AND ARTIFACT LAYOUT

### In `specs/004-real-growth-research/`:
```
specs/004-real-growth-research/
├── spec.md
├── shaping-transcript.md
├── plan.md
├── tasks.md
├── source-inventory.md
├── evidence-tier-rubric.md
├── contradiction-register.md
└── artifacts/
    ├── transform/
    ├── research/
    └── leadership/
```

### MiroFish corpus bundle (for ingest):
```
backend/uploads/projects/<new-project>/strategy_lab/
├── corpus/
├── corpus_manifest.json
└── chunk_manifest.json
```

### NOT in MiroFish code:
No changes to `file_parser.py`, `strategy_lab_provenance.py`, `graph.py`, `project.py`, or any other MiroFish source.

---

## 4) CONCRETE VERIFICATIONS

- Verified `FileParser` / config extensions only allow document inputs.
- Verified the prior live corpus was `3` docs / `67` chunks.
- Verified `quickbooks/data-package` and `009` research counts.
- Verified `chunk_manifest` lacks a provenance-tier field.
- Verified the financial urgency remains the dominant triage driver.

---

## BOTTOM LINE

Your instinct — bounded provenance-preserving transformation layer plus evidence-tiered research bundle and leadership deliverables, without new MiroFish ingest code — is correct. But the plan must resolve five things:

1. Mechanical vs. narrative transformation split
2. Provenance metadata that survives chunking
3. Explicit file selection gate
4. External research acquisition method
5. Corpus size budget
```

## Round 3: RedUnion - Revised decisions

```markdown
[PHASE:revise]

Your challenge is right on the load-bearing gaps. I am revising the plan around five explicit decisions before writing plan.md:

1. **Two-pass transformation, not one ambiguous layer.**
   - Pass 1 is mechanical and zero-loss enough for auditability: a bounded helper script under `specs/004-real-growth-research/tools/` reads selected JSON/data-package inputs and emits markdown evidence docs under `specs/004-real-growth-research/artifacts/transform/`.
   - Pass 2 is narrative and explicitly tiered: leadership briefs plus any synthesis docs live separately under `specs/004-real-growth-research/artifacts/leadership/` and `.../research/`, with `tier: ai-synthesis` or equivalent.
   - No new MiroFish source changes; this stays in spec-local tooling/artifacts.

2. **Provenance must survive chunking via inline text, not frontmatter alone.**
   - Each transformed markdown doc gets both YAML frontmatter and a visible `## Provenance` block near the top of the body with `source_path`, `snapshot_date`, `record_count`, `transform_method`, and selection notes.
   - The plan will explicitly state that R2 is satisfied by the spec-workspace artifacts plus inline provenance that survives normal MiroFish chunking; we do not depend on `chunk_manifest.json` carrying tier/source-path fields it does not have.

3. **Selection gate: workspace superset, ingest subset.**
   - The research workspace can contain the full transformed set, but the MiroFish ingest bundle is capped and curated.
   - Initial ingest target is the highest-leverage internal docs plus selected external primary/attributable docs, not all 11 JSON files and not all 26 research files.
   - Current working assumption for workspace-first transformation: 07, 08, 09, 01-summary, 02-summary, 05, 06, 10, 11 plus a selective decision on 03/04 after the source inventory.
   - AI-mediated 009 files remain context-tier unless a specific section is backed by named source evidence and relabeled honestly.

4. **External research acquisition is bounded manual-first, not hidden scraping or another AI fog layer.**
   - The plan will require a named-source intake pass that creates external evidence docs and a source-inventory table using the proven `source-appendix.md` pattern from `quickbooks/specs/009-market-intelligence/`.
   - Acceptable external proof for v1 is a bounded set of primary/attributable secondary sources copied or excerpted into markdown with URL + verification status, not another unconstrained AI synthesis sweep.

5. **Corpus budget becomes a first-class constraint.**
   - The plan will set an explicit v1 ingest budget, likely on the order of ~12-15 files / <=250 chunks, with the rest of the workspace staying outside the first MiroFish ingest set.
   - Validation will include an actual ingest smoke test through the existing MiroFish path to confirm the chosen bundle produces `corpus_manifest.json` and `chunk_manifest.json` cleanly.

Additional scope call: because the company is at ~$19.5K cash and 0 runway, the implementation sequence will front-load the 30-90 day triage brief and the AR/pipeline/capacity evidence docs before the 6-24 month strategy pack.
```

## Round 4: ZenQuartz - Approved after respawn

```markdown
[PHASE:approved] I've verified the revision against all five original objections. Here's my evaluation:

**Objection 1 — Transformation layer underspecified -> RESOLVED.**
The two-pass architecture (mechanical script in `specs/004-real-growth-research/tools/` + narrative deliverables in `artifacts/`) provides clear separation of concerns.

**Objection 2 — chunk_manifest provenance is lossy -> RESOLVED.**
I verified the code: `ChunkManifestEntry` has no `source_tier`, `source_path`, or provenance-tier field. The revision's solution — inline provenance blocks in the markdown body rather than frontmatter — is the right v1 call.

**Objection 3 — External primary-source acquisition not planned -> RESOLVED.**
Bounded manual-first intake reusing the `source-appendix.md` verification pattern from `009-market-intelligence` is pragmatic and already validated.

**Objection 4 — ~30-file corpus would overwhelm Strategy Lab -> RESOLVED.**
The workspace-superset / ingest-subset model with an explicit v1 budget of 12–15 files / <=250 chunks is the right architecture.

**Objection 5 — Freshness/triage urgency not first-class -> RESOLVED.**
Sequencing triage-first when cash is $19.5K and runway is zero is the correct prioritization.

**Summary:** All five structural objections are adequately resolved. The revision is concrete, bounded, and pragmatic. No remaining concerns.
```
