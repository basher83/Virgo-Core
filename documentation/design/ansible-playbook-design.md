---
title: Ansible Playbook Design
description: Patterns and best practices for creating task-oriented Ansible playbooks that orchestrate roles in Virgo-Core
---

# Ansible Playbook Design for Virgo-Core

**Version:** 1.0
**Last Updated:** 2025-10-20
**Status:** Team Standard

---

## Purpose

This document defines patterns and best practices for creating Ansible playbooks in Virgo-Core. Playbooks orchestrate roles to accomplish specific tasks and workflows.

**Related Documents**:

- [Ansible Philosophy](./ansible-philosophy.md) - Core design principles

- [Ansible Role Design](./ansible-role-design.md) - Role structure and implementation

- [Ansible Migration Plan](./ansible-migration-plan.md) - Migration implementation

---

## Playbook Philosophy

**Playbooks are task-oriented orchestration**:

- Named after the **task** they accomplish (not the component they manage)

- Combine multiple roles to achieve a goal

- Define execution order and dependencies

- Accept parameters for flexibility

- Document prerequisites and expected outcomes

**Playbooks answer**: "What am I trying to accomplish?"

**Roles answer**: "What component am I managing?"

---

## Playbook Categories

Virgo-Core playbooks are organized into three categories:

### 1. Setup/Initialization Playbooks

**Purpose**: Initial deployment and configuration (run once or rarely)

**Characteristics**:

- Creates infrastructure from scratch

- Can be destructive (cluster initialization)

- Requires careful planning and review

- Usually runs on all nodes simultaneously

**Examples**:

- `initialize-matrix-cluster.yml` - Complete Matrix cluster setup

- `deploy-ceph-storage.yml` - Initial CEPH deployment

- `setup-terraform-automation.yml` - Configure Terraform access

### 2. Configuration Management Playbooks

**Purpose**: Ongoing configuration and updates (run repeatedly)

**Characteristics**:

- Idempotent (safe to run multiple times)

- Updates existing configuration

- Can run on production clusters

- Maintains desired state

**Examples**:

- `configure-network.yml` - Update network configuration

- `manage-users.yml` - Add/remove user accounts

- `update-proxmox.yml` - Update Proxmox packages

### 3. Operational Playbooks

**Purpose**: On-demand operational tasks

**Characteristics**:

- Specific operational action

- May affect running services

- Often targets specific hosts

- Requires coordination

**Examples**:

- `add-cluster-node.yml` - Add node to existing cluster

- `expand-ceph.yml` - Add OSDs to existing CEPH

- `create-vm-template.yml` - Build new VM template

---

## Playbook Structure

### Standard Playbook Template

```yaml
---

# Playbook: <Brief Name>

# Purpose: <Detailed description of what this accomplishes>

# Target: <Which clusters/hosts this runs on>

# Category: <Setup/Configuration/Operational>
#

# Prerequisites:

#   - <Prerequisite 1>

#   - <Prerequisite 2>
#

# Usage:

#   ansible-playbook -i inventory/proxmox.yml playbooks/playbook-name.yml \

#     --limit <cluster_name>
#

# Reference: <Link to related documentation>

- name: <Descriptive Play Name>
  hosts: "{{ target_cluster | default('all') }}"
  gather_facts: true
  become: true

  vars:
    # Playbook-specific variables

  pre_tasks:
    - name: Retrieve secrets from Infisical
      include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
      vars:
        secret_name: 'SECRET_NAME'
        secret_var_name: 'variable_name'

  roles:
    - role: role_name
      vars:
        role_variable: value

  post_tasks:
    - name: Verify completion
      debug:
        msg: "Playbook completed successfully"

  handlers:
    - name: Custom handler
      command: /some/command

```

### Playbook Header

Every playbook must have a comprehensive header:

```yaml
---

# Playbook: Setup Terraform Automation Access

# Purpose: Create Linux system user and Proxmox API access for Terraform

# Target: All Proxmox clusters (Matrix, Doggos, Nexus)

# Category: Setup
#

# This playbook performs the following:

#   1. Creates Linux PAM user 'terraform' with SSH key access

#   2. Configures sudo rules for Proxmox storage and VM commands

#   3. Creates Proxmox user terraform@pam with TerraformUser role

#   4. Generates API token for programmatic access

#   5. Exports environment file for Terraform provider
#

# Prerequisites:

#   - Proxmox VE 9.x installed on all nodes

#   - Root SSH access configured

#   - Infisical secrets configured (PROXMOX_USERNAME, PROXMOX_PASSWORD)

#   - SSH public key available at ../files/terraform.pub
#

# Usage:

#   # Run on all clusters

#   ansible-playbook -i inventory/proxmox.yml playbooks/setup-terraform-automation.yml
#

#   # Run on specific cluster

#   ansible-playbook -i inventory/proxmox.yml playbooks/setup-terraform-automation.yml \

#     --limit matrix_cluster
#

# Expected Outcome:

#   - Linux user 'terraform' created on all nodes

#   - Proxmox user terraform@pam created with API token

#   - Environment file exported to ~/tmp/.proxmox-terraform/
#

# Reference: docs/terraform/terraform-provider-setup.md

```

---

## Playbook Examples

### Example 1: Setup Terraform Automation

**File**: `playbooks/setup-terraform-automation.yml`

**Purpose**: Complete Terraform automation setup (Linux user + Proxmox API access)

```yaml
---

# Playbook: Setup Terraform Automation Access

# Purpose: Create Linux system user and Proxmox API access for Terraform

# [Full header as shown above]

- name: Setup Terraform Automation on Proxmox
  hosts: "{{ target_cluster | default('all') }}"
  gather_facts: true
  become: true

  vars:
    # Infisical configuration

    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/{{ cluster_name }}'

    # Cluster name detection

    cluster_name: "{{ group_names | select('search', '_cluster') | first | regex_replace('_cluster$', '') }}"

    # Terraform user SSH keys

    terraform_ssh_keys:
      - "{{ lookup('file', playbook_dir + '/../files/terraform.pub') }}"

  pre_tasks:
    - name: Retrieve Proxmox username from Infisical
      include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
      vars:
        secret_name: 'PROXMOX_USERNAME'
        secret_var_name: 'proxmox_username'

    - name: Retrieve Proxmox password from Infisical
      include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
      vars:
        secret_name: 'PROXMOX_PASSWORD'
        secret_var_name: 'proxmox_password'

  roles:
    # 1. Create Linux system user

    - role: system_user
      vars:
        system_users:
          - name: terraform
            state: present
            shell: /bin/bash
            comment: "Terraform automation user (PAM realm)"
            ssh_keys: "{{ terraform_ssh_keys }}"
            sudo_rules:
              - /sbin/pvesm
              - /sbin/qm
              - "/usr/bin/tee /var/lib/vz/*"
            sudo_nopasswd: true

    # 2. Create Proxmox API access

    - role: proxmox_access
      vars:
        proxmox_api_host: "{{ ansible_default_ipv4.address }}"
        proxmox_api_user: "{{ proxmox_username }}"
        proxmox_api_password: "{{ proxmox_password }}"

        proxmox_roles:
          - name: TerraformUser
            privileges:
              - Datastore.Allocate
              - Datastore.AllocateSpace
              - Datastore.AllocateTemplate
              - Pool.Allocate
              - Sys.Audit
              - Sys.Console
              - VM.Allocate
              - VM.Clone
              - VM.Config.CDROM
              - VM.Config.Cloudinit
              - VM.Config.CPU
              - VM.Config.Disk
              - VM.Config.Memory
              - VM.Config.Network
              - VM.Migrate
              - VM.Monitor
              - VM.PowerMgmt

        proxmox_groups:
          - name: terraform-users
            comment: "Automation users for Terraform"

        proxmox_users:
          - userid: terraform@pam
            groups: [terraform-users]
            comment: "Terraform automation user"

        proxmox_tokens:
          - userid: terraform@pam
            tokenid: automation
            privsep: false
            expire: 0

        proxmox_acls:
          - path: /
            type: group
            ugid: terraform-users
            roleid: TerraformUser
            propagate: true

        export_terraform_env: true

  post_tasks:
    - name: Display setup summary
      debug:
        msg: |
          ========================================
          Terraform Automation Setup Complete
          ========================================
          Cluster: {{ cluster_name }}
          Linux User: terraform
          Proxmox User: terraform@pam
          API Token: terraform@pam!automation

          Test SSH Access:
            ssh terraform@{{ ansible_host }} sudo pvesm status

          Terraform Environment:
            source ~/tmp/.proxmox-terraform/proxmox-{{ cluster_name }}

```

---

### Example 2: Initialize Matrix Cluster

**File**: `playbooks/initialize-matrix-cluster.yml`

**Purpose**: Complete Matrix cluster initialization (network, cluster, CEPH)

```yaml
---

# Playbook: Initialize Matrix Cluster

# Purpose: Complete initialization of the Matrix Proxmox cluster

# Target: matrix_cluster (foxtrot, golf, hotel)

# Category: Setup
#

# This playbook performs the following:

#   1. Configures Proxmox repositories (no-subscription)

#   2. Configures network bridges and VLAN interfaces

#   3. Initializes Proxmox cluster with corosync

#   4. Deploys CEPH storage (monitors, managers, 12 OSDs)

#   5. Creates CEPH pools for VM storage
#

# Prerequisites:

#   - Proxmox VE 9.x fresh installation on all 3 nodes

#   - Network connectivity between all nodes

#   - Root SSH access

#   - NVMe drives available for CEPH (nvme1n1, nvme2n1)
#

# WARNING: This is a destructive operation. Only run on new clusters.
#

# Usage:

#   ansible-playbook -i inventory/proxmox.yml playbooks/initialize-matrix-cluster.yml
#

# Reference: docs/clusters/matrix-cluster-setup.md

- name: Initialize Matrix Cluster Infrastructure
  hosts: matrix_cluster
  gather_facts: true
  become: true

  vars:
    # Verify target cluster

    expected_cluster: matrix_cluster

  pre_tasks:
    - name: Verify target cluster
      assert:
        that:
          - "'matrix_cluster' in group_names"
          - groups['matrix_cluster'] | length == 3
        fail_msg: "This playbook must be run on matrix_cluster with exactly 3 nodes"

    # Pre-flight health checks

    - name: Verify cluster node health
      command: systemctl is-active pve-cluster
      register: cluster_status
      failed_when: cluster_status.rc != 0
      changed_when: false
      loop: "{{ groups['matrix_cluster'] }}"
      delegate_to: "{{ item }}"
      loop_control:
        label: "{{ item }}"

    - name: Verify network connectivity to all nodes
      wait_for:
        host: "{{ hostvars[item].ansible_host }}"
        port: 22
        timeout: 5
      loop: "{{ groups['matrix_cluster'] }}"
      delegate_to: localhost
      loop_control:
        label: "{{ item }}"

    - name: Confirm destructive operation
      pause:
        prompt: |
          WARNING: This will initialize the Matrix cluster.

          This operation will:
            - Configure network interfaces (may disrupt connectivity)
            - Initialize Proxmox cluster
            - Create CEPH storage cluster

          Nodes: {{ groups['matrix_cluster'] | join(', ') }}

          Type 'yes' to continue
      register: confirmation
      when: not (skip_confirmation | default(false))

    - name: Verify confirmation
      assert:
        that: confirmation.user_input == 'yes'
        fail_msg: "Cluster initialization cancelled"
      when: not (skip_confirmation | default(false))

  roles:
    # Phase 1: Base Configuration

    - role: proxmox_repository
      tags: [repository, base]
      vars:
        proxmox_enterprise_repo: false
        proxmox_no_subscription_repo: true
        ceph_version: "squid"

    # Phase 2: Network Configuration

    - role: proxmox_network
      tags: [network]
      # Uses group_vars/matrix_cluster.yml for bridge configuration

    # Phase 3: Cluster Formation

    - role: proxmox_cluster
      tags: [cluster]
      # Uses group_vars/matrix_cluster.yml for cluster configuration

    # Phase 4: CEPH Deployment

    - role: proxmox_ceph
      tags: [ceph, storage]
      # Uses group_vars/matrix_cluster.yml for OSD and pool configuration

  post_tasks:
    - name: Verify cluster status
      command: pvecm status
      register: cluster_status
      changed_when: false

    - name: Verify CEPH health
      command: ceph health
      register: ceph_health
      changed_when: false
      when: inventory_hostname == groups['matrix_cluster'][0]

    - name: Display cluster summary
      debug:
        msg: |
          ========================================
          Matrix Cluster Initialization Complete
          ========================================
          Cluster Name: Matrix
          Nodes: {{ groups['matrix_cluster'] | join(', ') }}

          Cluster Status:
          {{ cluster_status.stdout }}

          {% if ceph_health is defined %}
          CEPH Health:
          {{ ceph_health.stdout }}
          {% endif %}

          Next Steps:
            1. Verify cluster quorum: pvecm status
            2. Check CEPH health: ceph -s
            3. Create VM templates
            4. Configure NetBox integration
      when: inventory_hostname == groups['matrix_cluster'][0]

```

---

### Example 3: Create Admin User

**File**: `playbooks/create-admin-user.yml**

**Purpose**: Add administrative user across clusters

```yaml
---

# Playbook: Create Admin User

# Purpose: Create administrative user with SSH and sudo access

# Target: Configurable (default: all)

# Category: Configuration
#

# Usage:

#   ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml \

#     -e "admin_name=jdoe" \

#     -e "admin_ssh_key='ssh-rsa AAAAB3...'"

- name: Create Administrative User
  hosts: "{{ target_cluster | default('all') }}"
  gather_facts: true
  become: true

  vars:
    # Required extra vars

    admin_name: "{{ admin_name | mandatory }}"
    admin_ssh_key: "{{ admin_ssh_key | mandatory }}"

    # Optional extra vars

    admin_shell: "{{ admin_shell | default('/bin/bash') }}"
    admin_groups: "{{ admin_groups | default(['sudo']) }}"

  roles:
    - role: system_user
      vars:
        system_users:
          - name: "{{ admin_name }}"
            state: present
            shell: "{{ admin_shell }}"
            groups: "{{ admin_groups }}"
            ssh_keys:
              - "{{ admin_ssh_key }}"
            sudo_nopasswd: true

  post_tasks:
    - name: Display user creation summary
      debug:
        msg: |
          User '{{ admin_name }}' created successfully on {{ inventory_hostname }}

          Test SSH access:
            ssh {{ admin_name }}@{{ ansible_host }}

```

---

### Example 4: Update Network Configuration

**File**: `playbooks/configure-network.yml`

**Purpose**: Update network configuration (idempotent)

```yaml
---

# Playbook: Configure Network

# Purpose: Update Proxmox network configuration

# Target: Configurable (default: all)

# Category: Configuration
#

# This playbook is idempotent and safe to run on production clusters.
#

# Usage:

#   ansible-playbook -i inventory/proxmox.yml playbooks/configure-network.yml \

#     --limit matrix_cluster \

#     --check --diff  # Dry run first

- name: Configure Proxmox Network
  hosts: "{{ target_cluster | default('all') }}"
  gather_facts: true
  become: true

  vars:
    # Network reload requires confirmation

    reload_network: "{{ reload_network | default(false) }}"

  roles:
    - role: proxmox_network
      # Uses group_vars/<cluster_name>.yml for configuration

  post_tasks:
    - name: Confirm network reload
      pause:
        prompt: |
          Network configuration updated.

          WARNING: Reloading network may disrupt connectivity.

          Review changes above before proceeding.
          Type 'yes' to reload network
      register: reload_confirmation
      when:
        - reload_network | bool
        - not (skip_confirmation | default(false))

    - name: Reload network interfaces
      command: ifreload -a
      when:
        - reload_network | bool
        - reload_confirmation.user_input == 'yes' or (skip_confirmation | default(false))
      register: network_reload

    - name: Verify network connectivity
      wait_for_connection:
        timeout: 30
      when: network_reload is changed

```

---

## Playbook Best Practices

### 1. Use Descriptive Names

✅ **Good**:

- `setup-terraform-automation.yml`

- `initialize-matrix-cluster.yml`

- `deploy-ceph-storage.yml`

❌ **Bad**:

- `setup.yml` (too vague)

- `terraform.yml` (not descriptive enough)

- `cluster.yml` (what about the cluster?)

### 2. Document Prerequisites

Always document what must be in place before running:

```yaml

# Prerequisites:

#   - Proxmox VE 9.x installed

#   - Root SSH access configured

#   - Infisical secrets available

#   - Network connectivity verified

```

### 3. Provide Usage Examples

Include complete usage examples with common scenarios:

```yaml

# Usage:

#   # Default (all clusters)

#   ansible-playbook -i inventory/proxmox.yml playbooks/playbook.yml
#

#   # Specific cluster

#   ansible-playbook -i inventory/proxmox.yml playbooks/playbook.yml \

#     --limit matrix_cluster
#

#   # Dry run

#   ansible-playbook -i inventory/proxmox.yml playbooks/playbook.yml \

#     --check --diff
#

#   # With extra variables

#   ansible-playbook -i inventory/proxmox.yml playbooks/playbook.yml \

#     -e "admin_name=jdoe" -e "admin_email=jdoe@example.com"

```

### 4. Use Tags for Granular Execution

Assign tags to roles for selective execution:

```yaml
roles:
  - role: proxmox_repository
    tags: [repository, base]

  - role: proxmox_network
    tags: [network]

  - role: proxmox_cluster
    tags: [cluster]

  - role: proxmox_ceph
    tags: [ceph, storage]

# Usage:

# Run only network configuration

# ansible-playbook playbook.yml --tags network

# Skip storage setup

# ansible-playbook playbook.yml --skip-tags storage

```

### 5. Add Safety Checks

For destructive operations, add confirmation prompts:

```yaml
pre_tasks:
  - name: Confirm destructive operation
    pause:
      prompt: |
        WARNING: This will reinitialize the cluster.
        All VMs will be stopped.

        Type 'yes' to continue
    register: confirmation
    when: not (skip_confirmation | default(false))

  - name: Verify confirmation
    assert:
      that: confirmation.user_input == 'yes'
      fail_msg: "Operation cancelled"
    when: not (skip_confirmation | default(false))

```

### 6. Use Variable Precedence Correctly

Understand variable precedence:

```yaml

# Lowest precedence: role defaults

# roles/role_name/defaults/main.yml

# Medium: group_vars

# group_vars/matrix_cluster.yml

# High: playbook vars

vars:
  variable: value

# Highest: extra vars (-e)

# ansible-playbook -e "variable=value"

```

#### Common Variable Precedence Pitfalls

Be aware of these common gotchas that can cause unexpected behavior:

**Gotcha 1: group_vars/all.yml overriding role defaults**

```yaml

# roles/my_role/defaults/main.yml

service_port: 8080  # Role default

# group_vars/all.yml

service_port: 9000  # This OVERRIDES role default for ALL hosts!

```

**Problem**: `group_vars` has higher precedence than role `defaults`, so the role default is ignored.

**Solution**: Use role defaults for sensible defaults, use `group_vars` only for environment-specific overrides.

**Gotcha 2: Extra vars (-e) bypassing safety checks**

```bash

# Playbook has safety checks

ansible-playbook deploy.yml --limit production

# But extra vars can override EVERYTHING, even safety checks

ansible-playbook deploy.yml --limit production -e "skip_safety_checks=true"

```

**Problem**: Extra vars have highest precedence and can bypass critical safety validations.

**Solution**: Never use `-e` in automation/CI/CD for critical variables. Use inventory or group_vars instead.

**Gotcha 3: Playbook vars unexpectedly overriding role configuration**

```yaml

# playbook.yml

- hosts: all
  vars:
    http_port: 8080  # Playbook var

  roles:
    - role: webserver
      # This role's http_port default is IGNORED because playbook vars have higher precedence

```

**Problem**: Playbook `vars:` have higher precedence than role `defaults/`, making role configuration inflexible.

**Solution**: Use `defaults/` for role defaults, `vars/` for constants only. Let users override via `group_vars` or role parameters.

### 7. Validate Configuration

Add pre-flight checks:

```yaml
pre_tasks:
  - name: Verify required variables
    assert:
      that:
        - cluster_name is defined
        - groups[cluster_name] | length >= 3
      fail_msg: "cluster_name must be defined with at least 3 nodes"

  - name: Check Proxmox version
    command: pveversion
    register: pve_version
    changed_when: false
    failed_when: "'pve-manager/9' not in pve_version.stdout"

```

### 8. Provide Post-Task Summaries

Display clear completion messages:

```yaml
post_tasks:
  - name: Display completion summary
    debug:
      msg: |
        ========================================
        Playbook Completed Successfully
        ========================================
        Cluster: {{ cluster_name }}
        Nodes: {{ groups[cluster_name] | join(', ') }}

        Next Steps:
          1. Verify cluster: pvecm status
          2. Check CEPH: ceph -s
          3. Review logs: journalctl -u pve-cluster

```

---

## Playbook Organization

### Directory Structure

```text
ansible/
├── playbooks/
│   ├── setup-terraform-automation.yml
│   ├── initialize-matrix-cluster.yml
│   ├── deploy-ceph-storage.yml
│   ├── configure-network.yml
│   ├── create-admin-user.yml
│   ├── update-proxmox.yml
│   └── create-vm-template.yml
├── roles/
│   └── [role directories]
├── inventory/
│   └── proxmox.yml
├── group_vars/
│   ├── all.yml
│   ├── matrix_cluster.yml
│   ├── doggos_cluster.yml
│   └── nexus_cluster.yml
├── tasks/
│   └── infisical-secret-lookup.yml
└── templates/
    └── sudoers.j2

```

### Naming Conventions

**Playbooks**: `action-component.yml`

- `setup-terraform-automation.yml`

- `initialize-matrix-cluster.yml`

- `deploy-ceph-storage.yml`

**Roles**: `component_name`

- `proxmox_network`

- `system_user`

- `proxmox_ceph`

---

## When to Create a New Playbook

Create a new playbook when:

1. **New Workflow**: Accomplishing a distinct task not covered by existing playbooks

2. **Different Target**: Same roles but different host selection or ordering

3. **Specific Combination**: Unique combination of roles for a specific purpose

4. **Operational Task**: One-off operational procedure (backup, migration, etc.)

**Don't create a new playbook when**:

1. **Minor Variation**: Use extra vars or tags instead

2. **Different Configuration**: Use group_vars or host_vars

3. **Testing**: Use limits and check mode on existing playbooks

---

## Playbook Testing Strategy

### 1. Syntax Check

Always run syntax check first:

```bash
ansible-playbook --syntax-check playbooks/playbook-name.yml

```

### 2. Check Mode (Dry Run)

Run in check mode to see what would change:

```bash
ansible-playbook -i inventory/proxmox.yml playbooks/playbook-name.yml \
  --check --diff

```

### 3. Limited Execution

Test on a single host first:

```bash
ansible-playbook -i inventory/proxmox.yml playbooks/playbook-name.yml \
  --limit foxtrot

```

### 4. Tag-Based Testing

Test individual phases:

```bash
ansible-playbook -i inventory/proxmox.yml playbooks/playbook-name.yml \
  --tags network --check

```

---

## Mise Task Integration

Create mise tasks for common playbook operations:

```toml

# .mise.toml

[tasks."ansible:setup-terraform"]
description = "Setup Terraform automation on specified cluster"
run = """
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml \
  playbooks/setup-terraform-automation.yml \
  --limit ${CLUSTER:-matrix_cluster}
"""

[tasks."ansible:init-matrix"]
description = "Initialize Matrix cluster (WARNING: Destructive)"
run = """
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml \
  playbooks/initialize-matrix-cluster.yml
"""

[tasks."ansible:test"]
description = "Test playbook with check mode"
run = """
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml \
  playbooks/${PLAYBOOK} \
  --check --diff ${LIMIT:+--limit $LIMIT}
"""

```

**Usage**:

```bash

# Setup terraform on matrix cluster

mise run ansible:setup-terraform

# Test network configuration

PLAYBOOK=configure-network.yml LIMIT=matrix_cluster mise run ansible:test

# Initialize matrix cluster

mise run ansible:init-matrix

```

---

## Common Playbook Patterns

### Pattern 1: Multi-Phase Deployment

```yaml
roles:
  # Phase 1: Prerequisites

  - role: proxmox_repository
    tags: [phase1, repository]

  # Phase 2: Infrastructure

  - role: proxmox_network
    tags: [phase2, network]

  # Phase 3: Services

  - role: proxmox_cluster
    tags: [phase3, cluster]

  # Phase 4: Storage

  - role: proxmox_ceph
    tags: [phase4, storage]

# Run specific phase:

# ansible-playbook playbook.yml --tags phase2

```

### Pattern 2: Conditional Role Execution

```yaml
roles:
  - role: proxmox_network
    when: configure_network | default(true)

  - role: proxmox_ceph
    when: enable_ceph | default(true)

```

### Pattern 3: Dynamic Targets

```yaml

- name: Configure Infrastructure
  hosts: "{{ target_cluster | default('all') }}"

  # Usage: -e "target_cluster=matrix_cluster"

```

### Pattern 4: Variable Validation

```yaml
vars:
  required_vars:
    - cluster_name
    - admin_email

pre_tasks:
  - name: Validate required variables
    assert:
      that: "{{ item }} is defined"
      fail_msg: "Required variable '{{ item }}' is not defined"
    loop: "{{ required_vars }}"

```

---

## References

- [Ansible Philosophy](./ansible-philosophy.md)

- [Ansible Design Patterns](./ansible-design-patterns.md)

- [Ansible Role Design](./ansible-role-design.md)

- [Ansible Playbook Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)

---

**This document defines the authoritative patterns for Ansible playbooks in Virgo-Core.**
