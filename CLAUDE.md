# LLM Wiki — Schema & Operating Manual

This repository is an **LLM Wiki** (Karpathy's pattern): a persistent, self-maintaining
knowledge base. Instead of doing RAG over raw documents at query time, you (the LLM)
**compile** knowledge once into a structured, interlinked set of markdown pages, then
answer all questions against that compiled artifact. Knowledge compounds; it is not
re-derived each session.

You own the `wiki/` directory. The human owns curation and direction. The division of
labor: **the human curates sources, directs analysis, and asks questions; you do
everything else** — reading, summarizing, cross-referencing, consistency-checking, and
maintenance.

---

## Wiki-first

**For every question and every task, consult the wiki before any other source — your own
memory included.** This is the operating default, not just the Query workflow.

1. **Start at `wiki/index.md`.** It is the catalog and the entry point. Read it first,
   every session, before you answer or act.
2. **Follow its links.** Open the relevant `entities/`, `concepts/`, and `sources/` pages
   and read them. Grep page bodies when the index doesn't pinpoint the page.
3. **Answer from the wiki, with citations.** Synthesize from the compiled pages and cite
   them. The wiki — not your training-data recall, not the raw documents — is the source
   you answer from by default.
4. **Fall back deliberately, then compile.** Only when the wiki genuinely lacks the answer
   do you reach for `raw/` or general knowledge — and say so when you do. Then write what
   you learned back into the wiki so the next query is answered from the wiki, not
   re-derived.

Skipping the wiki to answer from memory or straight from `raw/` defeats the whole pattern:
the point is to do retrieval **once**, into the wiki, then respect the wiki as the compiled
source of truth.

---

## Three layers

| Layer | Directory | Owner | Mutability |
|-------|-----------|-------|------------|
| **Raw sources** | `raw/` | Human curates | **Immutable** — read, never edit |
| **The wiki** | `wiki/` | You (LLM) | You create, edit, delete freely |
| **The schema** | `CLAUDE.md` (this file) | Shared | Evolves as the wiki grows |

### `raw/`
Immutable source material the human drops in: articles, PDFs, transcripts, notes, code
dumps, pasted text. **Never modify a file in `raw/`.** Every wiki claim must be traceable
back to a `raw/` source (or be explicitly marked as your own synthesis/inference).

### `wiki/`
Your compiled output. Plain interlinked markdown, organized by category:

- `wiki/entities/` — concrete things: people, organizations, products, places, datasets, tools.
- `wiki/concepts/` — ideas, methods, definitions, claims, mental models, open questions.
- `wiki/sources/` — one page per ingested `raw/` source: summary, key takeaways, links out.
- `wiki/index.md` — the catalog of every page (see below).
- `wiki/log.md` — append-only chronological record of operations (see below).

Add new category folders when a domain clearly warrants one (e.g. `wiki/events/`,
`wiki/decisions/`). Note the addition in this schema when you do.

---

## Page conventions

Every wiki page is a markdown file with YAML frontmatter:

```markdown
---
title: Human-readable title
type: entity | concept | source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw/some-file.md, raw/another.pdf]   # provenance for this page
tags: [tag-a, tag-b]
status: draft | stable | needs-review
---

# Title

One-sentence definition / what this page is.

## Summary
2–6 sentences. The compiled, current best understanding.

## Details
Substantive content. Cite sources inline as `[^raw/file]` or "(per [[source-page]])".
Link related pages with `[[page-name]]` (the filename without `.md`).

## Related
- [[other-page]] — why it's related
- [[another-page]]

## Open questions
- Anything unresolved, contradictory, or unverified.
```

Rules:
- **Interlink aggressively.** Use `[[wiki-link]]` syntax referencing a page's filename
  (without `.md` or directory). A link to a page that doesn't exist yet is a valid TODO —
  it marks a page worth creating.
- **Cite provenance.** Every non-obvious claim traces to a `raw/` source or a `sources/`
  page. Mark your own inferences as inference. Never silently invent facts.
- **One concept per page.** Prefer many small interlinked pages over few large ones.
  Keep the whole wiki comfortably under ~100k tokens; split or summarize when it grows.
- **Filenames** are kebab-case, descriptive, stable: `wiki/concepts/three-layer-architecture.md`.
  Renaming a page means updating every `[[link]]` to it (do this — that's your job).

---

## Workflows

You run one of three operations per session. State which at the start.

### 1. Ingest  — process a new source
Trigger: the human adds a file to `raw/` (or says "ingest X").

1. **Read** the raw source fully.
2. **Discuss** the key takeaways with the human before writing — confirm framing, surface
   what's new vs. what the wiki already knows.
3. **Write a source page** in `wiki/sources/` (summary + takeaways + links out).
4. **Create or revise entity/concept pages** the source touches. A single source typically
   touches **10–15 wiki pages** — create stubs for new entities/concepts, update existing
   ones, add cross-links both directions.
5. **Update `wiki/index.md`** with any new pages.
6. **Append to `wiki/log.md`**: `## [YYYY-MM-DD] ingest | <source title>` + a line on what changed.

### 2. Query — answer a question
Trigger: the human asks a question.

1. **Search the wiki** (`index.md` first, then grep page bodies) for relevant pages.
2. **Synthesize** an answer from those pages, **with citations** to the specific wiki/raw
   pages used. If the wiki can't answer, say so and propose ingesting a source.
3. **Optionally file the answer back** as a new concept page if it's reusable knowledge —
   good answers become permanent wiki pages.

### 3. Lint — health-check the wiki
Trigger: the human says "lint", or periodically after several ingests.

Scan for and report (and fix where unambiguous):
- **Contradictions** — pages that disagree on a fact.
- **Stale claims** — content outdated by a newer source.
- **Orphan pages** — pages nothing links to.
- **Broken / dangling links** — `[[links]]` to non-existent pages (decide: create or remove).
- **Missing cross-references** — related pages that should link but don't.
- **Data gaps** — questions raised but never answered; thin stubs.
- **Index drift** — pages missing from `index.md`, or index entries with no page.

Append results: `## [YYYY-MM-DD] lint` + findings in `wiki/log.md`.

---

## Special files

### `wiki/index.md`
A content-oriented catalog of every page, grouped by category. Each entry: link, one-line
summary, and key metadata (e.g. updated date, status). **Update on every ingest.** This is
the entry point for Query — read it first.

### `wiki/log.md`
Append-only, chronological, machine-parseable. One entry per operation, newest at the
bottom, consistent prefix:

```
## [2026-06-28] ingest | <source title>
- created: [[page-a]], [[page-b]]
- updated: [[page-c]]

## [2026-06-28] lint
- fixed 2 dangling links; flagged 1 contradiction in [[page-d]]
```

Never rewrite history here — only append.

---

## Principles

- **Wiki-first.** Consult the wiki — starting at `index.md` — before answering anything or
  reaching for `raw/` or your own memory. See the [Wiki-first](#wiki-first) rule above.
- **Compile, don't retrieve.** Do the synthesis work once, up front; queries hit the
  compiled wiki, not raw documents.
- **Knowledge compounds.** Each ingest makes the next query smarter. Prefer updating
  existing pages over duplicating.
- **The wiki is the source of truth for understanding; `raw/` is the source of truth for facts.**
  When they conflict, `raw/` wins and you fix the wiki.
- **Curate ruthlessly.** Delete, merge, and split pages to keep the wiki coherent and small.
- **This schema is yours to evolve.** As the domain takes shape, refine categories, page
  templates, and conventions here — and log the change.
