---
title: /opt/contact — the deployed PLM instance
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [contact-software, plm, deployment, opt-contact, instance]
status: stable
---

# /opt/contact

The live, running deployment of [[contact-software-plm]] (CIM Database PLM v16.2) on
[[vsi-precision-3680]]. **This is "the program" the analysis targets** — not a binary, but a
Python application stack.

## Summary
`/opt/contact` is a self-contained CONTACT Elements instance: a Python 3.14 virtualenv plus
an offline wheel cache, an instance config/data directory, and localization files. It was
installed **fully offline** (air-gapped) from bundles (see [[contact-offline-install]]). The
running system is a ~12-service constellation fronted by a [[contact-plm-architecture|gatekeeper]]
auth gateway, backed by [[contact-plm-data-tier|PostgreSQL + Solr + Tika + Redis + etcd]].
Files are owned by OS user `vsi`; the tree is world-readable, so the full Python **source is
readable** (`.py`, not just `.pyc`).

## Details
Top-level layout:

| Path | What it is |
|---|---|
| `venv/` | the virtualenv — installed Python **source** for `cdb` core + all `cs.*` modules. site-packages: `venv/lib/python3.14/site-packages` |
| `venv/bin/` | service & CLI entry points: `cdbsrv`, `cdbsh`, `cdbsql`, `cdbimp`/`cdbexp`, `cdbacs`, `cdbpkg`, `gatekeeper`, `oidc_server`, `ologin`, `blobstore`, `role_cache_updater`, `wfqueue`, `daily_mail_service`, … |
| `packages/` | 361 offline wheels (the install cache; mirrors `Source/packages`) |
| `instance/` | per-instance config + data (see below) — passed as `--instancedir` to every service |
| `xlf/` | localization / translation units, one dir per `cs.*` module (`cs.documents`, `cs.projects`, …) |

`instance/` highlights:
- `etc/` — all config: `cdbsrv.conf`, `gatekeeper.conf`, `oidc_auth.json`, `dbtab.yml`
  (DB mapping), `tls_config.json`, `secrets.json`, `passwd`, `csrf_exemptions.yml`,
  `acs/` (access control), `services.json`, `blobstore.conf`, `wallets/` (restricted), …
- `app_conf/` — per-module config under `cs/<module>/`, `cscdb/`, `cust/`
- `cust.plm/` — the customer customization package — in practice a **Vietnamese language
  pack** (editable install; see [[contact-customization-cust-plm]] and
  [[contact-vietnamese-localization]])
- `certs/`, `etcd/` (an "etc dynamic" cache, *not* an etcd service), `storage/`, `lib/`,
  `updates/`, `tmp/`

Identity / runtime:
- Runs as OS user **`vsi`**; DB role **`plmvsi`**, database **`ce16db`**.
- OIDC issuer host **`plm_vsi`** (`https://plm_vsi/oidc`).
- Managed by **systemd** units prefixed `contact-*` and `elements-*`
  (see [[contact-plm-architecture]]).

## Related
- [[contact-software-plm]] — the product this instantiates
- [[contact-plm-architecture]] — nginx front door, services, ports, request flow
- [[contact-plm-data-tier]] — PostgreSQL / Solr / Tika / Redis backends
- [[contact-plm-modules]] — the installed `cs.*` functional-module inventory
- [[cdb-platform]] / [[cdb-platform-mom]] / [[contact-powerscript]] — the core framework in `venv`
- [[contact-plm-config]] — instance config & deployment model
- [[contact-plm-operations]] — service control, logs, admin CLIs, backups
- [[contact-offline-install]] — the air-gapped install runbook
- [[contact-plm-security]] — security posture (network/host weaknesses)
- [[contact-customization-cust-plm]] / [[contact-vietnamese-localization]] — the `cust.plm` Vietnamese localization
- [[vsi-precision-3680]] — the host it runs on
- [[contact-source-access-via-ansible]] — how this (vsi-owned) tree was read for analysis
- **Human-readable doc set:** `docs/contact-plm/` (linear digest of these pages, with diagrams & an ops runbook)

## Open questions
- Which services/modules are actually licensed & in active use vs installed-but-idle.
- Backup/DR story for `instance/` + PostgreSQL + blobstore (all on one 87%-full disk).
