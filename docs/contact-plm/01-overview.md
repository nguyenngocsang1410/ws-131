# 01 — Overview

## What this system is

`/opt/contact` is a running deployment of **CONTACT Software GmbH's CIM Database PLM**, the
company's flagship Product Lifecycle Management suite, delivered on the **CONTACT Elements**
low-code application platform. CONTACT is a German vendor (contact-software.com); source
headers read `Copyright (C) 1990 - 2026 CONTACT Software GmbH`.

It is **not a compiled binary** — it is a Python 3.14 application: a core framework (`cdb`)
plus dozens of functional modules (`cs.*`), all installed as readable source in a virtualenv.

## Product & versions

| Component | Identity | Version |
|---|---|---|
| Product | `cscdb.product` — "CIM Database PLM" | 16.2.0.4 |
| Platform | `cs.platform` — "CONTACT Elements Platform" | 16.2.8 |
| Build tooling | `setuptools-ce` | 16.1.1.2 |
| Core framework | `cdb` / `cdbwrapc` (compiled C kernel) | travels with the 16.2 product |
| Python runtime | CPython (via `uv`) | 3.14.6 |

Most functional modules are on the **16.2.0.x** train; a few lag at 16.1.0.x; the CAD/Office
desktop connectors are on a separate **15.x** train (they version against the external CAD/
Office apps, not the PLM server). Full list: [06-modules.md](06-modules.md).

## What this installation is specialized for

The installed module set makes this a **general engineering PLM** focused on:

- **Multi-CAD engineering** — desktop connectors for AutoCAD, Inventor, NX, SolidWorks (+ CADBASE),
  plus 3D visualization/conversion.
- **Document management & control** — documents, docmap, docportal, PDF viewer, ECM, with
  **e-signature** (`dsig`) and **audit trail**.
- **Project & portfolio management / costing** — projects, costs, scheduling, efforts,
  resources, taskboard/taskmanager, workplan.
- **Plus** classification, materials, requirements, variants, BOM, workflow.
- **Governance hardening present** — MFA (TOTP) + e-signature + audit trail.

It is **not** running IoT, ERP-connector, or ticketing — those appear only as translation/config
scaffolding in the catalog, not as installed code (see [06-modules.md](06-modules.md)).

## Host & operator context

- **Host:** `vsi-precision-3680`, Ubuntu 24.04 (noble), x86_64. Runs as OS user/group `vsi`.
- **Naming:** internal hostname `plm_vsi` (→ `172.17.10.131` in `/etc/hosts`); DB role `plmvsi`;
  database `ce16db`. The TLS CA is self-signed "SoluCA".
- **Deployment style:** fully **offline / air-gapped** install from pre-staged bundles
  (see [09-installation.md](09-installation.md)).
- **In flight:** a **Vietnamese (`vi`) localization** of the whole PLM
  (see [07-customization.md](07-customization.md)). The install guides themselves are in
  Vietnamese; host/DB naming and the SoluCA CA point to a Vietnam-based integrator.

## Directory layout (`/opt/contact`)

```
/opt/contact/
├── venv/        # the virtualenv — readable Python source for cdb + all cs.* modules
│   ├── bin/     # entry points: cdbsrv, cdbsh, cdbsql, gatekeeper, oidc_server, blobstore, ...
│   └── lib/python3.14/site-packages/{cdb, cs/<module>, cust/plm, ...}
├── packages/    # 361 offline wheels (the install cache) + all.txt/default.txt/constraints.txt
├── instance/    # per-instance config + data (CADDOK_BASE) — see 05-configuration.md
│   ├── etc/         # all config (site.conf, dbtab.yml, services.json, secrets.json, wallets/, ...)
│   ├── app_conf/    # per-module config (cs/, cscdb/, cust/)
│   ├── cust.plm/    # the customer customization package (editable install)
│   ├── storage/     # blobstore vault (bind-mounted from /data), Solr config template
│   ├── etcd/        # "etc dynamic" cache (NOT an etcd service)
│   └── lib/ updates/ certs/ tmp/
└── xlf/         # localization / translation catalog (one dir per cs.* module; a superset of installed code)
```

→ Next: [02-architecture.md](02-architecture.md)
