# Role: internet_lockdown

Cut a single local user off from the **public internet** on this host, enforced by a
dedicated `nftables` table (UID owner match in the `output` hook) that is loaded at boot
by a small `systemd` unit.

Why this design:

- **UID-scoped** — only the target user's packets are filtered; every other user is
  untouched (`meta skuid != <uid> accept`).
- **Isolated** — it lives in its own `inet` table, so it never edits or clobbers other
  firewall rules (ufw, docker, libvirt). Removing it removes only its own table.
- **Persistent** — a `oneshot` `systemd` unit (`RemainAfterExit`) re-applies the ruleset
  on every boot; `enabled: true` wires it into `multi-user.target`.
- **Reversible** — `state: absent` (or `systemctl stop`) runs `nft delete table`, fully
  restoring the user's connectivity.

## Key variables (see `defaults/main.yml`)

| Variable | Default | Meaning |
|---|---|---|
| `internet_lockdown_user` | `vsi` | User to lock down |
| `internet_lockdown_state` | `present` | `present` to enforce, `absent` to remove |
| `internet_lockdown_action` | `drop` | `drop` (silent) or `reject` (refused) |
| `internet_lockdown_allow_private` | `true` | Keep loopback + LAN reachable; block only the public internet. `false` = loopback only |

## Caveat — privileged users can bypass it

UID matching only governs packets owned by that user. A user with `sudo` can run programs
as another UID (`sudo <cmd>`), whose packets are **not** caught by this rule. If airtight
isolation is required for a sudo-capable account, also remove them from `sudo`, or move to
a network-namespace / default-deny approach. The target user `vsi` is currently in the
`sudo` group — see the wiki page `internet-lockdown-vsi` for details.
