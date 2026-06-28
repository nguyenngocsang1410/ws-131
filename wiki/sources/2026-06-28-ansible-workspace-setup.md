---
title: "Session: Ansible workspace setup on vsi-Precision-3680"
type: source
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, devops, session, provenance]
status: stable
---

# Session: Ansible workspace setup on vsi-Precision-3680

Provenance record for the 2026-06-28 Claude Code session that installed Ansible and
scaffolded a local Ansible workspace on this machine.

## Summary
On 2026-06-28 an Ansible control environment was set up to manage **this machine only**
([[vsi-precision-3680]]). [[ansible]] core 2.21.1 was installed in an isolated [[pipx]]
venv; a workspace was scaffolded at `~/sangnn10_workspace/ansible/` (see
[[ansible-workspace]]); and sudo escalation was wired to read the password from a
gitignored `.env` (see [[ansible-become-via-env]]). Every claim below was **verified by
running the command and observing output directly on the host** — this is empirical
provenance, not a transcribed document.

## Key takeaways
- Ansible runs against the control node itself over a **local connection**, with the
  **system** Python as the module interpreter (needed for `apt`) — see
  [[ansible-local-control-node]].
- Installing the `ansible` package via pipx requires `--include-deps` or only
  `ansible-community` is linked — see [[pipx-ansible-install]].
- The `yaml` stdout callback was removed; use `default` + `callback_result_format` —
  see [[ansible-yaml-stdout-callback]].
- Top-level `ansible_*` fact vars are deprecated in favour of `ansible_facts[...]` —
  see [[ansible-facts-injection-deprecation]].
- Sudo password is supplied from `.env` via an `env` lookup, with `-K` as fallback —
  see [[ansible-become-via-env]].

## What was verified
- `ansible local -m ping` → `pong`.
- `ansible-playbook playbooks/site.yml` → prints host summary, `ok=2 failed=0`.
- Become: no password set → `sudo: a password is required` (omit works, `-K` usable);
  wrong password → rejected; correct password → `id -un` returns `root`.

## Related
- [[ansible-workspace]] — the artifact produced by this session
- [[vsi-precision-3680]] — the machine configured
- [[ansible]], [[pipx]] — tools installed

## Open questions
- CPU count: `nproc` reported 32 but Ansible's `processor_vcpus` reported 24 — discrepancy
  noted in [[vsi-precision-3680]], unresolved.
- Whether to migrate the `.env` secret to Ansible Vault (offered, not yet decided).
