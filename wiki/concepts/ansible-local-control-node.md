---
title: Managing the Ansible control node itself (local connection + system python)
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, inventory, connection, python-interpreter]
status: stable
---

# Managing the Ansible control node itself

When the control node is also the managed node, use a local connection and point the
module interpreter at the system Python.

## Summary
[[vsi-precision-3680]] is managed by an Ansible install running on itself, so the inventory
uses `ansible_connection: local` (no SSH) and `ansible_python_interpreter: /usr/bin/python3`
(verified 2026-06-28, per [[2026-06-28-ansible-workspace-setup]]).

## Details
`inventory/hosts.yml`:
```yaml
all:
  children:
    local:
      hosts:
        vsi-precision-3680:
          ansible_connection: local
          ansible_python_interpreter: /usr/bin/python3
```
Why the **system** Python (3.12) and not conda/pipx Python:
- The `apt` module requires the `python3-apt` bindings, which exist only for
  `/usr/bin/python3` on this host. Conda's Python 3.13 lacks them.
- Module execution happens with the *target's* interpreter; with a local connection the
  target is this machine, so the interpreter choice directly affects `apt` and other
  system modules.

## Related
- [[vsi-precision-3680]] — the host and its two Pythons
- [[ansible-workspace]] — the inventory lives here
- [[ansible-become-via-env]] — sudo handling for privileged modules

## Open questions
- None.
