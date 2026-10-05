---
title: "Start from a task"
created: "2026-09-11"
updated: "2026-09-11"
type: "concept"
tags: ["virgo-core"]
sources: ["CLAUDE.md", "documentation/README.md", "ansible/playbooks/create-ansible-user.yml", ".mise.toml"]
confidence: "medium"
source_revision: "166734f0c4ad5169d7140b5177e315118edfa578"
---

# Start from a task

## Find the relevant implementation

| Task | Start here | Boundary to establish |
|---|---|---|
| Understand the repository | [CLAUDE.md](../CLAUDE.md), [documentation index](../documentation/README.md) | Source guidance versus live state |
| Create an automation account | [create-ansible-user.yml](../ansible/playbooks/create-ansible-user.yml), `system_user` | Target, chosen key, sudo scope, recovery login |
| Install Docker | [install-docker.yml](../ansible/playbooks/install-docker.yml) | `komodo` targeting and completion-marker behavior |
| Change Proxmox networking | [configure-network.yml](../ansible/playbooks/configure-network.yml), `proxmox_network` | Interface/bridge identity and out-of-band recovery |
| Form a cluster or deploy Ceph | [initialize-matrix-cluster.yml](../ansible/playbooks/initialize-matrix-cluster.yml) | Cluster membership, storage identities, data preservation |
| Provision a VM | [VM root configuration](../terraform/netbox-vm/main.tf) | State owner, module version, template and target node |
| Build a template | [template root configuration](../terraform/netbox-template/main.tf), `proxmox_template` | Choose a route deliberately; wrapper drift exists |
| Manage an LXC | [LXC role](../ansible/roles/proxmox_lxc/README.md) | Container identity, state, API trust and privileges |
| Upgrade Matrix hosts | [system-upgrade.yml](../ansible/playbooks/system-upgrade.yml) | Live health, reboot choice and recovery behavior |
| Configure a bare-metal inference host | Existing account/Docker components are candidates | No complete inference onboarding route is established here |

## Fresh-reader path

1. Read [[architecture]] for scope.
2. Follow the route above to source, then read defaults and included tasks.
3. Read [[access-and-secrets]] and [[validation-and-safety]] before proposing execution.
4. Check [[known-gaps]] for stale wrappers and source contradictions.

A route is a reading entry point, not an approved command or assurance that the target is reachable. This wiki does not replace inventory inspection, live observations, or the operator's scope decision.

## Pinned sources

- [CLAUDE.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/CLAUDE.md)
- [documentation/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/documentation/README.md)
- [ansible/playbooks/create-ansible-user.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/playbooks/create-ansible-user.yml)
- [.mise.toml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/.mise.toml)
