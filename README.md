# LLM Wiki

A persistent, self-maintaining knowledge base built on **Andrej Karpathy's LLM Wiki
pattern**. Rather than running RAG over raw documents on every question, an LLM agent
*compiles* your sources once into a structured, interlinked set of markdown pages, then
answers all queries against that compiled wiki. Knowledge **compounds** instead of being
re-derived each session.

It's just plain markdown + any coding agent (Claude Code, Codex, Cursor). Best for
personal knowledge bases up to ~100k tokens.

## Layout

```
.
├── CLAUDE.md          # the schema: how the wiki works + ingest/query/lint workflows
├── raw/               # immutable sources you curate (the LLM reads, never edits)
└── wiki/              # the LLM-compiled knowledge base
    ├── index.md       # catalog of every page — the entry point for queries
    ├── log.md         # append-only record of every operation
    ├── entities/      # people, orgs, products, tools, datasets
    ├── concepts/      # ideas, methods, definitions, claims
    └── sources/       # one page per ingested source
```

## How to use

1. **Curate** — drop a source into `raw/`.
2. **Ingest** — tell your agent: *"ingest `raw/<file>`"*. It reads, discusses takeaways,
   and writes/updates ~10–15 wiki pages (sources + entities + concepts), then updates
   `index.md` and `log.md`.
3. **Query** — ask a question. The agent searches `wiki/` and answers with citations.
4. **Lint** — periodically say *"lint the wiki"* to catch contradictions, stale claims,
   orphan pages, and broken links.

**Division of labor:** you curate sources, direct the analysis, and ask good questions.
The LLM does everything else — reading, summarizing, cross-referencing, and upkeep.

The full operating manual lives in [`CLAUDE.md`](./CLAUDE.md).

## Credit

Based on Andrej Karpathy's LLM Wiki gist (April 2026):
<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
