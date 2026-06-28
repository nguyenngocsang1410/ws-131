---
title: nftables
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [tool, firewall, networking, linux]
status: stable
---

# nftables

The Linux in-kernel packet-classification framework / firewall, successor to iptables; the
default backend on [[vsi-precision-3680]] (Ubuntu 24.04).

## Summary
Installed on the host as `nftables` (CLI `/usr/sbin/nft`, v1.0.9). On Ubuntu 24.04 the
`iptables` command is itself an nf_tables wrapper, so nftables is the real engine. Used
here to enforce [[internet-lockdown-vsi]] via a dedicated table (method:
[[nftables-uid-owner-block]]).

## Details
- Firewall tooling present on the host: `nft` (nftables 1.0.9), `iptables` (1.8.10,
  nf_tables backend), `ufw` (0.36.2). `firewall-cmd` is absent.
- Concepts used here: `inet` family tables, base chains with `type filter hook output
  priority N`, `meta skuid` (socket owner UID) matching, and `nft -f` to load a ruleset
  file atomically. `nft -c -f` (check-only) requires root.
- Persistence here is via a custom systemd unit rather than the distro `nftables.service` /
  `/etc/nftables.conf`, so the lockdown is fully self-contained.

## Related
- [[nftables-uid-owner-block]] — the technique
- [[internet-lockdown-vsi]] — what it currently enforces
- [[vsi-precision-3680]] — the host
- [[ansible-workspace]] — manages the ruleset

## Open questions
- Whether the distro `nftables.service` is enabled, or only our per-user unit (only our
  unit is relied upon for the lockdown).
