---
title: CONTACT PLM offline (air-gapped) install runbook
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, raw/contact/install-docs/]
tags: [contact-software, plm, install, offline, air-gapped, runbook, ubuntu, vietnamese]
status: stable
---

# CONTACT PLM offline (air-gapped) install runbook

How the [[opt-contact]] stack was stood up on Ubuntu 24.04, reconstructed from the operator's
four Vietnamese guides in `raw/contact/install-docs/`.

## Summary
The four PDFs are one runbook split by method. **`cailinux.pdf`** (24 pp) is the master,
*online* version (apt PPAs, `uv`, `nvm`, postgresql.org repo, `wget` for Solr/Tika) and also
carries the full systemd units, nginx TLS config, and Vietnamese language-pack steps.
**`kocointernet.pdf`** ("no internet") and **`caiphanmemnen.pdf`** ("install base software")
are the *offline* variants that replace every download with a pre-staged bundle.
**`caisass.pdf`** documents building the `sass`/`graphviz` offline bundles on an internet host.
The deployed host matches the docs structurally, but with site-specific values substituted.

## Details

### Offline bundles
- `contact-offline-bundle-noble-amd64.tar.gz` → unpacks to three nested tarballs:
  `contact-home-runtime.tar.gz` (→ `/home/<user>`: `uv`, `nvm`/node22), `contact-opt-project.tar.gz`
  (→ `/opt/contact`: venv + packages + instance skeleton), `offline-apt-repo-noble-amd64.tar.gz`
  (→ `/opt/offline-apt-repo`, registered as `deb [trusted=yes] file:/…`).
- `postgres17-offline.tar.gz`, `solr_tika_java_offline.tar.gz`, `sass-offline.tar.gz`,
  `graphviz-offline-clean.tar.gz`.

### Install sequence (reconstructed)
1. **PostgreSQL 17** — `dpkg -i` the debs; relocate cluster to `/data` (`pg_dropcluster` →
   `pg_createcluster 17 main --datadir=/data/postgresql/17/main`); `CREATE USER` + `CREATE
   DATABASE ce16db OWNER …` + `ALTER ROLE … CREATEROLE`. *(DB password is hardcoded in the
   PDFs — a leak; see [[contact-plm-security]]. Not recorded here.)*
2. **OS users + bundles** — extract home-runtime & opt-project; register the offline apt repo.
3. **Python app** — `uv venv --python=3.14 --seed venv`; offline wheel install:
   `pip install --no-index --find-links=/opt/contact/packages -r packages/default.txt -c
   packages/constraints.txt`, then `psycopg[binary]==3.3.4`. (361 wheels;
   `all.txt`/`default.txt`/`constraints.txt` manifests.)
4. **sass + graphviz** — extract `sass-offline` (node_modules) + a `/opt/contact/bin/sass`
   wrapper shim (needs `nvm use 22`); `apt install ./*.deb` for graphviz.
5. **Instance** — `mkinstance --instance_location=/opt/contact/instance
   --log_dir=/var/log/contact --namespace=cust postgres` (interactive prompts answered in the
   docs); then `cdbpkg new cust.plm`, `dump_messages`, `cdbpkg sync`; scp the `soeds` dir from
   a Windows CDB instance. → [[contact-customization-cust-plm]]
6. **Redis + nginx + OIDC** — Redis; nginx TLS reverse proxy with a **self-signed SoluCA CA**
   (added to the system trust store) fronting the `127.0.0.1` upstreams; `site.conf`/
   `services.json` OIDC/issuer/Redis wiring. → [[contact-plm-architecture]]
7. **Search/extract tier** — OpenJDK 21; **Solr 9.10.1-slim** (`/data/solr`, `solr create -c
   core1 -d instance/storage/index/search/core1`); **Tika 3.3.1** (`--host 0.0.0.0 --port
   9998`). → [[contact-plm-data-tier]]
8. **systemd fleet** — ~20 units (worker, gatekeeper, oidc, ologin, docportal, blobstore,
   queues, broker, 3D conversion, role-cache `:8888`, index-dispatcher) + `ce-session-cleanup`
   / `ce-license-clock-update` timers.
9. **Vietnamese language pack** — `powerscript …/add_language_attrs.py --language vi`; scp `vi`
   XLF dirs; loop `cdbpkg xliff --import --sourcelang en --targetlang vi <pkg>` + `cdbpkg
   build`; `cdbpkg sync` + `dump_messages`. → [[contact-vietnamese-localization]]

### Docs-vs-reality (this host was parameterized)
The PDFs are a **template**; the operator substituted values at install time:

| In the docs | On this host |
|---|---|
| OS user/group `contact` | `vsi` |
| DB role `contact` | `plmvsi` |
| hostname `messhipbuilding` / `192.168.200.158` | `plm_vsi` / `172.17.10.131` |
| big inline `nginx.conf` block | smaller live `nginx.conf` + `sites-enabled/default` |

Post-install cleanup removed `/opt/offline-apt-repo`, `sass-offline`, and the `vi`/`vi-project`
XLF dirs (build inputs).

## Related
- [[opt-contact]] — the result of this runbook
- [[contact-plm-architecture]] · [[contact-plm-data-tier]] · [[contact-plm-config]]
- [[contact-vietnamese-localization]] — the language-pack step
- [[contact-plm-security]] — the plaintext-password & `[trusted=yes]`/CA-trust notes
- [[contact-source-access-via-ansible]] — how these PDFs were read

## Open questions
- Why does the live `nginx.conf` differ from the doc's inline block (reconfigured post-install)?
- The DB password is written two ways in the PDFs (a one-digit typo between them) — which is the live value? (reconcile against the wallet; don't dump)
- `cailinux` is the online method but the host was installed offline — used as reference, with `kocointernet`/`caiphanmemnen` executed?
