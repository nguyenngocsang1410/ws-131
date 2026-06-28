---
title: Ansible workspace (~/sangnn10_workspace/ansible)
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, workspace, project, devops]
status: stable
---

# Ansible workspace

The local Ansible project directory that manages [[vsi-precision-3680]].

## Summary
Scaffolded 2026-06-28 at `/home/vietnq37/sangnn10_workspace/ansible/` — **inside the LLM
Wiki git repo** (a deliberate choice; it shows as untracked). Targets this machine only
over a local connection (per [[2026-06-28-ansible-workspace-setup]]). On 2026-06-28 it
gained its first real role, `internet_lockdown`, which enforces [[internet-lockdown-vsi]].

## Details
Layout — vars dirs live **under `inventory/`** so Ansible actually loads them (originally
they were at the project root and were silently ignored; see the gotcha in
[[ansible-become-via-env]]):
```
ansible/
├── ansible.cfg                 # inventory/roles paths, YAML output, sudo defaults
├── inventory/
│   ├── hosts.yml               # group `local` → this host, connection=local
│   ├── group_vars/all.yml      # ansible_become_password via env lookup
│   └── host_vars/vsi-precision-3680.yml
├── playbooks/
│   ├── ping.yml                # smoke test
│   ├── site.yml                # main entry point
│   └── internet-lockdown.yml   # block a user's internet ([[internet-lockdown-vsi]])
├── roles/
│   └── internet_lockdown/      # nftables UID-owner block ([[nftables-uid-owner-block]])
├── requirements.yml            # optional Galaxy deps (mostly redundant)
├── .env / .env.example         # become secret (.env gitignored, chmod 600)
└── .gitignore / README.md
```

Notable `ansible.cfg` settings: `inventory=inventory/hosts.yml`, `roles_path=roles`,
`stdout_callback=default` + `callback_result_format=yaml`
([[ansible-yaml-stdout-callback]]), `host_key_checking=False`, `forks=10`.

How to run (from inside `ansible/` so the cfg applies):
```bash
set -a; source .env; set +a          # load become password ([[ansible-become-via-env]])
ansible local -m ping
ansible-playbook playbooks/site.yml
ansible-playbook playbooks/internet-lockdown.yml      # block vsi's internet
```

## Related
- [[vsi-precision-3680]] — the managed host
- [[internet-lockdown-vsi]] — the first real configuration this workspace enforces
- [[ansible-local-control-node]] — connection + interpreter design
- [[ansible-become-via-env]] — sudo password handling (and the group_vars location gotcha)
- [[contact-source-access-via-ansible]] — the other current use of this workspace
- [[ansible]] — the tool

## Open questions
- The workspace lives in the wiki git repo; may want to split into its own repo later.
