---
title: "Session: mapping the claude-plugins-official marketplace"
type: source
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [claude-code, plugins, marketplace, session, source]
status: stable
---

# Session: mapping the claude-plugins-official marketplace

## What this is
A live Claude Code session (2026-06-28) that inventoried and mapped the
[[claude-plugins-official]] plugin marketplace installed on this machine, then ingested it
into the wiki as a **new "Claude Code tooling" domain** — distinct from the wiki's existing
CONTACT PLM / Ansible material. The human asked to "summarize claude-plugins-offical", then
"create a map", then "add description and ingest to wiki".

## Provenance
Live inspection (no `raw/` file) of the on-disk marketplace:

- `~/.claude/plugins/known_marketplaces.json` — the local marketplace registry.
- `~/.claude/plugins/marketplaces/claude-plugins-official/` — the checked-out marketplace:
  - `README.md` — trust tiers, install flow, plugin anatomy, strict-mode skill bundles.
  - `.claude-plugin/marketplace.json` — the **240**-entry catalog (parsed for counts/categories).
  - `plugins/` (37 dirs) and `external_plugins/` (15 dirs).
- `/reload-plugins` output in-session: **2 plugins · 6 agents** enabled.

General knowledge of Claude Code itself is marked as such on the pages; all counts and
structural claims were read from the live files above.

## Key takeaways
1. `claude-plugins-official` is the **official Anthropic marketplace** (`anthropics/claude-plugins-official`),
   synced locally 2026-06-26.
2. Catalog = **240 entries**, two trust tiers: **37** first-party (`/plugins`) + third-party
   (`/external_plugins`, 15 local).
3. Biggest categories: **development 103**, productivity 45, database 33; then monitoring 13,
   security 13, smaller buckets, and 14 uncategorized.
4. A plugin bundles commands / subagents / skills / hooks / MCP behind a required
   `.claude-plugin/plugin.json`; skills register as `<plugin>:<skill-name>`.
5. Only **2** plugins are actually enabled here (one is `claude-code-setup`).

## Pages created from this source
- **entities:** [[claude-code]], [[claude-plugins-official]]
- **concepts:** [[claude-code-plugin]], [[claude-code-plugin-marketplace]]

## Open questions
- The catalog is a snapshot; entry counts drift over time.
- Which 2 plugins are enabled beyond the confirmed `claude-code-setup`.
- This domain currently has no `raw/` source — it rests on live-system inspection only.
