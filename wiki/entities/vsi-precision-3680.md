---
title: vsi-Precision-3680 (the machine)
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [machine, host, ubuntu, hardware]
status: stable
---

# vsi-Precision-3680

The local workstation this wiki and Ansible workspace run on; it is both the Ansible
control node and the only managed node.

## Summary
A Dell Precision 3680 running Ubuntu 24.04.4 LTS, managed by Ansible over a local
connection (per [[2026-06-28-ansible-workspace-setup]]). The primary user `vietnq37` is in
the `sudo` group but the box has **no passwordless sudo**. It is a shared box (7 real
users); its lowest-uid account [[vsi-user]] (uid 1000) is currently blocked from the public
internet — see [[internet-lockdown-vsi]], enforced via [[nftables]].

## Details
Facts observed 2026-06-28:

| Property | Value |
|---|---|
| Hostname | `vsi-Precision-3680` |
| OS | Ubuntu 24.04.4 LTS (Noble Numbat) |
| Kernel | 6.17.0-29-generic |
| Arch | x86_64 |
| CPUs | `nproc` = 32 (Ansible `processor_vcpus` reported 24 — see open question) |
| Memory | ~62 GiB (62.5 GiB reported by Ansible) |
| Primary user | `vietnq37` (uid 1001, gid 1001; groups: `vietnq37`, `sudo`) |
| Passwordless sudo | No (`sudo -n true` fails) |

Local login users (uid ≥ 1000): `vsi` (1000, [[vsi-user]]), `vietnq37` (1001),
`duongpt29` (1002), `dattt48` (1003), `sangnn10` (1004), `huyntg` (1005), `haibt15` (1006).

Two Python interpreters matter here (per [[ansible-local-control-node]]):
- **System**: `/usr/bin/python3` → 3.12.3 (symlink to python3.12), **has `python3-apt`**.
  This is the Ansible module interpreter.
- **Conda**: `/home/vietnq37/conda/bin/python3` → 3.13.13. Used to bootstrap [[pipx]];
  lacks apt bindings, so not used for module execution.

Firewall backend: [[nftables]] (Ubuntu 24.04 default; `iptables` is an nf_tables wrapper).

## Related
- [[ansible-workspace]] — manages this host
- [[vsi-user]] — the uid-1000 account on this host
- [[internet-lockdown-vsi]] — this host now blocks vsi's public-internet access
- [[nftables]] — firewall backend used for the lockdown
- [[ansible-local-control-node]] — why local connection + system python
- [[ansible-become-via-env]] — how sudo is handled given no passwordless sudo

## Open questions
- `nproc` (32) vs Ansible `processor_vcpus` (24) mismatch — not investigated.
