---
title: Supplying the Ansible become password from a .env file
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, become, sudo, secrets, env]
status: stable
---

# Supplying the Ansible become password from a .env file

Pattern for feeding a sudo (become) password to Ansible from a `KEY=value` `.env` file,
while keeping `-K` (interactive prompt) working as a fallback.

## Summary
Ansible-core has **no native environment variable for the become password *value*** — only
`ANSIBLE_BECOME_PASSWORD_FILE` (a path to a file). So the value is injected via an `env`
lookup into `ansible_become_password` in group_vars. Needed because [[vsi-precision-3680]]
has no passwordless sudo. **Caveat:** the wiring only takes effect if Ansible actually
loads the group_vars file — see the gotcha below.

## Details
`inventory/group_vars/all.yml`:
```yaml
ansible_become_password: "{{ lookup('ansible.builtin.env', 'BECOME_PASSWORD') | default(omit, true) }}"
```
- `default(omit, true)` → when `BECOME_PASSWORD` is unset/empty the variable is **omitted
  entirely**, so `-K` still works. When set, the value is fed to sudo.
- The `env` lookup reads the **controller's** environment, so the var must be exported
  first: `set -a; source .env; set +a`.
- `.env` holds `BECOME_PASSWORD=...`; it is `chmod 600` and gitignored (`.env.example` is
  the tracked template). **The secret value is never stored in this wiki.**

## Gotcha: group_vars must sit beside the inventory (fixed 2026-06-28)
Ansible only auto-loads `group_vars/` and `host_vars/` from the directory of the
**inventory source** or the **playbook** — not from the project root. They were originally
created at `ansible/group_vars/` and `ansible/host_vars/`, adjacent to neither, so they
were **silently ignored**. This stayed hidden because the only playbooks at the time used
`become: false`; the first real `become: true` play (the [[internet-lockdown-vsi]] role)
failed with `sudo: a password is required` because `ansible_become_password` had never been
loaded. Fixed by moving them under `inventory/` (`inventory/group_vars/all.yml`,
`inventory/host_vars/`), after which the become password resolves (length verified) and the
`.env` flow works end-to-end (a privileged playbook re-ran `changed=0`).

Quick check that it loads:
```bash
set -a; source .env; set +a
ansible vsi-precision-3680 -m debug -a "msg={{ ansible_become_password | default('') | length }}"
```

## Related
- [[ansible-workspace]] — where the wiring lives
- [[internet-lockdown-vsi]] — first privileged play; surfaced the group_vars gotcha
- [[contact-source-access-via-ansible]] — another flow relying on `become`
- [[vsi-precision-3680]] — no passwordless sudo, hence this
- [[ansible-local-control-node]] — companion connection/interpreter config

## Open questions
- Migrate to Ansible Vault instead of plaintext `.env`?
