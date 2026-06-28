---
title: CONTACT PLM data & storage tier
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [contact-software, plm, postgresql, solr, tika, redis, etcd, blobstore, storage]
status: stable
---

# CONTACT PLM data & storage tier

The external data stores and storage services that back the [[opt-contact]] deployment.

## Summary
Transactional PLM metadata lives in **PostgreSQL 17** (db `ce16db`, role `plmvsi`). Binary
content (documents/CAD files) is held by the **blobstore** (FileStore vault on `/data`).
Full-text search is **Apache Solr 9.10.1** (core `core1`), fed by **Apache Tika 3.3.1**
(text/metadata extraction). **Redis** holds session & OIDC state. There is **no real etcd
service** — `instance/etcd` is an on-disk "etc dynamic" cache. All stores except Tika listen
on `127.0.0.1`; Tika is on `0.0.0.0:9998`. It's a single-node, self-hosted tier (no cloud).

## Details
Observed 2026-06-28 (`ps`, `ss`, `findmnt`, config):

| Store | Endpoint | Detail |
|---|---|---|
| **PostgreSQL 17** | `127.0.0.1:5432` | data `/data/postgresql/17/main`; DB `ce16db`, role `plmvsi`; psycopg via `dbtab.yml`, password from the `sqlapi` wallet (`$(CADDOK_DB_PASSWORD)`); `cdb.authentication.txpool.worker` pools auth txns |
| **blobstore** | `:8082` (`/signedblob`) | `cdb.storage.replication.server`; `vault_type=FileStore`. Vault is **bind-mounted from `/data/contact-storage`** into `instance/storage/blobstore/vault`; metadata in SQLite `filestore.db`; blob files UUID-named, bucketed by year/day. Cross-site replication present but **disabled** (`null` adapter) |
| **Apache Solr 9.10.1** | `127.0.0.1:8983` (core `core1`) | solr home `/data/solr/data`; config template in `instance/storage/index/search/core1`. Schema indexes PLM objects: `uniqueKey=object_id`, `object_type`, `owner_*`, analyzed `identifying/classifying/descriptive/content` + full-text `content` (extracted) |
| **Apache Tika 3.3.1** | `0.0.0.0:9998` | `tika-server-standard-3.3.1.jar` at `/data/tika`, started `--host 0.0.0.0`; client `auth: null`, timeout 900s. **Externally bound, unauthenticated — see [[contact-plm-security]].** |
| **Redis** | `127.0.0.1:6379` (db 0) | backs `cdb.sessionstore`, `cdb.storage.sessiondata`, `cdb.ologin.storage`, `cdb.oidc.storage`. **No `requirepass`** ([[contact-plm-security]]) |
| `instance/etcd` | (dir, not a service) | "etc dynamic" local cache: compiled eLink templates, keyfiles, registered OIDC client records, `msgs.json`. No 2379/2380 listener |

### Data flow (verified)
Document upload → **blobstore** persists the binary (vault on `/data`). Index jobs are queued
in **PostgreSQL** (`cdb.index.queue`), pulled by the **`index_job_processor`**
(`elements-index-job-dispatcher`), which sends content to **Tika** for extraction
(`TextExtractor` httpx client; cap `CADDOK_TES_MAX_TEXT_LENGTH` ≈ 5 M chars, stored as a
hidden `_cdb_extracted_text` blob) → pushed to **Solr** (`SolrConnection`, commitWithin
≈5 s). Object metadata/relations/BOMs/workflow state → **PostgreSQL** via
[[cdb-platform|cdb]] `sqlapi`/`ddl`.

### DB connection wiring
`dbtab.yml` single default entry `plmvsi` → Postgres `ce16db` (driver `python`/`psycopg`).
`instance/etc/tnsnames.ora` is an **unused Oracle template leftover** from `mkinstance`
(HOST `alibaba`); the backend is PostgreSQL only. See [[contact-plm-config]].

## Related
- [[opt-contact]] — the deployment these back
- [[contact-plm-architecture]] — the services that talk to these stores
- [[contact-plm-config]] — `services.json`/`dbtab.yml`/`blobstore.conf` wiring
- [[cdb-platform]] — the `sqlapi`/`ddl` data-access layer
- [[contact-plm-security]] — Tika/Redis exposure assessment

## Open questions
- Does blobstore (`:8082`) enforce auth for direct/presigned blob access?
- Is Solr basic auth enabled (`cs.platform/solr/auth` exists) or relying on loopback only?
- Backup/retention for `/data/contact-storage` + the DB (all on one 87%-full `/dev/sda4`)?
- Why are both Solr `:8983` and `:7983` listening?
