# raw/ — Immutable Sources

Drop source material here for the LLM to ingest: articles, PDFs, transcripts, pasted
notes, code dumps, exported threads, anything.

**Rules**

- This directory is **immutable to the LLM** — it reads these files but never edits them.
- One file per source. Use descriptive, stable filenames (`2026-04-karpathy-llm-wiki.md`).
- Everything in `wiki/` traces its provenance back to a file here.

**To ingest**: add a file here, then tell your coding agent to "ingest `raw/<file>`".
The agent will read it, discuss takeaways, and compile it into `wiki/` per the workflow in
`../CLAUDE.md`.
