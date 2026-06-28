# 10 — Operations Reference

Practical day-to-day reference. Service control is **systemd**; admin tooling is the `venv/bin`
CLIs. Most CONTACT commands take `--instancedir /opt/contact/instance` (or `-D`).

> Run interactive/maintenance commands as the service user `vsi`. Note `vsi` has an egress
> internet block and is in `sudo` (see [08-security.md](08-security.md)).

## Service management

```bash
# Status of the whole stack
systemctl list-units --type=service | grep -iE 'contact|elements|Threed|Quality'

# Inspect / restart a service
systemctl status  contact-worker-01
systemctl restart contact-worker-01      # the app server
sudo systemctl restart nginx             # the TLS front door

# Dependency-aware restart order: data tier (pg/redis/solr/tika) is independent;
# app units declare After/Wants contact-worker-01, so restart the worker first, then dependents.
```

Core units (see [02-architecture.md](02-architecture.md) for the full table):
`nginx`, `contact-worker-01`, `contact-gatekeeper`, `contact-oidc-server`, `contact-ologin`,
`contact-docportal`, `contact-blobstore`, `elements-broker`, `ThreedConversionServer`,
`elements-index-job-dispatcher`, `elements-wfqueue`, `elements-system-posting-queue`,
`elements-share-objects-queue`, `elements-daily-mail-service`,
`elements-authserver-role-cache-updater`, `QualityCharacteristicEngine`,
`elements-job-runner-oidc-client-sync`; timers `ce-session-cleanup`, `ce-license-clock-update`.

Backing services: `postgresql`, `redis-server`, `solr`, `tika`.

## Logs

| Source | Location |
|---|---|
| CONTACT app/service logs | `/var/log/contact/<CADDOK_TOOL>[-PID].log` (rotating, 10 MiB × 3) |
| systemd journal | `journalctl -u contact-worker-01 -f` (etc.) |
| nginx | `/var/log/nginx/{access,error}.log` |
| PostgreSQL | `/var/log/postgresql/` (cluster `17/main`) |

```bash
# Tail the app server log
tail -f /var/log/contact/cdbsrv*.log
# Or via journal
journalctl -u contact-worker-01 -n 200 -f
```

## Admin CLIs (`/opt/contact/venv/bin`)

| Command | Purpose |
|---|---|
| `cdbsh -D /opt/contact/instance` | interactive CONTACT shell |
| `cdbsql` | SQL access through the cdb layer |
| `cdbpkg` | package/config management — `cdbpkg sync`, `cdbpkg build <pkg>`, `cdbpkg xliff …` |
| `cdbimp` / `cdbexp` | data import / export |
| `cdbacs` | access-control administration |
| `cdbwallet` | secret-wallet management |
| `powerscript -m <module>` | run a module in the CONTACT runtime (e.g. regenerate views) |
| `dump_messages` | rebuild message/translation catalogs |

Activate the env first: `source /opt/contact/venv/bin/activate`.

## Common tasks

**Regenerate the `responsible` DD views** (after changing org-contexts or languages):
```bash
source /opt/contact/venv/bin/activate
powerscript -m cs.workflow.responsible_views     # then compile_views() runs
```
(See the `vi`-fallback caveat in [07-customization.md](07-customization.md).)

**Apply a customization / config change** (`cust.plm`): edit the package config, then
`cdbpkg build cust.plm && cdbpkg sync && dump_messages`.

**Database access:**
```bash
psql -h 127.0.0.1 -U plmvsi -d ce16db        # password from the sqlapi wallet
```

**Search index health:** `curl -s http://127.0.0.1:8983/solr/admin/cores?action=STATUS`.

## Ports cheat-sheet

External (via nginx): `https://plm_vsi/` (worker), `/doc`, `/signedblob`, `/ologin`, `/oidc`,
`/gatekeeper`. Direct backend ports `8080–8088` and Tika `9998` are also open on `0.0.0.0`
(should be firewalled — [08-security.md](08-security.md)). Loopback: PG `5432`, Redis `6379`,
Solr `8983`.

## Health checklist

- [ ] `systemctl --failed` is empty.
- [ ] `https://plm_vsi/` returns the login flow; OIDC `:8084`/`ologin` `:8083` up.
- [ ] PostgreSQL accepting connections; Redis `PING`→`PONG`; Solr `core1` healthy; Tika
      `/version` responds.
- [ ] `/data` partition has headroom (it was ~87% full — see [04-data-tier.md](04-data-tier.md)).
- [ ] Backups cover PostgreSQL `ce16db` **and** the blob vault `/data/contact-storage`.

## Backup essentials

| Must back up | How |
|---|---|
| PostgreSQL `ce16db` | `pg_dump`/cluster backup |
| Blob vault | `/data/contact-storage` (filesystem) |
| Instance config | `/opt/contact/instance/etc` (+ `wallets/` securely), `cust.plm/` |
| Rebuildable (optional) | Solr index `/data/solr`, `instance/etcd`, `instance/tmp` |

→ Back to [README.md](README.md)
