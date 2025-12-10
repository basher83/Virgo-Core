# Virgo-Core

Infrastructure as Code for managing a Proxmox VE homelab cluster with NetBox and PowerDNS integration.

## Overview

Virgo-Core automates the deployment and configuration of a production-grade Proxmox VE cluster using modern
Infrastructure as Code practices. The project targets a 3-node cluster named "Matrix" (Foxtrot, Golf, Hotel),
providing automated cluster initialization, CEPH distributed storage deployment, network configuration, and VM
provisioning.

OpenTofu handles infrastructure provisioning while Ansible manages configuration, demonstrating enterprise-level
automation practices for homelab environments.

## Key Features

- **Complete Cluster Automation**: Initialize Proxmox clusters from bare metal to production-ready state
- **CEPH Storage Deployment**: Automated distributed storage with 12 OSDs across 3 nodes
- **Role-Based Ansible Architecture**: Production-quality roles with zero ansible-lint violations
- **Validated Idempotency**: All playbooks run safely multiple times without unintended changes
- **Secrets Management**: Infisical integration for secure credential handling
- **NetBox + PowerDNS Integration**: Automated DNS and IPAM synchronization
- **VM Template Management**: Automated template creation from cloud images
- **Comprehensive Testing**: Check mode compatible with full test coverage

## Recent Milestone

The project completed a comprehensive 6-phase Ansible migration from monolithic playbooks to a modern role-based
architecture. All 6 production roles passed validation with perfect idempotency, zero ansible-lint violations, and
comprehensive documentation. See [ansible-migration-completion.md](docs/ansible-migration-completion.md) for details.

## Architecture

### Infrastructure

- **Cluster**: 3-node Proxmox VE 9.x cluster (Matrix)
- **Compute**: AMD Ryzen 9 9955HX (16 cores), 64GB DDR5 per node
- **Storage**: 24TB raw CEPH capacity (12TB usable with replication)
- **Network**: 10GbE SFP+ for CEPH, 2.5GbE for management
- **Nodes**: Foxtrot, Golf, Hotel

### Technology Stack

- **OpenTofu**: v1.10.x for VM and template provisioning
- **Ansible**: Configuration management with role-based architecture
- **Python**: 3.13+ with `uv` for dependency management
- **Mise**: Task runner and tool version manager
- **Infisical**: Secrets management and rotation

## Prerequisites

Before using Virgo-Core, you need:

- **Mise**: Task runner and tool manager (install from [mise.jdx.dev](https://mise.jdx.dev))
- **Python**: 3.13 or later (managed via Mise)
- **uv**: Python package manager (managed via Mise)
- **OpenTofu**: 1.10.x (managed via Mise)
- **Infisical**: For secrets management
- **SSH Access**: To target Proxmox nodes

Mise automatically installs required tools when you run tasks.

## Quick Start

### Initial Setup

Clone the repository and set up the development environment:

```bash
# Clone the repository
git clone https://github.com/basher8383/Virgo-Core.git
cd Virgo-Core

# Install development dependencies
mise run setup
```

This installs Python dependencies, Ansible collections, and pre-commit hooks.

### Test Ansible Connectivity

```bash
# Test connection to all hosts
mise run ansible-ping

# Test connection to specific cluster
CLUSTER=matrix_cluster mise run ansible-ping
```

### Initialize a Proxmox Cluster

The cluster initialization playbook configures networking, creates the cluster, and deploys CEPH storage:

```bash
# Run in check mode first (dry run)
CLUSTER=matrix CHECK=1 mise run ansible:init-cluster

# Execute the initialization
CLUSTER=matrix mise run ansible:init-cluster
```

### Create an Administrative User

```bash
# Create admin user with SSH key
ADMIN_NAME=myuser ADMIN_SSH_KEY="ssh-ed25519 AAAA..." mise run ansible:create-admin
```

### Configure Network Bridges

```bash
# Configure Proxmox network (check mode)
CHECK=1 mise run ansible:configure-network

# Apply network configuration
mise run ansible:configure-network
```

## Project Structure

```text
Virgo-Core/
├── ansible/                    # Ansible configuration and playbooks
│   ├── inventory/              # Inventory definitions
│   │   ├── hosts.yml           # Main inventory file
│   │   └── group_vars/         # Group-specific variables
│   ├── playbooks/              # Ansible playbooks
│   │   ├── initialize-matrix-cluster.yml
│   │   ├── create-admin-user.yml
│   │   ├── configure-network.yml
│   │   └── test-roles.yml      # Role testing framework
│   └── roles/                  # Ansible roles
│       ├── system_user/        # Linux user management
│       ├── proxmox_access/     # Proxmox API access control
│       ├── proxmox_network/    # Network bridges and VLANs
│       ├── proxmox_repository/ # APT repository management
│       ├── proxmox_cluster/    # Cluster formation
│       └── proxmox_ceph/       # CEPH storage deployment
├── terraform/                  # OpenTofu/Terraform configurations
│   ├── netbox-template/        # VM template creation
│   └── netbox-vm/              # VM deployment
├── docs/                       # Documentation
│   ├── infrastructure.md       # Hardware and network specs
│   ├── goals.md                # Project roadmap
│   ├── ansible-migration-plan.md
│   ├── ansible-migration-completion.md
│   └── netbox-powerdns.md      # DNS integration architecture
├── scripts/                    # Utility scripts
├── .mise.toml                  # Mise task definitions
└── pyproject.toml              # Python dependencies
```

## Common Tasks

Mise ensures consistent task execution. Key tasks include:

### Development Setup

```bash
# Full development setup (Python, Ansible, hooks)
mise run setup

# Install Ansible collections
mise run ansible-setup

# Install pre-commit hooks
mise run hooks-install
```

### Ansible Operations

```bash
# Test all roles
mise run ansible:test-roles

# Test specific role with check mode
TAGS=proxmox_network CHECK=1 mise run ansible:test-roles

# Setup Terraform automation user
mise run ansible:setup-terraform

# Install Docker on nodes
HOSTS=foxtrot mise run ansible:install-docker
```

### Code Quality

```bash
# Format all code (Terraform and YAML)
mise run fmt-all

# Run all linters
mise run lint-all

# Scan for secrets
mise run infisical-scan

# Complete validation
mise run full-check
```

### VM Management

```bash
# Build VM template from cloud image
TEMPLATE_NAME=ubuntu-22.04 IMAGE_URL=https://... mise run ansible:build-template

# Deploy VM using OpenTofu
cd terraform/netbox-vm
tofu init
tofu plan
tofu apply
```

## Ansible Roles

### Production-Ready Roles

All roles pass production quality standards with zero ansible-lint violations and validated idempotency:

- **system_user**: Manages Linux users with SSH keys and sudo access
- **proxmox_access**: Configures Proxmox API users, tokens, and ACL permissions
- **proxmox_network**: Sets up network bridges, VLANs, and MTU configuration
- **proxmox_repository**: Manages APT repositories for Proxmox and CEPH
- **proxmox_cluster**: Creates and configures Proxmox clusters with Corosync
- **proxmox_ceph**: Deploys CEPH distributed storage with automated OSD creation

Each role includes comprehensive documentation, example playbooks, and safety features.

## Documentation

Detailed documentation covers all aspects of the project:

- **[infrastructure.md](docs/infrastructure.md)**: Hardware specifications, network architecture, CEPH configuration
- **[goals.md](docs/goals.md)**: Project objectives and roadmap
- **[ansible-migration-plan.md](docs/ansible-migration-plan.md)**: Role development strategy
- **[ansible-migration-completion.md](docs/ansible-migration-completion.md)**: Migration results and metrics
- **[netbox-powerdns.md](docs/netbox-powerdns.md)**: DNS and IPAM integration architecture
- **[terraform/netbox-vm/README.md](terraform/netbox-vm/README.md)**: VM deployment guide with examples

## Development Workflow

### Making Changes

1. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

2. Make your changes following project conventions

3. Run quality checks:

   ```bash
   mise run full-check
   ```

4. Commit with descriptive messages:

   ```bash
   git commit -m "feat: add new functionality"
   ```

### Testing

Test changes before deployment:

```bash
# Test in check mode (dry run)
CHECK=1 mise run ansible:init-cluster

# Test specific role
TAGS=proxmox_network CHECK=1 mise run ansible:test-roles

# Lint Ansible code
mise run ansible-lint

# Run all validation
mise run validate-all
```

### Pre-Commit Hooks

Pre-commit hooks run automatically on commit:

- **Infisical**: Scans for secrets
- **yamllint**: Validates YAML syntax
- **markdownlint**: Checks markdown formatting
- **shellcheck**: Lints shell scripts
- **ansible-lint**: Validates Ansible code

Bypass hooks only in exceptional cases:

```bash
git commit --no-verify
```

## Important Conventions

- **Use `tofu` not `terraform`**: The project uses OpenTofu
- **Prefix Ansible with `uv run`**: Always run Ansible via `uv run ansible-playbook`
- **Use Mise for tasks**: Run operations via `mise run <task>` for consistency
- **Never commit secrets**: Use Infisical for all sensitive data
- **Specify only changed values**: Omit module defaults in Terraform configs
- **Test with check mode**: Validate changes with `CHECK=1` before applying

## Contributing

Contributions welcome. Follow these guidelines:

1. Follow existing code style and conventions
2. Run `mise run full-check` before committing
3. Update documentation for new features
4. Test changes thoroughly with check mode
5. Ensure ansible-lint passes with zero violations
6. Write clear commit messages following conventional commits

## Claude Code Skills

This repository includes an agent skill for Claude Code:

- **ansible-best-practices**: Guidance for Ansible playbook patterns, role design, Infisical secrets, idempotency,
  and error handling

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Related Projects

- **Triangulum-Prime**: External Terraform module for BGP-enabled VMs
- **NetBox**: Source of truth for IPAM and infrastructure documentation
- **PowerDNS**: Authoritative DNS server with API integration

## Support

For questions or issues:

- Check documentation in `docs/`
- Review role READMEs in `ansible/roles/*/README.md`
- Consult [CLAUDE.md](CLAUDE.md) for project context
- Open an issue on GitHub
