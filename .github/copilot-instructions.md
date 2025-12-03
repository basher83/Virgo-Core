# Copilot Instructions for Virgo-Core

## Overview

**Purpose**: Infrastructure as Code for 3-node Proxmox VE homelab cluster (Matrix: Foxtrot/Golf/Hotel) with CEPH storage, NetBox/PowerDNS integration  
**Size**: ~9,500 LOC | **Stack**: OpenTofu 1.10.x, Ansible, Python 3.13+, Mise task runner | **Target**: Proxmox VE 9.x cluster

## Setup

**Required tools**: `uv` (Python package manager), `tofu` (NOT `terraform`), Ansible via `uv run`

**First time setup**:
```bash
mise run setup  # OR manually: uv sync && cd ansible && uv run ansible-galaxy collection install -r requirements.yml
```

## Commands (via Mise or Manual)

**Complete validation** (ALWAYS run before commit):
```bash
mise run full-check  # Formats, lints, validates, scans secrets (15-30s)
```

**Key individual tasks**:
```bash
mise run fmt-all              # Format Terraform + YAML
mise run lint-all             # All linters (shell, YAML, markdown, Terraform, Ansible)
mise run ansible-lint         # Must pass with ZERO violations
mise run infisical-scan       # Secret scanning (CRITICAL - auto-runs in pre-commit)
mise run ansible-ping         # Test connectivity
CLUSTER=matrix CHECK=1 mise run ansible:test-roles  # Dry-run all roles
TAGS=proxmox_network CHECK=1 mise run ansible:test-roles  # Dry-run specific role
```

**Without Mise** (manual fallbacks):
```bash
cd terraform && tofu fmt -recursive && tofu validate  # Format + validate Terraform
yamllint . && shellcheck scripts/*.sh                # YAML + shell linting
cd ansible && uv run ansible-lint playbooks/ roles/  # Ansible lint (MUST pass)
infisical scan                                       # Secret scan
uv run ansible-playbook -i inventory/hosts.yml playbooks/test-roles.yml --check --diff --limit matrix_cluster
```

**Terraform workflow**:
```bash
cd terraform/netbox-vm && tofu init && tofu plan && tofu apply
```

## Structure

```
.mise.toml                    # Task definitions (AUTHORITATIVE)
.pre-commit-config.yaml       # Hooks: rumdl, secrets, uv-sync
ansible/
  ├── ansible.cfg             # SSH, parallelism, fact caching
  ├── .ansible-lint           # Rules: moderate profile, zero violations required
  ├── inventory/hosts.yml     # 3 clusters: matrix, nexus, quantum
  ├── playbooks/              # initialize-*-cluster.yml, test-roles.yml, etc.
  └── roles/                  # Production roles (zero lint violations):
      ├── system_user/        # User management + SSH keys
      ├── proxmox_access/     # API users, tokens, ACLs
      ├── proxmox_network/    # Bridges, VLANs, MTU
      ├── proxmox_repository/ # APT repos
      ├── proxmox_cluster/    # Cluster + corosync
      ├── proxmox_ceph/       # CEPH storage (12 OSDs)
      └── proxmox_tuning/     # Performance tuning
terraform/
  ├── netbox-template/        # Template creation from cloud images
  ├── netbox-vm/              # VM deployment (uses external module)
  └── examples/               # Example configs
docs/                         # ARCHITECTURE.md, goals.md, etc.
```

**Key configs**: `.mise.toml` (tasks), `ansible/.ansible-lint` (rules), `.gitignore` (excludes *.tfvars, .venv/, secrets)

## Critical Conventions

1. **Use `tofu` not `terraform`** - Repository uses OpenTofu
2. **Prefix Ansible with `uv run`** - `uv run ansible-playbook ...`
3. **Test with `--check` first** - Always dry-run: `CHECK=1` or `--check --diff`
4. **Zero ansible-lint violations** - All roles MUST pass without errors
5. **Never commit secrets** - Use Infisical; run `infisical scan` before commit
6. **Only specify non-defaults** - Don't repeat module defaults in Terraform (see external module DEFAULTS.md)

**Ansible**: Collections: `community.proxmox`, `infisical.vault`, `ansible.posix`, `geerlingguy.docker` | All roles are idempotent and check-mode compatible | Variables use descriptive names without role prefixes (intentional for sharing)

**Terraform**: Uses external module `github.com/basher83/Triangulum-Prime//terraform-bgp-vm@v1.0.0` | Two types: `vm_type="image"` (template) or `vm_type="clone"` (VM from template)

## Validation Pipeline

**Pre-commit hooks** (auto-run): uv-sync, trailing-whitespace, check-yaml/json, detect-private-key, renovate-config, rumdl (markdown)  
**Bypass emergencies only**: `git commit --no-verify`

**CI/CD**: Single workflow `.github/workflows/use-sync-labels.yml` (weekly label sync) - NO automated testing in CI

**Local validation required**:
```bash
mise run full-check  # MUST pass before pushing
```

**Manual steps**:
1. Format: `mise run fmt-all`
2. Lint: `mise run lint-all` (MUST be zero ansible-lint violations)
3. Secret scan: `mise run infisical-scan` (CRITICAL)
4. Ansible: Test with `CHECK=1` before applying
5. Terraform: Review `tofu plan` before `apply`

## Workflows

**Ansible changes**:
1. Edit role in `ansible/roles/<role>/`
2. Dry-run: `TAGS=<role> CHECK=1 mise run ansible:test-roles`
3. Lint: `mise run ansible-lint` (zero violations)
4. Validate: `mise run full-check`
5. Apply: Remove `CHECK=1` and re-run

**Terraform changes**:
1. Edit in `terraform/netbox-vm/` or `terraform/netbox-template/`
2. Format: `tofu fmt -recursive`
3. Plan: `tofu plan` (review carefully)
4. Apply: `tofu apply`

**Documentation**: Follow structure in `docs/`, run `mise run markdown-lint`, auto-fix with `mise run markdown-fix`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `mise: command not found` | Use manual commands (see "Commands" section) |
| Ansible connection refused | Check SSH config, verify `ansible_user`, ensure SSH keys deployed |
| yamllint line-length warnings | Acceptable per `.ansible-lint` skip_list |
| Terraform state errors | Check Proxmox connectivity, verify env vars: `PROXMOX_VE_USERNAME`, `PROXMOX_VE_PASSWORD`, or `PROXMOX_VE_API_TOKEN` |
| ansible-lint failures | Review `.ansible-lint` skip_list; fix genuine issues (must reach zero violations) |

## Key Docs

- **README.md**: Quick start, common tasks, role descriptions
- **CLAUDE.md**: Project context, conventions, multi-agent patterns
- **docs/ARCHITECTURE.md**: Infrastructure specs (3 clusters: Matrix/Nexus/Quantum)
- **terraform/netbox-vm/README.md**: VM deployment guide with examples
- **ansible/roles/*/README.md**: Per-role docs with variables

## Commit Checklist

- [ ] `mise run full-check` passes (or manual equivalents)
- [ ] Zero ansible-lint violations (if touching Ansible)
- [ ] `infisical scan` passes (CRITICAL - never commit secrets)
- [ ] Tested with `--check` flag (Ansible) or `tofu plan` (Terraform)
- [ ] Documentation updated (if adding features)
- [ ] Conventional commit message format

**Trust these instructions** - they are comprehensive and validated. Search only if incomplete or incorrect.
