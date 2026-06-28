# 09 — Installation Runbook (offline / air-gapped)

Reconstructed from the operator's four Vietnamese guides in `raw/contact/install-docs/`. The
host was installed **fully offline** on Ubuntu 24.04 (noble).

> ⚠ The PDFs contain the **plaintext PostgreSQL password** for the app role and register
> `[trusted=yes]` apt sources + a host-wide trusted CA. Treat the notes as sensitive. The
> password value is **not** reproduced here.

## The four guides

| PDF | Title (≈) | Role |
|---|---|---|
| `cailinux.pdf` (24 pp) | "install Linux" | **master** guide (online method) + full systemd units, nginx/TLS, vi pack |
| `kocointernet.pdf` | "no internet" | **offline** variant — swaps downloads for staged bundles |
| `caiphanmemnen.pdf` | "install base software" | **offline** variant (base/platform software) |
| `caisass.pdf` | "install sass" | how the `sass`/`graphviz` offline bundles were built upstream |

## Offline bundles (staged on the host)

| Bundle | Contents |
|---|---|
| `contact-offline-bundle-noble-amd64.tar.gz` | → `contact-home-runtime.tar.gz` (`/home/<user>`: uv + nvm/node22), `contact-opt-project.tar.gz` (`/opt/contact`: venv + packages + instance skeleton), `offline-apt-repo-noble-amd64.tar.gz` (`/opt/offline-apt-repo`) |
| `postgres17-offline.tar.gz` | PostgreSQL 17 debs |
| `solr_tika_java_offline.tar.gz` | OpenJDK 21, Solr 9.10.1-slim, Tika 3.3.1 |
| `sass-offline.tar.gz` | node_modules for the `sass` compiler |
| `graphviz-offline-clean.tar.gz` | graphviz debs |

## Install sequence

1. **PostgreSQL 17** — `dpkg -i` the debs; relocate the cluster to `/data`:
   `pg_dropcluster --stop 17 main` → `pg_createcluster 17 main --datadir=/data/postgresql/17/main`;
   create DB/role (`CREATE USER … ; CREATE DATABASE ce16db OWNER … ; ALTER ROLE … CREATEROLE;`).
2. **OS users + bundles** — extract `contact-home-runtime` and `contact-opt-project`; register the
   offline apt repo: `echo 'deb [trusted=yes] file:/opt/offline-apt-repo/apt-repo ./' >
   /etc/apt/sources.list.d/contact-offline.list && apt update`.
3. **Python app** — `cd /opt/contact && uv venv --python=3.14 --seed venv && source venv/bin/activate`;
   offline install:
   `pip install --no-index --find-links=/opt/contact/packages -r packages/default.txt -c packages/constraints.txt`,
   then `pip install --no-index psycopg[binary] psycopg-binary==3.3.4 --find-links=…`.
4. **sass + graphviz** — extract `sass-offline` (node_modules) + a `/opt/contact/bin/sass` wrapper
   shim (needs `nvm use 22`); `apt install ./*.deb` for graphviz.
5. **Instance** — `mkinstance --instance_location=/opt/contact/instance
   --log_dir=/var/log/contact --namespace=cust postgres` (the PDFs give the interactive prompt
   answers); then `cdbpkg new cust.plm`, `dump_messages`, `cdbpkg sync`; scp the `soeds` dir from a
   Windows CDB instance.
6. **Redis + nginx + OIDC** — install Redis; build the nginx TLS reverse proxy with a **self-signed
   SoluCA CA** (added to the system trust store) fronting the `127.0.0.1` upstreams; edit
   `site.conf`/`services.json` for OIDC issuer/login + Redis-backed sessions.
7. **Search/extract tier** — OpenJDK 21; **Solr 9.10.1-slim** to `/data/solr` + `solr create -c
   core1 -d /opt/contact/instance/storage/index/search/core1`; **Tika 3.3.1** to `/data/tika`,
   `tika.service` runs `java -jar tika-server-standard-3.3.1.jar --host 0.0.0.0 --port 9998`.
8. **systemd fleet** — install ~20 units (worker, gatekeeper, oidc, ologin, docportal, blobstore,
   queues, broker, 3D conversion, role-cache, index-dispatcher) + the `ce-session-cleanup` /
   `ce-license-clock-update` timers.
9. **Vietnamese language pack** — `powerscript …/add_language_attrs.py --language vi`; scp the `vi`
   XLF dirs; loop `cdbpkg xliff --import --sourcelang en --targetlang vi <pkg>` + `cdbpkg build`;
   finish with `cdbpkg sync` + `dump_messages`. (See [07-customization.md](07-customization.md).)

## Docs-vs-reality (this host was parameterized)

The PDFs are a **template**; the operator substituted values at install time:

| In the docs | On this host |
|---|---|
| OS user/group `contact` | `vsi` |
| DB role `contact` | `plmvsi` |
| hostname `messhipbuilding` / `192.168.200.158` | `plm_vsi` / `172.17.10.131` |
| large inline `nginx.conf` block | smaller live `nginx.conf` + `sites-enabled/default` |

Post-install cleanup removed build inputs (`/opt/offline-apt-repo`, `sass-offline`, the
`vi`/`vi-project` XLF dirs).

## Open questions

- Why does the live `nginx.conf` differ from the doc's inline block (reconfigured post-install)?
- The DB password is written two ways in the PDFs (a one-digit typo between them) — which is the live value?
- Was `cailinux` (online) used as reference while `kocointernet`/`caiphanmemnen` (offline) were
  actually executed?

→ Next: [10-operations.md](10-operations.md)
