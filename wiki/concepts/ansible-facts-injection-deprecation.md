---
title: ansible_facts[...] vs deprecated top-level ansible_* vars
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, facts, deprecation]
status: stable
---

# ansible_facts[...] vs deprecated top-level ansible_* vars

Use `ansible_facts['name']` instead of the auto-injected `ansible_name` variables.

## Summary
`INJECT_FACTS_AS_VARS` defaulting to `True` (which auto-injects facts as top-level
`ansible_*` vars) is **deprecated and slated for removal in ansible-core 2.24**. Reference
facts via `ansible_facts['<name>']` (no `ansible_` prefix). Hit and fixed in `site.yml`
2026-06-28 (per [[2026-06-28-ansible-workspace-setup]]).

## Details
Before (deprecation warning):
```jinja
{{ ansible_distribution }} {{ ansible_processor_vcpus }}
```
After:
```jinja
{{ ansible_facts['distribution'] }} {{ ansible_facts['processor_vcpus'] }}
```
Future-proof playbooks now; once the default flips, the `ansible_*` aliases vanish.

## Related
- [[ansible]] — core 2.21.1, warns; removal in 2.24
- [[ansible-yaml-stdout-callback]] — companion modern-Ansible change
- [[ansible-workspace]] — site.yml uses the new form

## Open questions
- None.
