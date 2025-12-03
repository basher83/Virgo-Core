---
title: Ansible Design Philosophy
description: Core design principles and decision-making guidance for Ansible automation in Virgo-Core
---

# Ansible Design Philosophy for Virgo-Core

**Version:** 1.0
**Last Updated:** 2025-10-20
**Status:** Team Standard

---

## Purpose

This document defines the core design philosophy and principles for Ansible automation in the Virgo-Core project.
All Ansible code should adhere to these principles to ensure maintainability, reusability, and consistency across
multiple Proxmox clusters.

> **Battle-Tested:** This architecture proved itself during v1.0.0 development. Comprehensive testing discovered
> and fixed 15 bugs, achieving perfect idempotency across the 3-node Matrix cluster. The 6-phase migration approach
> completed successfully with zero regressions.

> For detailed implementation patterns, anti-patterns, and review checklists, see [Ansible Design Patterns](./ansible-design-patterns.md).

---

## Core Principle: Roles = Infrastructure Components, Playbooks = Workflows

### The Fundamental Separation

**Roles answer the question**: "What infrastructure component does this manage?"

**Playbooks answer the question**: "What task am I trying to accomplish?"

This separation ensures:

- **Roles are reusable** across different workflows and clusters

- **Playbooks are task-oriented** and compose roles to accomplish goals

- **Configuration is declarative** and separated from implementation

- **Testing is focused** (test roles independently, test playbooks for integration)

### Examples

✅ **Correct Role Design**:

```yaml

# roles/proxmox_access/

# Manages: Proxmox API users, groups, tokens, ACLs

# Reusable for: Any need to create Proxmox API access

```

✅ **Correct Playbook Design**:

```yaml

# playbooks/setup-terraform-automation.yml

# Task: Setup Terraform automation access

# Uses: system_user + proxmox_access roles

```

❌ **Incorrect Role Design**:

```yaml

# roles/proxmox_terraform/

# Problem: Task-oriented naming (create terraform user)

# Problem: Conflates Linux users + Proxmox access

# Problem: Not reusable for other automation users

```

---

## What Is an Ansible Role?

### Definition

An Ansible role represents:

- ✅ **An infrastructure component** (network, storage, cluster)

- ✅ **A technology or service** (CEPH, Docker, DHCP)

- ✅ **A system aspect** (users, firewall, repositories)

- ✅ **Desired state of infrastructure** (how it should be configured)

An Ansible role should **NEVER** represent:

- ❌ **A task or workflow** ("create terraform user", "setup cluster")

- ❌ **A one-off operation** ("initialize", "migrate", "upgrade")

- ❌ **An end goal** ("prepare for X", "enable Y feature")

- ❌ **Multiple unrelated concerns** (network + storage in one role)

### Role Characteristics

A well-designed role should be:

1. **Component-Focused**
   - Manages one infrastructure component or service
   - Clear boundaries with other roles
   - Single responsibility principle

2. **Declarative**
   - Takes configuration as input (desired state)
   - Ensures system matches desired state
   - Idempotent (safe to run multiple times)

3. **Reusable**
   - Works across all Proxmox clusters (Matrix, Doggos, Nexus)
   - No cluster-specific logic inside the role
   - Cluster config externalized to `group_vars/`

4. **Composable**
   - Can be combined with other roles in playbooks
   - Clear dependencies and ordering
   - Minimal coupling between roles

5. **Testable**
   - Can be tested independently
   - Has clear inputs and expected outputs
   - Supports check mode (dry-run)

### Role Evolution and Versioning

As infrastructure requirements change, roles will need to evolve. Follow these guidelines:

**When to Extend a Role:**

- Adding new configuration options to the existing component

- Supporting new versions of the managed software

- Enhancing functionality within the role's scope

Example: `system_user` role adding SSH key management is acceptable - it's still managing user accounts.

**When to Split a Role:**

- Adding functionality for a different infrastructure component

- Introducing dependencies on external services that change the role's purpose

- Mixing multiple concerns that could be independently managed

Example: If `system_user` needs LDAP/AD integration, create a separate `ldap_integration` role:

```yaml

# DON'T: Extend system_user with LDAP logic

roles/system_user/
  tasks/
    - local_users.yml
    - ldap_users.yml      # ❌ Different auth mechanism, different component

# DO: Create focused roles that can be composed

roles/system_user/        # Manages local PAM users

roles/ldap_integration/   # Manages LDAP/AD integration

roles/ldap_user_sync/     # Syncs LDAP users to local system

# Playbook orchestrates both:

- hosts: all
  roles:
    - ldap_integration
    - ldap_user_sync

```

**Versioning Strategy:**

- Major changes: Document in role README's "Breaking Changes" section

- Keep roles backward-compatible when possible

- Use role variables with sensible defaults for new features

- Consider tagging major role versions in git if needed

---

## What Is an Ansible Playbook?

### Definition

An Ansible playbook represents:

- ✅ **A workflow or procedure** (initialize cluster, deploy application)

- ✅ **A task to accomplish** (setup automation, configure network)

- ✅ **An operational action** (add node, update packages, backup config)

- ✅ **Orchestration of roles** (which roles to run, in what order)

### Playbook Characteristics

A well-designed playbook should:

1. **Be Task-Oriented**
   - Named after the task it accomplishes
   - Clear purpose and scope
   - Documented pre-requisites and post-conditions

2. **Orchestrate Roles**
   - Combines multiple roles to achieve a goal
   - Defines role execution order
   - Passes configuration to roles

3. **Be Targeted**
   - Runs against specific inventory groups
   - Can be limited to specific clusters/hosts
   - Supports tags for partial execution

4. **Be Documented**
   - Clear description at the top
   - Usage examples
   - Expected outcomes

---

## Role vs Playbook Decision Tree

Use this decision tree when deciding whether to create a role or playbook:

```text
Question: What am I trying to do?

├─ Manage an infrastructure component?
│  └─ YES → Create a ROLE
│     Examples: CEPH storage, network bridges, user accounts
│
└─ Accomplish a specific task?
   └─ YES → Create a PLAYBOOK (that uses existing roles)
      Examples: Initialize cluster, setup automation, deploy app

Question: Is this reusable across multiple workflows?

├─ YES → Create a ROLE
│  Example: User management needed for terraform, ansible, manual access
│
└─ NO → Create a PLAYBOOK or put in existing role
   Example: One-time cluster migration

Question: Does this manage a single infrastructure aspect?

├─ YES → Create a ROLE
│  Example: Proxmox network bridges
│
└─ NO → Create a PLAYBOOK that orchestrates multiple roles
   Example: Complete cluster setup (network + cluster + storage)

```

### Decision Tree Clarifications

**What counts as "related concerns within the same component"?**

✅ **Related concerns (keep together in one role)**:

- `proxmox_access`: Users, groups, tokens, AND ACLs - all related to Proxmox API access control

- `proxmox_network`: Bridges, VLANs, routes - all network infrastructure

- `system_user`: User accounts, SSH keys, sudoers - all local user management

❌ **Unrelated concerns (split into separate roles)**:

- Mixing Linux PAM users + Proxmox API users - different authentication systems

- Combining network configuration + package management - different components

- Bundling CEPH storage + Proxmox cluster - independent services

**Key principle**: If two concerns share the same infrastructure component AND are always configured together, they can
live in one role. If they serve different purposes or could be used independently, split them.

**Example: `proxmox_access` role judgment**

Question: Why does `proxmox_access` bundle users, groups, tokens, and ACLs?

Answer: They're all part of the **Proxmox API access control** component:

- Users need groups for organization

- Groups need roles for permissions

- Roles need ACLs to grant access

- Tokens provide non-interactive auth

They form a cohesive access control system. Splitting them would make the role less useful.

---

## References

- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)

- [Ansible Role Design](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)

- [Virgo-Core Ansible Design Patterns](./ansible-design-patterns.md)

- [Virgo-Core Ansible Role Design](./ansible-role-design.md)

- [Virgo-Core Ansible Playbook Design](./ansible-playbook-design.md)

---

**This document is the authoritative source for Ansible design philosophy in Virgo-Core. For implementation patterns and anti-patterns, see [Ansible Design Patterns](./ansible-design-patterns.md).**
