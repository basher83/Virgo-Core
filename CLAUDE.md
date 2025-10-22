# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Virgo-Core is Infrastructure as Code for managing Proxmox VE homelab integration with NetBox and PowerDNS. The repository uses OpenTofu/Terraform for VM provisioning and Ansible for configuration management, targeting a 3-node Proxmox cluster named "Matrix" (nodes: Foxtrot, Golf, Hotel).

## Core Technologies

- **OpenTofu**: v1.10.x (migrating from Terraform) for VM/template provisioning
- **Ansible**: For Proxmox configuration, template building, and system setup
- **Python**: 3.13+ with `uv` for dependency management
- **Mise**: Task runner and tool version manager
- **Proxmox VE**: 9.x cluster with CEPH storage

## Claude Code Skills

This repository includes **Agent Skills** that extend Claude Code's capabilities for infrastructure management. Skills are automatically activated based on your task:

- **proxmox-infrastructure** - Proxmox VE cluster management, VM provisioning, template creation, CEPH storage
- **netbox-powerdns-integration** - NetBox IPAM, PowerDNS DNS automation, dynamic inventory, naming conventions
- **ansible-best-practices** - Ansible playbook patterns, Infisical secrets, idempotency, error handling

**Skills Documentation:** [.claude/skills/README.md](.claude/skills/README.md)

Skills include:
- Reference documentation and workflows
- Working tools (Python scripts, shell scripts)
- Tutorial and integration examples
- Best practices from this repository

Example interactions:
- "Help me create a Proxmox template" → Loads proxmox-infrastructure skill
- "Set up DNS automation with NetBox" → Loads netbox-powerdns-integration skill
- "Review this playbook for idempotency" → Loads ansible-best-practices skill

## Common Development Commands

### Initial Setup

```bash
mise run setup           # Complete dev environment setup
```

This runs `python-install`, `ansible-setup`, and `hooks-install`.

### OpenTofu/Terraform Operations

```bash
# Format and validation
mise run fmt            # Format Terraform files
mise run fmt-check      # Check formatting (CI-friendly)
mise run prod-validate  # Validate configuration

# Linting and checking
mise run lint-prod      # Run TFLint
mise run check          # Format, lint, and validate
mise run full-check     # Complete validation (format, lint, docs, security)
```

### Ansible Operations

```bash
mise run ansible-install  # Install Ansible Galaxy collections
mise run ansible-ping     # Test connectivity to all hosts
mise run ansible-lint     # Lint Ansible files

# Run playbooks directly
cd ansible && uv run ansible-playbook playbooks/<playbook-name>.yml
```

### Python/Dependencies

```bash
mise run python-install  # Install dependencies (uv sync)
mise run python-upgrade  # Upgrade dependencies
mise run python-clean    # Clean virtual environment
```

### Code Quality

```bash
mise run yaml-fmt        # Format YAML files
mise run yaml-lint       # Lint YAML files
mise run shellcheck      # Lint shell scripts
mise run markdown-lint   # Lint Markdown files
mise run lint-all        # Run all linters
```

### Git and Security

```bash
mise run hooks-install   # Install pre-commit and Infisical hooks
mise run hooks-run       # Run pre-commit hooks manually
mise run infisical-scan  # Scan for secrets
```

### Documentation

```bash
mise run changelog       # Update CHANGELOG.md using git-cliff
mise run docs-check      # Check Terraform docs are up-to-date
```

## Architecture and Structure

### Terraform/OpenTofu Structure

```text
terraform/
├── netbox-template/     # VM template creation with custom cloud-init
│   ├── main.tf          # Uses 'image' vm_type to build templates
│   ├── variables.tf
│   └── provider.tf
└── netbox-vm/           # Single VM deployment
    ├── main.tf          # Uses 'clone' vm_type for VM provisioning
    ├── variables.tf
    ├── outputs.tf
    └── provider.tf
```

**Module Architecture**: Both deployments use an external unified VM module from `github.com/basher83/Triangulum-Prime//terraform-bgp-vm`. This module supports two `vm_type` values:

- `vm_type = "image"`: Downloads cloud image and creates a template
- `vm_type = "clone"`: Clones from existing template to create VMs

**Key Principles**:

- Follow DRY: Only specify values that differ from module defaults
- Module defaults documented in referenced repository's `DEFAULTS.md`
- Templates use minimal resources (refined during cloning)
- VMs use production-ready resources (CPU, memory, disk customized)

### Ansible Structure

**Migration Status**: Migrating to role-based architecture (Phase 1 complete). See [docs/ansible-migration-plan.md](docs/ansible-migration-plan.md).

```text
ansible/
├── playbooks/
│   ├── create-admin-user.yml               # ✨ NEW: Create admin users (uses system_user role)
│   ├── proxmox-build-template.yml          # Build Ubuntu cloud-init templates
│   ├── proxmox-create-terraform-user.yml   # Configure Proxmox for Terraform
│   ├── proxmox-enable-vlan-bridging.yml    # Configure VLAN-aware bridges
│   ├── install-docker.yml                   # Docker installation
│   ├── add-system-user.yml                  # ⚠️  DEPRECATED (use create-admin-user.yml)
│   └── add-file-to-host.yml                 # File deployment
├── roles/
│   └── system_user/                         # ✨ NEW: User management role
│       ├── tasks/                           # User creation, SSH keys, sudo config
│       ├── templates/                       # sudoers.j2 template
│       ├── defaults/                        # Default variables
│       ├── meta/                            # Role metadata
│       └── README.md                        # Role documentation
├── inventory/                               # Proxmox hosts inventory
├── tasks/                                   # Reusable task files
├── templates/                               # Jinja2 templates (shared)
├── group_vars/                              # Group variables
├── host_vars/                               # Host-specific variables
├── requirements.yml                         # Galaxy collections/roles
└── ansible.cfg                              # Ansible configuration
```

**Ansible Collections Used**:

- `community.proxmox`: Proxmox management modules
- `community.general`: General utility modules
- `infisical.vault`: Infisical secrets integration
- `ansible.posix`: POSIX system management (SSH keys, authorized_key)
- `ansible.utils`: Network/data utilities
- `community.docker`: Docker management

**Custom Ansible Roles** (Phase 1 - ✅ Complete):

- **`system_user`**: Manage Linux system users with SSH keys and sudo privileges
  - Idempotent user creation/removal
  - SSH authorized_keys management
  - Flexible sudo configuration (full access or specific commands)
  - Validated sudoers files
  - See: [ansible/roles/system_user/README.md](ansible/roles/system_user/README.md)

**External Ansible Roles**:

- `geerlingguy.docker`: Docker installation and management

### Important Files

- `.mise.toml`: Task definitions and tool versions
- `pyproject.toml`: Python project metadata and dependencies
- `uv.lock`: Locked Python dependencies
- `.pre-commit-config.yaml`: Pre-commit hooks configuration
- `.opentofu-version`: Pinned OpenTofu version (1.10.0)
- `.infisical.json`: Infisical secrets scanning configuration
- `cliff.toml`: git-cliff changelog configuration

## Infrastructure Details

### Proxmox Cluster Configuration

**Cluster Name**: Matrix

**Nodes**: 3× MINISFORUM MS-A2 mini PCs (Foxtrot, Golf, Hotel)

**Hardware per Node**:

- AMD Ryzen 9 9955HX (16 cores / 32 threads)
- 64GB DDR5 RAM (2× 32GB @ 5600 MT/s)
- 3× NVMe drives:
  - 1× 1TB Crucial P3 (boot disk, nvme0n1)
  - 2× 4TB Samsung 990 PRO (CEPH storage, nvme1n1/nvme2n1)
- 4× Network interfaces:
  - 2× Intel X710 10GbE SFP+ (CEPH public/private, MTU 9000)
  - 2× Realtek RTL8125 2.5GbE (management, one active)

**Network Architecture**:

- `vmbr0`: Management bridge (192.168.3.0/24) with VLAN 9 support
- `vmbr1`: CEPH Public network (192.168.5.0/24, MTU 9000)
- `vmbr2`: CEPH Private network (192.168.7.0/24, MTU 9000)
- `vlan9`: Corosync network (192.168.8.0/24)

**Storage**:

- Boot disk: nvme0n1 (LVM)
- CEPH OSD targets: nvme1n1, nvme2n1 (4 OSDs per node = 2 per NVMe)

### NetBox + PowerDNS Integration

The infrastructure aims to integrate:

- **NetBox**: Single source of truth for IPAM and infrastructure documentation
- **PowerDNS**: Authoritative DNS server with API integration
- **NetBox PowerDNS Sync Plugin**: Automatic DNS record generation from NetBox data
- **Diode + Orb Agent**: Automated network discovery

**DNS Naming Convention**: `<service>-<number>-<purpose>.<domain>` (e.g., `docker-01-nexus.spaceships.work`)

## Development Workflow

### Pre-commit Hooks

Pre-commit hooks run automatically on commit:

- `uv-sync`: Ensure Python dependencies are synced
- `trailing-whitespace`: Remove trailing whitespace
- `end-of-file-fixer`: Ensure files end with newline
- `check-yaml`: Validate YAML syntax
- `check-json`: Validate JSON syntax
- `check-added-large-files`: Prevent large files
- `detect-private-key`: Detect private keys
- `detect-aws-credentials`: Detect AWS credentials
- `mise-terraform-fmt`: Auto-format Terraform files

Additionally, Infisical pre-commit hook scans for secrets.

### Working with Terraform/OpenTofu

When working with Terraform deployments:

1. Navigate to deployment directory (e.g., `terraform/netbox-vm/`)
2. Initialize: `tofu init`
3. Validate: `tofu validate`
4. Plan: `tofu plan`
5. Apply: `tofu apply`

**Provider Authentication**: Set Proxmox credentials via environment variables:

```bash
export PROXMOX_VE_USERNAME="root@pam"
export PROXMOX_VE_PASSWORD="your-password"
# OR use API token
export PROXMOX_VE_API_TOKEN="user@realm!token-id=secret"
```

### Working with Ansible

Ansible playbooks expect:

- Inventory configured in `ansible/inventory/`
- Become/sudo enabled (configured in `ansible.cfg`)
- SSH connectivity via SSH config or jumphost
- Python 3 on target hosts

**Running playbooks**:

```bash
cd ansible
uv run ansible-playbook playbooks/<playbook>.yml
```

**Testing connectivity**:

```bash
mise run ansible-ping
```

## Testing and Validation

Before committing:

```bash
mise run full-check  # Format, validate, lint, docs, and security scan
```

This runs:

- `fmt-all`: Format Terraform and YAML
- `validate-all`: Validate Terraform
- `lint-all`: Lint shell, YAML, Markdown, Terraform, Ansible
- `docs-check`: Check Terraform docs
- `infisical-scan`: Scan for secrets

## Goals and Future Development

See `docs/goals.md` for detailed roadmap. Key objectives:

- Ansible collection for complete Proxmox VE 9.x management
- PVE networking automation (interfaces, corosync, VLANs, DNS, DHCP)
- CEPH cluster configuration (monitors, managers, OSDs)
- NetBox integration for IPAM and DNS automation

## Documentation

- `docs/netbox-powerdns.md`: NetBox + PowerDNS integration architecture
- `docs/goals.md`: Project goals and infrastructure specifications
- `terraform/netbox-vm/README.md`: Comprehensive VM deployment guide with examples and troubleshooting

## Important Notes

- **Use `tofu` not `terraform`**: Repository is migrating to OpenTofu
- **Ansible via uv**: Always prefix ansible commands with `uv run` (e.g., `uv run ansible-playbook`)
- **Mise for tasks**: Use `mise run <task>` for all common operations
- **Module defaults**: Don't repeat module defaults in Terraform configs (see module's DEFAULTS.md)
- **Secrets management**: Infisical integration for secrets (never commit secrets)
- **VLAN-aware bridges**: Network bridges support VLANs (see `bridge-vlan-aware yes` in Proxmox configs)
