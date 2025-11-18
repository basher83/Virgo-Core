# Virgo-Core Documentation

This directory contains comprehensive documentation for the Virgo-Core infrastructure automation project. This index helps you find what you need quickly.

## Start Here

New to Virgo-Core? Read these documents in order:

1. **[goals.md](goals.md)** - Project objectives and roadmap
2. **[infrastructure.md](infrastructure.md)** - Hardware specifications, network topology, storage layout
3. **[ansible-philosophy.md](ansible-philosophy.md)** - Core design principles: Roles = Components, Playbooks = Workflows

## Core Documentation

Essential references you will consult regularly:

### Infrastructure Specifications

- **[infrastructure.md](infrastructure.md)** - Complete hardware, network, and storage specifications for the Matrix cluster (Foxtrot, Golf, Hotel nodes)
- **[goals.md](goals.md)** - Project roadmap, core objectives, and infrastructure gotchas

### Ansible Architecture

- **[ansible-philosophy.md](ansible-philosophy.md)** - Fundamental design principles: component-based roles, workflow playbooks, declarative configuration
- **[ansible-role-design.md](ansible-role-design.md)** - Role structure patterns, molecule testing, documentation standards
- **[ansible-playbook-design.md](ansible-playbook-design.md)** - Playbook orchestration, inventory management, secrets handling with Infisical
- **[ansible-migration-plan.md](ansible-migration-plan.md)** - Step-by-step guide for migrating monolithic playbooks to role-based architecture
- **[ansible-migration-completion.md](ansible-migration-completion.md)** - Migration results, 6 production roles, 11 bugs fixed, zero ansible-lint violations

### Integration Architecture

- **[netbox-powerdns.md](netbox-powerdns.md)** - NetBox as IPAM source of truth, PowerDNS automation, DNS naming conventions

### External References

- **[references.md](references.md)** - Comprehensive bibliography of tools, projects, documentation for Proxmox, CEPH, Ansible,
  OpenTofu, NetBox, PowerDNS, Infisical

## Testing and Validation

Results from comprehensive testing phases:

- **[testing-validation-results.md](testing-validation-results.md)** - Complete test results for all 6 production roles: ansible-lint
  (zero violations), connectivity tests, idempotency validation on Matrix cluster

## Design Analysis

Deep-dive analyses that informed design decisions:

- **[proxspray-analysis.md](proxspray-analysis.md)** - Pattern analysis from ProxSpray project, role design corrections, integration lessons

## Planning Documents

Implementation plans and strategy documents:

### Active Plans

- **[plans/2025-11-14-pr18-fixes.md](plans/2025-11-14-pr18-fixes.md)** - Bug fixes and improvements for PR #18

## Code Review Documents

Pull request reviews and after-action reports:

- **[reviews/pr-18-review.md](reviews/pr-18-review.md)** - Comprehensive review of PR #18
- **[pr21-aar.md](pr21-aar.md)** - After-action review for PR #21: debugging workflow improvements

## Skills Planning

Claude Code skills development and implementation:

- **[skills-planning.md](skills-planning.md)** - Planning document for Claude Code skills: proxmox-infrastructure,
  netbox-powerdns-integration, ansible-best-practices, python-uv-scripts

## Quick Reference Guide

### When to Read What

**Starting a new Ansible role?**

1. Read [ansible-philosophy.md](ansible-philosophy.md) for principles
2. Review [ansible-role-design.md](ansible-role-design.md) for structure
3. Check [ansible-migration-plan.md](ansible-migration-plan.md) for examples

**Configuring infrastructure?**

1. Consult [infrastructure.md](infrastructure.md) for specifications
2. Check [goals.md](goals.md) for gotchas

**Setting up NetBox and DNS?**

1. Read [netbox-powerdns.md](netbox-powerdns.md) for architecture
2. Review [references.md](references.md) for external documentation

**Debugging a role or playbook?**

1. Review [testing-validation-results.md](testing-validation-results.md) for test patterns
2. Check [ansible-migration-completion.md](ansible-migration-completion.md) for bug fixes

**Looking for tool documentation?**

1. Check [references.md](references.md) for links to Proxmox, CEPH, Ansible, OpenTofu, NetBox, PowerDNS

**Evaluating design decisions?**

1. Read [proxspray-analysis.md](proxspray-analysis.md) for pattern analysis
2. Review [ansible-philosophy.md](ansible-philosophy.md) for core principles

## Archive Directory

The `archive/` directory preserves historical research and planning documents that informed current designs:

- **archive/2025-10-23/** - Early research summaries, role validation studies, improvement plans

These documents provide historical context but are superseded by current documentation. Consult them only when researching design evolution.

## Documentation Standards

All documentation follows Strunk and White's *Elements of Style*:

- Active voice
- Positive form
- Concrete language
- Omit needless words

These principles ensure clarity and precision across all documents.

## Document Organization

### By Category

**Infrastructure**: infrastructure.md, goals.md
**Ansible Design**: ansible-philosophy.md, ansible-role-design.md, ansible-playbook-design.md
**Ansible Implementation**: ansible-migration-plan.md, ansible-migration-completion.md
**Integration**: netbox-powerdns.md
**Testing**: testing-validation-results.md
**Analysis**: proxspray-analysis.md
**Planning**: plans/
**Reviews**: reviews/, pr21-aar.md
**Skills**: skills-planning.md
**References**: references.md

### By Status

**Foundational** (read first): goals.md, infrastructure.md, ansible-philosophy.md
**Active Reference**: infrastructure.md, ansible-role-design.md, ansible-playbook-design.md, references.md
**Implementation Guides**: ansible-migration-plan.md, netbox-powerdns.md
**Results and Validation**: ansible-migration-completion.md, testing-validation-results.md
**Historical**: archive/

## Contributing

When creating new documentation:

1. Place core design documents in `docs/`
2. Place implementation plans in `docs/plans/`
3. Place code reviews in `docs/reviews/`
4. Follow Elements of Style principles
5. Update this README to include the new document

## Questions?

- Check [references.md](references.md) for links to external documentation
- Review [ansible-philosophy.md](ansible-philosophy.md) for design principles
- Consult [infrastructure.md](infrastructure.md) for specifications
