---
title: "Real Growth Research Foundation — Shaping Transcript"
date: 2026-03-19
bead: bd-7km
shaping: true
---

<!-- shape:complete:v1 | harness: codex/gpt-5.4 | date: 2026-03-19T22:10:34Z -->

# Real Growth Research Foundation — Shaping

## Source

> create a bead and issue to do real, meaningful research. you have complete access to my financial (quickbooks), production (forecast), and sales (pipedrive) data all on ~/dev ~/dev/pipedrive ~/dev/quickbooks ~/dev/forecast and then the full research findings in quickbooks/specs/009-market-intelligence but I would also want more real, quality research

## Problem

The current MiroFish strategy work exposed a real evidence-quality gap. The live Strategy Lab run used only three research documents, and most of the “insight” came from already-synthesized Groove Jones materials instead of raw finance, sales, and production evidence plus strong external source material. Groove Jones already has richer internal operating data available across QuickBooks, Pipedrive, and Forecast, but that evidence is mostly JSON and is not directly ingestible by current MiroFish. The next useful work is to shape the right research foundation before more strategy modeling happens.

## Outcome

Choose a shape for a decision-grade research foundation that:

- helps leadership make near-term and medium-term decisions,
- preserves provenance from raw evidence to synthesis,
- uses stronger external sources than the current corpus,
- remains ingestible by current MiroFish without product changes in v1,
- and stays bounded enough to matter in a cash crisis.

---

## Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | Produce a research package that directly supports an actual leadership decision in the current cash crisis, not just a better archive. | Core goal |
| R1 | Raw internal operating evidence from QuickBooks, Pipedrive, and Forecast must remain first-class source material, even if a transformed view is created for MiroFish ingestion. | Must-have |
| R2 | Any transformation from raw JSON/data into MiroFish-ingestible documents must preserve reversible provenance: source file, extraction date, row or record counts, and transformation method. | Must-have |
| R3 | External research must be tiered by evidence quality. Major claims may only rely on named primary or attributable secondary sources; AI syntheses can provide context but cannot stand alone as proof. | Must-have |
| R4 | The package must clearly separate 30–90 day survival or triage questions from 6–24 month strategic positioning questions. | Must-have |
| R5 | Contradictions, unsupported beliefs, and freshness limits must be explicit and easy to inspect. | Must-have |
| R6 | The human-readable deliverable must be strong enough that leadership can act without opening raw JSON, while still linking back to evidence. | Must-have |
| R7 | The final corpus must be ingestible by current MiroFish without requiring product changes in v1. | Must-have |
| R8 | v1 must stay bounded: no permanent warehouse, no new MiroFish ingest code, and no pretending this research is already a long-term data platform. | Must-have |

---

## A: 72-Hour Leadership War Room Package

| Part | Mechanism | Flag |
|------|-----------|:----:|
| A1 | Inventory the existing internal data-package and `009-market-intelligence` research corpus, then manually curate only the most decision-relevant evidence. | |
| A2 | Convert the needed raw JSON facts into annotated markdown tables by hand or one-off scripts, with source-path footers. | |
| A3 | Produce a leadership memo split into survival, near-term revenue, and strategic bets. | |
| A4 | Export the same memo and appendix bundle as MiroFish-ingestible markdown. | |

## B: Portable Evidence Bundle Builder

| Part | Mechanism | Flag |
|------|-----------|:----:|
| B1 | Define a source inventory and evidence-tier rubric covering internal raw data, prior syntheses, and new external research. | |
| B2 | Build a bounded transformation layer that converts selected raw JSON/data into markdown evidence docs while retaining raw snapshots and record counts. | |
| B3 | Curate external research into tiered source docs, explicitly quarantining AI-synthesis-only material from claim anchors. | |
| B4 | Emit a portable multi-file corpus: raw snapshot index, transformed evidence docs, contradiction register, and leadership memo. | |
| B5 | Feed the same corpus to MiroFish using existing `.md`, `.docx`, `.pdf`, and `.txt` intake only. | |

## C: Evidence Graph / Contradiction Map

| Part | Mechanism | Flag |
|------|-----------|:----:|
| C1 | Represent strategic claims as nodes with support, contradict, or unknown links to internal and external evidence. | ⚠️ |
| C2 | Generate confidence and contradiction views from the graph. | ⚠️ |
| C3 | Export graph-derived narrative summaries for leadership and MiroFish. | ⚠️ |

## D: Timeboxed Hybrid Bundle

| Part | Mechanism | Flag |
|------|-----------|:----:|
| D1 | Reuse B1–B3 to create a strict evidence-tiered, provenance-bearing corpus. | |
| D2 | Reuse A3 to produce an immediate leadership memo split into 30 or 90 day triage vs. strategic options. | |
| D3 | Reuse B5 to make the same corpus MiroFish-ingestible with no product changes. | |
| D4 | Ship a contradiction register and a “what we know vs. what we’re inferring” summary as first-class artifacts. | |

---

## Fit Check

| Req | Requirement | Status | A | B | C | D |
|-----|-------------|--------|---|---|---|---|
| R0 | Produce a research package that directly supports an actual leadership decision in the current cash crisis, not just a better archive. | Core goal | ✅ | ❌ | ❌ | ✅ |
| R1 | Raw internal operating evidence from QuickBooks, Pipedrive, and Forecast must remain first-class source material, even if a transformed view is created for MiroFish ingestion. | Must-have | ✅ | ✅ | ❌ | ✅ |
| R2 | Any transformation from raw JSON/data into MiroFish-ingestible documents must preserve reversible provenance: source file, extraction date, row or record counts, and transformation method. | Must-have | ❌ | ✅ | ❌ | ✅ |
| R3 | External research must be tiered by evidence quality. Major claims may only rely on named primary or attributable secondary sources; AI syntheses can provide context but cannot stand alone as proof. | Must-have | ❌ | ✅ | ❌ | ✅ |
| R4 | The package must clearly separate 30–90 day survival or triage questions from 6–24 month strategic positioning questions. | Must-have | ✅ | ❌ | ❌ | ✅ |
| R5 | Contradictions, unsupported beliefs, and freshness limits must be explicit and easy to inspect. | Must-have | ❌ | ✅ | ❌ | ✅ |
| R6 | The human-readable deliverable must be strong enough that leadership can act without opening raw JSON, while still linking back to evidence. | Must-have | ✅ | ✅ | ❌ | ✅ |
| R7 | The final corpus must be ingestible by current MiroFish without requiring product changes in v1. | Must-have | ✅ | ✅ | ❌ | ✅ |
| R8 | v1 must stay bounded: no permanent warehouse, no new MiroFish ingest code, and no pretending this research is already a long-term data platform. | Must-have | ✅ | ✅ | ❌ | ✅ |

**Notes:**
- A fails R2: annotated markdown and source footers are helpful, but they do not guarantee reversible provenance with counts and transformation metadata.
- A fails R3: it does not enforce a falsifiable quality bar on external research.
- A fails R5: it can summarize contradictions, but it does not make them a first-class artifact.
- B fails R0: it improves the corpus, but it does not force an immediate crisis-oriented leadership decision package.
- B fails R4: it builds the evidence layer but does not explicitly separate survival triage from longer-horizon strategy.
- C fails broadly: its core mechanisms remain flagged unknowns, which means it cannot claim fit yet.

---

## Selected Shape

**Selected Shape: D — Timeboxed Hybrid Bundle**

Shape D is selected because it is the only shape that passes the full fit check while respecting both the business urgency and the current MiroFish product constraints.

It combines:

- A’s immediate human-readable leadership utility,
- B’s provenance-bearing transformation layer and tiered source discipline,
- and the contradiction surfacing that C was reaching for,

without requiring new MiroFish ingest code or pretending this work is already a full long-term analytics platform.

### Why D Wins

- Groove Jones has roughly `$19.5K` cash and `0` months of runway, so a shape that does not produce an immediate leadership decision package is insufficient.
- Current MiroFish ingest only supports `.pdf`, `.docx`, `.md`, `.markdown`, and `.txt`, so raw JSON cannot be the final corpus format.
- The existing external research set is too AI-mediated to stand as a clean source of truth, so source tiering has to be part of the shape, not a nice-to-have.
- Leadership still needs a readable artifact, not a graph or a pile of transformed evidence docs.

---

## Detail D: Concrete Affordances

### UI Affordances

| ID | Affordance | Notes | Wires Out |
|----|------------|-------|-----------|
| U1 | Source inventory table | Lists every internal dataset, prior synthesis, and new external source with type, freshness, evidence tier, and ingest status. | N1, N3 |
| U2 | 30/90-day triage brief | Human-readable memo focused on cash, AR, pipeline, capacity, and near-term moves. | N2, N4, N5 |
| U3 | 6–24 month strategy brief | Human-readable memo focused on durable lanes, buyer demand, competitive position, and strategic constraints. | N2, N4, N5 |
| U4 | Contradiction register | Explicit table of what supports, contradicts, or remains unknown. | N4 |
| U5 | MiroFish corpus index | Shows which transformed files are intended for ingest and what raw sources each one came from. | N2, N5 |

### Non-UI Affordances

| ID | Affordance | Notes | Wires Out |
|----|------------|-------|-----------|
| N1 | Raw source index | Registry of internal JSON sources, prior research files, and new external documents with source metadata. | N2, N3, U1 |
| N2 | Provenance-preserving transformation layer | Converts selected raw data into markdown evidence docs while preserving file path, extraction date, and record counts. | U2, U3, U5 |
| N3 | Evidence-tier classifier | Labels sources as primary, attributable secondary, or AI-mediated/context-only. | U1, N4 |
| N4 | Claim/evidence ledger | Maps each major claim to supporting, contradicting, or missing evidence. | U2, U3, U4 |
| N5 | Corpus export bundle | Assembles the final markdown corpus for leadership review and MiroFish ingestion without new ingest code. | U2, U3, U5 |

### Wiring by Place

| Place | Affordances |
|-------|-------------|
| Internal source repos (`quickbooks`, `pipedrive`, `forecast`) | N1 |
| Research workspace / spec artifacts | N2, N3, N4, U1, U4 |
| Leadership package | U2, U3 |
| MiroFish intake bundle | N5, U5 |

---

## Transcript

### RedUnion → `crew-challenger` spawn prompt

```text
Read /Users/dalecarman/Groove Jones Dropbox/Dale Carman/Projects/dev/MiroFish/specs/004-real-growth-research/spec.md and challenge the shaping for this problem. Context you should verify yourself from the repo: the current live Strategy Lab run in backend/uploads/projects/proj_720421fb9a44/strategy_lab was driven by only three source files; quickbooks/data-package contains raw internal finance/sales/delivery evidence; quickbooks/specs/009-market-intelligence contains richer prior research but much of it is already synthesized. I need adversarial shaping, not agreement. Please: (1) identify missing or weak requirements, (2) propose at least 3 distinct shapes for solving the real problem, (3) include at least one concrete verification such as counts, file checks, or grep results in your challenge. Do not /ground yourself. Read only what you need from the referenced repos and respond with [PHASE:challenge].
```

### RedGrove → RedUnion `[PHASE:challenge]`

```text
I've read spec 004, verified the live Strategy Lab corpus, the quickbooks/data-package, 009-market-intelligence research, and MiroFish's actual ingest code. Here is my adversarial shaping challenge.

---

## ⚠️ CRITICAL GAP #1: MiroFish Cannot Ingest JSON — R1 Is Impossible As Written

The spec's R1 says: "Raw internal data must be part of the research base" and R7 says the bundle must be "ingested into MiroFish."

But MiroFish's `FileParser` (backend/app/utils/file_parser.py) only supports:
```
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.md', '.markdown', '.txt'}
```

**All 11 data-package files are `.json`.** There is zero JSON ingest path. The spec treats R1 and R7 as compatible requirements, but they are currently in direct tension. Either:
- someone builds a JSON-to-markdown transformer (new code, which the spec says is out of scope), or
- "raw operating data" gets pre-digested into markdown (which violates R1's intent of avoiding markdown summaries), or
- MiroFish gets a JSON parser added (product work, not research work).

This isn't a minor gap — it's the spec's central thesis (wider evidence base → MiroFish) blocked by the product's own format constraints. The spec must pick one: extend MiroFish ingest, or define an explicit transformation layer with provenance rules.

---

## ⚠️ CRITICAL GAP #2: The "Already Synthesized" Problem Is Worse Than the Spec Admits

The spec correctly identifies that the Strategy Lab ran on 3 files producing 67 chunks (verified: doc_5c518b9c8cc8=5, doc_a65bdd3b8250=41, doc_1149758b297c=21). Good diagnosis.

But the spec then lists `quickbooks/data-package/12-market-intelligence-synthesis.md` as an "Available Evidence Surface" — that file's own header says:

> "Generated 2026-03-18 | 5 parallel researcher agents (Sonnet + web search) | Synthesized by Opus"

It's an AI-synthesized document. The 009-market-intelligence/research/ folder has 26 .md files totaling 8,123 lines, but at least 4 are explicitly named after AI tools (`Gemini-market-research.md`, `Perplexity-market-research.md`, `deep-research-results.md`, `deep-research-tasks.md`). Even the files that cite Gartner/IDC (18 of 26 files do) were generated by AI agents scraping those sources — they are not primary documents.

R3 demands "higher quality external research" but the spec doesn't define a quality bar that would reject the 009 corpus. Without a falsifiable criterion (e.g., "must include verbatim quotes or data tables from the original source, not paraphrased by LLMs"), R3 is aspirational, not enforceable.

---

## ⚠️ GAP #3: The Spec Ignores the $19K Cash Reality

The QBO financial summary shows:
- **Cash position: $19,454.91**
- **Monthly burn: $397,455.67**
- **Runway: 0 months**
- **Net income: -$608,991.80**

The spec calls for a "decision-grade evidence base for leadership" but doesn't address the obvious: **a company with $19K in cash and zero runway has a fundamentally different decision space than one with resources.** The research foundation should be shaped around what Groove Jones can actually act on in the next 30-90 days, not what would be nice to know.

R4 asks "which strategic lanes are supported by both internal performance and external demand?" — but the actual decision is more like "which of our $242K in outstanding AR can we collect fastest, and which of our open pipeline deals close in 30 days?" The spec needs to explicitly address triage priority vs. strategic breadth.

---

## ⚠️ GAP #4: No Verification Criteria for "Decision-Grade"

R0 says "decision-grade" but defines no test. What makes evidence "decision-grade"? The comparative_report.md already rates all 5 lanes as "High" evidence strength. If the current output already claims high evidence strength, how would anyone detect that spec 004's output is materially better?

R6 says "leadership should be able to read the resulting outputs without needing to inspect raw JSON" — but who is "leadership"? How do they consume it? PDF? Slide deck? A meeting? The format constraint is undefined.

---

## THREE DISTINCT SHAPES

### Shape A: "72-Hour Leadership War Room Package"

**What it is:** A single-pass, human-readable dossier that combines the existing data-package JSONs (transformed to annotated markdown tables with source provenance), the best-of 009-market-intelligence research (curated, not bulk-imported), and a gap analysis showing what internal data contradicts external claims.

**Output:** 5-7 markdown files organized by decision domain (cash/survival, pipeline quality, capacity constraints, market demand, competitive position), plus a one-page "what we know vs. what we're guessing" summary.

**Why it fits the crisis:** $19K cash means leadership needs answers now, not a repeatable pipeline. This is disposable research — it serves one purpose (next board meeting / next investor call / next 30-day plan) and is honest about it.

**MiroFish angle:** The files are .md, so they ingest directly. No code changes needed.

**Risk:** It's a one-time artifact. If the business survives 90 days, it's stale and you do this again.

### Shape B: "Evidence Layer With Transformation Pipeline"

**What it is:** Build an explicit transformation layer (likely a Python script or notebook) that converts the 11 JSON data-package files into provenance-bearing markdown documents with embedded metadata (source file, extraction date, record count, field coverage). Add a curation pass over 009 research that tags each file's provenance tier (primary source, LLM-with-citations, LLM-synthesis-only). Package everything into a MiroFish-ready corpus directory.

**Output:** A `research-corpus/` directory with 20-30 files, a `corpus-inventory.yaml` with provenance metadata, transformation scripts, and a README explaining freshness and quality tiers.

**Why it fits:** It directly solves the JSON→MiroFish gap, creates a repeatable process, and makes the quality tiers explicit (addressing R2, R3, R5).

**Risk:** It's engineering work disguised as research. The spec says "not building a permanent ETL" is out of scope. Where's the line?

### Shape C: "Cross-Repo Evidence Graph With Contradiction Map"

**What it is:** Rather than producing documents, produce a structured evidence graph (could be a JSON knowledge graph or a set of linked markdown files) where each node is a claim, each edge is a support/contradict/unknown relationship, and each claim is annotated with its source tier. The graph explicitly maps where internal data (Pipedrive win rates, QBO financials, Forecast capacity) supports or contradicts external market claims (from 009 research).

**Output:** An evidence graph (JSON or markdown-linked), a contradiction report, a "confidence dashboard" showing which strategic claims have strong vs. weak evidentiary backing, and intake instructions for MiroFish.

**Why it fits:** This directly addresses R4 (cross-system questions) and R5 (contradictions explicit) in a way that Shapes A and B don't. It also gives MiroFish something richer than flat documents — it could drive a future "evidence-weighted" Strategy Lab.

**Risk:** Highest complexity. Might over-engineer the immediate need. Requires defining the ontology of "claims" and "evidence types" before you can build it.

---

## CONCRETE VERIFICATION PERFORMED

| Check | Result | Implication |
|-------|--------|-------------|
| MiroFish FileParser SUPPORTED_EXTENSIONS | `{'.pdf', '.docx', '.md', '.markdown', '.txt'}` — no .json | R1+R7 are incompatible without a transformation layer |
| corpus_manifest.json source count | 3 documents, 67 chunks (5+41+21) | Spec's claim is accurate |
| data-package JSON file count | 11 .json files + 2 .md files + 1 .md brief = 14 files total, 580K | Substantial raw data exists but none is ingestible as-is |
| 009 research files named after AI tools | 4 of 26 explicitly (`Gemini-`, `Perplexity-`, `deep-research-*`) | "Higher quality" bar needs a falsifiable definition |
| 009 research files citing named analysts | 18 of 26 files contain Gartner/IDC/etc. references | Citations exist but were AI-mediated, not primary |
| QBO cash position | $19,454.91, 0 months runway, -$608K net income | Urgency context missing from spec requirements |

---

## BOTTOM LINE

The spec correctly diagnoses the input quality problem but underspecifies three things: (1) how JSON data becomes MiroFish-ingestible without losing provenance, (2) what "decision-grade" means in falsifiable terms, and (3) how the urgency of $19K cash should constrain the shape.

I'd push hardest on Shape A (war room package) as the minimum viable shape, with Shape B's transformation scripts as a second pass if there's time. Shape C is the right long-term answer but wrong for a company measuring runway in days, not months.

What's your response to the JSON ingest gap and the urgency prioritization?
```

### RedUnion → RedGrove `[PHASE:revise]`

```text
Your challenge is right on the core tensions. I verified them locally:
- `backend/app/utils/file_parser.py:71` only supports `.pdf .docx .md .markdown .txt`
- `quickbooks/specs/009-market-intelligence/research/` has 26 markdown files, with at least 4 explicitly AI-named files
- `08-qbo-financial-summary.json` really shows cash `19454.91`, burn `397455.67`, runway `0`

I am revising the shaping around those facts instead of defending the old spec.

## Revised Requirements (R)

| ID | Requirement | Status |
|----|-------------|--------|
| R0 | Produce a research package that directly supports an actual leadership decision in the current cash crisis, not just a better archive. | Core goal |
| R1 | Raw internal operating evidence from QuickBooks, Pipedrive, and Forecast must remain first-class source material, even if a transformed view is created for MiroFish ingestion. | Must-have |
| R2 | Any transformation from raw JSON/data into MiroFish-ingestible documents must preserve reversible provenance: source file, extraction date, row/record counts, and transformation method. | Must-have |
| R3 | External research must be tiered by evidence quality. Major claims may only rely on named primary or attributable secondary sources; AI syntheses can provide context but not stand alone as proof. | Must-have |
| R4 | The package must clearly separate 30-90 day survival/triage questions from 6-24 month strategic positioning questions. | Must-have |
| R5 | Contradictions, unsupported beliefs, and freshness limits must be explicit and easy to inspect. | Must-have |
| R6 | The human-readable deliverable must be strong enough that leadership can act without opening raw JSON, while still linking back to evidence. | Must-have |
| R7 | The final corpus must be ingestible by current MiroFish without requiring product changes in v1. | Must-have |
| R8 | v1 must stay bounded: no permanent warehouse, no new MiroFish ingest code, no pretending this research is a long-term data platform. | Must-have |

## Shapes

### A: 72-Hour Leadership War Room Package
| Part | Mechanism | Flag |
|------|-----------|:----:|
| A1 | Inventory the existing internal data-package and 009 research corpus, then manually curate only the most decision-relevant evidence. | |
| A2 | Convert the needed raw JSON facts into annotated markdown tables by hand or one-off scripts, with source-path footers. | |
| A3 | Produce a leadership memo split into survival, near-term revenue, and strategic bets. | |
| A4 | Export the same memo + appendix bundle as MiroFish-ingestible markdown. | |

### B: Portable Evidence Bundle Builder
| Part | Mechanism | Flag |
|------|-----------|:----:|
| B1 | Define a source inventory and evidence-tier rubric covering internal raw data, prior syntheses, and new external research. | |
| B2 | Build a bounded transformation layer that converts selected raw JSON/data into markdown evidence docs while retaining raw snapshots and record counts. | |
| B3 | Curate external research into tiered source docs, explicitly quarantining AI-synthesis-only material from claim anchors. | |
| B4 | Emit a portable multi-file corpus: raw snapshot index, transformed evidence docs, contradiction register, and leadership memo. | |
| B5 | Feed the same corpus to MiroFish using existing `.md/.docx/.pdf/.txt` intake only. | |

### C: Evidence Graph / Contradiction Map
| Part | Mechanism | Flag |
|------|-----------|:----:|
| C1 | Represent strategic claims as nodes with support/contradict/unknown links to internal and external evidence. | ⚠️ |
| C2 | Generate confidence and contradiction views from the graph. | ⚠️ |
| C3 | Export graph-derived narrative summaries for leadership and MiroFish. | ⚠️ |

### D: Timeboxed Hybrid Bundle
| Part | Mechanism | Flag |
|------|-----------|:----:|
| D1 | Reuse B1-B3 to create a strict evidence-tiered, provenance-bearing corpus. | |
| D2 | Reuse A3 to produce an immediate leadership memo split into 30/90-day triage vs strategic options. | |
| D3 | Reuse B5 to make the same corpus MiroFish-ingestible with no product changes. | |
| D4 | Ship a contradiction register and “what we know vs what we’re inferring” summary as first-class artifacts. | |

My current belief is:
- A fits urgency but fails repeatability/provenance depth.
- B fits provenance/reuse but risks over-rotating into pipeline work.
- C is long-term-correct but too abstract and too slow for current cash reality.
- D is probably the right selected shape if it cleanly passes the fit check.

Please challenge this revised R/S set. If it still has holes, keep pushing with [PHASE:challenge]. If you think it now holds, answer with [PHASE:approved] and call out any last edge conditions I still need in the fit check or breadboard.
```

### YoungViper → RedUnion `[PHASE:approved]`

```text
I've verified the revised R0–R8 requirements and Shapes A–D against the live data. The set holds. Here's what I checked and why I'm satisfied:

Verified facts against live sources:

1. FileParser constraint confirmed — `file_parser.py` line: `SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.md', '.markdown', '.txt'}`. No JSON. R7 + R8's mandate for markdown transformation without new ingest code is correctly scoped.

2. Cash position confirmed — `08-qbo-financial-summary.json`: cash $19,454.91, monthly burn $397,455.67, runway 0. R0's urgency framing and R4's triage/strategy split are not optional — they're existential. Worth noting: AR outstanding is $242,641 with $226,465 current (0-day aging). That's 11.6× the cash position. The triage memo component of Shape D should foreground AR collection as the primary survival lever. Not a requirements gap — R0 + R4 cover it — but a critical execution detail.

3. AI provenance is worse than filename scan suggests — I ran a deeper audit. Of 26 research markdown files, 6 have explicit AI tool markers in filename or header (Gemini, Perplexity, pplx, deep-research), but many "clean" files also reveal AI origin: `research-fortune500-xr-2024-2025.md` says "compiled from training knowledge (cutoff early 2025)", `research-military-xr-contracts-2025.md` says "Generated: 2026-03-18". Realistic count of AI-generated files is 15-20 of the 26. R3's tiered quality requirement (AI syntheses cannot stand alone as proof) correctly addresses this. Without R3, the evidence bundle would be a circular loop of AI summarizing AI.

4. JSON data-package is real and substantial — 11 JSON files totaling ~520KB of actual operating data (pipeline, won deals, lost deals, capacity, AR, financials). These are the genuinely first-class evidence sources R1 demands. The transformation layer from R2 (reversible provenance) is the right mechanism to convert these to MiroFish-ingestible markdown without losing origin.

5. Existing 67-chunk corpus confirmed as thin — The spec correctly identifies that 3 docs → 67 chunks (5+41+21) was mostly re-organizing existing synthesis. The revised requirements demand materially richer inputs.

Requirement-by-requirement verdict:
- R0 ✅
- R1 ✅
- R2 ✅
- R3 ✅
- R4 ✅
- R5 ✅
- R6 ✅
- R7 ✅
- R8 ✅

Shape verdict:
Shape D (timeboxed hybrid) is clearly the winner. It's the only shape that simultaneously addresses urgency, evidence rigor, intellectual honesty, and technical compatibility.

No remaining objections.
```
