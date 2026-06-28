---
title: Installing Ansible via pipx (the --include-deps gotcha)
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [ansible, pipx, install, gotcha]
status: stable
---

# Installing Ansible via pipx (the --include-deps gotcha)

How to install the `ansible` package in an isolated [[pipx]] venv so all CLI binaries are
exposed.

## Summary
`pipx install ansible` only links the `ansible-community` script, **not** `ansible`,
`ansible-playbook`, `ansible-galaxy`, etc. Those binaries come from the `ansible-core`
dependency, and pipx by default only exposes apps from the top-level package. Fix: install
with `--include-deps` (verified 2026-06-28, per [[2026-06-28-ansible-workspace-setup]]).

## Details
Sequence used:
```bash
python3 -m pip install pipx           # bootstrap pipx (conda pip) → pipx 1.15.0
python3 -m pipx install --include-deps --force ansible
python3 -m pipx ensurepath            # adds ~/.local/bin to PATH (new shell needed)
```
After `--include-deps`, `~/.local/bin/` contains: `ansible`, `ansible-community`,
`ansible-config`, `ansible-console`, `ansible-doc`, `ansible-galaxy`,
`ansible-inventory`, `ansible-playbook`, `ansible-pull`, `ansible-test`, `ansible-vault`.

Result: `ansible [core 2.21.1]` (see [[ansible]]).

## Related
- [[ansible]] — what gets installed
- [[pipx]] — the isolation tool
- [[ansible-workspace]] — consumes this install

## Open questions
- None.
