---
title: "Validation, tooling and execution boundaries"
created: "2026-09-11"
updated: "2026-09-11"
type: "concept"
tags: ["virgo-core"]
sources: [".mise.toml", ".github/workflows/validate.yml", "pyproject.toml", "ansible/playbooks/test-roles.yml", "ansible/playbooks/system-upgrade.yml"]
confidence: "medium"
source_revision: "166734f0c4ad5169d7140b5177e315118edfa578"
---

# Validation, tooling and execution boundaries

## Toolchain at the inspected revision

`.mise.toml` pins Python 3.14.2, OpenTofu 1.11.1 and uv 0.9.18, among other tools. `pyproject.toml` requires Python >=3.13 and declares Ansible development tools, Infisical SDK, proxmoxer and requests. Tool installation is enabled automatically by mise settings. Reading this wiki does not install them. [Sources: .mise.toml, pyproject.toml]

## What CI is configured to do

The validation workflow installs dependencies and collections, then invokes formatting checks, Terraform validation/lint/docs checks, YAML lint, shellcheck, Markdown lint and Ansible lint. No current CI success or target-state validation was checked for this wiki. [Source: .github/workflows/validate.yml]

## Task names are not side-effect guarantees

| Entry point | Source-based caution |
|---|---|
| `mise run setup` | Installs dependencies, collections and hooks |
| `mise run full-check` | Includes `fmt-all`; can rewrite source files |
| `mise run ansible-ping` | Contacts inventory hosts; not an offline check |
| `mise run ansible:test-roles` | Runs a host-targeted playbook; check mode is conditional |
| `mise run prod-validate` | Runs init/validate in `terraform/`; do not assume recursion into child root modules |

These are navigation references, not instructions to execute without target and scope review. [Source: .mise.toml]

## Test and maintenance limits

`test-roles.yml` targets `matrix_cluster`, gathers facts, escalates privileges and includes roles. Some paths are conditional on check mode, but the file is not an isolated unit-test suite. Its presence does not prove all roles are covered or that running it is non-mutating. [Source: test-roles.yml]

`system-upgrade.yml` runs serially against `matrix_cluster` and defaults automatic reboot off. Its pre-upgrade Ceph check warns rather than halting on unhealthy status; the post-reboot wait accepts either HEALTH_OK or HEALTH_WARN. The label “Ceph-aware” must not be interpreted as a strict healthy-cluster gate. [Source: system-upgrade.yml]

## Before an infrastructure operation

Establish exact host selection, delegated targets, credential identity, privileges, live preconditions, rollback/recovery and operation-specific evidence. Disk, network and cluster operations require review beyond successful lint or a dry-run result. This wiki grants no execution permission.

Related: [[access-and-secrets]], [[known-gaps]], [[task-routing]].

## Pinned sources

- [.mise.toml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/.mise.toml)
- [.github/workflows/validate.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/.github/workflows/validate.yml)
- [pyproject.toml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/pyproject.toml)
- [ansible/playbooks/test-roles.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/playbooks/test-roles.yml)
- [ansible/playbooks/system-upgrade.yml](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/playbooks/system-upgrade.yml)
