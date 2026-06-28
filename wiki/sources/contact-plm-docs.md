---
title: "Deliverable: docs/contact-plm/ documentation set"
type: source
created: 2026-06-28
updated: 2026-06-28
sources: [docs/contact-plm/, session:claude-code/2026-06-28]
tags: [contact-software, plm, documentation, deliverable, source]
status: stable
---

# Deliverable: docs/contact-plm/ documentation set

The human-readable documentation folder for the [[opt-contact]] deployment, at
`docs/contact-plm/` in this repo — a linear digest of the wiki's CONTACT pages with diagrams,
command references, and an operations runbook.

## What it is
An 11-file Markdown documentation set authored 2026-06-28 from the same analysis that produced
the CONTACT wiki pages. It is **derived from** the wiki (and the live system), not an
independent source — the wiki remains the atomic source of truth; this set is the readable,
linear presentation for humans.

## Contents
`README.md` (at-a-glance + navigation) and: `01-overview`, `02-architecture` (ASCII topology
diagram + port map), `03-platform-framework` (cdb/MoM/powerscript), `04-data-tier`,
`05-configuration`, `06-modules`, `07-customization`, `08-security` (findings + remediation
checklist), `09-installation` (offline runbook), `10-operations` (service control/logs/CLIs/
backup/health).

## Net-new knowledge folded back into the wiki on ingest
- [[contact-plm-operations]] — the operations reference (was only in `10-operations.md`).
- [[contact-plm-architecture]] — gained the ASCII topology diagram.

## Provenance & cross-links
- Built from [[2026-06-28-opt-contact-analysis]] (the analysis session) + live-system checks.
- Mirrors: [[opt-contact]], [[contact-plm-architecture]], [[contact-plm-data-tier]],
  [[contact-plm-config]], [[contact-plm-security]], [[contact-plm-modules]],
  [[cdb-platform-mom]], [[contact-powerscript]], [[contact-offline-install]],
  [[contact-customization-cust-plm]], [[contact-vietnamese-localization]].
- Secrets (e.g. the install-PDF DB password) are deliberately excluded from both artifacts.

## Open questions
- Keep the docs folder in sync manually, or generate it from the wiki pages later?
