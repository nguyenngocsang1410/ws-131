---
title: "Session: Internet lockdown for user vsi"
type: source
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, nftables, firewall, security, session, provenance]
status: stable
---

# Session: Internet lockdown for user vsi

Provenance record for the 2026-06-28 Claude Code session that blocked public-internet
access for the local user [[vsi-user]] on [[vsi-precision-3680]], encoded as Ansible.

## Summary
The human asked to "lock down internet access for user vsi", using the Ansible workspace
as the source of truth ("ansible as the wiki state"). Implemented as a new role
(`roles/internet_lockdown`) that installs a dedicated [[nftables]] table matching the
user's UID in the `output` hook, loaded at boot by a systemd unit — method:
[[nftables-uid-owner-block]], resulting state: [[internet-lockdown-vsi]]. Applied and
**verified live on the host**.

## What was done
- Created `roles/internet_lockdown` + `playbooks/internet-lockdown.yml` in [[ansible-workspace]].
- Default policy: block only the **public** internet for vsi (loopback + RFC1918 / LAN /
  multicast still allowed); all other users untouched; action = `drop`.
- Discovered + fixed a latent bug: `group_vars/` / `host_vars/` sat at the project root and
  were never loaded, so the `.env` become flow ([[ansible-become-via-env]]) silently did
  nothing on a `become: true` play. Moved them under `inventory/`.
- Fixed an `INJECT_FACTS_AS_VARS` deprecation by reading `ansible_facts['getent_passwd']`
  ([[ansible-facts-injection-deprecation]]).

## What was verified (live, on host)
- Baseline: vsi `curl https://1.1.1.1` → HTTP 301 (had internet).
- After apply: vsi `curl https://1.1.1.1` → timeout / HTTP 000 (**blocked**); vsi loopback
  + DNS still work; other user `vietnq37` → HTTP 301 (**unaffected**).
- `systemctl is-enabled/is-active vsi-internet-lockdown` → enabled / active (reboot-safe).
- Re-run via the `.env` flow → `changed=0` (idempotent) and the become password now loads.

## Caveat surfaced
- [[vsi-user]] is in the `sudo` group, so the UID-owner block can be bypassed with `sudo`
  (root-owned packets aren't matched). Documented, not closed — see [[internet-lockdown-vsi]].

## Related
- [[internet-lockdown-vsi]] — the resulting state + role
- [[nftables-uid-owner-block]] — the method
- [[nftables]] — the tool used
- [[ansible-workspace]] — where the role lives
- [[vsi-user]], [[vsi-precision-3680]] — target user + host

## Open questions
- Want it airtight against the sudo bypass (remove vsi from sudo / netns)?
- Switch `drop` → `reject` for faster failures?
