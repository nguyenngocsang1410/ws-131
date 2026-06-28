---
title: Claude Code
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [claude-code, anthropic, cli, tooling, agent]
status: stable
---

# Claude Code

Anthropic's official agentic command-line tool for software engineering — and the host
program that loads the [[claude-plugins-official]] marketplace this wiki now catalogs. It is
also the tool that maintains this wiki.

## Summary
Claude Code is an interactive CLI agent (also available as desktop, web, and IDE-extension
front ends) that reads/edits code, runs commands, and drives multi-step engineering tasks.
It is **extensible**: behaviour can be added without forking the tool, through five surfaces —
**slash commands**, **subagents**, **skills**, **hooks**, and **MCP servers**. A
[[claude-code-plugin]] is the package format that bundles those surfaces; a
[[claude-code-plugin-marketplace]] is how plugins are discovered and installed. _(General
knowledge of Claude Code is marked as such; the plugin/marketplace specifics on this page and
its links were verified against the live install on 2026-06-28.)_

## Details
Extension surfaces relevant to plugins:

| Surface | What it adds | Where it lives in a plugin |
|---|---|---|
| Slash commands | `/name` commands | `commands/*.md` |
| Subagents | specialized agents the Agent tool can spawn | `agents/*.md` |
| Skills | model-invoked capability bundles (`SKILL.md`) | `skills/<name>/` |
| Hooks | shell handlers fired at lifecycle events | `hooks/` |
| MCP servers | external tool/data connections | `.mcp.json` |

Locally, installed marketplaces are registered in
`~/.claude/plugins/known_marketplaces.json` and checked out under
`~/.claude/plugins/marketplaces/`. On this machine exactly one marketplace is registered —
[[claude-plugins-official]] — and `/reload-plugins` reported **2 plugins** enabled (one being
`claude-code-setup`, whose `claude-code-setup:claude-automation-recommender` skill then
appeared).

## Related
- [[claude-code-plugin]] — the package format that extends this tool
- [[claude-code-plugin-marketplace]] — how plugins are distributed and installed
- [[claude-plugins-official]] — the one marketplace registered on this machine
- [[2026-06-28-claude-plugins-marketplace-map]] — the session that compiled this domain

## Open questions
- Exact version of Claude Code running on this host (not recorded this session).
- Which **2** plugins are enabled beyond the confirmed `claude-code-setup`.
