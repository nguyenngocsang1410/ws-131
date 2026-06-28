---
title: CONTACT PLM operations reference
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, docs/contact-plm/]
tags: [contact-software, plm, operations, systemd, runbook, backup, cli]
status: stable
---

# CONTACT PLM operations reference

Day-to-day operation of the [[opt-contact]] deployment: service control, logs, admin CLIs,
and backups. Service management is **systemd**; admin tooling is the `venv/bin` CLIs.

## Summary
The stack is run by systemd units (`contact-*`, `elements-*`, plus `nginx` and the data-tier
services). CONTACT admin commands live in `/opt/contact/venv/bin` and take
`--instancedir /opt/contact/instance` (or `-D`). Run interactive/maintenance commands as the
service user `vsi` (which has an egress internet block and is in `sudo` — see
[[internet-lockdown-vsi]]). Logs go to `/var/log/contact`. Backups must cover **PostgreSQL +
the blob vault**.

## Details

### Service control
```bash
systemctl list-units --type=service | grep -iE 'contact|elements|Threed|Quality'
systemctl status  contact-worker-01      # the app server (cdbsrv)
systemctl restart contact-worker-01      # restart the worker first, then its dependents
sudo systemctl restart nginx             # the TLS front door
```
App units declare `After/Wants contact-worker-01` (with `ExecStartPre=/bin/sleep 20`), so on a
full restart bring up the data tier (`postgresql`, `redis-server`, `solr`, `tika`) and the
worker before the dependent services. Unit catalogue: [[contact-plm-architecture]].

### Logs
| Source | Location |
|---|---|
| CONTACT app/service | `/var/log/contact/<CADDOK_TOOL>[-PID].log` (rotating 10 MiB × 3) |
| systemd journal | `journalctl -u contact-worker-01 -f` |
| nginx | `/var/log/nginx/{access,error}.log` |
| PostgreSQL | `/var/log/postgresql/` (cluster `17/main`) |

### Admin CLIs (`/opt/contact/venv/bin`, after `source venv/bin/activate`)
| Command | Purpose |
|---|---|
| `cdbsh -D /opt/contact/instance` | interactive CONTACT shell |
| `cdbsql` | SQL via the cdb layer |
| `cdbpkg` | package/config mgmt — `cdbpkg sync` / `build <pkg>` / `xliff …` |
| `cdbimp` / `cdbexp` | data import / export |
| `cdbacs` | access-control admin |
| `cdbwallet` | secret-wallet mgmt |
| `powerscript -m <module>` | run a module in the runtime ([[contact-powerscript]]) |
| `dump_messages` | rebuild message/translation catalogs |

### Common tasks
- **Regenerate the `responsible` DD views** (after org-context/language changes):
  `powerscript -m cs.workflow.responsible_views` — note the vi-fallback caveat in
  [[responsible-views-vi-hotfix]].
- **Apply a `cust.plm` change:** `cdbpkg build cust.plm && cdbpkg sync && dump_messages`
  ([[contact-customization-cust-plm]]).
- **DB access:** `psql -h 127.0.0.1 -U plmvsi -d ce16db` (password from the sqlapi wallet).
- **Solr health:** `curl -s http://127.0.0.1:8983/solr/admin/cores?action=STATUS`.

### Backups
| Must back up | How |
|---|---|
| PostgreSQL `ce16db` | `pg_dump` / cluster backup |
| Blob vault | `/data/contact-storage` (filesystem) — see [[contact-plm-data-tier]] |
| Instance config | `instance/etc` (+ `wallets/` securely), `instance/cust.plm/` |
| Rebuildable (optional) | Solr index `/data/solr`, `instance/etcd`, `instance/tmp` |

⚠ Everything on `/data` shares one root partition that was **~87 % full** — watch headroom.

### Health checklist
- `systemctl --failed` empty.
- `https://plm_vsi/` serves the login flow; OIDC `:8084` / ologin `:8083` up.
- PostgreSQL accepting; Redis `PING`→`PONG`; Solr `core1` healthy; Tika `/version` responds.
- `/data` has headroom; backups cover PostgreSQL **and** the blob vault.

## Related
- [[contact-plm-architecture]] — the units/ports being operated
- [[contact-plm-data-tier]] — what to back up
- [[contact-plm-config]] — config the CLIs act on
- [[contact-plm-security]] — hardening to do alongside ops
- [[opt-contact]] — the deployment

## Open questions
- Is there an existing backup/retention job, or is this greenfield ops?
