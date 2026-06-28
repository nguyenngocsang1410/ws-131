---
title: YAML stdout output in modern Ansible (the removed yaml callback)
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, callback, config, gotcha]
status: stable
---

# YAML stdout output in modern Ansible

How to get human-readable YAML playbook output now that the old `yaml` callback is gone.

## Summary
`stdout_callback = yaml` fails on current Ansible: the `community.general.yaml` callback was
**removed in community.general v12**. Replacement is the built-in `default` callback with
`callback_result_format = yaml` (verified 2026-06-28, per
[[2026-06-28-ansible-workspace-setup]]).

## Details
`ansible.cfg`:
```ini
[defaults]
stdout_callback        = default
callback_result_format = yaml
```
- `callback_result_format` (ini key under `[defaults]`; env
  `ANSIBLE_CALLBACK_RESULT_FORMAT`) accepts `json` or `yaml`; added to ansible-core's
  `default` callback in 2.13+.
- Symptom before the fix: `[ERROR]: The 'community.general.yaml' callback plugin has been
  removed.` — but only on `ansible-playbook`, not ad-hoc `ansible` (ad-hoc ignores
  `stdout_callback` unless `bin_ansible_callbacks=True`).

## Related
- [[ansible]] — version where this applies (core 2.21.1)
- [[ansible-workspace]] — where ansible.cfg lives
- [[ansible-facts-injection-deprecation]] — another modern-Ansible change hit this session

## Open questions
- None.
