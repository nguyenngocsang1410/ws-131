---
title: Reading the vsi-owned CONTACT source via Ansible become
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, become, sudo, access, contact, operations]
status: stable
---

# Reading the vsi-owned CONTACT source via Ansible become

How the analysis read source material owned by OS user `vsi` from the `vietnq37` account.

## Summary
The CONTACT install material lives under `/home/vsi/Downloads/Source`, and `/home/vsi` is
mode `0750 vsi:vsi` — so `vietnq37` cannot traverse into it, and there is **no passwordless
sudo** ([[vsi-precision-3680]]). The workaround was the existing [[ansible-workspace]]: run
privileged, read-only commands through Ansible with `become`, supplying the sudo password
from `.env` ([[ansible-become-via-env]]). The deployed app at [[opt-contact]] itself is
world-readable and needed no escalation.

## Details
Recipe used (read-only; from inside `ansible/` so `ansible.cfg` applies):
```bash
cd /home/vietnq37/sangnn10_workspace/ansible
set -a; source .env; set +a
ansible local -b -m command -a "ls -la /home/vsi/Downloads/Source"
```
- `-b` (become) escalates to root via sudo; the password comes from `BECOME_PASSWORD`.
- Used `command`/`shell` modules for `ls`, `cp`, `tar tzf`, etc.
- To copy `vsi`-owned files into the `vietnq37` workspace, the playbook `cp`'d them then
  `chown -R vietnq37:vietnq37` the destination (`raw/contact/`).

What `Source/` contained: install-guide PDFs (Vietnamese), the CONTACT offline bundle
(`contact-offline-bundle-noble-amd64.tar.gz` → `contact-home-runtime` + `contact-opt-project`
+ `offline-apt-repo`), third-party offline installers (postgres17, solr/tika/java, sass,
graphviz), a 361-wheel `packages/` cache, and the loose working file `responsible_views.py`.
Only the small non-redundant artifacts were copied (the bundles duplicate [[opt-contact]]).

Security note: this used the same plaintext-`.env` sudo password discussed in
[[ansible-become-via-env]]; all commands were read-only except the scoped copy+chown.

## Related
- [[ansible-become-via-env]] — the sudo-password mechanism reused here
- [[ansible-workspace]] — the project that ran the commands
- [[vsi-precision-3680]] — why escalation was needed (perms, no NOPASSWD)
- [[opt-contact]] — the (world-readable) analysis target
- [[contact-offline-install]] — what the copied install material documents _(stub)_

## Open questions
- None — operational note.
