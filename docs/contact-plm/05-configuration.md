# 05 — Configuration & Deployment Model

## The "one venv + one instancedir" model

Every service is a systemd unit running a `venv/bin` entry point with
`--instancedir=/opt/contact/instance`. That instance directory becomes **`CADDOK_BASE`** and
holds all configuration and instance data. Configuration is layered:

```
instance/
├── etc/         # engine + service config (see table below)
├── app_conf/    # per-module config: cs/<module>/, cscdb/, cust/
├── cust.plm/    # the customer customization package (editable install)
├── lib/         # user-exit (.ue) scripts + service code
├── storage/     # blobstore vault + Solr index config
├── etcd/        # "etc dynamic" runtime cache (not an etcd service)
├── updates/     # custom update/migration scripts (only the stock template is present)
├── certs/       # dhparam.pem
└── tmp/
```

## Key files in `instance/etc/`

| File | Purpose / notable settings |
|---|---|
| `site.conf` | Main engine config. `enable_config('std-solution')`; `CADDOK_WWWSERVICE_URL`/`OIDC_ISSUER`/`OIDC_LOGIN` = `https://plm_vsi…`; **`CADDOK_ACTIVE_GUI_LANGUAGES` = en / de / vi** (Tiếng Việt); `CADDOK_CDBPKG_HOST=vsi-precision-3680`; `CADDOK_SERVICE_CONFIG` → `services.json`; SMTP STARTTLS on. |
| `dbtab.yml` | DB mapping — single default entry `plmvsi` → Postgres `ce16db` (psycopg). Rest is commented Oracle/MSSQL/SQLite examples. |
| `services.json` | service → backend wiring (Redis, blobstore, Solr, Tika, 3D broker) — see [02-architecture.md](02-architecture.md). `webdev_services.json` is the dev alternative. |
| `secrets.json` | **Wallet manifest** (not values): maps `cs.platform/{sqlapi,oidc,ologin,beaker,sessionstore,solr,blobstore,…}` → wallet files under `etc/wallets/` (0700), each `default_auto_unlock`. |
| `oidc_auth.json` | OIDC ACR → `ElementsAuth` (local password verify). `*.example.json` variants for ldap/azure/adfs2016/kerberos. |
| `blobstore.conf` | `vault_type=FileStore`, vault/db under `storage/blobstore` (`base_url :8998` overridden by the unit's `--base-url :8082`). |
| `logging.yaml`, `cdbsrv_logging.yaml` | Rotating file logs (10 MiB × 3) to `/var/log/contact`; cdbsrv adds session/client IDs. |
| `cdbpkg_sync.conf` | Config domains kept in sync: AccessControl, ObjectLifeCycle, Rules, Decompositions, BatchOperations, PowerReports. |
| `csrf_exemptions.yml` | One legacy elink path exempted from CSRF check. |
| `tls_config.json` | TLS settings → system CA bundle. |
| `tnsnames.ora` | **Unused** Oracle template leftover. |
| `acs/` | Access-control config (`acs.conf`, `acs_threed.conf`). |
| `wallets/` | Secret material (0700, vsi-only). |

## Secrets & wallets

**No cleartext credentials in config.** `$(CADDOK_DB_PASSWORD)` and other service secrets are
resolved at runtime from per-service **wallets** (`cdbwallet`) under `etc/wallets/` (mode 0700,
vsi-only). `mkinstance` generates a separate wallet per service.

⚠ Every wallet entry is `default_auto_unlock`, so wallets unlock automatically at unattended
service start — meaning the unlock material is on-host and host compromise yields the secrets.
And `instance/etc` itself is world-readable (config disclosure). See
[08-security.md](08-security.md).

## Customization plumbing

- The customer package `cust.plm` is installed **editable** (`__editable__.cust_plm-1.0.0`), so
  its source stays in `instance/cust.plm/` but imports as `cust.plm`
  ([07-customization.md](07-customization.md)).
- At config-apply time, `cdb.comparch` projects each module's "master" config into the running
  instance under `app_conf/<ns>/<module>/{master,current}/`, where per-module `patches.json`
  becomes `local_changes.json`.
- Schema/content changes are driven through this `configuration/patches` mechanism, **not** via
  imperative `updates/` scripts (only the stock `custom_update_template.py` exists there).
- This host is the package/config master (`CADDOK_CDBPKG_HOST`).

## Offline install footprint

`packages/` holds **361 wheels** (the pip install cache) plus manifests `all.txt`,
`default.txt`, `constraints.txt`. The stand-up path is `mkinstance` + offline wheels; no network
access is required. Full procedure: [09-installation.md](09-installation.md).

→ Next: [06-modules.md](06-modules.md)
