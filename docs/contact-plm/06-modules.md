# 06 — Module Inventory

**55 separately-versioned `cs_*` functional modules** are installed over the compiled core
(`cdb`/`cdbwrapc`), plus the customer package `cust.plm`. Product = `cscdb.product` 16.2.0.4
("CIM Database PLM") on `cs.platform` 16.2.8.

## By capability (versions as installed)

| Area | Modules (version) |
|---|---|
| **Documents** | documents 16.2.0.5, docmap 16.2.0.4, docportal 16.2.0.2, pdfviewer 16.2.0.5, **ecm 16.1.0.5** |
| **Product structure / BOM** | bomcreator 16.2.0.2, projectstructure 16.2.0.5, variants 16.2.0.5, baselining 16.2.0.1, semanticlinks 16.2.0.1 |
| **Classification / materials** | classification 16.2.0.4, materials 16.2.0.4 |
| **Quality / issues** | defects 16.2.0.3, issues 16.2.0.3, checklists 16.2.0.5 |
| **Projects / portfolio / costing** | projects 16.2.0.7, projectcosts 16.2.0.4, projectscheduling 16.2.0.4, projectexchange 16.2.0.2, costing 16.2.0.5, efforts 16.2.0.2, resources 16.2.0.4, workplan 16.2.0.0, taskboard 16.2.0.5, taskmanager 16.2.0.8 |
| **Requirements** | requirements 16.2.0.3 |
| **CAD desktop connectors** | **autocad 15.18.1.0, inventor 15.19.0.1, nx 15.13.1.2, solidworks 15.21.0.1**, cadbase 16.2.0.3 |
| **3D / visualization** | threed 16.2.0.3, threedlibs 16.2.1.0, vp 16.2.0.5, vp_pcs 16.2.0.2 |
| **Workflow / process** | workflow 16.2.0.3, actions 16.2.0.2, batchoperations 16.2.0.1, activitystream 16.2.0.5 |
| **Governance / security** | audittrail 16.2.0.4, dsig (e-signature) 16.2.0.1, mfa 16.2.0.1, admin 16.2.0.1 |
| **Reporting / metrics** | powerreports 16.2.0.2, metrics 16.2.0.1 |
| **Office / Teams** | office 15.6.2.3, officelink 16.2.0.1, **msteams 16.1.0.2** |
| **Licensing analytics** | **licdashboard 16.1.0.5, licreport 16.1.0.0** |
| **Web / UI / workspaces** | web 16.2.0.8, workspaces 15.6.10.2, workspaces_server 16.2.0.0, workspaces_vp 15.6.10.2, designsystem 15.9.0.2, userassistance 16.2.0.5 |

## Version trains (why versions differ)

- **16.2.0.x** — the current server train (most modules; platform itself 16.2.8).
- **16.1.0.x** — minor laggards: `ecm`, `licdashboard`, `licreport`, `msteams`.
- **15.x** — CAD/Office/Workspaces/designsystem connectors. CAD/Office connectors version
  against the **external desktop app/SDK** cadence, not the PLM server — expected. But
  `designsystem`/`workspaces` at 15.x against `web` 16.2.0.8 is a possible UI-layer mismatch.

Patch-currency review is recommended for the 16.1.x/15.x modules — see
[08-security.md](08-security.md).

## Catalog ≠ installed

`/opt/contact/xlf` (67 entries) and `instance/app_conf/cs/` (60 dirs) are **supersets** of the
installed code — they ship translations/config scaffolding for modules with **no installed
package**: `iot`, `erp`, `ticket`, `xplan`, `prmm`, `srp`, `prp`, `prt`, `prx`, `migration`,
`xml`. So the catalog overstates capability: **IoT, ERP connectivity, and ticketing are not
running here.**

`app_conf/cs/` also contains cross-module integration configs that don't map 1:1 to modules
(e.g. `requirements_reqif`, `cad_wsm_synchronizer`, `defects_vp`, `projectstructure_workflows`,
`*_documents`) — these wire installed modules together.

## How to enumerate yourself

```bash
ls /opt/contact/venv/lib/python3.14/site-packages | grep -iE 'dist-info' | grep -iE '^cs_|^cscdb|^cust'
cat /opt/contact/packages/all.txt          # pinned component versions in the offline bundle
ls /opt/contact/xlf                          # localization catalog (superset)
ls /opt/contact/instance/app_conf/cs         # configured features
```

→ Next: [07-customization.md](07-customization.md)
