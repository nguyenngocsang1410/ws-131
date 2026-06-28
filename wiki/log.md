# Wiki Log

Append-only, chronological record of every operation. Newest entries at the bottom.
Never rewrite — only append. Consistent prefixes so this stays parseable:

- `## [YYYY-MM-DD] ingest | <source title>`
- `## [YYYY-MM-DD] query | <question>`
- `## [YYYY-MM-DD] lint`

---

## [2026-06-28] init
- Scaffolded the LLM Wiki (Karpathy pattern): `raw/`, `wiki/{entities,concepts,sources}/`, `index.md`, `log.md`, `CLAUDE.md`.
- No sources ingested yet.
