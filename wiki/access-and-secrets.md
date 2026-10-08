---
title: "SSH, automation accounts and secrets"
created: "2026-09-11"
updated: "2026-09-11"
type: "concept"
tags: ["virgo-core"]
sources: ["CLAUDE.md", "ansible/ansible.cfg", "ansible/playbooks/create-ansible-user.yml", "ansible/roles/system_user/templates/sudoers.j2", "ansible/roles/system_user/tasks/ssh_keys.yml", "ansible/tasks/infisical-secret-lookup.yml"]
confidence: "medium"
source_revision: "166734f0c4ad5169d7140b5177e315118edfa578"
---

# SSH, automation accounts and secrets

## Documented controller model

`CLAUDE.md` describes modular controller SSH configuration under `~/.ssh/config.d/` and 1Password-managed keys. Hostname aliases are intended to keep connection details out of inventory. This documents the existing controller convention; it does not configure a fresh controller or prove it has those files or an unlocked agent. [Source: CLAUDE.md]

## Existing ansible-account pattern

`create-ansible-user.yml` defaults to `matrix_cluster`, retrieves `PROD_PUB_KEY` from Infisical's `prod` environment at `/ssh`, parses newline-separated public keys, and passes an `ansible` account to `system_user`. It selects `/bin/bash` and `sudo_nopasswd: true`. The template renders full `NOPASSWD:ALL` access for that setting. [Sources: create-ansible-user.yml, sudoers.j2]

The key task adds supplied keys with `state: present`; it does not request exclusive replacement. Do not treat adding a new key as proof that an old key was revoked. [Source: system_user/tasks/ssh_keys.yml]

The reusable lookup task references Universal Auth client ID/secret environment variables, optional environment fallback, `no_log`, and non-cacheable secret facts. These are implementation mechanisms, not proof that every secret-handling path has been audited. No credential values were retrieved to produce this wiki. [Source: infisical-secret-lookup.yml]

## Important active defaults

`ansible/ansible.cfg` currently disables host-key checking, enables sudo-to-root escalation, and disables interactive become-password prompting. The remote-user setting is commented out. These defaults must be evaluated for a new controller; do not silently describe this checkout as enforcing verified host identity. [Source: ansible.cfg]

## Fresh-controller checklist — proposed, not an executed runbook

- Establish target identity and a trusted host-key fingerprint.
- Choose the controller identity and credential-use policy independently of the shared `ansible` username.
- Verify local SSH configuration, credential-agent availability and exact effective target.
- Explicitly choose the public key and target group; do not inherit cluster-wide defaults.
- Agree the required privilege and preserve a separate recovery login.
- Test authentication and privilege separately before disabling bootstrap access.

Related: [[task-routing]], [[validation-and-safety]], [[known-gaps]].

## Pinned sources

- [CLAUDE.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/CLAUDE.md)
- [ansible/ansible.cfg](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/ansible.cfg)
- [ansible/playbooks/create-ansible-user.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/playbooks/create-ansible-user.yml)
- [ansible/roles/system_user/templates/sudoers.j2](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/system_user/templates/sudoers.j2)
- [ansible/roles/system_user/tasks/ssh_keys.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/system_user/tasks/ssh_keys.yml)
- [ansible/tasks/infisical-secret-lookup.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/tasks/infisical-secret-lookup.yml)
