---
title: CONTACT PLM instance configuration & deployment model
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [contact-software, plm, config, instance, systemd, secrets, wallets, deployment]
status: stable
---

# CONTACT PLM instance configuration & deployment model

How the [[opt-contact]] instance is configured and stood up: "one venv + one instancedir,"
driven by systemd, with layered config and wallet-based secrets.

## Summary
The deployment model is **one virtualenv plus one shared *instance directory***. Every
service is a systemd unit running a `venv/bin` entry point with
`--instancedir=/opt/contact/instance` (which becomes `CADDOK_BASE`). Configuration is layered
under that instance dir: `etc/` (engine + service config), `app_conf/{cs,cscdb,cust}/`
(per-module), `cust.plm/` (the customer package), `lib/` (user-exit scripts), `storage/`,
`etcd/`, `updates/`. The DB backend is PostgreSQL; secrets are wallet-isolated.

## Details

### Service launch
All app units run `User=vsi`, `WorkingDirectory=/opt/contact/instance`, `Type=simple`,
`Restart=always`, `Environment=CADDOK_LOGDIR=/var/log/contact` + a per-service
`CADDOK_TOOL`. Dependent services declare `After/Wants contact-worker-01` and
`ExecStartPre=/bin/sleep 20`. (Full unit list: [[contact-offline-install]].)

### Key config files (`instance/etc/`)
| File | Purpose / notable settings |
|---|---|
| `site.conf` | main engine config: `enable_config('std-solution')`; `CADDOK_WWWSERVICE_URL/OIDC_ISSUER/OIDC_LOGIN` = `https://plm_vsi…`; `CADDOK_ACTIVE_GUI_LANGUAGES` = en/de/**vi** (Tiếng Việt); `CADDOK_CDBPKG_HOST=vsi-precision-3680`; SMTP STARTTLS on |
| `dbtab.yml` | DB mapping — single default entry `plmvsi` → `host=localhost port=5432 dbname=ce16db user=plmvsi password=$(CADDOK_DB_PASSWORD)`, driver `python`/`psycopg`. Rest of file is commented Oracle/MSSQL/SQLite examples |
| `services.json` | service→backend wiring (Redis sessions, blobstore, Solr, Tika, 3D broker) — see [[contact-plm-data-tier]] |
| `secrets.json` | **wallet manifest** (not values): maps `cs.platform/{sqlapi,oidc,ologin,beaker,sessionstore,solr,blobstore,…}` → wallet files under `etc/wallets/` (0700), each `default_auto_unlock` |
| `oidc_auth.json` | OIDC ACR → `ElementsAuth` (local password verify) — see [[contact-plm-architecture]] |
| `blobstore.conf` | `vault_type=FileStore`, vault/db under `storage/blobstore` (note: conf `base_url :8998` is overridden by the unit's `--base-url :8082`) |
| `logging.yaml`, `cdbsrv_logging.yaml` | rotating file logs (10 MiB ×3) to `/var/log/contact`; cdbsrv adds session/client IDs |
| `cdbpkg_sync.conf` | config domains kept in sync: AccessControl, ObjectLifeCycle, Rules, Decompositions, BatchOperations, PowerReports |
| `tnsnames.ora` | **unused** Oracle template leftover (HOST `alibaba`) — backend is PostgreSQL |
| `csrf_exemptions.yml` | one legacy elink path exempted from CSRF check |

### Secrets / wallets
No cleartext credentials in config. `$(CADDOK_DB_PASSWORD)` and other service secrets are
resolved at runtime from per-service **wallets** (`cdbwallet`) in `etc/wallets/` (0700,
vsi-only). `mkinstance` generates a separate wallet per service. Caveat: all wallets
`default_auto_unlock` (host compromise → creds) — see [[contact-plm-security]].

### Config selection & package sync
`site.conf` points `CADDOK_SERVICE_CONFIG` at `services.json` (production profile;
`webdev_services.json` is the dev alternative). The host is the package/config master
(`CADDOK_CDBPKG_HOST`); customizations are applied through the comparch
`configuration/patches` mechanism into `app_conf/cust/plm/{master,current}`
([[contact-customization-cust-plm]]), not via imperative `updates/` scripts (only the stock
`custom_update_template.py` exists there).

## Related
- [[opt-contact]] — the instance these files configure
- [[contact-plm-architecture]] — services launched from this config
- [[contact-plm-data-tier]] — `services.json`/`dbtab.yml` backends
- [[contact-customization-cust-plm]] — the `cust.plm` layer & app_conf mirror
- [[contact-offline-install]] — how the instance was created (`mkinstance`)
- [[contact-plm-security]] — secrets/wallet & world-readable-config posture

## Open questions
- Contents of `app_conf/{cs,cscdb,cust}/` per-module overrides (not fully enumerated).
- Wallet auto-unlock key location/perms.
