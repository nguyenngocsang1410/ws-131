---
title: "Session: AI coding-agents survey (alternatives to Claude Code)"
type: source
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ai-agents, coding-agents, survey, session, provenance]
status: stable
---

# Session: AI coding-agents survey (alternatives to Claude Code)

Provenance record for the 2026-06-28 Claude Code session that surveyed AI coding-agent
software besides Claude Code, then ingested it into the wiki.

## Summary
The human asked, in sequence: what other agent software exists besides the Claude Code
CLI; which can be run **offline and free**; whether Claude Code itself can be installed
against a third-party API; and finally to **classify the agents by Type** (CLI / IDE /
Cloud / Framework) and ingest the result. This extends the wiki's existing **Claude Code
tooling** domain (alongside [[claude-code]], [[claude-plugins-official]]) with a
cross-vendor agent landscape.

## What this source is (and its provenance caveat)
This is **general-knowledge synthesis**, not a `raw/` document — there is no source file to
trace claims to. The assistant's knowledge cutoff is **January 2026** and this space moves
fast, so per-tool details (especially proprietary tools' local-model / BYOK features) are
marked as needing re-verification. **Exception:** the Claude-Code-specific backend facts
were **verified against official Claude Code docs** (env-vars / llm-gateway / data-usage
pages) via a `claude-code-guide` subagent during the session.

## Key takeaways
- Agents sort into four **Types**: **CLI**, **IDE**, **Cloud**, **Framework/SDK** —
  see [[ai-coding-agents]] for the full comparison table.
- "Free + offline" = open-source tool **and** a local model backend. The natively-local,
  open-source agents ([[aider]], [[goose-agent]], [[opencode]], [[openai-codex-cli]],
  [[cline]], [[continue-dev]]) are the clean fits; how-to in [[local-model-coding-agent]].
- [[claude-code]] **can** use third-party/custom backends (Bedrock/Vertex/Foundry/AWS
  flags, or any Anthropic-Messages-compatible endpoint via `ANTHROPIC_BASE_URL` + auth),
  and a local model **via an Anthropic-format proxy** — but it is proprietary and not
  designed for fully-offline use, so it is the *harder* free+local path.
- Cursor / Windsurf / Copilot remain cloud-tethered; Devin / Jules / Factory are paid cloud.

## Related
- [[ai-coding-agents]] — the landscape page this session produced
- [[local-model-coding-agent]] — the free+offline how-to
- [[claude-code]] — updated this session with third-party/local-model backend facts
- [[internet-lockdown-vsi]] — why an offline agent is relevant on this host

## Open questions
- Nothing installed or benchmarked on this host; the survey is capability-based.
- Proprietary tools' local-model support is the least-certain part (cutoff Jan 2026).
