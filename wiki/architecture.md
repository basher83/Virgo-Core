---
title: "Architecture and ownership"
created: "2026-09-11"
updated: "2026-09-11"
type: "concept"
tags: ["virgo-core"]
sources: ["README.md", "CLAUDE.md", "terraform/netbox-vm/main.tf", "ansible/roles/proxmox_cluster/tasks/main.yml"]
confidence: "medium"
source_revision: "166734f0c4ad5169d7140b5177e315118edfa578"
---

# Architecture and ownership

## What Virgo-Core does

Virgo-Core combines Proxmox configuration management with VM/template provisioning. Its root guidance centers Matrix and Ceph, but the role tree also contains LXC, template-building, tuning, and general account-management components. Presence of those components is not proof of a universal Linux fleet-management boundary. [Sources: README.md, CLAUDE.md]

```text
Operator / controller
  ├─ SSH configuration + credential agent
  ├─ mise → uv → Ansible → Proxmox hosts / selected machines
  │                    └─ roles, inventory, workflow playbooks
  └─ OpenTofu → external Triangulum-Prime module → Proxmox VMs/templates
```

The VM configuration pins the external module to `v1.0.0`; the implementation is not vendored here. Ansible's cluster role selects the first member of `cluster_group` for initialization and joins other nodes conditionally. Inventory order and grouping therefore influence behavior. [Sources: terraform/netbox-vm/main.tf, ansible/roles/proxmox_cluster/tasks/main.yml]

## Repository navigation

| Area | Read it for |
|---|---|
| `ansible/` | Configuration, role implementations, inventory and orchestration |
| `terraform/` | VM/template root configurations and examples |
| `documentation/` | Design guidance and navigation |
| `docs/` | Additional documentation, plans and historical material |
| `scripts/` | Validator and research helpers |
| `.claude/`, `ai_docs/` | Agent-support material, not deployment state |

## Boundary of this wiki

This is source-based orientation, not a live infrastructure inventory. No claim here establishes deployed versions, cluster health, credential availability, or permission to execute. A new bare-metal inference host has no dedicated implementation in the inspected routes; ownership requires an explicit decision rather than inference from shared tooling.

Continue with [[ansible-roles]], [[provisioning]], and [[task-routing]].

## Pinned sources

- [README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/README.md)
- [CLAUDE.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/CLAUDE.md)
- [terraform/netbox-vm/main.tf](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/terraform/netbox-vm/main.tf)
- [ansible/roles/proxmox_cluster/tasks/main.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_cluster/tasks/main.yml)
