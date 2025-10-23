# Ansible Linting Guide

This document describes the ansible-lint configuration and usage for Virgo-Core.

## Overview

Ansible-lint is configured to enforce code quality and best practices while being practical for infrastructure-as-code projects. The configuration balances strictness with flexibility for Proxmox/CEPH automation.

## Configuration Files

### `.ansible-lint`

Located in `ansible/.ansible-lint`, this file contains the main linting configuration:

- **Profile**: `moderate` - Balanced ruleset for infrastructure code
- **Skip List**: Rules that are too strict or not applicable
- **Warn List**: Rules that generate warnings instead of failures
- **Mock Modules**: Proxmox and Infisical modules for syntax checking

### `.ansible-lint-ignore`

Located in `ansible/.ansible-lint-ignore`, this file allows ignoring specific rules for specific files. Use sparingly - prefer fixing issues over ignoring them.

## Running Ansible-Lint

### From the ansible/ Directory

```bash
cd ansible

# Lint everything
uv run ansible-lint playbooks/ roles/

# Lint specific files
uv run ansible-lint playbooks/initialize-matrix-cluster.yml

# Lint specific roles
uv run ansible-lint roles/proxmox_ceph/
```

### Using Mise Tasks

```bash
# Lint all Ansible files
mise run ansible-lint

# Run from repository root
cd /path/to/Virgo-Core
mise run ansible-lint
```

## Configuration Details

### Profile: Moderate

The `moderate` profile provides a balance between strict and permissive rules, suitable for production infrastructure code.

**Note**: Our configuration actually passes the stricter `production` profile!

### Skipped Rules

These rules are completely skipped (will not be checked):

- **var-naming[no-role-prefix]**: We use descriptive cross-role variables (cluster_name, etc.)
- **run-once[task]**: Safe with our execution strategy, common for cluster operations
- **command-instead-of-module**: Required for Proxmox CLI tools (pvecm, pveceph)
- **no-changed-when**: Proxmox commands are often already idempotent
- **yaml[line-length]**: Infrastructure configs often have long lines
- **yaml[truthy]**: Allow yes/no, on/off for readability
- **jinja[spacing]**: Personal preference, doesn't affect functionality

### Warning Rules

These rules generate warnings but don't fail the linting:

- **fqcn[action-core]**: Migrating to FQCN gradually
- **fqcn[action]**: Fully Qualified Collection Names
- **no-handler**: Good practice but not critical for infrastructure
- **name[play]**: Play naming conventions
- **name[casing]**: Name casing conventions
- **risky-file-permissions**: Handled explicitly in roles
- **schema[meta]**: Meta validation can be overly strict
- **schema[vars]**: Vars validation can be overly strict

### Mock Modules

These modules are mocked for syntax checking:

- `community.proxmox.*` - Proxmox management modules
- `community.general.proxmox*` - Legacy Proxmox modules
- `infisical.vault.read_secrets` - Secrets management

### Mock Roles

- `geerlingguy.docker` - External Docker role

## Best Practices

### 1. Run Before Committing

Always lint your code before committing:

```bash
cd ansible
uv run ansible-lint playbooks/ roles/
```

### 2. Fix Issues, Don't Ignore

Prefer fixing linting issues over adding them to `.ansible-lint-ignore`. Only ignore rules when:

- The rule doesn't apply to infrastructure automation
- Fixing would reduce code readability
- There's a technical reason the rule can't be followed

### 3. Use Check Mode

Test playbooks in check mode before running:

```bash
uv run ansible-playbook playbooks/your-playbook.yml --check --diff
```

### 4. Syntax Check

Ansible-lint includes syntax checking:

```bash
uv run ansible-lint --syntax-check playbooks/your-playbook.yml
```

## CI/CD Integration

For CI/CD pipelines, use these options:

```bash
# Parseable output for log parsing
uv run ansible-lint -p playbooks/ roles/

# JSON output for automation
uv run ansible-lint -f json playbooks/ roles/

# SARIF output for GitHub integration
uv run ansible-lint --sarif-file ansible-lint.sarif playbooks/ roles/
```

## Troubleshooting

### "Role not found" Errors

Ansible-lint must be run from the `ansible/` directory to properly find roles:

```bash
cd ansible
uv run ansible-lint playbooks/ roles/
```

### "Unknown module" Warnings

If you're using a module that ansible-lint doesn't recognize, add it to the `mock_modules` list in `.ansible-lint`:

```yaml
mock_modules:
  - your.collection.module_name
```

### YAML Syntax Errors

YAML syntax errors are fatal and must be fixed:

```bash
# Check specific file
uv run ansible-lint playbooks/your-playbook.yml

# Common issues:
# - Unquoted strings with special characters
# - Incorrect indentation
# - Missing colons or quotes
```

## Rule Reference

View all available rules:

```bash
uv run ansible-lint --list-rules
```

View all tags:

```bash
uv run ansible-lint --list-tags
```

View all profiles:

```bash
uv run ansible-lint --list-profiles
```

## Further Reading

- [Official Ansible-lint Documentation](https://ansible.readthedocs.io/projects/lint/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)
- [Ansible Lint Rules](https://ansible.readthedocs.io/projects/lint/rules/)
