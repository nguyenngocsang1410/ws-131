---
title: cdb — the CONTACT Elements core platform
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, raw/contact/responsible_views.py]
tags: [contact-software, cdb, platform, framework, core, mom]
status: stable
---

# cdb — the CONTACT Elements core platform

The base Python package every CONTACT module and customization is built on; the runtime of
the application server at [[opt-contact]].

## Summary
`cdb` is CONTACT's core framework. It provides the **Meta-Object Model** (`cdb.platform.mom`
— entities, fields, views), a SQL abstraction (`cdb.sqlapi`), schema/DDL tooling
(`cdb.ddl`), internationalization (`cdb.i18n`), workflow primitives (`cdb.workflow`), and
authentication. The application server (`cdbsrv`, run as `contact-worker-01`) is a `cdb`
process; the `cs.*` functional modules and the `cust.*` customer code all import from `cdb`.
Customer logic is typically written as **powerscript** ([[contact-powerscript]]) against the
[[cdb-platform-mom|MoM]].

## Details
Verified 2026-06-28 (in `venv/lib/python3.14/site-packages/cdb`, full `.py` source present):

- Sub-packages/modules seen: `cdb.platform.mom` (`entities`, `fields`), `cdb.sqlapi`,
  `cdb.ddl`, `cdb.i18n`, `cdb.workflow`, `cdb.sqlite`, `cdb.tools`, `cdb.InstallScript`,
  `cdb.authentication` (incl. `txpool.worker`), `cdb.objects.org` (e.g. `Person`).
- CLI / service entry points (in `venv/bin`): `cdbsrv` (app server), `cdbsh` (shell),
  `cdbsql`, `cdbimp`/`cdbexp` (import/export), `cdbacs` (access control), `cdbpkg` (package
  mgmt), `cdbfls`, `cdbldap`, `cdbwallet`, plus the gatekeeper/oidc/blobstore services.

Worked example — `raw/contact/responsible_views.py` (a powerscript) imports:
```python
from cdb import ddl, i18n, sqlapi
from cdb.objects.org import Person
from cdb.platform.mom.entities import View
from cdb.platform.mom.fields import DDMultiLangField
from cs.workflow.subjects import get_context_ml_field_names, get_contexts
```
…which directly exposes the model: **entities** and **Views** from the MoM, multi-language
fields (`DDMultiLangField`), the `sqlapi`/`ddl` data layer, and `cs.*` building on `cdb`.

The runtime is Python **3.14** (CPython 3.14.6 via `uv`), with both `.py` and matching
`.pyc` present (438/438 in `cdb`), i.e. shipped as readable source.

Note: `cdbsrv` (`cdb.wsgi.worker`) is the WSGI application server (systemd `contact-worker-01`,
`:8080`); business logic runs as user exits via per-class `event_map` `(operation,phase)→method`
and DD hooks ([[cdb-platform-mom]]).

## Related
- [[contact-software-plm]] — the product cdb underpins
- [[opt-contact]] — the deployment where cdb runs
- [[cdb-platform-mom]] — the Meta-Object Model & customization surface in depth
- [[contact-powerscript]] — the runtime launcher (run-levels)
- [[contact-customization-cust-plm]] — how customers extend cdb/cs
- [[contact-plm-modules]] — the `cs.*` family layered on cdb

## Open questions
- How `cdb.comparch` discovers/orders `cs.*` packages at `APPLICATIONS_LOADED`.
- The `cdbwrapc` C-kernel object-handle/operation-context semantics (binary-only).
