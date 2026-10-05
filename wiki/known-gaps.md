---
title: "Known gaps and source inconsistencies"
created: "2026-09-11"
updated: "2026-09-11"
type: "concept"
tags: ["virgo-core"]
sources: ["README.md", "CLAUDE.md", ".mise.toml", "ansible/ansible.cfg", "ansible/roles/proxmox_lxc/README.md", "ansible/roles/proxmox_tuning/README.md"]
confidence: "medium"
source_revision: "166734f0c4ad5169d7140b5177e315118edfa578"
---

# Known gaps and source inconsistencies

## Findings from source inspection

| Finding | Evidence | Consequence |
|---|---|---|
| Root guidance highlights six roles; the tree contains nine | README/CLAUDE versus role directories | Read the role tree, not only the root summary |
| Tool versions differ across guidance and configuration | CLAUDE describes Python 3.13+ / OpenTofu 1.10.x; mise pins 3.14.2 / 1.11.1 | Resolve versions from current configuration and compatibility checks |
| Template task points at a missing active playbook | `.mise.toml` references `playbooks/proxmox-build-template.yml`; the tracked file is under `.deprecated/` | Do not use that wrapper unchanged |
| Host-key verification is disabled | `ansible/ansible.cfg` | A fresh secure-controller setup needs an explicit policy decision |
| PVE compatibility wording is inconsistent | Root guidance targets 9.x; LXC/tuning READMEs list 7.x/8.x | Do not infer compatibility or incompatibility without checking implementations and supported versions |
| Generic Linux/inference ownership is not established by these components | Proxmox-oriented guidance plus general user/Docker pieces | Treat reuse as a proposal, not a declared onboarding path |

## Limits

This is a scoped source review, not an exhaustive bug/security audit. Historical “production-ready” or idempotency statements remain source claims. We have not reproduced them, run deployments, tested authentication, or queried live clusters.

Do not silently repair underlying code while updating this wiki. Record findings, inspect their effect and make a separately scoped change. A newer source does not automatically resolve a contradiction; inspect the actual behavior and ownership.

Related: [[validation-and-safety]], [[architecture]], [[task-routing]].

## Pinned sources

- [README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/README.md)
- [CLAUDE.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/CLAUDE.md)
- [.mise.toml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/.mise.toml)
- [ansible/ansible.cfg](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/ansible.cfg)
- [ansible/roles/proxmox_lxc/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_lxc/README.md)
- [ansible/roles/proxmox_tuning/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_tuning/README.md)
