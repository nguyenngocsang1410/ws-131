---
title: powerscript — the CONTACT runtime launcher
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, raw/contact/responsible_views.py]
tags: [contact-software, cdb, powerscript, runtime, run-levels]
status: stable
---

# powerscript — the CONTACT runtime launcher

What "powerscript" actually is in [[cdb-platform]]: not a separate language, but a CPython
launcher that boots the CONTACT runtime and then runs ordinary Python inside it.

## Summary
`venv/bin/powerscript` is a thin entry point into `cdb.scripts.powerscript.main`. It builds a
runtime argument parser at run-level `APPLICATIONS_LOADED`, enters `with rte.Runtime(options):`
(which connects the DB and loads configured packages), then dispatches like CPython: `-m`
runs a module (`runpy`), `-c` execs a string, a path runs as `__main__`, otherwise it opens
an interactive **"CONTACT Elements PowerScript"** REPL. So a `#!/usr/bin/env powerscript`
shebang means **"run this `.py` as CPython 3.14 inside the initialized, DB-connected CONTACT
environment."** `instance/etc/powerscript.conf` is effectively empty (38 bytes).

## Details

### Run-level bootstrap (`cdb.rte`)
Every CONTACT entry point (powerscript, `cdbsrv`, `cdbsql`, the queue workers, services)
shares an ordered, non-lowerable init sequence, each level emitting a `cdb.sig` signal:

| Level | Name | What becomes usable |
|---|---|---|
| 0 | `INTERPRETER_RUNNING` | bare Python |
| 1 | `ENVIRONMENT_SET_UP` | `CADDOK_HOME`/PATH set |
| 2 | `INSTANCE_ATTACHED` | config files loaded, python path + logging |
| 3 | `DATABASE_CONNECTED` | `cdb.sqlapi` usable (importing it opens the DB) |
| 4 | `APPLICATIONS_LOADED` | configured `cs.*`/`cust` packages loaded |

User-exit and powerscript code runs at level 4. Apps connect to the per-level hook signals
(e.g. `APPLICATIONS_LOADED_HOOK`) for startup logic.

### Usage seen in this deployment
- Services launched as powerscript modules: docportal (`powerscript -m cs.docportal.app …`),
  the 3D broker (`powerscript -m cs.threed.services.broker_service`).
- Maintenance scripts: regenerating DD views via `powerscript -m cs.workflow.responsible_views`
  (see [[responsible-views-vi-hotfix]]); the Vietnamese language attrs step
  (`powerscript …/add_language_attrs.py --language vi`, see [[contact-vietnamese-localization]]).
- `raw/contact/responsible_views.py` carries the `#!/usr/bin/env powerscript` shebang.

## Related
- [[cdb-platform]] — the framework powerscript boots
- [[cdb-platform-mom]] — what level-4 code manipulates
- [[responsible-views-vi-hotfix]] — a powerscript module worked example
- [[contact-plm-architecture]] — services run as powerscript modules

## Open questions
- How (if at all) powerscript differs from plain CPython beyond runtime init (sandboxing? injected globals?).
