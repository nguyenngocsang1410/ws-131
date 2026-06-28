---
title: Ansible
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, devops, tool]
status: stable
---

# Ansible

IT automation / configuration-management tool used here to manage [[vsi-precision-3680]].

## Summary
Installed 2026-06-28 as the `ansible` community package (which bundles ~91 collections) in
an isolated [[pipx]] venv, yielding **`ansible [core 2.21.1]`** (per
[[2026-06-28-ansible-workspace-setup]]). Binaries live in `~/.local/bin/`.

## Details
- **Version**: ansible-core 2.21.1; Python runtime is the pipx venv's conda Python 3.13.13
  at `~/.local/share/pipx/venvs/ansible/bin/python`.
- **Install method**: see [[pipx-ansible-install]] (the `--include-deps` gotcha).
- **Bundled collections** (subset, from the `ansible` package): community.general 13.1.0,
  ansible.posix 2.2.0, community.docker 5.2.1, ansible.utils 6.0.3. So `requirements.yml`
  Galaxy installs are usually unnecessary.
- **Known breaking changes encountered**: removed `yaml` stdout callback
  ([[ansible-yaml-stdout-callback]]); `INJECT_FACTS_AS_VARS` deprecation
  ([[ansible-facts-injection-deprecation]]); no native env var for the become password
  value, only `ANSIBLE_BECOME_PASSWORD_FILE` ([[ansible-become-via-env]]).

## Related
- [[ansible-workspace]] — the project layout and how to run it
- [[pipx]] — how it's installed/isolated
- [[pipx-ansible-install]] — install gotcha

## Open questions
- None.
