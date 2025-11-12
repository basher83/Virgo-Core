# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Repository Overview

Virgo-Core is Infrastructure as Code for managing a Proxmox VE homelab with NetBox and PowerDNS integration. The repository uses OpenTofu/Terraform for VM provisioning and Ansible for configuration management, targeting a 3-node Proxmox cluster named "Matrix" (nodes: Foxtrot, Golf, Hotel).

## Core Technologies

- **OpenTofu**: v1.10.x for VM/template provisioning
- **Ansible**: For Proxmox configuration, template building, and system setup
- **Python**: 3.13+ with `uv` for dependency management
- **Mise**: Task runner and tool version manager
- **Proxmox VE**: 9.x cluster with CEPH storage

## Claude Code Skills

This repository includes an Agent Skill that extends Claude Code's capabilities:

- **ansible-best-practices** - Ansible playbook patterns, role design, Infisical secrets, idempotency, error handling

## Project Structure

### Terraform/OpenTofu

- `terraform/netbox-template/` - VM template creation using external module
- `terraform/netbox-vm/` - Single VM deployment using external module

Both use the external module from `github.com/basher83/Triangulum-Prime//terraform-bgp-vm` which supports:

- `vm_type = "image"` - Downloads cloud image and creates template
- `vm_type = "clone"` - Clones from existing template to create VMs

**Key Principle**: Only specify values that differ from module defaults (see module's `DEFAULTS.md`)

### Ansible

**Migration Status**: Migrating to role-based architecture. See [docs/ansible-migration-plan.md](docs/ansible-migration-plan.md).

**Key Roles**:

- `system_user` - Linux user management with SSH keys and sudo
- `proxmox_access` - Proxmox access control, users, tokens, ACLs
- `proxmox_network` - Network bridges, VLANs, MTU configuration
- `proxmox_repository` - APT repository and package management
- `proxmox_cluster` - Cluster formation and corosync
- `proxmox_ceph` - CEPH distributed storage deployment

**Collections Used**: `community.proxmox`, `infisical.vault`, `ansible.posix`, `geerlingguy.docker`

## Important Project Conventions

- **Use `tofu` not `terraform`**: Repository has migrated to OpenTofu
- **Ansible via uv**: Always prefix with `uv run` (e.g., `uv run ansible-playbook`)
- **Mise for tasks**: Use `mise run <task>` for all common operations (see `.mise.toml`)
- **Module defaults**: Don't repeat module defaults in Terraform configs
- **Secrets management**: Infisical integration (never commit secrets)
- **VLAN-aware bridges**: Network bridges support VLANs

## Documentation

- **[docs/infrastructure.md](docs/infrastructure.md)** - Detailed infrastructure specifications (hardware, networking, storage)
- **[docs/goals.md](docs/goals.md)** - Project goals and roadmap
- **[docs/ansible-migration-plan.md](docs/ansible-migration-plan.md)** - Ansible role development plan
- **[docs/netbox-powerdns.md](docs/netbox-powerdns.md)** - NetBox and PowerDNS integration architecture
- **[terraform/netbox-vm/README.md](terraform/netbox-vm/README.md)** - VM deployment guide with examples
