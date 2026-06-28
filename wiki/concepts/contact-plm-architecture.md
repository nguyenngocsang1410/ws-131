---
title: CONTACT PLM service architecture & topology
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [contact-software, plm, architecture, services, ports, systemd, topology]
status: stable
---

# CONTACT PLM service architecture & topology

How the [[opt-contact]] deployment is decomposed into cooperating services, and which
network port each one listens on.

## Summary
A single **nginx** TLS reverse proxy is the front door: `:80`→`:443` (301), TLS terminated
with a self-signed cert, then **path-prefix routing to six `127.0.0.1` backends**. The core
is **`cdbsrv`** (`cdb.wsgi.worker`, systemd `contact-worker-01`) on `:8080`, serving
[[cdb-platform-mom|MoM]] business logic. Authentication is a **self-hosted OIDC triad** —
`oidc_server` (provider), `ologin` (login client/RP), `gatekeeper` (`cdb.authentication.main`
auth gateway). Supporting services (docportal, blobstore, 3D broker) and a fleet of
background queue workers run under systemd. **Key trust-boundary issue:** every CONTACT
backend binds `0.0.0.0` while nginx proxies only to `127.0.0.1`, so the TLS/auth front door
can be bypassed by hitting backend HTTP ports directly ([[contact-plm-security]]).

## Details

### Topology
```
                     Internet / LAN
                           │
                :80 ─301─▶ :443  nginx (TLS, self-signed plm_vsi cert)
                           │  path-prefix routing → 127.0.0.1 upstreams
   ┌──────────┬───────────┼───────────┬───────────┬────────────┐
   ▼ /        ▼ /doc      ▼ /signedblob▼ /ologin   ▼ /oidc       ▼ /gatekeeper
 cdbsrv8080 docportal8081 blobstore8082 ologin8083 oidc_srv8084 gatekeeper8085
 (app srv)  (cs.docportal)(FileStore)  (OIDC RP)  (OIDC OP)    (auth gateway)
   │                                        └────────┬──────────┘ self-hosted OIDC
   ▼ MoM logic                                       │ ElementsAuth (DB)
 ┌──────── data tier (127.0.0.1) ────────┐   background workers + 3D:
 │ PostgreSQL ce16db · Redis · Solr core1 │   wfqueue · queues · role_cache:8888 ·
 │ blob vault on /data                    │   index-dispatcher→Tika:9998→Solr ·
 └────────────────────────────────────────┘   broker:8086 · HOOPS:8087 (NOT proxied)

 ⚠ Every backend ALSO binds 0.0.0.0 and there is no inbound firewall →
   the nginx front door is bypassable on the LAN ([[contact-plm-security]]).
```

### nginx front door (path-prefix routing)
`/etc/nginx/nginx.conf` (`server_name plm_vsi 172.17.10.131`, TLSv1.2/1.3, 8 workers,
`client_max_body_size 128m`) routes:

| Location | Upstream (127.0.0.1) | Service |
|---|---|---|
| `/` | `:8080` | `cdbsrv` app-server worker |
| `^~ /doc` | `:8081` | docportal |
| `^~ /signedblob` | `:8082` | blobstore (presigned file delivery) |
| `^~ /ologin` | `:8083` | ologin (OIDC login client) |
| `^~ /oidc` | `:8084` | oidc_server (OpenID Provider) |
| `^~ /gatekeeper` | `:8085` | gatekeeper (auth gateway) |

### systemd units (all *active* 2026-06-28)
`contact-worker-01` (cdbsrv `--auth-plugins ologin,newsession,basic --listen 0.0.0.0:8080`),
`contact-gatekeeper`, `contact-oidc-server` (`--issuer https://plm_vsi/oidc`),
`contact-ologin`, `contact-docportal` (`powerscript -m cs.docportal.app -r /doc/`),
`contact-blobstore` (`--http2`), `elements-job-runner-oidc-client-sync`,
`elements-authserver-role-cache-updater` (`:8888`), `elements-broker`
(`powerscript -m cs.threed.services.broker_service`), `ThreedConversionServer`,
`elements-daily-mail-service`, `elements-wfqueue`, `elements-system-posting-queue`,
`elements-share-objects-queue`, `elements-index-job-dispatcher` (`index_job_processor`),
`QualityCharacteristicEngine` (metrics), plus `ce-session-cleanup` / `ce-license-clock-update`
timers. (Full list & ExecStart: [[contact-offline-install]].)

### Port map (observed via `ss -tlnp`)
| Port | Bind | Service |
|---|---|---|
| 80 / 443 | `0.0.0.0` | **nginx** (80→443 redirect; TLS front door) |
| 8080 | `0.0.0.0` | `cdbsrv` app-server worker |
| 8081 | `0.0.0.0` | docportal (`/doc`) |
| 8082 | `0.0.0.0` | blobstore (`/signedblob`) |
| 8083 | `0.0.0.0` | ologin |
| 8084 | `0.0.0.0` | oidc_server |
| 8085 | `0.0.0.0` | gatekeeper |
| 8086 | `0.0.0.0` | 3D broker (`cs.threed`) — **not** proxied by nginx |
| 8087 | `0.0.0.0` | HOOPS Node communicator (3D) |
| 8888 | `0.0.0.0` | role_cache_updater |
| 9998 | `0.0.0.0` | **Apache Tika** (see [[contact-plm-data-tier]]; flagged in [[contact-plm-security]]) |
| 8010 | `0.0.0.0` | **unrelated** Docker container (filter-v2-api) — not CONTACT |
| 5432 / 6379 / 8983 | `127.0.0.1` | PostgreSQL 17 / Redis / Solr |
| 8180, 6010–6018 | `127.0.0.1` | unrelated dev app / internal helpers |

### Request flow (verified)
Client → nginx `:443` (TLS) → by path → `cdbsrv` `:8080` (or docportal/blobstore/ologin/
oidc/gatekeeper). `cdbsrv` runs [[cdb-platform-mom|MoM]] logic against
[[contact-plm-data-tier|PostgreSQL]]; sessions/OIDC state in **Redis**; search via
**index-job-dispatcher → Tika → Solr**. Auth: `ologin` (RP) ↔ `oidc_server` (OP, issuer
`https://plm_vsi/oidc`) ↔ `gatekeeper`, verifying identity with
`cdb.oidc_server.authn.ElementsAuth` against the Elements DB; TOTP 2FA via `cs.mfa`.

### Trust boundary
The data tier (PostgreSQL, Redis, Solr) is localhost-only. The problem is every CONTACT
*app/auth* backend binds `0.0.0.0` and answers plain HTTP directly (probed: 8080→307,
8082→302, 8085→400), **bypassing nginx** — and there is **no host firewall**. Full
assessment: [[contact-plm-security]].

## Related
- [[opt-contact]] — the deployment
- [[cdb-platform]] / [[cdb-platform-mom]] — what `cdbsrv` runs
- [[contact-plm-data-tier]] — the backends these services talk to
- [[contact-plm-security]] — exposure & auth assessment
- [[contact-plm-config]] — `services.json`/systemd wiring
- [[contact-plm-operations]] — operating these services (control, logs, restart order)
- [[contact-offline-install]] — the full systemd unit set

## Open questions
- How 3D clients actually reach the broker (`services.json` says `https://plm_vsi/broker` but nginx has no `/broker` location).
- Number of app-server workers (only `contact-worker-01` present — scaled to 1?).
- Both Solr `:8983` and `:7983` listen — second node vs admin?
