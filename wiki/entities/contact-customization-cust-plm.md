---
title: cust.plm — the customer customization package
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [contact-software, plm, customization, cust-plm, vietnamese, localization]
status: stable
---

# cust.plm — the customer customization package

The single editable customer package that customizes [[opt-contact]] — in practice, a
**Vietnamese localization** of the whole PLM, delivered as data/config, not code.

## Summary
`cust.plm` ("Customer module", v1.0.0) is installed editable (`__editable__.cust_plm-1.0.0`)
at `instance/cust.plm/`, depending only on `cs.platform`. It contains **no custom business
logic** — `cust/plm/__init__.py` is a 2-line stub, `cdb_services=[]`, no hooks. All
customization is **declarative**: a schema delta adding Vietnamese (`vi`) columns and 56
per-module label-translation patch sets. It is the live face of the
[[contact-vietnamese-localization]] effort.

## Details

### Contents
- `cust/plm/configuration/schema.json` — adds **207 columns across 163 tables**, of which 205
  are `vi`/`*_vi` multilang variants (`name_vi`×83, `description_vi`×25, `label_vi`×10, …).
- `cust/plm/configuration/patches/cs.*/patches.json` — **56 patch sets** (55 `cs.*` modules +
  `cust.plm`) supplying Vietnamese UI label strings (e.g. `cdb_check_frame` →
  "Kiểm tra Cấu hình").
- `cust/plm/configuration/content/cdbdd_field.json` — seeds `cdb_iso_language_code='vi'` DD fields.
- `setup.py`: `find_namespace_packages(['cust.*'])`, `setuptools_ce.build` backend,
  `cdb_modules=['cust.plm']`; `module_metadata.json` registers it (built vs `cs.platform`
  16.2.8, has a `cdb_object_id`).

### The `cust` namespace + app_conf mirror mechanism
The package uses the PEP-420 `cust.*` namespace, installed editable so source stays in
`instance/cust.plm/` but imports as `cust.plm`. At config-apply time CONTACT's `comparch`
projects the package's "master" config into the running instance under
`app_conf/cust/plm/{master,current}/`, where per-module `patches.json` becomes
`local_changes.json` (verified byte-identical for `cs.admin`). This is the standard
"extend without forking core" path ([[cdb-platform-mom]]).

### What it does *not* do
No custom entities-as-logic, no services, no powerscript hooks, no applied `updates/` scripts
(only the stock template). The in-flight `responsible_views.py` fix is **not** part of
`cust.plm` yet ([[responsible-views-vi-hotfix]]).

## Related
- [[contact-vietnamese-localization]] — the broader rollout this implements
- [[opt-contact]] — the instance it customizes
- [[cdb-platform-mom]] — the DD/config extension model it uses
- [[contact-plm-config]] — the app_conf mirror & customization plumbing
- [[responsible-views-vi-hotfix]] — a related, not-yet-folded-in dev fix

## Open questions
- Will the `responsible_views` vi-fallback fix be folded into `cust.plm` (vs patching the venv, which a reinstall would overwrite)?
- Do role-definition multilang fields genuinely lack `vi` variants in the DB (making the fallback load-bearing)?
