# Ansible Design Philosophy for Virgo-Core

**Version:** 1.0
**Last Updated:** 2025-10-20
**Status:** Team Standard

---

## Purpose

This document defines the core design philosophy and principles for Ansible automation in the Virgo-Core project. All Ansible code should adhere to these principles to ensure maintainability, reusability, and consistency across multiple Proxmox clusters.

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

## Design Principles for Virgo-Core Roles

### 1. Component-Based Naming

Role names should describe the **component** they manage, not the **task** they perform.

✅ **Good Role Names**:
- `proxmox_access` - Manages Proxmox API access control
- `proxmox_network` - Manages Proxmox network infrastructure
- `system_user` - Manages Linux PAM user accounts
- `proxmox_ceph` - Manages CEPH storage infrastructure

❌ **Bad Role Names**:
- `create_terraform_user` - Action-oriented (create)
- `proxmox_terraform` - Task-oriented (for terraform)
- `setup_cluster` - Workflow-oriented (setup)
- `enable_vlan` - Action-oriented (enable)

### 2. Single Responsibility

Each role manages **one and only one** infrastructure component.

✅ **Good Separation**:
```yaml
# roles/system_user/
# Responsibility: Linux PAM users, SSH keys, sudo configuration
# Scope: /etc/passwd, /home/*, /etc/sudoers.d/

# roles/proxmox_access/
# Responsibility: Proxmox API users, groups, tokens, ACLs
# Scope: pveum commands, Proxmox API, /etc/pve/
```

❌ **Bad Conflation**:
```yaml
# roles/user_management/
# Problem: Mixes Linux users AND Proxmox users
# Problem: Unclear which aspect to modify
# Problem: Hard to test independently
```

### 3. No Cluster-Specific Logic

Roles should work for **any cluster** by accepting configuration as variables.

✅ **Good Approach** (cluster-agnostic):
```yaml
# roles/proxmox_network/tasks/main.yml
- name: Configure network bridges
  template:
    src: interfaces.j2
    dest: /etc/network/interfaces
  vars:
    bridges: "{{ proxmox_bridges }}"

# Cluster-specific config in group_vars/matrix_cluster.yml
proxmox_bridges:
  - name: vmbr0
    interface: enp4s0
    address: "192.168.3.{{ node_id }}/24"
```

❌ **Bad Approach** (cluster-specific):
```yaml
# roles/proxmox_network/tasks/main.yml
- name: Configure Matrix cluster network
  template:
    src: matrix-interfaces.j2  # ❌ Hardcoded for Matrix
  when: cluster_name == "Matrix"  # ❌ Cluster check in role
```

### 4. Declarative Configuration Model

Roles should accept **desired state** as configuration and ensure the system matches it.

✅ **Good Declarative Model**:
```yaml
# Input: Desired state
system_users:
  - name: terraform
    state: present
    shell: /bin/bash
    ssh_keys:
      - "ssh-rsa AAAAB3..."
    sudo_rules:
      - /sbin/pvesm
      - /sbin/qm
  - name: olduser
    state: absent

# Role ensures:
# - terraform user exists with correct config
# - olduser is removed
# - Idempotent (safe to run multiple times)
```

❌ **Bad Imperative Model**:
```yaml
# Tasks that assume state
- name: Create terraform user  # ❌ What if it exists?
  user:
    name: terraform
    create_home: yes

- name: Add SSH key  # ❌ What if key changed?
  lineinfile:
    line: "ssh-rsa AAAAB3..."
```

### 5. Secrets via Infisical

All secrets must be retrieved from Infisical, never hardcoded.

✅ **Good Secrets Management**:
```yaml
# roles/proxmox_access/tasks/secrets.yml
- name: Retrieve Proxmox root password
  include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'
    infisical_project_id: "{{ infisical_project_id }}"
    infisical_env: "{{ infisical_env }}"
```

❌ **Bad Secrets Management**:
```yaml
# roles/proxmox_access/defaults/main.yml
proxmox_password: "changeme123"  # ❌ NEVER
terraform_user_password: "terraform123!"  # ❌ NEVER
```

### 6. Native Modules First

Prefer Ansible native modules over shell commands for better idempotency and error handling.

✅ **Good Module Usage**:
```yaml
# Use community.proxmox module
- name: Create Proxmox group
  community.proxmox.proxmox_group:
    name: "{{ item.name }}"
    state: present
    comment: "{{ item.comment }}"
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_password: "{{ proxmox_api_password }}"
```

❌ **Bad Shell Usage**:
```yaml
# Shell command when module exists
- name: Create Proxmox group
  shell: |
    pveum group add {{ item.name }} -comment "{{ item.comment }}"
  # ❌ No idempotency check
  # ❌ No error handling
  # ❌ Shell parsing issues
```

**When Shell Is Acceptable**:
- No native module exists (e.g., `pvecm`, `pveceph`)
- Complex operations requiring pipelines
- Temporary until modules are available

**Shell Best Practices**:
```yaml
- name: Create CEPH OSD
  shell: |
    pveceph osd create {{ device }}
  args:
    creates: "/var/lib/ceph/osd/ceph-{{ osd_id }}"  # ✅ Idempotency
  register: osd_create
  changed_when: "'successfully created' in osd_create.stdout"  # ✅ Change detection
  failed_when:
    - osd_create.rc != 0
    - "'already exists' not in osd_create.stderr"  # ✅ Error handling
```

**Advanced Shell Patterns** (beyond `creates:`):

The `args.creates` pattern only checks file existence, not file contents or state. For more robust idempotency:

**Pattern 1: Output-Based Change Detection**
```yaml
- name: Create resource with output detection
  shell: |
    create_resource.sh resource-name
  register: result
  changed_when: "'successfully created' in result.stdout"
  failed_when:
    - result.rc != 0
    - "'already exists' not in result.stderr"
```

Advantages over `creates:`:
- Detects actual changes, not just file presence
- Handles cases where file exists but resource wasn't created
- Provides accurate change reporting for Ansible

**Pattern 2: State Verification Before Action**
```yaml
- name: Check resource state
  command: check_resource.sh resource-name
  register: state
  changed_when: false
  failed_when: false

- name: Create resource only if missing
  shell: create_resource.sh resource-name
  when: state.rc != 0 or 'missing' in state.stdout
  register: create_result
  changed_when: create_result.rc == 0
```

Advantages:
- Explicitly checks current state
- Clearer intent (check, then act)
- Better for complex state verification (not just file existence)

**Pattern 3: Stateful Commands with JSON Output**
```yaml
- name: Ensure pool configuration
  shell: |
    ceph osd pool get {{ pool_name }} size -f json
  register: current_config
  changed_when: false

- name: Update pool if needed
  command: ceph osd pool set {{ pool_name }} size {{ desired_size }}
  when: (current_config.stdout | from_json).size != desired_size
```

Advantages:
- Handles configuration drift detection
- Works for resources that always exist but may need updates
- `creates:` can't handle this scenario

### 7. Idempotency

Roles must be safe to run multiple times without causing errors or unwanted changes.

✅ **Good Idempotency**:
```yaml
- name: Ensure VLAN interface exists
  shell: |
    if ! ip link show vmbr0.{{ vlan_id }} >/dev/null 2>&1; then
      ip link add link vmbr0 name vmbr0.{{ vlan_id }} type vlan id {{ vlan_id }}
      echo "created"
    else
      echo "exists"
    fi
  register: vlan_create
  changed_when: "'created' in vlan_create.stdout"
```

❌ **Bad Idempotency**:
```yaml
- name: Create VLAN interface
  shell: ip link add link vmbr0 name vmbr0.{{ vlan_id }} type vlan id {{ vlan_id }}
  # ❌ Fails if already exists
  # ❌ Always reports changed
```

---

## Anti-Patterns to Avoid

### 1. Task-Oriented Role Names

❌ **Anti-Pattern**: `proxmox_terraform`, `create_users`, `setup_cluster`

**Problem**: Role names describe a task, not a component.

**Solution**: Name roles after the component they manage:
- `proxmox_terraform` → `proxmox_access` + `system_user`
- `create_users` → `system_user`
- `setup_cluster` → `proxmox_cluster`

### 2. Conflating Multiple Concerns

❌ **Anti-Pattern**: Role manages both Linux users AND Proxmox users

**Problem**: Unclear responsibilities, hard to test, not reusable.

**Example**:
```yaml
# roles/user_management/tasks/main.yml
- name: Create Linux user
  user:
    name: terraform

- name: Create Proxmox user
  command: pveum user add terraform@pam
```

**Solution**: Separate into distinct roles:
```yaml
# roles/system_user/ - Manages Linux users only
# roles/proxmox_access/ - Manages Proxmox users only
```

### 3. Cluster-Specific Roles

❌ **Anti-Pattern**: `matrix_networking`, `doggos_setup`

**Problem**: Not reusable across clusters, duplicates code.

**Solution**: Generic roles + cluster-specific configuration:
```yaml
# roles/proxmox_network/ - Generic network role
# group_vars/matrix_cluster.yml - Matrix-specific config
# group_vars/doggos_cluster.yml - Doggos-specific config
```

### 4. Hardcoded Secrets

❌ **Anti-Pattern**: Passwords in `defaults/main.yml` or `vars/main.yml`

**Problem**: Security risk, audit trail issues, hard to rotate.

**Solution**: Always use Infisical for secrets.

### 5. Excessive Use of `failed_when: false`

❌ **Anti-Pattern**: Silencing all errors

**Problem**: Hides real failures, creates inconsistent state.

**Solution**: Explicit error handling:
```yaml
failed_when:
  - result.rc != 0
  - "'already exists' not in result.stderr"
```

### 6. No Error Handling

❌ **Anti-Pattern**: Commands without `register` and `failed_when`

**Problem**: Silent failures, unclear error messages.

**Solution**: Always register results and handle errors:
```yaml
- name: Join cluster
  shell: pvecm add {{ primary_node }}
  register: cluster_join
  failed_when:
    - cluster_join.rc != 0
    - "'already in a cluster' not in cluster_join.stderr"
```

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

**Key principle**: If two concerns share the same infrastructure component AND are always configured together, they can live in one role. If they serve different purposes or could be used independently, split them.

**Example: `proxmox_access` role judgment**

Question: Why does `proxmox_access` bundle users, groups, tokens, and ACLs?

Answer: They're all part of the **Proxmox API access control** component:
- Users need groups for organization
- Groups need roles for permissions
- Roles need ACLs to grant access
- Tokens provide non-interactive auth

They form a cohesive access control system. Splitting them would make the role less useful.

---

## Examples: Good vs Bad Design

### Example 1: Terraform User Setup

❌ **Bad Design** (Task-oriented role):
```yaml
# roles/proxmox_terraform/
# Problem: Conflates multiple concerns
# Problem: Not reusable for other automation users
```

✅ **Good Design** (Component-based roles):
```yaml
# roles/system_user/ - Manages Linux PAM users
# roles/proxmox_access/ - Manages Proxmox API access
# playbooks/setup-terraform-automation.yml - Orchestrates both
```

### Example 2: Network Configuration

❌ **Bad Design** (Action-oriented):
```yaml
# roles/enable_vlan_bridging/
# Problem: Named after action, not component
# Problem: Too specific, not reusable
```

✅ **Good Design** (Component-based):
```yaml
# roles/proxmox_network/
# Manages: ALL network infrastructure (bridges, VLANs, interfaces)
# Reusable for: Any network configuration need
```

### Example 3: Cluster Initialization

❌ **Bad Design** (Workflow as role):
```yaml
# roles/initialize_cluster/
# Problem: Workflow, not a component
# Problem: Runs once, not reusable
```

✅ **Good Design** (Role + Playbook):
```yaml
# roles/proxmox_cluster/ - Manages cluster state
# playbooks/initialize-matrix-cluster.yml - Orchestrates setup
```

---

## Review Checklist

Before creating or modifying a role, ask:

- [ ] Is the role named after an infrastructure component (not a task)?
- [ ] Does the role have a single, clear responsibility?
- [ ] Is the role reusable across all clusters?
- [ ] Does the role use declarative configuration?
- [ ] Are all secrets retrieved from Infisical?
- [ ] Does the role prefer native modules over shell?
- [ ] Is the role idempotent (safe to run multiple times)?
- [ ] Does the role have proper error handling?
- [ ] Can the role be tested independently?
- [ ] Is cluster-specific config externalized to `group_vars/`?

---

## References

- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)
- [Ansible Role Design](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)
- [Virgo-Core Ansible Role Design](./ansible-role-design.md)
- [Virgo-Core Ansible Playbook Design](./ansible-playbook-design.md)
- [Virgo-Core Ansible Migration Plan](./ansible-migration-plan.md)

---

**This document is the authoritative source for Ansible design philosophy in Virgo-Core. All Ansible code should adhere to these principles.**
