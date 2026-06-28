---
title: Internet lockdown for user vsi (current state)
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [security, firewall, nftables, ansible, state]
status: stable
---

# Internet lockdown for user vsi

**Current state:** the local user [[vsi-user]] (uid 1000) on [[vsi-precision-3680]] is
blocked from the public internet, enforced by [[nftables]] and managed by [[ansible-workspace]].

## Summary
Active since 2026-06-28 (per [[2026-06-28-vsi-internet-lockdown]]). A dedicated nftables
table `vsi_lockdown` drops vsi's outbound packets to non-local destinations; loopback and
LAN / private ranges stay reachable, and every other user is unaffected. A `oneshot`
systemd unit `vsi-internet-lockdown.service` reloads the ruleset at every boot. Mechanism
details: [[nftables-uid-owner-block]].

## How it is managed (Ansible is the source of truth)
- Role: `roles/internet_lockdown`; playbook: `playbooks/internet-lockdown.yml`.
- Key vars (`defaults/main.yml`): `internet_lockdown_user: vsi`, `internet_lockdown_state:
  present`, `internet_lockdown_action: drop`, `internet_lockdown_allow_private: true`.
- Apply / re-apply (idempotent):
  ```bash
  cd ansible && set -a; source .env; set +a
  ansible-playbook playbooks/internet-lockdown.yml
  ```
- Undo:
  ```bash
  ansible-playbook playbooks/internet-lockdown.yml -e internet_lockdown_state=absent
  ```
  (or `sudo systemctl stop vsi-internet-lockdown` — its `ExecStop` deletes the table.)

## On-host footprint
| Artifact | Path |
|---|---|
| Ruleset | `/etc/nftables/vsi-internet-lockdown.nft` |
| Service | `/etc/systemd/system/vsi-internet-lockdown.service` |
| nft table | `inet vsi_lockdown` (chain `output`, priority 0) |

## Verified behaviour (2026-06-28)
- vsi → public internet: **blocked** (curl times out, HTTP 000).
- vsi → loopback + DNS (systemd-resolved): works.
- vietnq37 (other user) → internet: works.
- Service enabled + active; playbook idempotent (`changed=0` on re-run).

## Caveat / limitation
[[vsi-user]] is in the `sudo` group. UID-owner matching only governs packets *owned by*
that uid, so `sudo <cmd>` (running as root / another uid) **bypasses** the block. For an
airtight cut-off, remove vsi from `sudo`, or use a network-namespace / default-deny approach.

## Related
- [[nftables-uid-owner-block]] — the general method
- [[vsi-user]] — the target account (and the sudo caveat)
- [[vsi-precision-3680]] — the host
- [[ansible-workspace]] — the managing project
- [[2026-06-28-vsi-internet-lockdown]] — provenance

## Open questions
- Make it bypass-proof against vsi's sudo access?
- `drop` vs `reject` (silent timeout vs fast refusal)?
