---
title: cdb Meta-Object Model (MoM) & customization surface
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, raw/contact/responsible_views.py]
tags: [contact-software, cdb, mom, orm, data-dictionary, user-exits, customization]
status: stable
---

# cdb Meta-Object Model (MoM) & customization surface

The developer-facing programming model of [[cdb-platform]]: a self-describing
object-relational metamodel plus the hook points customizers extend.

## Summary
In MoM, **every persistent thing is a Python class** deriving from
`cdb.objects.core.Object` (metaclass `cdb.objects.core.Class`), bound to a DB table via
`__maps_to__` and to a Data-Dictionary (DD) class via `__classname__`, with declarative
`Reference`/`Reference_1`/`Reference_N` relations and a class-level query/CRUD API
(`Query`, `KeywordQuery`, `ByKeys`, `Create`, `Update`, `Delete`). The **DD itself is modeled
in the same ORM** — entities/fields/views are first-class persistent objects — so
customization edits *DD content*, not raw DDL. Business/customer logic attaches through
**user exits** (`cdb.ue`), per-class `event_map` `(operation, phase)→method` entries, and
DD-configured operation hooks. This all runs under [[contact-powerscript]] at run-level
`APPLICATIONS_LOADED`.

## Details

### The ORM core
- `cdb.objects.core.Object` (base) / `Class` (metaclass) provide the ORM. `__maps_to__` →
  physical table (e.g. `Component.__maps_to__='cdb_components'`); `__classname__` → DD class
  (`View.__classname__='cdb_view'`); `__match__` drives polymorphic subclass resolution.
- `cdb.platform.mom.entities` models the DD: `Entity` (maps to `switch_tabelle`),
  `View(Entity)`, `Class(Entity)`, with `DDFields`, `Relships`, `Constraints`, `PrimaryKey`.
- `cdb.platform.mom.fields` is the field-type hierarchy: `DDCharField`/`DDIntegerField`/
  `DDFloatField`/`DDDateField`/`DDTextField`, plus the multi-language family
  `DDMultiLangField` (its `.LangFields` map each active language to a physical column —
  central to the [[contact-vietnamese-localization]] effort).
- `cdb.sqlapi` — high-level rows (`RecordSet2`/`Record`), low-level SQL, and `SQLdbms()`
  vendor dispatch; all field types collapse to four internal types (CHAR/INTEGER/FLOAT/DATE).
- `cdb.ddl` — introspect/build physical schema (`Table(name).hasColumn()`, `Column`, `Index`).

### DD view generators (`GENERATOR:` directive)
A userdefined DD view whose stored definition begins with `GENERATOR:` resolves a
fully-qualified Python function (`tools.getObjectByName`), calls it, and uses the returned
string as the view SQL (`cdb.platform.mom.relations.DDUserDefinedView`). This is exactly how
`raw/contact/responsible_views.py` is wired in: DD content registers
`cdbwf_responsible[_template]` with longtext `GENERATOR: cs.workflow.responsible_views.…`,
and `View.compile()` materializes a real DB view. See [[responsible-views-vi-hotfix]].

### Customization surface (how customers extend without forking)
1. **`event_map`** — per-class `(operation, phase) → method` dicts, merged across the class
   hierarchy/mix-ins (e.g. `Component.event_map = {('*','pre_mask'):'scan'}`).
2. **User exits** (`cdb.ue`) and **operation hooks** (`cdb.platform.mom.hooks`:
   `PowerscriptHook`, `OperationHook`) — declaratively attach code to operations.
3. **Entry-point plugins** — e.g. workflow org-contexts register under the setuptools group
   `cs.workflow_org_context` (`pkg=mod:CONTEXT`); loaded via `importlib.metadata`.
4. **DD content + `configuration/patches`** — JSON fixtures seeding entities/views/labels;
   the customer package mirrors into `app_conf` ([[contact-customization-cust-plm]]).

## Related
- [[cdb-platform]] — the package this model lives in
- [[contact-powerscript]] — the runtime that loads it
- [[responsible-views-vi-hotfix]] — worked example of a `GENERATOR:` view
- [[contact-customization-cust-plm]] — the declarative-config extension path
- [[contact-plm-modules]] — the `cs.*` family built on MoM

## Open questions
- How `cdb.comparch` discovers/orders the `cs.*` packages at `APPLICATIONS_LOADED`.
- The `cdbwrapc` C-kernel object-handle/operation-context semantics (opaque from Python).
- Full request lifecycle inside `cdb.wsgi.worker.app` (which hooks fire per HTTP request).
