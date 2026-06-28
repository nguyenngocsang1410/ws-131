# 02 — Architecture & Topology

The deployment is a multi-process Python application managed by **systemd**, fronted by a
single **nginx** TLS reverse proxy, backed by a self-hosted OIDC auth stack and a localhost
data tier.

## Topology diagram

```
                         Internet / LAN
                               │
                    :80 ──301──▶ :443  (nginx, TLS, self-signed plm_vsi cert)
                               │  path-prefix routing to 127.0.0.1 upstreams
        ┌──────────────┬───────┴────────┬───────────┬───────────┬─────────────┐
        ▼ /            ▼ /doc            ▼ /signedblob ▼ /ologin   ▼ /oidc       ▼ /gatekeeper
   cdbsrv :8080   docportal :8081   blobstore :8082  ologin:8083 oidc_srv:8084 gatekeeper:8085
   (app server)   (cs.docportal)    (FileStore)      (OIDC RP)   (OIDC OP)     (auth gateway)
        │                                  │              └────────┬───────────┘
        │ MoM business logic               │                 self-hosted OIDC
        │ (cdb.platform.mom)               │            issuer https://plm_vsi/oidc
        ▼                                  ▼            identity = ElementsAuth (DB)
  ┌─────────────────────── data tier (127.0.0.1) ───────────────────────┐
  │  PostgreSQL 17  Redis :6379   Solr 9.10.1 :8983      blobstore vault │
  │  ce16db :5432   (sessions/    (core1, /data/solr)    /data/contact-  │
  │  (metadata)     OIDC state)        ▲                 storage         │
  └────────────────────────────────────┼───────────────────────────────┘
                                        │ index jobs (queued in PG)
        background workers ─────────────┘ → Tika :9998 (extract) → Solr (index)
   wfqueue · system_posting_queue · share_objects_queue · daily_mail ·
   role_cache_updater :8888 · index_job_dispatcher · metrics engine · txpool worker

   3D subsystem (NOT proxied by nginx — reached via direct ports):
   elements-broker :8086 (cs.threed) · HOOPS node communicator :8087 · ThreedConversionServer

   ⚠ Trust-boundary issue: every backend above ALSO binds 0.0.0.0, and there is no
     inbound host firewall → the nginx front door is bypassable. See 08-security.md.
```

## Services (systemd, all active 2026-06-28)

| Unit | Process / entry point | Port | Role |
|---|---|---|---|
| `contact-worker-01` | `cdbsrv` (`cdb.wsgi.worker`) `--auth-plugins ologin,newsession,basic` | 8080 | **application server** (MoM business logic) |
| `contact-docportal` | `powerscript -m cs.docportal.app -r /doc/` | 8081 | document portal web app |
| `contact-blobstore` | `blobstore --http2` (`cdb.storage.replication.server`) | 8082 | binary/file storage |
| `contact-ologin` | `cdb.ologin.main` | 8083 | OIDC login client (relying party) |
| `contact-oidc-server` | `cdb.oidc_server.main --issuer https://plm_vsi/oidc` | 8084 | OpenID Connect provider |
| `contact-gatekeeper` | `cdb.authentication.main` | 8085 | auth gateway (auth events, LDAP) |
| `elements-broker` | `powerscript -m cs.threed.services.broker_service` | 8086 | 3D broker |
| _(node)_ | HOOPS communicator (`cs.threedlibs`) | 8087 | 3D streaming |
| `ThreedConversionServer` | `cs.threed.services.threedcs` | — | CAD→3D conversion |
| `elements-authserver-role-cache-updater` | `role_cache_updater` | 8888 | auth role-cache refresh |
| `elements-index-job-dispatcher` | `cdb.index_job_processor.main` | — | dispatch Solr index jobs |
| `elements-wfqueue` | `cs.workflow.wfqueue` | — | workflow engine queue |
| `elements-system-posting-queue` | `system_posting_queue` | — | posting queue |
| `elements-share-objects-queue` | `share_objects_queue` | — | object-sharing queue |
| `elements-daily-mail-service` | `daily_mail_service` | — | scheduled notifications |
| `QualityCharacteristicEngine` | `metrics-computation-engine-svc` | — | metrics computation |
| `elements-job-runner-oidc-client-sync` | `oidc_client_sync` | — | register/sync OIDC clients |
| `ce-session-cleanup` / `ce-license-clock-update` | timers (`OnCalendar` daily) | — | housekeeping |

All app units run `User=vsi`, `WorkingDirectory=/opt/contact/instance`, `Restart=always`,
`Environment=CADDOK_LOGDIR=/var/log/contact`; dependents `After/Wants contact-worker-01` with
`ExecStartPre=/bin/sleep 20`.

## Port map (verified via `ss -tlnp`)

| Port | Bind | Service | Notes |
|---|---|---|---|
| 80, 443 | `0.0.0.0` | **nginx** | 80→443 redirect; only intended entry point |
| 8080 | `0.0.0.0` | cdbsrv app server | plain HTTP; should be loopback |
| 8081 | `0.0.0.0` | docportal | |
| 8082 | `0.0.0.0` | blobstore | conf says `:8998`, CLI flag `--base-url :8082` wins |
| 8083 | `0.0.0.0` | ologin | |
| 8084 | `0.0.0.0` | oidc_server | |
| 8085 | `0.0.0.0` | gatekeeper | |
| 8086 | `0.0.0.0` | 3D broker | **not** proxied by nginx |
| 8087 | `0.0.0.0` | HOOPS node | |
| 8888 | `0.0.0.0` | role_cache_updater | |
| 9998 | `0.0.0.0` | **Apache Tika** | unauthenticated — see [08-security.md](08-security.md) |
| 8010 | `0.0.0.0` | **unrelated** Docker container (filter-v2-api) | not part of CONTACT |
| 5432 | `127.0.0.1` | PostgreSQL 17 | |
| 6379 | `127.0.0.1` | Redis | no password |
| 8983 (+7983) | `127.0.0.1` | Solr | |
| 8180, 6010–6018 | `127.0.0.1` | unrelated dev app / internal helpers | |

## Request & auth flow (verified)

1. Client → nginx `:443` (TLS terminate) → routed by path prefix to a `127.0.0.1` backend.
2. Unmatched paths (`/`) → **cdbsrv** `:8080`, which executes Meta-Object-Model business logic
   (see [03-platform-framework.md](03-platform-framework.md)) against **PostgreSQL**.
3. Auth: **ologin** (RP) ⇄ **oidc_server** (OP, issuer `https://plm_vsi/oidc`) ⇄ **gatekeeper**;
   identity verified by `cdb.oidc_server.authn.ElementsAuth` against the Elements DB; TOTP 2FA
   via `cs.mfa`.
4. Sessions / ologin / OIDC state → **Redis**.
5. Documents → **blobstore** (vault on `/data`); search → **index-job-dispatcher → Tika → Solr**.

## Service wiring (`instance/etc/services.json`)

Logical service → backend bindings:

| Logical service | Backend |
|---|---|
| `cdb.sessionstore`, `cdb.storage.sessiondata`, `cdb.ologin.storage`, `cdb.oidc.storage` | `redis://127.0.0.1:6379/0` |
| `cdb.oidc.provider`, `cdb.ologin` | `https://plm_vsi` |
| `cdb.gatekeeper` | `http://127.0.0.1:8085` |
| `cdb.storage.blobstore` / `main` | `http://127.0.0.1:8082` (http adapter) |
| `cdb.index.solr` | `http://localhost:8983/solr/core1` |
| `cdb.tika` | `http://localhost:9998` (auth `null`, timeout 900s) |
| `cs.threed` broker | `https://plm_vsi/broker`, port 8086 |
| `cdb.storage.replication` | `null` adapter (single-site; replication off) |

→ Next: [03-platform-framework.md](03-platform-framework.md) · Related: [04-data-tier.md](04-data-tier.md), [08-security.md](08-security.md)
