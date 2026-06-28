---
title: Claude Code plugin marketplace
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [claude-code, plugins, marketplace, distribution]
status: stable
---

# Claude Code plugin marketplace

The distribution and discovery layer for [[claude-code-plugin]]s — a git repo (or hosted
JSON) whose `.claude-plugin/marketplace.json` catalogs installable plugins, added with
`/plugin marketplace add` and installed from with `/plugin install <name>@<marketplace>`.

## Summary
A marketplace turns scattered plugin repos into a browsable catalog. Each registered
marketplace is recorded locally in `~/.claude/plugins/known_marketplaces.json` and checked
out under `~/.claude/plugins/marketplaces/<name>/`; its `marketplace.json` manifest is the
list of entries shown in `/plugin > Discover`. [[claude-plugins-official]] is the official
Anthropic instance and the only one registered on this machine. _Mechanics here were read
from the live registry and the marketplace `README.md` on 2026-06-28._

## Details
- **Adding / installing.** `/plugin marketplace add <git-repo-or-url>` registers a
  marketplace; `/plugin install <name>@<marketplace>` installs an entry from it.
- **Local registry.** `known_marketplaces.json` maps each marketplace to its `source`
  (e.g. `{source: github, repo: anthropics/claude-plugins-official}`), `installLocation`,
  and `lastUpdated`.
- **Trust tiers.** A marketplace may separate first-party plugins (`/plugins`) from
  third-party ones (`/external_plugins`); the host vendor does not control or guarantee
  third-party entries, so trust is the installer's responsibility.
- **Strict mode / skill bundles.** When a source repo ships `SKILL.md` skills without a
  plugin manifest, a marketplace entry can declare them directly with `strict: false` plus an
  explicit `skills: [...]` array over a `git-subdir` source. Each path points at a directory
  containing a `SKILL.md`, registered as `<plugin-name>:<skill-name>`.

## Related
- [[claude-plugins-official]] — the official marketplace; a concrete instance of this concept
- [[claude-code-plugin]] — what the catalog entries install
- [[claude-code]] — the host tool that registers and reads marketplaces

## Open questions
- Update cadence / how a registered marketplace is refreshed beyond the recorded
  `lastUpdated`.
