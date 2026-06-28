# 04 — Data & Storage Tier

A single-node, self-hosted data tier (no cloud). All stores listen on `127.0.0.1` **except**
Apache Tika.

## Components

| Store | Endpoint | Where it lives | Role |
|---|---|---|---|
| **PostgreSQL 17** | `127.0.0.1:5432` | `/data/postgresql/17/main` | transactional PLM metadata (objects, relations, BOMs, workflow state). DB `ce16db`, role `plmvsi` |
| **blobstore** | `:8082` (`/signedblob`) | vault bind-mounted from `/data/contact-storage`; metadata SQLite `filestore.db` | binary content (documents, CAD files) |
| **Apache Solr 9.10.1** | `127.0.0.1:8983`, core `core1` | solr home `/data/solr/data` | full-text + object search index |
| **Apache Tika 3.3.1** | `0.0.0.0:9998` ⚠ | jar in `/data/tika` | text/metadata extraction from uploads |
| **Redis** | `127.0.0.1:6379` db 0 | — | sessions, session data, ologin + OIDC state |
| `instance/etcd` | (directory, **not** a service) | `/opt/contact/instance/etcd` | "etc dynamic" cache: compiled templates, keyfiles, OIDC client records, `msgs.json` |

> **Tika is the lone externally-bound store** (`--host 0.0.0.0`, `auth: null`). PostgreSQL,
> Redis and Solr are correctly loopback-only. See [08-security.md](08-security.md).

## Database connection

- `instance/etc/dbtab.yml` has a single default entry `plmvsi`:
  `host=localhost port=5432 dbname=ce16db user=plmvsi password=$(CADDOK_DB_PASSWORD)`,
  driver `python`, mode `psycopg`.
- `$(CADDOK_DB_PASSWORD)` is **not** a literal — it is resolved at runtime from the `sqlapi`
  wallet (`instance/etc/wallets/sqlapi.json`); see [05-configuration.md](05-configuration.md).
- `cdb.authentication.txpool.worker` pools auth transactions (distinct from per-request
  psycopg connections).
- `instance/etc/tnsnames.ora` is an **unused Oracle template leftover** from `mkinstance`
  (HOST `alibaba`). The backend is PostgreSQL only.

## Blob storage

- `instance/etc/blobstore.conf`: `vault_type=FileStore`,
  `vault_path=${CADDOK_BASE}/storage/blobstore/vault`,
  `database=${CADDOK_BASE}/storage/blobstore/filestore.db`.
- The `vault` subdir is a **bind mount** from `/data/contact-storage/blobstore/vault` (verified
  via `findmnt` + matching inodes), so large binaries physically live on `/data`, while the
  metadata index (`filestore.db`) and replication DB (`repl.db`) stay under `instance/storage`.
- Blobs are UUID-named files bucketed by year/day-of-year.
- The service entry point is `cdb.storage.replication.server`; cross-site **replication is
  configured but disabled** (`null` adapter — single site).
- `site.conf` documents `CADDOK_WEBUI_USE_PRESIGNED_BLOB_URL`: when set, web clients get
  presigned URLs to fetch files **directly from blobstore, bypassing the app server**.

## Search index pipeline

```
upload ─▶ blobstore (vault on /data)
            │
index job queued in PostgreSQL (cdb.index.queue)
            │
index_job_processor  (systemd: elements-index-job-dispatcher)
            │── send content ─▶ Tika :9998  (TextExtractor, httpx; cap CADDOK_TES_MAX_TEXT_LENGTH ≈ 5,000,000 chars)
            │                      └─ extracted text stored as hidden blob "_cdb_extracted_text"
            └── push document ─▶ Solr core1  (SolrConnection; commitWithin ≈ 5000 ms)
```

- Solr `core1` schema models PLM objects: `uniqueKey=object_id`, plus `object_type`, `owner_*`,
  and CONTACT analyzed field types `identifying` / `classifying` / `descriptive` / `content`
  (extracted full-text, `stored=false`), `contentHL`, `summary`, `lang` (multi-valued),
  `autocomplete`, `cdb_obsolete`, timestamps.
- Solr config template lives at `instance/storage/index/search/core1/conf/` (schema.xml,
  solrconfig.xml, synonyms/stopwords) and is copied into the Solr home.

## Redis usage

Backs four logical services (all `redis://127.0.0.1:6379/0`): `cdb.sessionstore`,
`cdb.storage.sessiondata` (`RedisBackend`), `cdb.ologin.storage`, `cdb.oidc.storage`. It is
**not** the index queue (that is SQL-backed). Runs **without a password** — see
[08-security.md](08-security.md).

## Operational notes

- Everything (`/data/postgresql`, `/data/contact-storage`, `/data/solr`, `/data/tika`) is on a
  single root partition `/dev/sda4` reported **~87% full** — watch disk headroom.
- Backups must cover **both** PostgreSQL (`ce16db`) **and** the blob vault (`/data/contact-storage`);
  the Solr index and `instance/etcd` are rebuildable/excludable.

→ Next: [05-configuration.md](05-configuration.md)
