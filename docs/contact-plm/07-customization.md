# 07 — Customization & the Vietnamese Localization

The only customization on this deployment is a single package, **`cust.plm`** — which is, in
practice, a **Vietnamese (`vi`) language pack** for the entire PLM. This doc also covers the
in-flight `responsible_views` hotfix that the localization triggered.

## `cust.plm` — the customer package

- "Customer module", version 1.0.0, installed **editable** (`__editable__.cust_plm-1.0.0`) at
  `instance/cust.plm/`, depending only on `cs.platform`.
- **No custom business logic** — `cust/plm/__init__.py` is a 2-line stub; `cdb_services=[]`; no
  hooks, no service classes, no entities-as-logic. All customization is **declarative
  config/data**:

| Artifact | What it does |
|---|---|
| `cust/plm/configuration/schema.json` | adds **207 columns across 163 tables**, 205 of them `vi`/`*_vi` multilang variants (`name_vi`×83, `description_vi`×25, `label_vi`×10, …) |
| `cust/plm/configuration/patches/cs.*/patches.json` | **56 patch sets** (55 modules + `cust.plm`) supplying Vietnamese UI label strings (e.g. `cdb_check_frame` → "Kiểm tra Cấu hình") |
| `cust/plm/configuration/content/cdbdd_field.json` | seeds `cdb_iso_language_code='vi'` DD fields |

### The `cust` namespace + app_conf mirror

`cust.plm` uses the PEP-420 `cust.*` namespace. At config-apply time, `cdb.comparch` projects the
package's "master" config into the running instance under `app_conf/cust/plm/{master,current}/`,
where each `patches.json` becomes `local_changes.json` (verified byte-identical for `cs.admin`).
This is the standard "extend without forking core" path (see
[03-platform-framework.md](03-platform-framework.md)).

## The Vietnamese localization rollout (the connective theme)

Adding `vi` as a third UI language (alongside `en`/`de`) spans three layers:

1. **Activate the language** — `site.conf`:
   `CADDOK_ACTIVE_GUI_LANGUAGES = {English:en, Deutsch:de, Tiếng Việt:vi}`; install runs
   `powerscript …/add_language_attrs.py --language vi`. Now `i18n.Languages()` enumerates `vi`.
2. **Add `vi` data columns** — `cust.plm` `schema.json` adds `vi`/`*_vi` multilang columns;
   `DDMultiLangField` gains a per-language physical column.
3. **Translate the UI** — `cust.plm` label patches across 55 modules + the install-time XLF loop
   `cdbpkg xliff --import --sourcelang en --targetlang vi <pkg>` + `cdbpkg build`
   (see [09-installation.md](09-installation.md)).

This explains why "Vietnamese" appears everywhere: the install guides are in Vietnamese, the
host/DB naming (`plm_vsi`/`plmvsi`) and the SoluCA CA point to a Vietnam-based integrator.

## The `responsible_views.py` hotfix (active dev work)

A loose working file (`/home/vsi/Downloads/Source/responsible_views.py`, copied to
`raw/contact/responsible_views.py`) is an **edited copy of the stock module**
`venv/.../cs/workflow/responsible_views.py`.

- **What the module does:** a powerscript that generates the SQL for two Data-Dictionary
  **userdefined views** (`cdbwf_responsible`, `cdbwf_responsible_template`) via the `GENERATOR:`
  mechanism. The views enumerate workflow **"responsible" subjects** — who/what can be assigned
  responsibility — unioning users, global roles, and pluggable per-context roles, with one
  localized column per active UI language.
- **The only change:** in `_get_multilang_type` / `_get_multilang`, stock code does direct dict
  indexing `type_map[isocode]` for every active language; the edit adds a
  **`vi → en → de → first` fallback** (`.get(isocode, fallback)`).
- **Root cause:** adding `vi` makes the generator iterate `vi`, but some role-definition
  multilang fields have no `vi` variant → **`KeyError`** while building the UNION SELECT.
- **Regenerate with:** `powerscript -m cs.workflow.responsible_views` (then `compile_views()`).

> ⚠ **Status / risk:** this fix lives **only in the loose file** — not in the venv, not in
> `cust.plm`. If it's patched directly into the venv, an offline reinstall will overwrite it; to
> be durable it should be folded into `cust.plm` (e.g. as a registered powerscript override).
> Other stock modules using the same direct-isocode-indexing pattern may hit the same `KeyError`
> under `vi` and haven't necessarily been found yet.

→ Next: [08-security.md](08-security.md)
