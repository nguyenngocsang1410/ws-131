---
title: Claude Code plugin
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [claude-code, plugins, extensibility, anatomy]
status: stable
---

# Claude Code plugin

A self-contained, shareable package that extends [[claude-code]] by bundling slash commands,
subagents, skills, hooks, and/or MCP servers behind a single manifest — so capability moves
between projects and teams as one installable unit instead of hand-copied config.

## Summary
Rather than configuring each repo by hand, a plugin packages one or more extension surfaces
once and installs everywhere. Plugins are discovered and installed through a
[[claude-code-plugin-marketplace]] (e.g. [[claude-plugins-official]]) and managed with the
`/plugin` command; `/reload-plugins` re-reads them in an active session. _Anatomy below is
from the `claude-plugins-official` `README.md`, read on 2026-06-28._

## Anatomy
A plugin is a directory with this standard layout:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # metadata: name, version, description, author (REQUIRED)
├── .mcp.json            # MCP server configuration (optional)
├── commands/            # slash commands (optional)
├── agents/              # subagent definitions (optional)
├── skills/              # skill definitions, each a SKILL.md (optional)
└── README.md            # documentation
```

- **`.claude-plugin/plugin.json`** is the only required file; everything else is opt-in.
- A plugin can ship **any combination** of the surfaces — commands-only, an MCP-server
  wrapper, a skills bundle, etc.
- **Skills register namespaced** as `<plugin-name>:<skill-name>` in Claude Code. Observed
  live this session: installing `claude-code-setup` surfaced the skill
  `claude-code-setup:claude-automation-recommender`.

## Install & manage
- `/plugin` — interactive UI to Discover, install, enable/disable, remove.
- `/plugin install <name>@<marketplace>` — install a specific entry.
- `/reload-plugins` — reload plugins/agents/skills/hooks/MCP without restarting.
- Only what you install is active; the marketplace catalog is just the menu.

## Related
- [[claude-code-plugin-marketplace]] — how plugins are distributed/installed
- [[claude-plugins-official]] — the official catalog of plugins
- [[claude-code]] — the host tool and the extension surfaces a plugin fills

## Open questions
- Precedence/conflict rules when two plugins define the same command or skill name.
