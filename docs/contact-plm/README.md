# CONTACT CIM Database PLM — Deployment Documentation

Documentation for the **CONTACT Software CIM Database / Elements PLM** deployment installed at
`/opt/contact` on host `vsi-precision-3680`.

> **Scope & provenance.** This is a reverse-engineered operations/architecture reference,
> compiled 2026-06-28 from inspecting the live (running) system and its source — not vendor
> documentation. It reflects *this* installation, which is mid Vietnamese-localization rollout.
> The atomic, interlinked knowledge-base version lives in [`../../wiki/`](../../wiki/) (see
> [`wiki/index.md`](../../wiki/index.md)); this folder is the linear, human-readable digest.

## Deployment at a glance

| | |
|---|---|
| **Product** | CONTACT CIM Database PLM on the CONTACT Elements platform |
| **Version** | 16.2 (`cscdb.product` 16.2.0.4, `cs.platform` 16.2.8) |
| **Runtime** | Python 3.14 (uv-provided CPython 3.14.6), single virtualenv |
| **Install root** | `/opt/contact` (`venv/`, `packages/`, `instance/`, `xlf/`) |
| **Host** | `vsi-precision-3680` — Ubuntu 24.04 (noble); OS user `vsi` |
| **Front door** | nginx TLS reverse proxy (`:80`→`:443`), self-signed `plm_vsi` cert |
| **App server** | `cdbsrv` (`cdb.wsgi.worker`), systemd `contact-worker-01`, `:8080` |
| **Auth** | self-hosted OIDC (oidc_server / ologin / gatekeeper) + TOTP 2FA |
| **Database** | PostgreSQL 17 — `ce16db` / role `plmvsi` (localhost) |
| **Storage/search** | blobstore (FileStore on `/data`) · Solr 9.10.1 · Tika 3.3.1 · Redis |
| **Install method** | fully offline / air-gapped (bundled wheels + offline apt repo) |
| **Customization** | `cust.plm` — a Vietnamese (`vi`) language pack (config/data only) |

## How to read this folder

| Doc | Audience | Contents |
|---|---|---|
| [01-overview.md](01-overview.md) | everyone | what the product is, versions, what it's specialized for |
| [02-architecture.md](02-architecture.md) | ops / dev | topology diagram, services, port map, request flow, trust boundary |
| [03-platform-framework.md](03-platform-framework.md) | developers | `cdb`, the Meta-Object Model, powerscript, customization surface |
| [04-data-tier.md](04-data-tier.md) | ops / DBA | PostgreSQL, blobstore, Solr, Tika, Redis + the data flow |
| [05-configuration.md](05-configuration.md) | ops | instance model, config files, secrets/wallets |
| [06-modules.md](06-modules.md) | functional | installed `cs.*` module inventory + version trains |
| [07-customization.md](07-customization.md) | dev / functional | `cust.plm`, the Vietnamese localization, the `responsible_views` hotfix |
| [08-security.md](08-security.md) | security / ops | posture, findings, remediation checklist |
| [09-installation.md](09-installation.md) | deployers | reconstructed offline install runbook |
| [10-operations.md](10-operations.md) | ops | service management, logs, ports cheat-sheet, common tasks |

## Most important things to know

1. **It's a Python app stack, not a binary** — full readable source under `venv/`.
2. **nginx is the only intended entry point**, but **every backend also binds `0.0.0.0`** and
   there is **no inbound host firewall** → the TLS/auth front door is bypassable on the LAN.
   See [08-security.md](08-security.md). This is the top issue.
3. **An unauthenticated Apache Tika** listens on `0.0.0.0:9998`.
4. The deployment is **mid Vietnamese-localization rollout**; a needed fix to
   `cs.workflow.responsible_views` currently lives only as a loose working file (not yet folded
   into `cust.plm` or the venv) — see [07-customization.md](07-customization.md).

## Conventions

- Paths are absolute (`/opt/contact/...`) or relative to the instance dir
  (`CADDOK_BASE = /opt/contact/instance`).
- **Secrets are never reproduced here** (e.g. the DB password that appears in the install PDFs).
- "Verified" = confirmed against the live system on 2026-06-28.
