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

## [2026-06-28] ingest | Session: Ansible workspace setup on vsi-Precision-3680
- Provenance: live Claude Code session (no raw/ file); facts verified by running commands on the host.
- created source: [[2026-06-28-ansible-workspace-setup]]
- created entities: [[vsi-precision-3680]], [[ansible]], [[pipx]], [[ansible-workspace]]
- created concepts: [[pipx-ansible-install]], [[ansible-become-via-env]], [[ansible-local-control-node]], [[ansible-yaml-stdout-callback]], [[ansible-facts-injection-deprecation]]
- updated: [[index]] (first real catalog entries)
- note: actual sudo password deliberately excluded from the wiki (secret).

## [2026-06-28] ingest | Session: Analysis of the /opt/contact CONTACT PLM deployment
- Provenance: live host inspection of `/opt/contact` + running services; copied artifacts in `raw/contact/` (read via [[contact-source-access-via-ansible]]).
- created source: [[2026-06-28-opt-contact-analysis]]
- created entities: [[contact-software-plm]], [[opt-contact]], [[cdb-platform]]
- created concepts: [[contact-plm-architecture]], [[contact-plm-data-tier]], [[contact-source-access-via-ansible]]
- updated: [[index]]
- stubs to fill from in-progress deep analysis: [[contact-plm-security]], [[contact-offline-install]], [[contact-plm-modules]], [[contact-customization-cust-plm]], [[cdb-platform-mom]], [[contact-powerscript]], [[contact-plm-config]]
- note: ~700 MB of offline installer bundles in `Source/` deliberately NOT copied (redundant with the deployed tree).

## [2026-06-28] ingest | Session: Internet lockdown for user vsi
- created source: [[2026-06-28-vsi-internet-lockdown]]
- created concepts: [[internet-lockdown-vsi]], [[nftables-uid-owner-block]]
- created entities: [[nftables]], [[vsi-user]]
- updated: [[ansible-workspace]], [[vsi-precision-3680]], [[ansible-become-via-env]]
- ansible: added `roles/internet_lockdown` + `playbooks/internet-lockdown.yml`; relocated
  `group_vars`/`host_vars` under `inventory/` so the `.env` become flow actually loads.
- applied + verified live: user `vsi` (uid 1000) blocked from the public internet (loopback
  + LAN intact); other users unaffected; service enabled; playbook idempotent (changed=0).
- open: `vsi` is in `sudo`, so the uid block is bypassable via `sudo` — flagged, not closed.

## [2026-06-28] ingest (cont.) | /opt/contact deep analysis — stubs filled
- Method: 8-dimension multi-agent workflow (30 agents) + adversarial re-verification of every security finding against the live host.
- created entities: [[contact-customization-cust-plm]]
- created concepts: [[contact-plm-config]], [[contact-plm-security]], [[contact-plm-modules]], [[cdb-platform-mom]], [[contact-powerscript]], [[contact-offline-install]], [[contact-vietnamese-localization]]
- created sources: [[responsible-views-vi-hotfix]]
- updated (corrections from deep analysis): [[contact-plm-architecture]] (nginx — not gatekeeper — is the TLS front door; full port map), [[contact-plm-data-tier]] (etcd is a cache dir not a service; blob vault on /data; Solr 9.10.1), [[opt-contact]], [[cdb-platform]], [[2026-06-28-opt-contact-analysis]], [[index]]
- cross-link: [[contact-plm-security]] ↔ [[internet-lockdown-vsi]] — clarified the nftables lockdown is egress-only and does NOT mitigate the inbound 0.0.0.0 exposure (no contradiction).
- headline findings: live CONTACT CIM Database PLM 16.2 mid Vietnamese-localization rollout; sound app/identity design but weak host/network layer (no inbound firewall, backends bind 0.0.0.0, unauthenticated Tika on :9998). Secrets value (DB password in install PDFs) deliberately NOT recorded in the wiki.

## [2026-06-28] ingest | Deliverable: docs/contact-plm/ documentation set
- Source: the `docs/contact-plm/` human-readable doc folder (11 files) authored this session; derived from the wiki + live system.
- created source: [[contact-plm-docs]]
- created concepts: [[contact-plm-operations]] (net-new knowledge: service control, logs, admin CLIs, backups, health checklist)
- updated: [[contact-plm-architecture]] (added ASCII topology diagram), [[opt-contact]] (link to ops + docs)
- regenerated [[index]] via `scripts/build_index.py` (33 pages).
- note: docs set is a derived digest, not a raw/ source; wiki remains source of truth. Secrets still excluded.

## [2026-06-28] lint
- scope: 33 pages (10 entities, 18 concepts, 5 sources).
- fixed 1 orphan: [[contact-plm-docs]] had no inbound links — [[opt-contact]] mentioned the doc set only by path. Converted that mention to a `[[contact-plm-docs]]` wiki-link (matches what the docs-ingest log entry claimed).
- links: 0 dangling, 0 broken `[[links]]`; all `sources:` frontmatter paths (`raw/contact/responsible_views.py`, `raw/contact/install-docs/`, `docs/contact-plm/`) resolve on disk.
- contradictions: none. Checked repeated facts across pages — Solr 9.10.1, Tika :9998, vsi uid 1000, 87%-full disk all consistent. The 16.0/16.1/16.2 spread is not a conflict: 16.2 is the deployment train with documented laggard modules on 16.1.x/15.x.
- index: `build_index.py --check` clean (no drift); body-only edit, no regeneration needed.
- no stale claims, no thin stubs, no unanswered-gap markers flagged this pass.

## [2026-06-28] ingest | claude-plugins-official marketplace (new domain)
- Source: live inspection of the Claude Code plugin marketplace on this host (`~/.claude/plugins/known_marketplaces.json` + `~/.claude/plugins/marketplaces/claude-plugins-official/` README/manifest); no `raw/` file. Introduces a new **Claude Code tooling** domain, separate from CONTACT PLM / Ansible.
- created entities: [[claude-code]], [[claude-plugins-official]]
- created concepts: [[claude-code-plugin]], [[claude-code-plugin-marketplace]]
- created sources: [[2026-06-28-claude-plugins-marketplace-map]]
- headline: official Anthropic marketplace `anthropics/claude-plugins-official` (synced 2026-06-26); 240-entry catalog = 37 first-party (`/plugins`) + third-party (`/external_plugins`, 15 local); top categories development 103 / productivity 45 / database 33; a plugin bundles commands+subagents+skills+hooks+MCP behind `.claude-plugin/plugin.json`, skills namespaced `<plugin>:<skill>`; only 2 plugins enabled locally (incl. `claude-code-setup`). Includes a Mermaid map on [[claude-plugins-official]].
- index: regenerated on the main branch post-merge (not in the worktree, per schema).

## [2026-06-28] ingest | Session: AI coding-agents survey (alternatives to Claude Code)
- Source: general-knowledge synthesis in a Claude Code session (no `raw/` file; assistant cutoff Jan 2026, per-tool details flagged as needing re-check). Claude-Code-specific backend facts verified against official Claude Code docs via a `claude-code-guide` subagent. Extends the **Claude Code tooling** domain with a cross-vendor agent landscape.
- created sources: [[2026-06-28-ai-coding-agents-survey]]
- created concepts: [[ai-coding-agents]] (Type-classified landscape + comparison table), [[local-model-coding-agent]] (free+offline how-to, tied to [[internet-lockdown-vsi]])
- created entities: [[aider]], [[goose-agent]], [[opencode]], [[openai-codex-cli]], [[cline]], [[continue-dev]] (the realistic free + open-source + local-model candidates)
- updated: [[claude-code]] — added a "Backends" section (Bedrock/Vertex/Foundry/AWS flags; custom `ANTHROPIC_BASE_URL`+auth; local model via Anthropic-format proxy; free-to-install but proprietary, not fully-offline) + cross-links into the new landscape.
- headline: classified agents by **Type** (CLI / IDE / Cloud / Framework) per the user's request. Free+offline+local = open-source tool + local model backend; clean fits are the natively-local open-source agents (Aider/Goose/OpenCode/Codex-CLI, Cline/Continue), no proxy. Claude Code can do it too but only via an Anthropic-format proxy and stays proprietary — the harder path. Cursor/Windsurf/Copilot stay cloud-tethered; Devin/Jules/Factory are paid cloud.
- curation: non-qualifying agents (Cursor, Windsurf, Copilot, Amazon Q CLI, Gemini CLI, Roo Code, Devin, Jules, Factory, frameworks) kept as rows/notes in [[ai-coding-agents]] rather than separate pages — can be promoted later.
- index: NOT regenerated in the worktree; rebuild on main post-merge via `python3 scripts/build_index.py` (per schema). Expect 38 → 47 pages.
