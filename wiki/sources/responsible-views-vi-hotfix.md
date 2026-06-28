---
title: "Source: responsible_views.py (vi-fallback hotfix)"
type: source
created: 2026-06-28
updated: 2026-06-28
sources: [raw/contact/responsible_views.py]
tags: [contact-software, cs-workflow, responsible, hotfix, vietnamese, source]
status: stable
---

# Source: responsible_views.py (vi-fallback hotfix)

The loose working file copied to `raw/contact/responsible_views.py` — a developer-edited copy
of a stock CONTACT module, central to the [[contact-vietnamese-localization]] rollout.

## What it is
A `#!/usr/bin/env powerscript` module that generates the SQL for two Data-Dictionary
**userdefined views**, `cdbwf_responsible` and `cdbwf_responsible_template`, via the
`GENERATOR:` mechanism ([[cdb-platform-mom]]). The views enumerate workflow **"responsible"
subjects** — who/what can be assigned responsibility or be a task recipient — unioning users
(`angestellter`), global roles (`cdb_global_role`), and pluggable per-context roles. Each row
exposes `subject_uuid`, `subject_type` (+ localized `subject_type_XX`), `subject_id`/`_id2`,
an `order_by`, and localized `name_XX`/`description_XX` per active UI language.

## Key fact — it is a hotfix, not a cust.plm file
It is an **edited copy of the shipped module**
`venv/.../site-packages/cs/workflow/responsible_views.py`. The **only functional change** is
in `_get_multilang_type` / `_get_multilang`: stock code does direct dict indexing
`type_map[isocode]` / `field_map[isocode]` for every language from `i18n.Languages()`; the
edit adds a **`vi → en → de → first` fallback** via `.get(isocode, fallback)`.

- **Root cause:** adding `vi` as an active GUI language ([[contact-vietnamese-localization]])
  makes the generator iterate `vi`, but some role-definition multilang fields have no `vi`
  variant → `KeyError` while building the UNION SELECT.
- **Status:** the fix exists **only in this loose file** — not in the venv copy, not in
  [[contact-customization-cust-plm|cust.plm]]. Regeneration is run via
  `powerscript -m cs.workflow.responsible_views` (then `compile_views()`).

## Framework it demonstrates
Its imports map onto [[cdb-platform]] layers: `cdb.ddl` (`Table(t).hasColumn` schema
introspection), `cdb.i18n` (`Languages()` to fan out per-language columns), `cdb.sqlapi`
(`SQLdbms()` dispatch — emits `COLLATE` only on MSSQL), `cdb.platform.mom.entities.View`
(+`compile()`), `cdb.platform.mom.fields.DDMultiLangField` (`.LangFields` → physical column
per language), and `cs.workflow.subjects` (the entry-point-pluggable org-context registry,
group `cs.workflow_org_context`).

## Related
- [[contact-vietnamese-localization]] — why this bug appeared
- [[cdb-platform-mom]] — the `GENERATOR:` DD-view mechanism & `DDMultiLangField`
- [[contact-powerscript]] — how it's run
- [[contact-customization-cust-plm]] — where the fix arguably belongs

## Open questions
- Will the fix be folded into `cust.plm` (durable) or patched into the venv (lost on reinstall)?
- Are other stock modules vulnerable to the same `vi` `KeyError`?
