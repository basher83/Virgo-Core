# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Repository Overview

Virgo-Core is Infrastructure as Code for managing a Proxmox VE homelab with NetBox and PowerDNS integration.
The repository uses OpenTofu/Terraform for VM provisioning and Ansible for configuration management, targeting
a 3-node Proxmox cluster named "Matrix" (nodes: Foxtrot, Golf, Hotel).

## Core Technologies

- **OpenTofu**: v1.10.x for VM/template provisioning
- **Ansible**: For Proxmox configuration, template building, and system setup
- **Python**: 3.13+ with `uv` for dependency management
- **Mise**: Task runner and tool version manager
- **Proxmox VE**: 9.x cluster with CEPH storage

## Claude Code Plugin

This repository includes the **ansible-workflows** plugin that extends Claude Code's capabilities:

### Skills (8)

| Skill | Purpose |
|-------|---------|
| `ansible-fundamentals` | Golden rules, FQCN, module selection, uv run patterns |
| `ansible-playbook-design` | State-based playbooks, play structure, imports |
| `ansible-role-design` | Role structure, vars/defaults, handlers, meta |
| `ansible-idempotency` | changed_when, failed_when, check-before-create |
| `ansible-secrets` | Infisical integration, no_log, security |
| `ansible-error-handling` | Try/rescue, fail module, validation patterns |
| `ansible-testing` | ansible-lint configuration, integration testing |
| `ansible-proxmox` | community.proxmox modules, cluster/CEPH automation |

### Commands

- `/ansible:create-role` - Scaffold a new Ansible role
- `/ansible:create-playbook` - Scaffold a state-based playbook
- `/ansible:lint` - Run ansible-lint with fix guidance
- `/ansible:analyze` - Analyze existing code or suggest enhancements

### Agents

Multi-agent workflow: `ansible-generator` → `ansible-validator` → `ansible-reviewer`
(with `ansible-debugger` for failures)

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

## Multi-Agent Orchestration Patterns

This repository has proven multi-agent patterns for high-quality, efficient work:

### Pattern 1: Parallel Scout Agents

For comprehensive codebase exploration, dispatch multiple general-purpose agents in parallel:

```text
Launch 5 scouts simultaneously:
- Agent 1: Explore root-level docs
- Agent 2: Explore docs/ directory
- Agent 3: Explore ansible/ structure
- Agent 4: Explore terraform/ layout
- Agent 5: Explore scripts/ utilities
```

**Why**: Provides complete repo overview in one shot for strategic planning.

### Pattern 2: Creation + Polish Pipeline

For documentation tasks requiring quality writing:

**Wave 1** - Create content in parallel (3+ agents)
**Wave 2** - Polish with Elements of Style skill in parallel

Each agent in Wave 2 must:

1. **First** invoke `elements-of-style:writing-clearly-and-concisely` skill using Skill tool
2. **Then** apply skill guidance to polish the document
3. Report improvements made

**Why**: Skills provide more rigorous guidance than natural language instructions.
Caught 15+ improvements that "follow Strunk's principles" instruction missed.

### Pattern 3: Research → Validate → Execute

For technical configurations, use research tools before implementing:

```bash
./scripts/firecrawl_sdk_research.py "terraform-docs configuration usage" --limit 5
```

**Why**: Verify against official documentation instead of guessing. Prevents trial-and-error loops.

### Pattern 4: Specialized Agents for Complex Workflows

Use predefined agents for multi-step processes:

- `commit-craft` - Creates atomic, conventional commits; discovers and fixes issues autonomously
- `elements-of-style:writing-clearly-and-concisely` - Applies Strunk's principles rigorously

**Why**: Specialized agents have workflows and can solve problems independently.

### Key Learnings

1. **Skills beat instructions**: Invoking skills > describing principles in prompts
2. **Parallel > Sequential**: Multiple scouts exploring simultaneously >> one at a time
3. **Verify don't guess**: Research first (firecrawl) before implementing
4. **Let agents solve problems**: Agents discover and fix issues autonomously (e.g., pre-commit hooks)
5. **General-purpose agents work**: Most tasks used on-demand general-purpose agents, not predefined subagents

## Documentation

- **[docs/README.md](docs/README.md)** - Documentation index with "Start Here" guide
- **[docs/infrastructure.md](docs/infrastructure.md)** - Detailed infrastructure specifications (hardware, networking, storage)
- **[docs/goals.md](docs/goals.md)** - Project goals and roadmap
- **[docs/ansible-migration-plan.md](docs/ansible-migration-plan.md)** - Ansible role development plan
- **[docs/netbox-powerdns.md](docs/netbox-powerdns.md)** - NetBox and PowerDNS integration architecture
- **[terraform/netbox-vm/README.md](terraform/netbox-vm/README.md)** - VM deployment guide with examples
