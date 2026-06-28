---
title: Running a coding agent free + offline on a local model
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [local-model, offline, ollama, coding-agents, open-source, how-to]
status: stable
---

# Running a coding agent free + offline on a local model

How to run an AI coding agent **free and fully offline** by pairing an open-source agent
(see [[ai-coding-agents]]) with a locally-hosted open-weight model — and what that means
on [[vsi-precision-3680]] under [[internet-lockdown-vsi]].

## Summary
"Free + offline" needs **two things together**: (1) the agent itself is open-source/free,
and (2) it can point at a **local** model runner so inference never leaves the box. The
open-source CLI/IDE agents do both with no proxy. [[claude-code]] can also be driven by a
local model, but only through an Anthropic-format proxy, and the tool stays proprietary —
the *harder* path.

## The recipe
1. **Model runner:** install **Ollama** (easiest; also llama.cpp / vLLM / LM Studio).
2. **Open-weight coding model:** e.g. Qwen2.5-Coder, DeepSeek-Coder-V2, or Codestral —
   sized to local hardware.
3. **Agent:** pick an open-source one that speaks to the runner natively —
   [[aider]] is the cleanest CLI starting point; [[goose-agent]], [[opencode]],
   [[openai-codex-cli]] are close alternatives; [[cline]] / [[continue-dev]] if you want
   it inside an editor.
4. Point the agent at the local endpoint (e.g. Aider: `--model ollama/qwen2.5-coder`) and
   work disconnected.

## The Claude Code variant
[[claude-code]] is *free to install but not open-source*. To run it on a local model you
set `ANTHROPIC_BASE_URL` to a local **Anthropic-Messages-compatible proxy** (LiteLLM /
claude-code-router) wrapping Ollama, and disable non-essential egress
(`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`, `DISABLE_TELEMETRY=1`, settings
`skipWebFetchPreflight: true`). It works, but it is a networked client by design — more
moving parts than the natively-local agents.

## Caveats
- **One-time internet** to download the agent + the model weights; offline only afterward.
- **Local hardware**: a capable coding model wants a real GPU or lots of RAM; quality/speed
  sit below frontier cloud models.
- Open-weight model quality < frontier (Claude/GPT/Gemini) — expect more hand-holding.

## On this machine ([[internet-lockdown-vsi]])
User [[vsi-user]] (uid 1000) is firewalled off the public internet. A local-model agent is
exactly what still functions under that lockdown **once set up** — but the lockdown also
blocks the *initial* agent/model download for `vsi`. So **stage the agent binary + model
weights from an unrestricted account first** (e.g. `vietnq37`), then run offline as `vsi`.
The lockdown is egress-by-uid and bypassable via `sudo` (see the caveat in
[[internet-lockdown-vsi]]), but for a normal `vsi` session it does block the download.

## Related
- [[ai-coding-agents]] — the full landscape + comparison table
- [[claude-code]] — the proprietary-tool-via-proxy variant
- [[aider]] — recommended free+local CLI starting point
- [[internet-lockdown-vsi]] — the egress block that makes "offline" relevant here
- [[vsi-precision-3680]] — the host

## Open questions
- Nothing installed/benchmarked yet — this is a plan, not a deployed setup on this host.
