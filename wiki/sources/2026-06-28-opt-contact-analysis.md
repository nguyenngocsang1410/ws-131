---
title: "Session: Analysis of the /opt/contact CONTACT PLM deployment"
type: source
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28, raw/contact/responsible_views.py, raw/contact/install-docs/]
tags: [contact-software, plm, analysis, session, source]
status: stable
---

# Session: Analysis of the /opt/contact CONTACT PLM deployment

## What this is
A live Claude Code session (2026-06-28) that analyzed the program at [[opt-contact]]. The
human asked: *"analyze /opt/contact program; its source is at /home/vsi/Downloads/Source,
copy to this workspace."* Facts here were verified by reading the deployed tree and
inspecting the running system (`ps`, `ss`, `systemctl`), plus the copied source artifacts.

## Provenance
- **Live host inspection** of `/opt/contact` (world-readable) and process/port/service state.
- **Copied artifacts** in `raw/contact/` (read via [[contact-source-access-via-ansible]]):
  - `responsible_views.py` — a CONTACT `cs.workflow` powerscript (active-development file).
  - `install-docs/{cailinux,caiphanmemnen,caisass,kocointernet}.pdf` — Vietnamese install guides.
- **Not copied** (deliberately): ~700 MB of offline installer bundles + a duplicate of the
  deployed project (redundant with [[opt-contact]]).

## Key takeaways
1. `/opt/contact` is a **live deployment of [[contact-software-plm]]** (CIM Database PLM
   **v16.2**, Python 3.14) — a Python app stack, not a binary.
2. Built on the **`cdb` core** ([[cdb-platform]]) with many `cs.*` functional modules and a
   customer **`cust.plm`** customization layer.
3. Architecture: a **gatekeeper/OIDC auth front** + **cdbsrv application-server worker** +
   docportal/blobstore/queues, under systemd ([[contact-plm-architecture]]).
4. Data tier: **PostgreSQL 17** (`ce16db`) + **Solr** + **Tika** + **Redis** + **etcd**
   ([[contact-plm-data-tier]]).
5. Installed **fully offline / air-gapped** from bundles ([[contact-offline-install]]).
6. Notable exposure to assess: **Apache Tika on `0.0.0.0:9998`** and several app ports on
   `0.0.0.0` ([[contact-plm-security]]).

## How it was produced
Direct recon established the runtime ground truth; an 8-dimension multi-agent workflow
(30 agents) then deep-read each subsystem, with an adversarial pass re-verifying every
security finding against the live host. The deep pass also *corrected* initial inferences —
e.g. **nginx** (not gatekeeper) is the TLS front door, `etcd` is a cache dir (not a service),
and the DH param is an adequate 2048-bit (not weak).

## Pages created from this source
- **entities:** [[contact-software-plm]], [[opt-contact]], [[cdb-platform]],
  [[contact-customization-cust-plm]]
- **concepts:** [[contact-plm-architecture]], [[contact-plm-data-tier]],
  [[contact-plm-config]], [[contact-plm-security]], [[contact-plm-modules]],
  [[cdb-platform-mom]], [[contact-powerscript]], [[contact-offline-install]],
  [[contact-vietnamese-localization]], [[contact-source-access-via-ansible]]
- **sources:** [[responsible-views-vi-hotfix]]

## Open questions
- Licensed module scope; whether the `0.0.0.0` ports are shielded off-host; backup/DR;
  is TOTP 2FA enforced for all logins.
