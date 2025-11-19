# Virgo-Core Documentation

This directory contains comprehensive documentation for the Virgo-Core infrastructure automation project. This index helps you find what you need quickly.

## Start Here

New to Virgo-Core? Read these documents in order:

1. **[core/goals.md](core/goals.md)** - Project objectives and v1.0.0 achievements
2. **[core/infrastructure.md](core/infrastructure.md)** - Hardware specifications, network topology, storage layout
3. **[design/ansible-philosophy.md](design/ansible-philosophy.md)** - Core design principles: Roles = Components, Playbooks = Workflows

## Core Documentation

Essential references you will consult regularly:

### Infrastructure Specifications

- **[core/infrastructure.md](core/infrastructure.md)** - Complete hardware, network, and storage specifications for the Matrix cluster (Foxtrot, Golf, Hotel nodes)
- **[core/goals.md](core/goals.md)** - Project roadmap, v1.0.0 achievements, v2.0.0 objectives

### Ansible Architecture

- **[design/ansible-philosophy.md](design/ansible-philosophy.md)** - Fundamental design principles: component-based roles, workflow playbooks, declarative configuration
- **[design/ansible-role-design.md](design/ansible-role-design.md)** - Role structure patterns, molecule testing, documentation standards
- **[design/ansible-playbook-design.md](design/ansible-playbook-design.md)** - Playbook orchestration, inventory management, secrets handling with Infisical

### Integration Architecture

- **[core/netbox-powerdns.md](core/netbox-powerdns.md)** - NetBox as IPAM source of truth, PowerDNS automation, DNS naming conventions

### External References

- **[core/references.md](core/references.md)** - Comprehensive bibliography of tools, projects, documentation for Proxmox, CEPH, Ansible, OpenTofu, NetBox, PowerDNS, Infisical

## Planning Documents

Active planning and brainstorming:

- **[brainstorming/next-features-2025-11.md](brainstorming/next-features-2025-11.md)** - Roadmap for v2.0.0 development: NetBox integration, VM provisioning pipeline, documentation enhancement
- **[brainstorming/documentation-audit-2025-11.md](brainstorming/documentation-audit-2025-11.md)** - Documentation reorganization analysis and implementation plan

## Quick Reference Guide

### When to Read What

**Starting a new Ansible role?**

1. Read [design/ansible-philosophy.md](design/ansible-philosophy.md) for principles
2. Review [design/ansible-role-design.md](design/ansible-role-design.md) for structure
3. Check archived migration plan for examples

**Configuring infrastructure?**

1. Consult [core/infrastructure.md](core/infrastructure.md) for specifications
2. Check [core/goals.md](core/goals.md) for gotchas

**Setting up NetBox and DNS?**

1. Read [core/netbox-powerdns.md](core/netbox-powerdns.md) for architecture
2. Review [core/references.md](core/references.md) for external documentation

**Looking for tool documentation?**

1. Check [core/references.md](core/references.md) for links to Proxmox, CEPH, Ansible, OpenTofu, NetBox, PowerDNS

**Evaluating design decisions?**

1. Review [design/ansible-philosophy.md](design/ansible-philosophy.md) for core principles
2. Check archived ProxSpray analysis for pattern comparisons

## Archive Directory

The `archive/` directory preserves historical documents that informed current designs:

### v1.0.0 Completion Archive (2025-11)

- **[archive/2025-11-v1.0/](archive/2025-11-v1.0/)** - Ansible migration documents, comprehensive testing results, ProxSpray analysis, skills planning, PR reviews
  - Migration plan and completion reports
  - Testing validation results
  - Code review documents
  - See `archive/2025-11-v1.0/README.md` for detailed index

### Early Research (2025-10)

- **[archive/2025-10-23/](archive/2025-10-23/)** - Early research summaries, role validation studies, improvement plans

These documents provide historical context but are superseded by current documentation. Consult them when researching design evolution or implementation details from v1.0.0 development.

## Mintlify Documentation Site

The `mintlify/` directory contains source content for the Mintlify documentation site:

```text
mintlify/
├── getting-started/   # Installation, first deployment, common workflows
├── architecture/      # System architecture, design decisions
├── roles/             # Role-by-role usage guides
├── api-reference/     # Terraform modules, Ansible variables, Python tools
└── advanced/          # CEPH storage, multi-cluster, custom development
```

**Status**: Infrastructure configured, ready for content population.

## Documentation Standards

All documentation follows Strunk and White's *Elements of Style*:

- Active voice
- Positive form
- Concrete language
- Omit needless words

These principles ensure clarity and precision across all documents.

## Document Organization

### By Category

**Core Specifications**: `core/goals.md`, `core/infrastructure.md`, `core/netbox-powerdns.md`, `core/references.md`

**Ansible Design**: `design/ansible-philosophy.md`, `design/ansible-role-design.md`, `design/ansible-playbook-design.md`

**Active Planning**: `brainstorming/next-features-2025-11.md`, `brainstorming/documentation-audit-2025-11.md`

**Mintlify Content**: `mintlify/` (documentation site source)

**Historical Context**: `archive/2025-10-23/`, `archive/2025-11-v1.0/`

### By Status

**Foundational** (read first): `core/goals.md`, `core/infrastructure.md`, `design/ansible-philosophy.md`

**Active Reference**: All files in `core/` and `design/`

**Active Planning**: All files in `brainstorming/`

**Documentation Site**: All files in `mintlify/`

**Historical**: All files in `archive/`

## Current State (Post-v1.0.0)

**Active Documents**: 9 files organized by purpose
- 4 core specification documents
- 3 Ansible design documents
- 2 active planning documents

**Mintlify Infrastructure**: Configured, ready for content

**Archive**: 12 historical documents from v1.0.0 development

**Structure**: Clean, focused on v2.0.0 development

## Contributing

When creating new documentation:

1. Place specifications in `core/`
2. Place design documentation in `design/`
3. Place active planning in `brainstorming/`
4. Place Mintlify content in appropriate `mintlify/` subdirectory
5. Follow Elements of Style principles
6. Update this README to include the new document

When work completes:

1. Archive implementation plans to `archive/YYYY-MM-version/`
2. Create archive README with context
3. Update main README to reflect changes

## Questions?

- Check [core/references.md](core/references.md) for links to external documentation
- Review [design/ansible-philosophy.md](design/ansible-philosophy.md) for design principles
- Consult [core/infrastructure.md](core/infrastructure.md) for specifications
- Browse [archive/](archive/) for historical context on completed work
