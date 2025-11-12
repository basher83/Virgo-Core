# Ansible Migration Plan for Virgo-Core

**Version:** 1.0
**Last Updated:** 2025-10-20
**Status:** Implementation Plan

---

## Purpose

This document provides a step-by-step migration plan for converting Virgo-Core's existing Ansible playbooks to the new component-based role architecture.
This migration will improve code reusability, maintainability, and consistency across multiple Proxmox clusters.

**Related Documents**:

- [Ansible Philosophy](./ansible-philosophy.md) - Core design principles
- [Ansible Role Design](./ansible-role-design.md) - Role structure and patterns
- [Ansible Playbook Design](./ansible-playbook-design.md) - Playbook orchestration

---

## Migration Overview

### Current State

```text
ansible/
├── playbooks/
│   ├── proxmox-build-template.yml          # VM template creation
│   ├── proxmox-create-terraform-user.yml   # Terraform user setup
│   ├── proxmox-enable-vlan-bridging.yml    # VLAN configuration
│   ├── install-docker.yml                   # Docker installation
│   ├── add-system-user.yml                  # User creation
│   └── add-file-to-host.yml                 # File deployment
├── tasks/
│   └── infisical-secret-lookup.yml         # Secrets retrieval
├── templates/
│   └── sudoers.j2
└── inventory/
    └── proxmox.yml
```

**Issues**:

- Playbooks contain role-worthy logic
- Code duplication across playbooks
- Not easily reusable across clusters
- Conflates multiple concerns (Linux users + Proxmox users)

### Target State

```text
ansible/
├── roles/
│   ├── proxmox_repository/      # NEW: APT repo management
│   ├── proxmox_network/          # NEW: Network infrastructure
│   ├── proxmox_cluster/          # NEW: Cluster formation
│   ├── proxmox_ceph/             # NEW: CEPH storage
│   ├── proxmox_access/           # CONVERTED: Proxmox API access
│   ├── proxmox_vm_template/      # CONVERTED: Template creation
│   ├── system_user/              # CONVERTED: Linux user management
│   └── docker/                   # CONVERTED: Docker installation
├── playbooks/
│   ├── setup-terraform-automation.yml      # REFACTORED: Uses roles
│   ├── configure-network.yml               # REFACTORED: Uses roles
│   ├── initialize-matrix-cluster.yml       # NEW: Full cluster setup
│   ├── create-admin-user.yml               # REFACTORED: Uses system_user
│   ├── create-vm-template.yml              # REFACTORED: Uses roles
│   └── install-docker.yml                  # REFACTORED: Uses docker role
├── tasks/
│   └── infisical-secret-lookup.yml         # PRESERVED
├── templates/
│   └── sudoers.j2                          # MOVED to system_user/templates/
└── inventory/
    └── proxmox.yml                         # PRESERVED
```

**Benefits**:

- Component-based, reusable roles
- Clear separation of concerns
- Consistent across all clusters
- Easier to test and maintain

---

## Migration Strategy

### Principles

1. **Incremental Migration**: Convert one playbook at a time
2. **Backwards Compatibility**: Keep old playbooks until new ones are tested
3. **Testing First**: Test each conversion thoroughly before removing old code
4. **Documentation**: Document as we migrate
5. **No Regression**: Maintain existing functionality

### Approach

1. Create role structure
2. Migrate simplest playbook first (build confidence)
3. Migrate complex playbooks
4. Create new functionality (cluster, CEPH)
5. Test all conversions
6. Remove old playbooks
7. Update documentation

---

## Migration Phases

### Phase 1: Foundation Setup (Week 1)

**Goal**: Create role directory structure and migrate simplest playbook

#### 1.1 Create Role Directory Structure

```bash
# Create role directories
mkdir -p ansible/roles/{proxmox_repository,proxmox_network,proxmox_cluster,proxmox_ceph,proxmox_access,proxmox_vm_template,system_user,docker}

# Create standard subdirectories for each role
for role in ansible/roles/*/; do
  mkdir -p "$role"/{tasks,defaults,handlers,templates,vars,files,meta}
  touch "$role"/tasks/main.yml
  touch "$role"/defaults/main.yml
  touch "$role"/meta/main.yml
  touch "$role"/README.md
done
```

#### 1.2 Convert `add-system-user.yml` to `system_user` Role

**Why Start Here**: Simplest playbook, clear single responsibility

**Current Playbook** (`playbooks/add-system-user.yml`):

```yaml
---
- name: Add System User
  hosts: all
  become: true
  tasks:
    - name: Create user
      user:
        name: "{{ username }}"
        shell: /bin/bash
        create_home: true

    - name: Add SSH key
      authorized_key:
        user: "{{ username }}"
        key: "{{ ssh_key }}"

    - name: Configure sudo
      lineinfile:
        path: /etc/sudoers.d/{{ username }}
        line: "{{ username }} ALL=(ALL) NOPASSWD:ALL"
        create: true
        validate: 'visudo -cf %s'
```

**New Role** (`roles/system_user/`):

```yaml
# roles/system_user/defaults/main.yml
---
system_users: []

# roles/system_user/tasks/main.yml
---
- name: Create/update system users
  user:
    name: "{{ item.name }}"
    state: "{{ item.state | default('present') }}"
    shell: "{{ item.shell | default('/bin/bash') }}"
    groups: "{{ item.groups | default([]) }}"
    create_home: true
  loop: "{{ system_users }}"
  when: item.state | default('present') == 'present'

- name: Configure SSH keys
  authorized_key:
    user: "{{ item.name }}"
    key: "{{ item_key }}"
    state: present
  loop: "{{ system_users | subelements('ssh_keys', skip_missing=True) }}"
  loop_control:
    loop_var: item
    loop_var: item_key
  when: item.state | default('present') == 'present'

- name: Configure sudo rules
  template:
    src: sudoers.j2
    dest: "/etc/sudoers.d/{{ item.name }}"
    owner: root
    group: root
    mode: '0440'
    validate: '/usr/sbin/visudo -cf %s'
  loop: "{{ system_users }}"
  when:
    - item.state | default('present') == 'present'
    - item.sudo_rules is defined or item.sudo_nopasswd is defined

# roles/system_user/templates/sudoers.j2
# Sudo configuration for {{ item.name }}
{% if item.sudo_nopasswd | default(false) %}
{{ item.name }} ALL=(ALL) NOPASSWD:ALL
{% elif item.sudo_rules is defined %}
{% for rule in item.sudo_rules %}
{{ item.name }} ALL=(ALL) NOPASSWD: {{ rule }}
{% endfor %}
{% endif %}
```

**New Playbook** (`playbooks/create-admin-user.yml`):

```yaml
---
# Playbook: Create Admin User
# Purpose: Create administrative user with SSH and sudo access

- name: Create Administrative User
  hosts: "{{ target_cluster | default('all') }}"
  gather_facts: true
  become: true

  vars:
    admin_name: "{{ admin_name | mandatory }}"
    admin_ssh_key: "{{ admin_ssh_key | mandatory }}"

  roles:
    - role: system_user
      vars:
        system_users:
          - name: "{{ admin_name }}"
            state: present
            shell: /bin/bash
            groups: [sudo]
            ssh_keys:
              - "{{ admin_ssh_key }}"
            sudo_nopasswd: true
```

**Testing**:

```bash
# Test syntax
ansible-playbook --syntax-check playbooks/create-admin-user.yml

# Test in check mode
ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml \
  -e "admin_name=testuser" \
  -e "admin_ssh_key='ssh-rsa AAAAB3...'" \
  --limit foxtrot --check --diff

# Run on test host
ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml \
  -e "admin_name=testuser" \
  -e "admin_ssh_key='ssh-rsa AAAAB3...'" \
  --limit foxtrot

# Verify
ssh testuser@foxtrot sudo id
```

---

### Phase 2: Terraform User Migration (Week 2)

**Goal**: Convert complex multi-concern playbook to two focused roles

#### 2.1 Analyze Current Playbook

**Current**: `playbooks/proxmox-create-terraform-user.yml` (296 lines)

**Responsibilities Identified**:

1. Linux user creation (lines 88-127) → `system_user` role
2. Proxmox user creation (lines 150-224) → `proxmox_access` role
3. Proxmox role/group/ACL (lines 150-206) → `proxmox_access` role
4. API token generation (lines 225-248) → `proxmox_access` role
5. Secrets retrieval (lines 52-64) → Shared pattern

#### 2.2 Create `proxmox_access` Role

```yaml
# roles/proxmox_access/defaults/main.yml
---
proxmox_api_host: "{{ ansible_default_ipv4.address }}"
proxmox_validate_certs: false

proxmox_roles: []
proxmox_groups: []
proxmox_users: []
proxmox_tokens: []
proxmox_acls: []

export_terraform_env: false

# roles/proxmox_access/tasks/main.yml
---
- name: Retrieve secrets from Infisical
  include_tasks: secrets.yml

- name: Create custom Proxmox roles
  include_tasks: roles.yml
  when: proxmox_roles | length > 0

- name: Create Proxmox groups
  include_tasks: groups.yml
  when: proxmox_groups | length > 0

- name: Create Proxmox users
  include_tasks: users.yml
  when: proxmox_users | length > 0

- name: Generate API tokens
  include_tasks: tokens.yml
  when: proxmox_tokens | length > 0

- name: Configure ACL permissions
  include_tasks: acls.yml
  when: proxmox_acls | length > 0

- name: Export environment files
  include_tasks: env_export.yml
  when: export_terraform_env | bool

# roles/proxmox_access/tasks/secrets.yml
---
- name: Retrieve Proxmox username
  include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'PROXMOX_USERNAME'
    secret_var_name: 'proxmox_api_user'
    infisical_project_id: "{{ infisical_project_id }}"
    infisical_env: "{{ infisical_env }}"
    infisical_path: "{{ infisical_path }}"

- name: Retrieve Proxmox password
  include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_api_password'
    infisical_project_id: "{{ infisical_project_id }}"
    infisical_env: "{{ infisical_env }}"
    infisical_path: "{{ infisical_path }}"

# roles/proxmox_access/tasks/roles.yml
---
- name: Check existing roles
  command: pveum role list
  register: existing_roles
  changed_when: false

- name: Create custom roles
  command: >
    pveum role add {{ item.name }}
    -privs "{{ item.privileges | join(' ') }}"
  loop: "{{ proxmox_roles }}"
  when: item.name not in existing_roles.stdout
  register: role_create

# roles/proxmox_access/tasks/groups.yml
---
- name: Create Proxmox groups
  community.proxmox.proxmox_group:
    name: "{{ item.name }}"
    state: present
    comment: "{{ item.comment | default('') }}"
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_password: "{{ proxmox_api_password }}"
    validate_certs: "{{ proxmox_validate_certs }}"
  loop: "{{ proxmox_groups }}"
  delegate_to: localhost
  become: false

# roles/proxmox_access/tasks/users.yml
---
- name: Check existing Proxmox users
  command: pveum user list
  register: existing_users
  changed_when: false

- name: Create Proxmox users (PAM realm)
  command: >
    pveum user add {{ item.userid }}
    --groups {{ item.groups | join(',') }}
    --comment "{{ item.comment | default('') }}"
  loop: "{{ proxmox_users }}"
  when:
    - item.userid not in existing_users.stdout
    - "'@pam' in item.userid"

# roles/proxmox_access/tasks/tokens.yml
---
- name: Check existing tokens
  command: pveum user token list {{ item.userid }}
  loop: "{{ proxmox_tokens }}"
  register: existing_tokens
  changed_when: false
  failed_when: false

- name: Generate API tokens
  command: >
    pveum user token add {{ item.0.userid }} {{ item.0.tokenid }}
    -privsep {{ '0' if not item.0.privsep | default(true) else '1' }}
  loop: "{{ proxmox_tokens | zip(existing_tokens.results) | list }}"
  when: item.0.tokenid not in item.1.stdout
  register: token_create

- name: Store token values
  set_fact:
    generated_tokens: "{{ generated_tokens | default({}) | combine({item.item.0.userid: item.stdout}) }}"
  loop: "{{ token_create.results }}"
  when: item.changed
  no_log: true

# roles/proxmox_access/tasks/acls.yml
---
- name: Configure ACL permissions
  community.proxmox.proxmox_access_acl:
    path: "{{ item.path }}"
    type: "{{ item.type }}"
    ugid: "{{ item.ugid }}"
    roleid: "{{ item.roleid }}"
    state: present
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_password: "{{ proxmox_api_password }}"
    validate_certs: "{{ proxmox_validate_certs }}"
  loop: "{{ proxmox_acls }}"
  delegate_to: localhost
  become: false

# roles/proxmox_access/tasks/env_export.yml
---
- name: Create environment file directory
  file:
    path: "{{ lookup('env', 'HOME') }}/tmp/.proxmox-terraform"
    state: directory
    mode: '0755'
  delegate_to: localhost
  become: false

- name: Export Terraform environment file
  copy:
    content: |
      # Proxmox API Configuration for {{ inventory_hostname }}
      export TF_VAR_proxmox_url="{{ proxmox_api_host }}"
      export TF_VAR_proxmox_user="{{ proxmox_api_user }}"
      export TF_VAR_proxmox_token_id="{{ item.userid }}!{{ item.tokenid }}"
      export TF_VAR_proxmox_token_secret="{{ generated_tokens[item.userid] | default('ALREADY_EXISTS') }}"
    dest: "{{ lookup('env', 'HOME') }}/tmp/.proxmox-terraform/proxmox-{{ inventory_hostname_short }}"
    mode: '0600'
  loop: "{{ proxmox_tokens }}"
  delegate_to: localhost
  become: false
  when: generated_tokens is defined
```

#### 2.3 Create New Orchestration Playbook

```yaml
# playbooks/setup-terraform-automation.yml
---
# Playbook: Setup Terraform Automation Access
# Purpose: Create Linux system user and Proxmox API access for Terraform

- name: Setup Terraform Automation on Proxmox
  hosts: "{{ target_cluster | default('all') }}"
  gather_facts: true
  become: true

  vars:
    infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
    infisical_env: 'prod'
    infisical_path: '/{{ cluster_name }}'
    cluster_name: "{{ group_names | select('search', '_cluster') | first | regex_replace('_cluster$', '') }}"

  roles:
    - role: system_user
      vars:
        system_users:
          - name: terraform
            state: present
            shell: /bin/bash
            ssh_keys:
              - "{{ lookup('file', playbook_dir + '/../files/terraform.pub') }}"
            sudo_rules:
              - /sbin/pvesm
              - /sbin/qm
              - "/usr/bin/tee /var/lib/vz/*"
            sudo_nopasswd: true

    - role: proxmox_access
      vars:
        infisical_project_id: "{{ infisical_project_id }}"
        infisical_env: "{{ infisical_env }}"
        infisical_path: "{{ infisical_path }}"

        proxmox_roles:
          - name: TerraformUser
            privileges:
              - Datastore.Allocate
              - Datastore.AllocateSpace
              - VM.Allocate
              - VM.Clone
              - VM.Config.CDROM
              - VM.Config.CPU
              - VM.Config.Disk
              - VM.Config.Memory
              - VM.Config.Network
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

        proxmox_acls:
          - path: /
            type: group
            ugid: terraform-users
            roleid: TerraformUser

        export_terraform_env: true
```

#### 2.4 Testing

```bash
# Test new playbook
ansible-playbook -i inventory/proxmox.yml playbooks/setup-terraform-automation.yml \
  --limit foxtrot --check --diff

# Run on test node
ansible-playbook -i inventory/proxmox.yml playbooks/setup-terraform-automation.yml \
  --limit foxtrot

# Verify Linux user
ssh terraform@foxtrot sudo pvesm status

# Verify Proxmox user
ssh root@foxtrot pveum user list | grep terraform

# Verify environment file
cat ~/tmp/.proxmox-terraform/proxmox-foxtrot

# Test full workflow
source ~/tmp/.proxmox-terraform/proxmox-foxtrot
cd terraform/netbox-vm
tofu plan
```

---

### Phase 3: Network and Docker Roles (Week 3)

#### 3.1 Convert `proxmox-enable-vlan-bridging.yml` to `proxmox_network` Role

**Current Playbook**: Only enables VLAN bridging on vmbr1

**Enhanced Role**: Manages all network infrastructure

See [Ansible Role Design](./ansible-role-design.md#2-proxmox_network) for complete implementation.

#### 3.2 Convert `install-docker.yml` to `docker` Role

**Current Playbook**:

```yaml
---
- name: Install Docker
  hosts: all
  become: true
  tasks:
    - name: Install dependencies
      apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
        state: present

    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg

    - name: Add Docker repository
      apt_repository:
        repo: deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable

    - name: Install Docker
      apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
        state: present
```

**New Role**: `roles/docker/`

```yaml
# roles/docker/defaults/main.yml
---
docker_edition: 'ce'
docker_packages:
  - docker-{{ docker_edition }}
  - docker-{{ docker_edition }}-cli
  - containerd.io

docker_users: []

# roles/docker/tasks/main.yml
---
- name: Install prerequisites
  apt:
    name:
      - apt-transport-https
      - ca-certificates
      - curl
      - gnupg
    state: present
    update_cache: yes

- name: Add Docker GPG key
  apt_key:
    url: https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg
    state: present

- name: Add Docker repository
  apt_repository:
    repo: "deb [arch={{ dpkg_architecture }}] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} stable"
    state: present

- name: Install Docker packages
  apt:
    name: "{{ docker_packages }}"
    state: present
    update_cache: yes

- name: Add users to docker group
  user:
    name: "{{ item }}"
    groups: docker
    append: yes
  loop: "{{ docker_users }}"
  when: docker_users | length > 0

- name: Ensure Docker service is running
  service:
    name: docker
    state: started
    enabled: yes
```

**New Playbook**: `playbooks/install-docker.yml`

```yaml
---
# Playbook: Install Docker
# Purpose: Install Docker CE on Proxmox nodes

- name: Install Docker
  hosts: "{{ target_cluster | default('all') }}"
  gather_facts: true
  become: true

  roles:
    - role: docker
      vars:
        docker_users:
          - admin
          - developer
```

---

### Phase 4: New Functionality (Week 4)

**Goal**: Implement roles for cluster formation and CEPH storage

#### 4.1 Create `proxmox_cluster` Role

See [Ansible Role Design](./ansible-role-design.md#3-proxmox_cluster) for complete implementation.

**Key Tasks**:

- Cluster initialization
- Node joining
- Corosync configuration
- /etc/hosts management

#### 4.2 Create `proxmox_ceph` Role

See [Ansible Role Design](./ansible-role-design.md#4-proxmox_ceph) for complete implementation.

**Key Tasks**:

- CEPH installation
- Monitor deployment
- Manager deployment
- **Automated OSD creation** (improves on ProxSpray)
- Pool configuration

#### 4.3 Create Complete Cluster Initialization Playbook

```yaml
# playbooks/initialize-matrix-cluster.yml
---
# Playbook: Initialize Matrix Cluster
# Purpose: Complete Matrix cluster initialization

- name: Initialize Matrix Cluster
  hosts: matrix_cluster
  gather_facts: true
  become: true

  roles:
    - role: proxmox_repository
    - role: proxmox_network
    - role: proxmox_cluster
    - role: proxmox_ceph
```

---

### Phase 5: Testing and Validation (Week 5)

#### 5.1 Create Test Playbooks

```yaml
# playbooks/test-roles.yml
---
- name: Test All Roles
  hosts: foxtrot
  gather_facts: true
  become: true

  roles:
    - role: system_user
      vars:
        system_users:
          - name: testuser1
            state: present

    - role: proxmox_access
      vars:
        proxmox_groups:
          - name: test-group
      tags: [proxmox]
```

#### 5.2 Automated Testing

```bash
# Create mise task for testing
# .mise.toml
[tasks."ansible:test-all"]
description = "Test all roles with check mode"
run = """
cd ansible
for playbook in playbooks/*.yml; do
  echo "Testing $playbook..."
  uv run ansible-playbook --syntax-check "$playbook"
  uv run ansible-playbook "$playbook" --check --diff --limit foxtrot
done
"""
```

#### 5.3 Integration Testing

```bash
# Test complete workflow on Matrix cluster
ansible-playbook -i inventory/proxmox.yml playbooks/initialize-matrix-cluster.yml \
  --limit foxtrot --check --diff

# Verify cluster status
ssh root@foxtrot pvecm status
ssh root@foxtrot ceph -s
```

---

### Phase 6: Cleanup and Documentation (Week 6)

#### 6.1 Remove Old Playbooks

Once all conversions are tested:

```bash
# Backup old playbooks
mkdir -p ansible/playbooks/.deprecated
mv ansible/playbooks/proxmox-create-terraform-user.yml ansible/playbooks/.deprecated/
mv ansible/playbooks/add-system-user.yml ansible/playbooks/.deprecated/
mv ansible/playbooks/proxmox-enable-vlan-bridging.yml ansible/playbooks/.deprecated/
```

#### 6.2 Update Documentation

- Update `CLAUDE.md` with new role structure
- Create role README files
- Update playbook usage in docs
- Document migration

#### 6.3 Update Mise Tasks

```toml
# .mise.toml updates
[tasks."ansible:setup-terraform"]
description = "Setup Terraform automation (new role-based)"
run = """
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml \
  playbooks/setup-terraform-automation.yml \
  --limit ${CLUSTER:-matrix_cluster}
"""

[tasks."ansible:init-cluster"]
description = "Initialize cluster (WARNING: Destructive)"
run = """
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml \
  playbooks/initialize-${CLUSTER:-matrix}-cluster.yml
"""
```

---

## Migration Checklist

### Phase 1: Foundation

- [ ] Create role directory structure
- [ ] Convert `add-system-user.yml` to `system_user` role
- [ ] Create `create-admin-user.yml` playbook
- [ ] Test `system_user` role on all clusters
- [ ] Document `system_user` role

### Phase 2: Terraform User

- [x] Create `proxmox_access` role (tasks, templates, defaults)
- [x] Create `setup-terraform-automation.yml` playbook
- [ ] Test on single node (foxtrot)
- [ ] Test on full cluster (matrix_cluster)
- [ ] Verify Terraform integration works
- [x] Document `proxmox_access` role

### Phase 3: Network and Docker

- [x] Create `proxmox_network` role
- [x] Create `configure-network.yml` playbook
- [ ] Test network configuration
- [x] Docker role decision: Keep using `geerlingguy.docker` (no wrapper needed)
  - Rationale: Well-maintained community role, already in requirements.yml
  - Playbook already follows role-based patterns
- [x] Verify `install-docker.yml` follows Phase 3 patterns
- [ ] Test Docker installation

### Phase 4: New Functionality

- [x] Create `proxmox_cluster` role
- [x] Create `proxmox_ceph` role
- [x] Create `proxmox_repository` role
- [x] Create `initialize-matrix-cluster.yml` playbook
- [ ] Test cluster initialization (non-production)
- [x] Document cluster formation process

### Phase 5: Testing

- [x] Run ansible-lint on all roles
  - **Status**: ✅ Complete (2025-11-11)
  - **Results**: 0 failures, 0 warnings, Production profile passed
  - **Files**: 67 files processed (after cleanup)
- [ ] Create test playbooks
- [x] Test all roles in check mode
  - **Status**: 🟡 Partial
  - **Tested**: `create-admin-user.yml`, `configure-network.yml` on Matrix cluster
  - **Results**: Playbook structures valid, prerequisites pass
- [x] Verify idempotency (run twice, second run no changes)
  - **Status**: 🟡 Partial
  - **Completed**: `system_user` role - Perfect idempotency (changed=0)
  - **Deferred**: `proxmox_network` role - Conditional logic issue prevents testing
  - **Validated**: `install-docker.yml` - Production-proven (user uses regularly)
  - **Tested**: Matrix cluster (Foxtrot, Golf, Hotel)
- [x] Create inventory structure
  - **Status**: ✅ Complete (2025-11-11)
  - **Created**: `inventory/hosts.yml`, `group_vars/matrix_cluster.yml`
  - **Validated**: Variables load and template correctly
- [ ] Test full cluster initialization
- [ ] Performance testing

### Phase 6: Cleanup

- [x] Remove old playbooks (move to .deprecated/)
  - **Status**: ✅ Complete (2025-11-11)
  - **Moved**: `proxmox-enable-vlan-bridging.yml`, `proxmox-create-terraform-user.yml`, `add-system-user.yml`
- [x] Update CLAUDE.md
  - **Status**: ✅ Complete (2025-11-11)
  - **Changes**: Refactored to Core 4 principles, reduced from 289 to 68 lines
- [ ] Create role README files
- [ ] Update mise tasks
- [x] Update team documentation
  - **Status**: 🟡 Partial
  - **Created**: `docs/infrastructure.md`, `docs/testing-validation-results.md`
  - **Updated**: `docs/goals.md`
- [ ] Create migration completion summary

---

## Rollback Procedures

If issues arise during migration:

### Immediate Rollback

```bash
# Restore old playbooks
mv ansible/playbooks/.deprecated/* ansible/playbooks/

# Remove new roles
rm -rf ansible/roles/
```

### Partial Rollback

Keep working roles, revert problematic ones:

```bash
# Example: Revert proxmox_access but keep system_user
rm -rf ansible/roles/proxmox_access
mv ansible/playbooks/.deprecated/proxmox-create-terraform-user.yml ansible/playbooks/
```

---

## Success Criteria

Migration is complete when:

1. **All playbooks converted** to use roles
2. **All roles tested** on at least one cluster
3. **Documentation updated** with new structure
4. **Team trained** on new patterns
5. **Old playbooks removed** or archived
6. **No regressions** in existing functionality
7. **New functionality working** (cluster, CEPH)

---

## Timeline Summary

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1 | Foundation | `system_user` role, role structure |
| 2 | Terraform User | `proxmox_access` role, new playbook |
| 3 | Network/Docker | `proxmox_network`, `docker` roles |
| 4 | New Functionality | `proxmox_cluster`, `proxmox_ceph` roles |
| 5 | Testing | Test suite, validation |
| 6 | Cleanup | Documentation, cleanup, training |

**Total Duration**: 6 weeks

---

## References

- [Ansible Philosophy](./ansible-philosophy.md)
- [Ansible Role Design](./ansible-role-design.md)
- [Ansible Playbook Design](./ansible-playbook-design.md)
- [ProxSpray Analysis](./proxspray-analysis.md)

---

**This migration plan provides a structured, low-risk approach to modernizing Virgo-Core's Ansible automation.**
