# Ansible Workspace — vsi-Precision-3680

Local Ansible workspace for managing **this machine only** (Ubuntu 24.04, host
`vsi-Precision-3680`). The control node is also the managed node, so the inventory
uses a **local connection** (no SSH).

## Layout

```
ansible/
├── ansible.cfg                 # points at inventory/, roles/, sets defaults
├── inventory/
│   └── hosts.yml               # this machine, group `local`, connection=local
├── group_vars/
│   └── all.yml                 # vars for all hosts
├── host_vars/
│   └── vsi-precision-3680.yml  # vars for this host
├── playbooks/
│   ├── ping.yml                # connectivity smoke test
│   └── site.yml                # main entry point
├── roles/                      # put roles here
├── requirements.yml            # optional Galaxy deps
└── README.md
```

## Setup notes

- **Ansible** is installed in an isolated **pipx** venv: `ansible [core 2.21.1]`,
  binaries at `~/.local/bin/` (e.g. `~/.local/bin/ansible-playbook`).
- Make sure `~/.local/bin` is on your `PATH` (pipx added it to your shell rc;
  open a new shell or `source ~/.bashrc`). Until then, call the binaries by full
  path or run `export PATH="$HOME/.local/bin:$PATH"`.
- Module execution on this host uses the **system** Python `/usr/bin/python3`
  (it has `python3-apt`); the pipx/conda pythons do not.

## Usage

Run commands from inside this `ansible/` directory (so `ansible.cfg` is picked up):

```bash
cd ansible

# Smoke test
ansible local -m ping
ansible-playbook playbooks/ping.yml

# Gather all facts about this machine
ansible local -m setup

# Main playbook
ansible-playbook playbooks/site.yml
```

### Privileged (root) tasks

This machine does **not** have passwordless sudo. Two ways to supply the password:

**A) Prompt each run** — pass `-K`:

```bash
ansible-playbook playbooks/site.yml -K
```

**B) Store it in `.env`** (no prompt) — put your sudo password in `.env` (gitignored,
`chmod 600`), then source it before running. `group_vars/all.yml` reads it via an
`env` lookup into `ansible_become_password`:

```bash
$EDITOR .env                      # set BECOME_PASSWORD=...   (template: .env.example)
set -a; source .env; set +a       # export it for this shell
ansible-playbook playbooks/site.yml   # uses the password, no -K
```

When `BECOME_PASSWORD` is unset the variable is `omit`ted, so option **A** (`-K`)
keeps working. Never commit `.env` — only the `.env.example` template is tracked.

### Adding a role

```bash
ansible-galaxy role init roles/base
# then reference it from playbooks/site.yml
```
