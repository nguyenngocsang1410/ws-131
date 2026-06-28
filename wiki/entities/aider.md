---
title: Aider
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [aider, cli, agent, open-source, local-model, tool]
status: stable
---

# Aider

Open-source command-line AI pair-programming agent; the cleanest free path to running a
coding agent on a **local** model.

**Type:** CLI · **License:** open-source (free) · **Local model:** ✅ native

## Summary
Mature terminal agent that edits a git repo through an LLM. Model-agnostic via LiteLLM, so
it talks to cloud APIs **or** a local runner — `aider --model ollama/qwen2.5-coder` points
it at a local [Ollama](https://ollama.com) model with no proxy. Because the tool is
open-source and the model can be local, the whole stack can be free and offline (see
[[local-model-coding-agent]]).

## Details
- One of the recommended "free + install + local model" CLI agents in [[ai-coding-agents]].
- Contrast with [[claude-code]], which needs an Anthropic-format proxy to use a local model.

## Related
- [[ai-coding-agents]] — landscape it sits in
- [[local-model-coding-agent]] — recommended starting point there
- [[goose-agent]], [[opencode]], [[openai-codex-cli]] — peer CLI agents

## Open questions
- Not installed on this host; capability profile only, not measured here.
