---
title: pipx
type: entity
created: 2026-06-28
updated: 2026-06-28
sources: [session:claude-code/2026-06-28]
tags: [python, tool, packaging]
status: stable
---

# pipx

Tool for installing Python CLI applications into isolated virtual environments.

## Summary
Used to install [[ansible]] in isolation so it does not pollute the conda base env (per
[[2026-06-28-ansible-workspace-setup]]). pipx **1.15.0** was itself bootstrapped via
`python3 -m pip install pipx` using conda's pip 26.1.2.

## Details
- Apps are exposed in `~/.local/bin/`; venvs live under `~/.local/share/pipx/venvs/`.
- `pipx ensurepath` added `~/.local/bin` to the shell rc — **existing shells must be
  re-sourced** (`source ~/.bashrc`) or use full paths until then.
- Because pipx ran under conda's Python, the ansible venv interpreter is conda Python
  3.13.13 — fine for Ansible's controller; module execution on targets still uses the
  target's own interpreter ([[ansible-local-control-node]]).
- Key gotcha when installing the `ansible` meta-package: see [[pipx-ansible-install]].

## Related
- [[ansible]] — installed via pipx
- [[pipx-ansible-install]] — the `--include-deps` requirement

## Open questions
- None.
