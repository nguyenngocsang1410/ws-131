---
title: Vietnamese localization rollout of CONTACT PLM
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, raw/contact/responsible_views.py, raw/contact/install-docs/]
tags: [contact-software, plm, vietnamese, localization, i18n, project]
status: stable
---

# Vietnamese localization rollout of CONTACT PLM

The connective theme behind this whole deployment: standing up CONTACT CIM Database PLM
**localized to Vietnamese (`vi`)** on [[opt-contact]]. It explains the customer package, the
loose dev file, and the Vietnamese install guides as parts of one effort.

## Summary
The operator is rolling out **`vi` as a third UI language** (alongside `en`/`de`) across the
entire PLM. Evidence converges from three places: (1) `site.conf` registers
`CADDOK_ACTIVE_GUI_LANGUAGES = {English:en, Deutsch:de, Tiếng Việt:vi}`; (2) the customer
package [[contact-customization-cust-plm]] is essentially a `vi` language pack (schema `vi`
columns + 56-module label patches); (3) the install runbook ([[contact-offline-install]])
ends with a Vietnamese XLF import/build loop. The loose
[[responsible-views-vi-hotfix|responsible_views.py]] is a dev hotfix for a bug this rollout
surfaced.

## Details

### The three layers of the rollout
1. **Activate the language** — `site.conf`: `vi` added to `CADDOK_ACTIVE_GUI_LANGUAGES`; the
   install runs `powerscript …/add_language_attrs.py --language vi` to add the language
   attribute. This makes `i18n.Languages()` enumerate `vi`.
2. **Add `vi` data columns** — `cust.plm/configuration/schema.json` adds `vi`/`*_vi` multilang
   columns to 163 tables; new DD `vi` fields are seeded. Multilang fields
   (`DDMultiLangField`) gain a per-language physical column.
3. **Translate the UI** — Vietnamese label strings via `cust.plm` patches across 55 modules,
   plus the runbook's `cdbpkg xliff --import --sourcelang en --targetlang vi <pkg>` +
   `cdbpkg build` loop over `/opt/contact/vi/xlf/*` (XLF dirs shipped from a Windows host,
   since cleaned post-build).

### The bug it surfaced
Adding `vi` broke the stock DD-view generator `cs.workflow.responsible_views`: it indexed
`type_map[isocode]`/`field_map[isocode]` for *every* active language, raising `KeyError` for
`vi` when a role-definition multilang field had no `vi` variant. The fix (a `vi→en→de`
fallback) lives only in the loose working copy so far — see
[[responsible-views-vi-hotfix]]. This is the canonical risk of adding a language to a mature
PLM: stock code that assumed every active language has every translation.

### Why "Vietnamese" shows up everywhere here
- Install guides are in Vietnamese ([[contact-offline-install]]): *cài linux*, *cài phần mềm
  nền*, *cài sass*, *không có internet*.
- The host/DB naming (`plm_vsi`, `plmvsi`) and the SoluCA self-signed CA point to a Vietnam-
  based integrator deploying for a Vietnamese customer.

## Related
- [[contact-customization-cust-plm]] — the `vi` language pack package
- [[responsible-views-vi-hotfix]] — the bug/fix this rollout caused
- [[contact-offline-install]] — the install runbook incl. the XLF import loop
- [[cdb-platform-mom]] — `DDMultiLangField`/`i18n.Languages()` mechanics
- [[opt-contact]] — the deployment being localized

## Open questions
- How many other stock `cs.*` modules share the direct-isocode-indexing pattern and will `KeyError` under `vi`?
- Is the rollout complete (all labels translated), or partial?
