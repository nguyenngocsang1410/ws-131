# 03 — Platform & Framework (`cdb`)

Everything in CONTACT Elements is built on **`cdb`**, a mature object-relational application
framework sitting on a compiled C kernel (`cdbwrapc`). This doc covers the programming model a
developer/customizer works with.

## The Meta-Object Model (MoM)

**Every persistent thing is a Python class.** Classes derive from `cdb.objects.core.Object`
(metaclass `cdb.objects.core.Class`) and bind declaratively to the database:

- `__maps_to__` → physical table (e.g. `Component.__maps_to__ = 'cdb_components'`)
- `__classname__` → Data-Dictionary (DD) class (e.g. `View.__classname__ = 'cdb_view'`)
- `__match__` → polymorphic subclass resolution
- `Reference` / `Reference_1` / `Reference_N` → declared relationships
- Class-level API on every object: `Query`, `KeywordQuery`, `ByKeys`, `Create`, `Update`,
  `Delete`, `GetTableName`, `GetTablePKeys`

### The Data Dictionary is self-describing

The DD (entities, fields, views, relations) is modeled with the *same* ORM:

- `cdb.platform.mom.entities` — `Entity` (maps to `switch_tabelle`), `View(Entity)`,
  `Class(Entity)`, exposing `DDFields`, `Relships`, `Constraints`, `PrimaryKey`.
- `cdb.platform.mom.fields` — the field-type hierarchy: `DDCharField`, `DDIntegerField`,
  `DDFloatField`, `DDDateField`, `DDTextField`, and the multi-language family
  **`DDMultiLangField`** (its `.LangFields` maps each active UI language to a physical column —
  central to the Vietnamese rollout, [07-customization.md](07-customization.md)).

Because entities/fields/views are themselves persistent objects, **customization edits DD
content, not raw DDL.**

### Data access (`cdb.sqlapi`, `cdb.ddl`)

- `cdb.sqlapi` — high-level rows (`RecordSet2`, `Record`), low-level SQL, `quote()`/
  `make_literals()`, and `SQLdbms()` vendor dispatch. All field types collapse to four internal
  types: CHAR / INTEGER / FLOAT / DATE (→ `str`/`int`/`float`/`datetime`, NULL → `None`). The DB
  connection opens implicitly on import.
- `cdb.ddl` — introspect/build physical schema: `Table(name).hasColumn()`, `Column`, `Index`, `View`.
- `cdb.i18n` — `Languages()` enumerates active UI languages; pervasive multi-language behavior.

## DD view generators (the `GENERATOR:` directive)

A userdefined DD view whose stored definition begins with `GENERATOR:` resolves a
fully-qualified Python function, calls it, and uses the returned string as the view's SQL
(`cdb.platform.mom.relations.DDUserDefinedView`). `View.compile()` then materializes a real DB
view. This is exactly how the `cdbwf_responsible` views are produced — see the worked example in
[07-customization.md](07-customization.md).

## `powerscript` — the runtime launcher

`venv/bin/powerscript` is **not a separate language**; it's a thin launcher into
`cdb.scripts.powerscript.main` that boots the CONTACT runtime and then runs ordinary CPython:

- `powerscript -m <module>` runs a module, `-c` execs a string, a path runs as `__main__`,
  otherwise it opens the **"CONTACT Elements PowerScript"** REPL.
- A `#!/usr/bin/env powerscript` shebang means **"run this `.py` as CPython 3.14 inside the
  initialized, DB-connected CONTACT environment."**
- Several services run as powerscript modules (docportal, the 3D broker); maintenance scripts
  too (e.g. regenerating views).

### Run-level bootstrap (`cdb.rte`)

Every entry point (powerscript, `cdbsrv`, `cdbsql`, queues) shares an ordered init sequence;
each level emits a `cdb.sig` signal:

| Level | Name | What becomes usable |
|---|---|---|
| 0 | `INTERPRETER_RUNNING` | bare Python |
| 1 | `ENVIRONMENT_SET_UP` | `CADDOK_HOME`/PATH |
| 2 | `INSTANCE_ATTACHED` | config loaded, python path + logging |
| 3 | `DATABASE_CONNECTED` | `cdb.sqlapi` usable |
| 4 | `APPLICATIONS_LOADED` | configured `cs.*`/`cust` packages loaded |

User-exit and powerscript code runs at level 4.

## The application server (`cdbsrv`)

`cdbsrv` = `cdb.wsgi.worker` (systemd `contact-worker-01`, `:8080`). It serves
`cdb.wsgi.worker.app.application` via a WSGI server. Customer/business logic is injected via:

1. **`event_map`** — per-class `(operation, phase) → method` dicts, merged across the class
   hierarchy/mix-ins (e.g. `Component.event_map = {('*','pre_mask'): 'scan'}`).
2. **User exits** (`cdb.ue`) and **operation hooks** (`cdb.platform.mom.hooks`:
   `PowerscriptHook`, `OperationHook`).
3. **Entry-point plugins** — e.g. workflow org-contexts register under the setuptools group
   `cs.workflow_org_context`.
4. **DD content + `configuration/patches`** — JSON fixtures seeding entities/views/labels (the
   path `cust.plm` uses, [07-customization.md](07-customization.md)).

## The `cs.*` module family

~55 `cs.*` functional packages are layered over `cdb`, each shipping `module_metadata.json` +
`configuration/content/*.json` DD fixtures, loaded at `APPLICATIONS_LOADED` via `cdb.comparch`.
The customer package `cust.plm` is just another package in this scheme. Inventory:
[06-modules.md](06-modules.md).

## Notes / caveats

- The core ships as a **compiled C extension** (`cdbwrapc._cdbwrapc…so`) — no pip-visible
  version; it travels with the 16.2 product and **bundles Oracle Instant Client 23.1** libs even
  though the backend is PostgreSQL ([08-security.md](08-security.md)).
- `SQLdbms()` dispatch means hand-built SQL must handle cross-vendor differences (e.g. emit
  `COLLATE` only on MSSQL) — the developer's responsibility.

→ Next: [04-data-tier.md](04-data-tier.md) · Related: [07-customization.md](07-customization.md)
