---
title: AI coding agents (landscape)
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ai-agents, coding-agents, cli, ide, framework, landscape, comparison, open-source, local-model]
status: stable
---

# AI coding agents (landscape)

The landscape of AI coding-agent software, classified by **Type** (CLI / IDE / Cloud / Framework) and by whether each is free to install, open-source, and able to run against a **local** model.

## Summary
[[claude-code]] is one of many AI coding agents. This page catalogs the alternatives and
sorts them on the two axes that matter for running one **free and offline**: is the tool
itself open-source/free, and can it talk to a **local** open-weight model (via Ollama /
llama.cpp / vLLM) instead of a paid cloud API. The clean "free + local" fits are the
open-source CLI/IDE agents that speak to a local model **natively, with no proxy** — a
*lower-friction* path than Claude Code, which is proprietary and needs an Anthropic-format
proxy in front of a local model. See [[local-model-coding-agent]] for the actual setup
(and how it interacts with this machine's [[internet-lockdown-vsi]]).

_Provenance: compiled in a 2026-06-28 Claude Code session from general knowledge
(assistant cutoff Jan 2026 — this space moves fast, treat per-tool details as needing a
re-check). The Claude-Code-specific backend facts were verified against official Claude
Code docs (per [[2026-06-28-ai-coding-agents-survey]])._

## The Type taxonomy
- **CLI** — runs in the terminal; drives edits/commands in a repo. (Claude Code's form.)
- **IDE** — integrated into an editor, either a standalone AI editor or an extension.
- **Cloud** — async/autonomous SaaS agents you hand a task to; run on the vendor's servers.
- **Framework / SDK** — libraries for *building* your own agents, not ready-to-use assistants.

The frontmatter `type:` of every wiki page is still `entity`/`concept`/`source`; the
Type above is a **content attribute** of each agent, shown per row below and on each
agent's entity page as a `**Type:**` line.

## Comparison — "can I install it free and run it on a local model?"
Legend: ✅ yes · ⚠️ partial / with caveats · ❌ no.

### CLI agents
| Agent | Type | Free to install | Open-source | Local model | Note |
|---|---|---|---|---|---|
| [[claude-code]] | CLI (+IDE/desktop/web) | ✅ (binary) | ❌ proprietary | ⚠️ only via Anthropic-format proxy | needs a translation proxy |
| [[aider]] | CLI | ✅ | ✅ | ✅ native (Ollama/LiteLLM) | cleanest free+local CLI |
| [[goose-agent]] | CLI (+desktop) | ✅ | ✅ | ✅ native | by Block |
| [[opencode]] | CLI | ✅ | ✅ | ✅ native (OpenAI-compatible) | provider-agnostic |
| [[openai-codex-cli]] | CLI | ✅ | ✅ (Apache) | ✅ via OpenAI-compatible base URL | OpenAI's open CLI |
| Gemini CLI | CLI | ✅ | ✅ (Apache) | ⚠️ Gemini-centric | local only via workarounds |
| Amazon Q Developer CLI | CLI | ✅ (free tier) | ❌ | ❌ Bedrock-bound | AWS |

### IDE agents
| Agent | Type | Free to install | Open-source | Local model | Note |
|---|---|---|---|---|---|
| [[cline]] | IDE (VS Code) | ✅ | ✅ | ✅ native (Ollama/LM Studio) | |
| Roo Code | IDE (VS Code) | ✅ | ✅ | ✅ native | a Cline fork |
| [[continue-dev]] | IDE (VS Code/JetBrains) | ✅ | ✅ | ✅ native | |
| Cursor | IDE (standalone editor) | ⚠️ free tier | ❌ | ❌ cloud-tethered | custom keys still route via Cursor |
| Windsurf | IDE (standalone editor) | ⚠️ free tier | ❌ | ❌ cloud-bound | Codeium |
| GitHub Copilot | IDE (+cloud agent) | ⚠️ free tier, needs account | ❌ | ⚠️ some Ollama/BYOK in Chat | still needs Copilot auth |
| JetBrains Junie / AI Assistant | IDE | ⚠️ paid / free tier | ❌ | ❌ | |

### Cloud / autonomous agents
| Agent | Type | Free | Open-source | Local model | Note |
|---|---|---|---|---|---|
| Devin (Cognition) | Cloud | ❌ paid | ❌ | ❌ | autonomous SWE |
| Google Jules | Cloud | ⚠️ beta/free tier | ❌ | ❌ | async |
| Factory (Droids) | Cloud | ❌ paid | ❌ | ❌ | |
| GitHub Copilot coding agent | Cloud | ❌ paid | ❌ | ❌ | |

### Frameworks / SDKs (for building agents, not ready-to-use)
| Tool | Type | Free | Open-source | Local model | Note |
|---|---|---|---|---|---|
| Claude Agent SDK | Framework | ✅ | ✅ | ⚠️ Anthropic-format | build-your-own |
| OpenAI Agents SDK | Framework | ✅ | ✅ | ⚠️ OpenAI-compatible | |
| LangGraph / LangChain | Framework | ✅ | ✅ | ✅ | model-agnostic |
| Microsoft AutoGen | Framework | ✅ | ✅ | ✅ | |
| CrewAI | Framework | ✅ | ✅ | ✅ | multi-agent |
| smolagents (Hugging Face) | Framework | ✅ | ✅ | ✅ | |
| Pydantic AI | Framework | ✅ | ✅ | ✅ | |

## Verdict
- **Best "free + install + local model" fits:** the open-source CLI/IDE agents — [[aider]],
  [[goose-agent]], [[opencode]], [[openai-codex-cli]] (CLI) and [[cline]], Roo Code,
  [[continue-dev]] (IDE). They take a local model natively, no proxy, and cost nothing.
- **Claude Code is the *harder* free+local path,** not the easiest: proprietary tool + you
  must run an Anthropic-format proxy (e.g. LiteLLM / claude-code-router) in front of the
  local model. Detail on [[claude-code]].
- **Cursor / Windsurf / Copilot** stay cloud-tethered; **Devin / Jules / Factory** are paid
  cloud SaaS — none qualify as free+offline.

## Related
- [[local-model-coding-agent]] — how to actually run one free+offline on this machine
- [[claude-code]] — the anchor / the tool that maintains this wiki
- [[aider]], [[goose-agent]], [[opencode]], [[openai-codex-cli]], [[cline]], [[continue-dev]] — the realistic free+local candidates
- [[internet-lockdown-vsi]] — why an offline-capable agent is relevant on this host

## Open questions
- Fast-moving space; the proprietary tools' local-model/BYOK features (Copilot, Cursor)
  change often — re-verify before relying on a row here.
- No agent benchmarked on this machine yet; "best" is by capability profile, not measured.
