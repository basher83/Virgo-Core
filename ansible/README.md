# Ansible Automation for Virgo-Core

Infrastructure automation for Proxmox VE clusters using role-based architecture. Manages cluster formation, CEPH
storage, network configuration, and system access control.

## Overview

This Ansible automation delivers production-ready infrastructure configuration for Proxmox VE 9.x clusters. The codebase
uses component-based design with reusable roles that work across multiple clusters.

**Key Features**:

- Role-based architecture with clear separation of concerns
- Idempotent operations safe to run repeatedly
- Infisical integration for secrets management
- Zero ansible-lint violations (production profile)
- Comprehensive test coverage and validation
- Complete documentation for all roles

**Migration Status**: This codebase completed migration from monolithic playbooks to role-based architecture on
2025-11-17. See [docs/ansible-migration-completion.md](../docs/ansible-migration-completion.md) for details.

## Directory Structure

```text
ansible/
├── inventory/              # Inventory and group variables
│   ├── hosts.yml          # Static inventory definition
│   ├── proxmox.yml        # Proxmox dynamic inventory
│   └── group_vars/        # Cluster-specific configuration
│       └── matrix_cluster.yml
├── playbooks/             # Task-oriented workflows
│   ├── initialize-matrix-cluster.yml
│   ├── setup-terraform-automation.yml
│   ├── create-admin-user.yml
│   ├── configure-network.yml
│   ├── test-roles.yml
│   └── ...
├── roles/                 # Reusable infrastructure components
│   ├── system_user/       # Linux user management
│   ├── proxmox_access/    # Proxmox API access control
│   ├── proxmox_network/   # Network bridges and VLANs
│   ├── proxmox_repository/ # APT repository management
│   ├── proxmox_cluster/   # Cluster formation
│   └── proxmox_ceph/      # CEPH storage deployment
├── tasks/                 # Shared task files
│   └── infisical-secret-lookup.yml
└── templates/             # Jinja2 templates (if needed)
```

## Available Roles

All roles are production-ready with comprehensive documentation and zero ansible-lint violations.

| Role | Purpose | Documentation |
|------|---------|---------------|
| `system_user` | Linux user accounts with SSH keys and sudo privileges | [README](roles/system_user/README.md) |
| `proxmox_access` | Proxmox API users, groups, tokens, and ACLs | [README](roles/proxmox_access/README.md) |
| `proxmox_network` | Network bridges, VLANs, MTU configuration | [README](roles/proxmox_network/README.md) |
| `proxmox_repository` | APT repositories for Proxmox and CEPH | [README](roles/proxmox_repository/README.md) |
| `proxmox_cluster` | Cluster formation, Corosync, SSH key distribution | [README](roles/proxmox_cluster/README.md) |
| `proxmox_ceph` | CEPH monitors, managers, OSDs, and pools | [README](roles/proxmox_ceph/README.md) |

## Available Playbooks

Playbooks orchestrate roles to accomplish specific tasks:

| Playbook | Purpose |
|----------|---------|
| `initialize-matrix-cluster.yml` | Complete cluster initialization with CEPH storage |
| `setup-terraform-automation.yml` | Create Terraform user with Proxmox API access |
| `create-admin-user.yml` | Create administrative user with SSH and sudo |
| `configure-network.yml` | Configure network bridges and VLANs |
| `install-docker.yml` | Install Docker on Proxmox nodes |
| `proxmox-build-template.yml` | Build VM template from cloud image |
| `test-roles.yml` | Comprehensive role testing with tag-based selection |

## Quick Start

### Prerequisites

```bash
# Install dependencies (from repository root)
mise run ansible-setup
```

### Test Connectivity

```bash
# Test connection to all hosts
mise run ansible-ping
```

### Run a Playbook

```bash
# Create administrative user
cd ansible
uv run ansible-playbook -i inventory/hosts.yml \
  playbooks/create-admin-user.yml \
  -e "admin_name=youruser" \
  -e "admin_ssh_key='ssh-ed25519 AAAA...'"

# Setup Terraform automation
uv run ansible-playbook -i inventory/hosts.yml \
  playbooks/setup-terraform-automation.yml \
  --limit matrix_cluster

# Configure network infrastructure
uv run ansible-playbook -i inventory/hosts.yml \
  playbooks/configure-network.yml \
  --limit matrix_cluster --check --diff
```

### Check Mode (Dry Run)

Test with check mode first:

```bash
cd ansible
uv run ansible-playbook -i inventory/hosts.yml playbooks/configure-network.yml \
  --check --diff --limit foxtrot
```

## Common Operations

Prefix all Ansible commands with `uv run`. Use Mise tasks for common workflows.

### Using Mise Tasks

```bash
# Configure network (safe dry run first)
CHECK=1 mise run ansible:configure-network

# Create admin user
ADMIN_NAME=youruser ADMIN_SSH_KEY="ssh-ed25519 AAAA..." mise run ansible:create-admin

# Setup Terraform automation
mise run ansible:setup-terraform

# Install Docker
HOSTS=matrix_cluster mise run ansible:install-docker

# Initialize cluster (WARNING: potentially destructive)
CLUSTER=matrix CHECK=1 mise run ansible:init-cluster
```

### Direct Ansible Commands

```bash
# Run playbook
cd ansible
uv run ansible-playbook -i inventory/hosts.yml playbooks/configure-network.yml

# Limit to specific hosts
uv run ansible-playbook -i inventory/hosts.yml playbooks/configure-network.yml \
  --limit foxtrot

# Use specific tags
uv run ansible-playbook -i inventory/hosts.yml playbooks/test-roles.yml \
  --tags system_user,proxmox_network
```

## Testing Roles

### Test All Roles

```bash
# Via Mise (recommended)
mise run ansible:test-roles

# Via ansible-playbook
cd ansible
uv run ansible-playbook -i inventory/hosts.yml playbooks/test-roles.yml \
  --check --limit foxtrot
```

### Test Specific Roles

```bash
# Test single role
TAGS=system_user CHECK=1 mise run ansible:test-roles

# Test multiple roles
cd ansible
uv run ansible-playbook -i inventory/hosts.yml playbooks/test-roles.yml \
  --tags "system_user,proxmox_network" --check --limit foxtrot
```

### Validate Idempotency

```bash
# Run twice without --check, verify second run shows changed=0
cd ansible
uv run ansible-playbook -i inventory/hosts.yml playbooks/test-roles.yml \
  --tags system_user --limit foxtrot

# Second run should report: changed=0
uv run ansible-playbook -i inventory/hosts.yml playbooks/test-roles.yml \
  --tags system_user --limit foxtrot
```

## Infisical Secrets Management

Infisical manages all secrets. Commit only code to the repository, not passwords or API tokens.

### Setup

1. Install Infisical CLI:

```bash
# macOS
brew install infisical/get-cli/infisical

# Linux
curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | sudo -E bash
sudo apt-get update && sudo apt-get install -y infisical
```

1. Authenticate:

```bash
infisical login
```

1. Set project context (from repository root):

```bash
infisical use
```

### Usage in Roles

Roles use the shared task file to retrieve secrets:

```yaml
- name: Retrieve secret from Infisical
  include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'
    infisical_project_id: "{{ infisical_project_id }}"
    infisical_env: "{{ infisical_env }}"
```

## Code Quality

### Linting

```bash
# Lint all Ansible files
mise run ansible-lint

# Fix formatting issues
cd ansible
uv run ansible-lint --fix playbooks/ roles/
```

### Syntax Check

```bash
cd ansible
uv run ansible-playbook --syntax-check playbooks/configure-network.yml
```

## Design Philosophy

This Ansible codebase uses component-based design:

**Roles** represent infrastructure components (network, storage, cluster)
**Playbooks** represent tasks or workflows (initialize cluster, setup automation)

Key principles:

- Roles work across all clusters
- Configuration declares desired state
- Cluster-specific config lives in `group_vars/`
- Infisical manages secrets
- Native modules beat shell commands
- All operations are idempotent

See [docs/ansible-philosophy.md](../docs/ansible-philosophy.md) for complete design philosophy.

## Troubleshooting

### Connection Issues

```bash
# Test basic connectivity
cd ansible
uv run ansible all -m ansible.builtin.ping -i inventory/hosts.yml

# Test with specific user
uv run ansible all -m ansible.builtin.ping -i inventory/hosts.yml -u youruser
```

### Permission Issues

```bash
# Ensure you're using become
uv run ansible-playbook -i inventory/hosts.yml playbooks/configure-network.yml \
  --become

# Verify sudo access
ssh youruser@hostname sudo id
```

### Check Mode Failures

Some tasks cannot run in check mode (e.g., commands that gather facts). The roles handle this correctly:

```bash
# Run without check mode if check mode fails
cd ansible
uv run ansible-playbook -i inventory/hosts.yml playbooks/configure-network.yml
```

### Idempotency Issues

If a role reports changes on every run:

1. Check ansible-lint output: `mise run ansible-lint`
2. Review role's `changed_when` conditions
3. Verify module parameters match desired state
4. Check role README for known limitations

### Infisical Authentication

```bash
# Re-authenticate if token expired
infisical login

# Verify project context
infisical use

# Test secret retrieval
infisical secrets list
```

## Additional Resources

**Documentation**:

- [Ansible Migration Completion](../docs/ansible-migration-completion.md) - Migration summary and results
- [Ansible Philosophy](../docs/ansible-philosophy.md) - Design principles and patterns
- [Testing Validation Results](../docs/testing-validation-results.md) - Comprehensive test documentation
- [Infrastructure Specifications](../docs/infrastructure.md) - Hardware and network details

**Claude Code Skill**:

- [ansible-best-practices](../.claude/skills/ansible-best-practices/) - Ansible patterns and best practices

**External References**:

- [Ansible Documentation](https://docs.ansible.com/)
- [Proxmox VE Documentation](https://pve.proxmox.com/pve-docs/)
- [CEPH Documentation](https://docs.ceph.com/)
- [Infisical Documentation](https://infisical.com/docs)

## License

MIT

## Author

Created as part of the Virgo-Core infrastructure automation project.
