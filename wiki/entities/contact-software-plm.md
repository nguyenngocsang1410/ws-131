---
title: CONTACT Software — CIM Database / Elements PLM
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, raw/contact/responsible_views.py]
tags: [contact-software, plm, product, vendor, cim-database, elements]
status: stable
---

# CONTACT Software — CIM Database / Elements PLM

The commercial Product Lifecycle Management (PLM) platform deployed at [[opt-contact]].

## Summary
**CONTACT Software GmbH** (contact-software.com) is a German vendor; its flagship product
is **CIM Database PLM**, delivered on the **CONTACT Elements** low-code platform. The
deployment on this host is **version 16.2** (most `cs.*` modules are `16.2.0.x`), running on
**Python 3.14**. It is a modular suite: a small core ([[cdb-platform]]) plus dozens of
optional functional `cs.*` modules (documents, BOM/product structure, workflow,
classification, defects, projects/costing, CAD integrations, e-signature, MFA, reporting,
etc.). Copyright headers read `Copyright (C) 1990 - 2026 CONTACT Software GmbH`.

## Details
Verified facts (observed 2026-06-28 from the deployed venv at [[opt-contact]]):

| Property | Value |
|---|---|
| Vendor | CONTACT Software GmbH (http://www.contact-software.com) |
| Product | CIM Database PLM on the CONTACT Elements platform |
| Version | 16.2 (`cs_*` dist-info mostly `16.2.0.x`; `cscdb_product 16.2.0.4`) |
| Runtime | Python 3.14 (uv-provided CPython 3.14.6) |
| Core package | `cdb` (see [[cdb-platform]]) |
| Module namespace | `cs.*` (functional), `cscdb.*`, `cust.*` (customer) |
| Customization | editable `cust.plm` package (see [[contact-customization-cust-plm]]) |

Version note: a few modules lag the 16.2 train — e.g. `cs_autocad 15.18.1.0` — i.e. CAD
connector versions are pinned independently of the core. (Full module inventory: pending
deep analysis, see [[contact-plm-modules]].)

The product is **customizable/low-code**: customers extend it via the `cust` namespace and
"powerscript" ([[contact-powerscript]]) against the Meta-Object Model ([[cdb-platform-mom]]).
`raw/contact/responsible_views.py` is a concrete example of such a script (generates DB
views for workflow "responsible" context-roles).

## Related
- [[opt-contact]] — the concrete deployment of this product on this host
- [[cdb-platform]] — the core framework everything is built on
- [[contact-plm-architecture]] — how the services fit together
- [[contact-plm-modules]] — the installed functional module inventory _(stub)_
- [[contact-software-plm]] self

## Open questions
- Exact edition/licensed scope (which modules are licensed vs merely installed).
- Release date / patch level of the 16.2 train deployed here.
