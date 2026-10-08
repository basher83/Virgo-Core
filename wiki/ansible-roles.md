---
title: "Ansible roles and workflows"
created: "2026-09-11"
updated: "2026-09-11"
type: "concept"
tags: ["virgo-core"]
sources: ["ansible/roles/proxmox_cluster/tasks/main.yml", "ansible/roles/proxmox_ceph/tasks/main.yml", "ansible/roles/proxmox_lxc/README.md", "ansible/roles/proxmox_template/README.md", "ansible/roles/proxmox_tuning/README.md", "ansible/playbooks/install-docker.yml"]
confidence: "medium"
source_revision: "166734f0c4ad5169d7140b5177e315118edfa578"
---

# Ansible roles and workflows

## Role catalog

These are discovered role directories, not assertions of current deployment or validated safety. Each link opens the owner's README; inspect defaults and tasks for an actual change.

| Role | Responsibility |
|---|---|
| [system_user](../ansible/roles/system_user/README.md) | Accounts, authorized keys, sudo configuration |
| [proxmox_access](../ansible/roles/proxmox_access/README.md) | Proxmox users, groups, roles, tokens and ACLs |
| [proxmox_cluster](../ansible/roles/proxmox_cluster/README.md) | Cluster initialization/join, hosts and Corosync configuration |
| [proxmox_ceph](../ansible/roles/proxmox_ceph/README.md) | Ceph packages, monitors, managers, OSDs and pools |
| [proxmox_network](../ansible/roles/proxmox_network/README.md) | Bridges and VLANs |
| [proxmox_repository](../ansible/roles/proxmox_repository/README.md) | Repositories, packages and related host maintenance |
| [proxmox_lxc](../ansible/roles/proxmox_lxc/README.md) | LXC lifecycle, API integration and optional TUN access |
| [proxmox_template](../ansible/roles/proxmox_template/README.md) | Ubuntu cloud-image templates and cloud-init |
| [proxmox_tuning](../ansible/roles/proxmox_tuning/README.md) | Sysctl, journald, memory and optional tuning features |

## Workflows, not universal host setup

`proxmox_cluster/tasks/main.yml` sequences prerequisites, optional hosts/SSH changes, initialization or join, Corosync and optional verification. `proxmox_ceph/tasks/main.yml` sequences installation, initialization, monitors/managers, keyrings, disk preparation, OSD creation and pools behind individual flags. Those flags and target variables must be reviewed together; a role label is not a safety boundary. [Sources: role task entry points]

`install-docker.yml` targets `komodo`, installs through `geerlingguy.docker`, and ends processing for hosts with `/opt/.docker_install_complete`. This is marker-based bootstrap behavior, not evidence that future Docker configuration drift will converge. [Source: ansible/playbooks/install-docker.yml]

The tuning README describes minimal/balanced/aggressive profiles. Its claims that settings are safe or proven are owner documentation, not independently tested by this wiki. [Source: proxmox_tuning/README.md]

## Reading order for a change

1. Workflow playbook: targets, privileges, delegation and execution order.
2. Inventory/group variables: selected hosts and supplied state.
3. Role defaults, task entry point, included tasks and templates.
4. Recovery and validation requirements for that exact operation.

Related: [[access-and-secrets]], [[validation-and-safety]], [[provisioning]].

## Pinned sources

- [ansible/roles/proxmox_cluster/tasks/main.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_cluster/tasks/main.yml)
- [ansible/roles/proxmox_ceph/tasks/main.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_ceph/tasks/main.yml)
- [ansible/roles/proxmox_lxc/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_lxc/README.md)
- [ansible/roles/proxmox_template/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_template/README.md)
- [ansible/roles/proxmox_tuning/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_tuning/README.md)
- [ansible/playbooks/install-docker.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/playbooks/install-docker.yml)
