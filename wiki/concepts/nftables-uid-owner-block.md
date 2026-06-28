---
title: Blocking a single user's internet with an nftables UID-owner rule
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [nftables, firewall, networking, security, linux]
status: stable
---

# Blocking one user's internet with an nftables UID-owner rule

Method for cutting a single Linux user off from the (public) internet without affecting
other users: filter locally-generated packets by socket owner UID in the nftables `output`
hook. First applied for [[internet-lockdown-vsi]].

## Summary
In nftables' `output` hook, `meta skuid <uid>` matches packets whose originating socket is
owned by that user. A dedicated `inet` table that accepts everyone else, accepts loopback +
LAN, then drops the target uid's remaining (internet-bound) traffic gives a clean per-user
internet block. Made persistent with a systemd unit and isolated from other firewall rules
by living in its own table.

## The ruleset
```nft
add table inet vsi_lockdown
flush table inet vsi_lockdown            # add+flush => `nft -f` is reload-safe
table inet vsi_lockdown {
    chain output {
        type filter hook output priority 0; policy accept;
        meta skuid != 1000 accept        # other users: untouched
        oifname "lo" accept              # loopback always allowed
        ip  daddr { 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12,
                    192.168.0.0/16, 169.254.0.0/16, 224.0.0.0/4 } accept
        ip6 daddr { ::1, fc00::/7, fe80::/10, ff00::/8 } accept
        meta skuid 1000 drop             # this user's internet traffic: blocked
    }
}
```

## Why these choices
- **Dedicated table** — across base chains on a hook, an `accept` is not final (only `drop`
  is), so keeping our own table means we compose with (don't clobber) ufw / docker rules.
- **`inet` family** — one table covers IPv4 + IPv6; `ip` / `ip6` match expressions are
  simply skipped for the other family.
- **add + flush** — lets `nft -f <file>` be re-applied idempotently / atomically.
- **Persistence** — a `oneshot` + `RemainAfterExit` systemd unit runs `nft -f` on boot
  (`ExecStop` deletes the table for clean teardown).

## Limitations
- **UID bypass:** only governs packets owned by the uid; a user with `sudo` can run as
  another uid and escape it (see [[vsi-user]]).
- Established connections are cut too (an output drop hits all packets, not just new ones).

## Related
- [[internet-lockdown-vsi]] — the concrete deployment
- [[nftables]] — the tool
- [[ansible-workspace]] — the Ansible role that templates this

## Open questions
- Equivalent with `iptables -m owner --uid-owner` (legacy backend) if ever needed.
