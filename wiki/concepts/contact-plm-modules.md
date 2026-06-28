---
title: CONTACT PLM installed module inventory (16.2)
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [contact-software, plm, modules, inventory, versions, cad]
status: stable
---

# CONTACT PLM installed module inventory (16.2)

What functional capabilities the [[opt-contact]] deployment actually has installed, at what
versions, and what it is specialized for.

## Summary
The product is **CIM Database PLM** (`cscdb.product` 16.2.0.4) on the **CONTACT Elements
Platform** (`cs.platform` 16.2.8), built with `setuptools-ce` 16.1.1.2. **55 separately-
versioned `cs_*` functional modules** are installed plus the compiled core (`cdb`,
`cdbwrapc`) and the customer package `cust.plm`. The install is a **general engineering PLM
specialized for multi-CAD desktop integration, document control, and project/portfolio
management** — with governance hardening (MFA + e-signature + audit trail). It is **not**
running IoT, ERP-connector, or ticketing, despite the localization/config catalog shipping
scaffolding for them.

## Details

### Capability groups (installed `cs_*`, all 16.2.0.x unless noted)
- **Documents:** documents, docmap, docportal, pdfviewer, ecm (16.1.0.5)
- **Product structure / BOM:** bomcreator, projectstructure, variants, baselining, semanticlinks
- **Classification / materials:** classification, materials
- **Quality / issues:** defects, issues, checklists
- **Projects / portfolio / costing:** projects, projectcosts, projectscheduling, projectexchange, costing, efforts, resources, workplan, taskboard, taskmanager
- **Requirements:** requirements (+ `requirements_reqif` config)
- **CAD desktop connectors:** autocad 15.18.1.0, inventor 15.19.0.1, nx 15.13.1.2, solidworks 15.21.0.1, cadbase (16.2)
- **3D / visualization:** threed, threedlibs 16.2.1.0, vp, vp_pcs
- **Workflow / process:** workflow, actions, batchoperations, activitystream
- **Governance / security:** audittrail, dsig (e-signature), mfa, admin
- **Reporting / metrics:** powerreports, metrics
- **Office / Teams:** office 15.6.2.3, officelink, msteams 16.1.0.2
- **Licensing analytics:** licdashboard 16.1.0.5, licreport 16.1.0.0
- **Web / UI / workspaces:** web 16.2.0.8, workspaces 15.6.10.2, workspaces_server, workspaces_vp 15.6.10.2, designsystem 15.9.0.2, userassistance

### Version trains (why versions differ)
- **16.2.0.x** — current server train (most modules; platform 16.2.8).
- **16.1.0.x** — minor laggards: ecm, licdashboard, licreport, msteams.
- **15.x** — CAD/Office/Workspaces/designsystem connectors, versioned against the **external
  desktop app/SDK** cadence, not the server release (expected for CAD; but `designsystem`/
  `workspaces` at 15.x against `web` 16.2 is a potential UI mismatch). Patch-currency flagged
  in [[contact-plm-security]].

### Catalog ≠ installed
`/opt/contact/xlf` (67 entries) and `app_conf/cs/` (60 dirs) are **supersets** of installed
code — they ship translations/config for modules with **no installed package** (`iot`, `erp`,
`ticket`, `xplan`, `prmm`, `srp`, `prp`, `prt`, `prx`, `migration`, `xml`). So the catalog
overstates capability; those features are not running here.

### Compiled core note
`cdb`/`cdbwrapc` ship as a compiled C extension (`_cdbwrapc…so`) with no pip-visible version
(travels with the 16.2 product). It **bundles Oracle Instant Client 23.1 libs** despite the
PostgreSQL backend — dormant surface ([[contact-plm-security]]).

## Related
- [[contact-software-plm]] — the product these compose
- [[cdb-platform]] / [[cdb-platform-mom]] — what the modules are built on
- [[contact-customization-cust-plm]] — the customer module (`cust.plm`)
- [[contact-plm-security]] — version-currency & Oracle-libs notes

## Open questions
- Exact compiled `cdbwrapc` build revision (binary-only; venv python not executable by analysis user).
- Which configured sub-features (reqif, cad_wsm_synchronizer, defects_vp…) are enabled at runtime vs scaffolding.
- Are the 15.x/16.1.x versions intentionally pinned (CAD/SDK compat) or just un-upgraded?
