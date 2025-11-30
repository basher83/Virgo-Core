---
title: Ansible Role Design
description: Structure, responsibilities, and implementation patterns for creating component-based Ansible roles in Virgo-Core
---

# Ansible Role Design for Virgo-Core

**Version:** 1.0
**Last Updated:** 2025-10-20
**Status:** Team Standard

---

## Purpose

This document defines the structure, responsibilities, and implementation patterns for Ansible roles in Virgo-Core. It
provides concrete guidance for creating component-based, reusable roles that manage Proxmox VE infrastructure across
multiple clusters.

**Related Documents**:

- [Ansible Philosophy](./ansible-philosophy.md) - Core design principles

- [Ansible Playbook Design](./ansible-playbook-design.md) - Playbook orchestration patterns

- [Ansible Migration Plan](./ansible-migration-plan.md) - Migration implementation

---

## Recommended Role Structure

Virgo-Core uses component-based roles organized by infrastructure aspect:

```text
ansible/roles/
├── proxmox_repository/      # APT repositories, packages, updates

├── proxmox_network/          # Bridges, VLANs, interfaces, MTU

├── proxmox_cluster/          # Cluster formation, corosync, quorum

├── proxmox_ceph/             # Monitors, managers, OSDs, pools

├── proxmox_access/           # PVE users, groups, ACLs, tokens, roles

├── proxmox_vm_template/      # Cloud-init template creation

├── system_user/              # Linux PAM users, SSH, sudo

└── docker/                   # Docker installation and configuration

```

### Standard Role Directory Structure

Each role follows this structure:

```text
roles/role_name/
├── tasks/
│   ├── main.yml              # Entry point (includes other task files)

│   ├── secrets.yml           # Infisical secret retrieval

│   ├── prerequisites.yml     # Validation and checks

│   ├── component_setup.yml   # Main component configuration

│   └── verify.yml            # Post-configuration verification

├── defaults/
│   └── main.yml              # Default variables (user can override)

├── vars/
│   └── main.yml              # Internal variables (higher precedence)

├── templates/
│   └── config.j2             # Jinja2 templates

├── handlers/
│   └── main.yml              # Service restart handlers

├── files/
│   └── static_file           # Static files to copy

├── meta/
│   └── main.yml              # Role metadata and dependencies

└── README.md                 # Role documentation

```

---

## Role Definitions and Responsibilities

### 1. `proxmox_repository`

**Manages**: Proxmox VE and CEPH APT repository configuration

**Scope**:

- `/etc/apt/sources.list.d/pve-*.list`

- `/etc/apt/sources.list.d/ceph-*.list`

- Proxmox package installation

- System updates

**Responsibilities**:

- Disable Proxmox Enterprise repositories

- Enable no-subscription repositories

- Configure CEPH repositories (Squid for PVE 9.x)

- Install/update Proxmox VE packages

- Clean up old kernels

**Operational Notes**:
> For major version upgrades (e.g., PVE 8.x → 9.x), kernel updates, and reboot requirements, see the role's README.md for detailed upgrade procedures and best practices.

**Configuration Model**:

```yaml

# group_vars/all.yml

proxmox_version: "9.0"
proxmox_enterprise_repo: false
proxmox_no_subscription_repo: true
ceph_version: "squid"

# Optional package updates

proxmox_packages:
  - proxmox-ve
  - pve-kernel
  - postfix
  - open-iscsi

auto_update_packages: false  # Set true for automatic updates

```

**Example Usage in Playbook**:

```yaml

- hosts: all
  roles:
    - role: proxmox_repository
      vars:
        proxmox_enterprise_repo: false
        auto_update_packages: true

```

---

### 2. `proxmox_network`

**Manages**: Network infrastructure (bridges, VLANs, interfaces, MTU)

**Scope**:

- `/etc/network/interfaces`

- Network bridge configuration (vmbr0, vmbr1, vmbr2)

- VLAN interfaces

- MTU settings

- IP addressing

**Responsibilities**:

- Create and configure network bridges

- Configure VLAN-aware bridges

- Create VLAN subinterfaces

- Set MTU for jumbo frames (CEPH networks)

- Configure IP addresses and gateways

- Reload network configuration

**Configuration Model**:

```yaml

# group_vars/matrix_cluster.yml

# Declarative network configuration

proxmox_bridges:
  - name: vmbr0
    interface: enp4s0
    address: "192.168.3.{{ node_id }}/24"
    gateway: 192.168.3.1
    vlan_aware: true
    vlan_ids: [9]
    comment: "Management network"

  - name: vmbr1
    interface: enp5s0f0np0
    address: "192.168.5.{{ node_id }}/24"
    mtu: 9000
    comment: "CEPH Public network"

  - name: vmbr2
    interface: enp5s0f1np1
    address: "192.168.7.{{ node_id }}/24"
    mtu: 9000
    comment: "CEPH Private network"

# VLAN subinterfaces

proxmox_vlans:
  - id: 9
    raw_device: vmbr0
    address: "192.168.8.{{ node_id }}/24"
    comment: "Corosync network"

# Node-specific IDs

node_ids:
  foxtrot: 5
  golf: 6
  hotel: 7

```

**Task Structure**:

```yaml

# roles/proxmox_network/tasks/main.yml

---

- name: Include prerequisite checks
  include_tasks: prerequisites.yml

- name: Configure network bridges
  include_tasks: bridges.yml

- name: Configure VLAN interfaces
  include_tasks: vlans.yml

- name: Configure MTU settings
  include_tasks: mtu.yml
  when: jumbo_frames_enabled | default(false)

- name: Reload network configuration
  include_tasks: reload.yml
  when: network_changed

- name: Verify network configuration
  include_tasks: verify.yml

```

---

### 3. `proxmox_cluster`

**Manages**: Proxmox VE cluster formation and management

**Scope**:

- Cluster initialization (`pvecm create`)

- Node joining (`pvecm add`)

- Corosync configuration (`/etc/corosync/corosync.conf`, `/etc/pve/corosync.conf`)

- `/etc/hosts` management

- Cluster quorum

- SSH key distribution

**Responsibilities**:

- Initialize cluster on first node

- Join additional nodes to cluster

- Configure corosync network (VLAN 9 for Matrix)

- Manage cluster membership

- Configure SSH for passwordless cluster operations

- Update SSL certificates

- Verify cluster health and quorum

**Configuration Model**:

```yaml

# group_vars/matrix_cluster.yml

cluster_name: "Matrix"
cluster_group: "matrix_cluster"

# Corosync configuration

corosync_network: "192.168.8.0/24"  # VLAN 9

corosync_bindnetaddr: "192.168.8.0"
corosync_mcastaddr: "239.192.8.1"
corosync_mcastport: 5405

# Node configuration

cluster_nodes:
  - name: foxtrot
    hostname: foxtrot.matrix.spaceships.work
    management_ip: 192.168.3.5
    corosync_ip: 192.168.8.5
    node_id: 1

  - name: golf
    hostname: golf.matrix.spaceships.work
    management_ip: 192.168.3.6
    corosync_ip: 192.168.8.6
    node_id: 2

  - name: hotel
    hostname: hotel.matrix.spaceships.work
    management_ip: 192.168.3.7
    corosync_ip: 192.168.8.7
    node_id: 3

```

**Task Structure**:

```yaml

# roles/proxmox_cluster/tasks/main.yml

---

- name: Verify prerequisites
  include_tasks: prerequisites.yml

- name: Configure /etc/hosts
  include_tasks: hosts_config.yml

- name: Initialize cluster (first node)
  include_tasks: cluster_init.yml
  when: inventory_hostname == groups[cluster_group][0]

- name: Join cluster (other nodes)
  include_tasks: cluster_join.yml
  when: inventory_hostname != groups[cluster_group][0]

- name: Configure corosync
  include_tasks: corosync.yml

- name: Verify cluster health
  include_tasks: verify.yml

```

---

### 4. `proxmox_ceph`

**Manages**: CEPH distributed storage infrastructure

**Scope**:

- CEPH installation (`pveceph install`)

- CEPH initialization (`pveceph init`)

- Monitor deployment (`pveceph mon create`)

- Manager deployment (`pveceph mgr create`)

- OSD creation (`pveceph osd create`)

- Pool configuration

- CRUSH rules

**Responsibilities**:

- Install CEPH packages

- Initialize CEPH cluster

- Deploy monitors on all nodes

- Deploy managers on all nodes

- Prepare and create OSDs

- Configure CEPH pools with replication

- Set up CRUSH rules

- Verify CEPH health

**Configuration Model**:

```yaml

# group_vars/matrix_cluster.yml

ceph_network: "192.168.5.0/24"          # vmbr1 - Public

ceph_cluster_network: "192.168.7.0/24"  # vmbr2 - Private

# OSD configuration (4 OSDs per node = 12 total)

# 2 OSDs per NVMe × 2 NVMe drives per node × 3 nodes = 12 OSDs

ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      partitions: 2
      db_device: null        # Use same device for DB

      wal_device: null       # Use same device for WAL

      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

  golf:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

  hotel:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

# Pool configuration

ceph_pools:
  - name: vm_ssd
    pg_num: 128
    pgp_num: 128
    size: 3              # Replicate across 3 nodes

    min_size: 2          # Minimum 2 replicas required

    application: rbd
    crush_rule: replicated_rule

  - name: vm_containers
    pg_num: 64
    pgp_num: 64
    size: 3
    min_size: 2
    application: rbd

```

> **Note on CRUSH Rules**: The `replicated_rule` (default) spreads replicas across hosts, providing host-level failure domains. This is appropriate for single-site clusters like Matrix. Custom CRUSH rules (for rack or datacenter-aware placement) are beyond the scope of homelab deployments.

**Task Structure**:

```yaml

# roles/proxmox_ceph/tasks/main.yml

---

- name: Install CEPH packages
  include_tasks: install.yml

- name: Initialize CEPH cluster
  include_tasks: init.yml
  when: inventory_hostname == groups[cluster_group][0]

- name: Create CEPH monitors
  include_tasks: monitors.yml

- name: Create CEPH managers
  include_tasks: managers.yml

- name: Prepare OSD disks
  include_tasks: osd_prepare.yml

- name: Create OSDs
  include_tasks: osd_create.yml

- name: Create CEPH pools
  include_tasks: pools.yml
  when: inventory_hostname == groups[cluster_group][0]

- name: Verify CEPH health
  include_tasks: verify.yml

```

**OSD Creation Pattern** (improves on ProxSpray):

```yaml

# roles/proxmox_ceph/tasks/osd_create.yml

---

- name: Check existing OSDs
  command: pveceph osd ls
  register: existing_osds
  changed_when: false

- name: Create OSDs from configuration
  command: >
    pveceph osd create {{ item.0.device }}
    {% if item.0.db_device %}--db_dev {{ item.0.db_device }}{% endif %}
    {% if item.0.wal_device %}--wal_dev {{ item.0.wal_device }}{% endif %}
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  when: item.0.device not in existing_osds.stdout
  register: osd_create
  changed_when: "'successfully created' in osd_create.stdout"
  failed_when:
    - osd_create.rc != 0
    - "'already in use' not in osd_create.stderr"

```

---

### 5. `proxmox_access`

**Manages**: Proxmox API access control (users, groups, tokens, ACLs, roles)

**Scope**:

- Proxmox users (`pveum user`, `community.proxmox.proxmox_user`)

- Proxmox groups (`pveum group`, `community.proxmox.proxmox_group`)

- Proxmox roles (`pveum role`)

- API tokens (`pveum user token`)

- ACL permissions (`community.proxmox.proxmox_access_acl`)

**Responsibilities**:

- Create custom Proxmox roles with specific privileges

- Create Proxmox groups

- Create Proxmox users (PVE realm or PAM realm)

- Generate API tokens

- Configure ACL permissions

- Export environment files for Terraform integration

**Configuration Model**:

```yaml

# playbook or group_vars

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
    # Note: PAM users authenticate via Linux PAM

proxmox_tokens:
  - userid: terraform@pam
    tokenid: automation
    privsep: false  # Token has full user privileges

    expire: 0       # Never expires

proxmox_acls:
  - path: /
    type: group
    ugid: terraform-users
    roleid: TerraformUser
    propagate: true

```

**Task Structure**:

```yaml

# roles/proxmox_access/tasks/main.yml

---

- name: Retrieve secrets from Infisical
  include_tasks: secrets.yml

- name: Create custom roles
  include_tasks: roles.yml

- name: Create groups
  include_tasks: groups.yml

- name: Create users
  include_tasks: users.yml

- name: Generate API tokens
  include_tasks: tokens.yml

- name: Configure ACL permissions
  include_tasks: acls.yml

- name: Export environment files
  include_tasks: env_export.yml
  when: export_terraform_env | default(false)

```

**Separation from `system_user` Role**:

This role manages **Proxmox API access** only, not Linux system users. For creating the corresponding Linux PAM user,
use the `system_user` role.

---

### 6. `system_user`

**Manages**: Linux PAM user accounts, SSH keys, sudo configuration

**Scope**:

- `/etc/passwd` (user accounts)

- `/home/*/` (home directories)

- `/home/*/.ssh/` (SSH keys)

- `/etc/sudoers.d/` (sudo rules)

**Responsibilities**:

- Create Linux user accounts

- Configure shell and home directory

- Deploy SSH public keys

- Configure sudo rules (specific commands or NOPASSWD)

- Manage user groups

- Remove users when state: absent

**Configuration Model**:

```yaml

# Declarative user configuration

system_users:
  - name: terraform
    state: present
    shell: /bin/bash
    comment: "Terraform automation user"
    groups: []
    ssh_keys:
      - "{{ lookup('file', 'files/terraform.pub') }}"
    sudo_rules:
      - /sbin/pvesm
      - /sbin/qm
      - "/usr/bin/tee /var/lib/vz/*"
    sudo_nopasswd: true

  - name: admin
    state: present
    shell: /bin/zsh
    groups: [sudo, docker]
    ssh_keys:
      - "ssh-rsa AAAAB3NzaC1yc2E..."
    sudo_nopasswd: true

  - name: olduser
    state: absent  # Remove this user

```

**Task Structure**:

```yaml

# roles/system_user/tasks/main.yml

---

- name: Create/update user accounts
  include_tasks: create_users.yml

- name: Configure SSH keys
  include_tasks: ssh_keys.yml

- name: Configure sudo rules
  include_tasks: sudo_config.yml

- name: Remove absent users
  include_tasks: remove_users.yml

```

**Sudo Configuration Pattern**:

```yaml

# roles/system_user/tasks/sudo_config.yml

---

- name: Create sudoers.d directory
  file:
    path: /etc/sudoers.d
    state: directory
    mode: '0750'

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

```

```jinja2
{# roles/system_user/templates/sudoers.j2 #}

# Sudo configuration for {{ item.name }}

# Managed by Ansible - DO NOT EDIT MANUALLY

{% if item.sudo_nopasswd | default(false) %}
{{ item.name }} ALL=(ALL) NOPASSWD:ALL
{% elif item.sudo_rules is defined %}
{% for rule in item.sudo_rules %}
{{ item.name }} ALL=(ALL) NOPASSWD: {{ rule }}
{% endfor %}
{% endif %}

```

---

### 7. `proxmox_vm_template`

**Manages**: VM template creation with cloud-init

**Scope**:

- VM template creation

- Cloud image downloads

- Cloud-init configuration

- Template customization

**Responsibilities**:

- Download cloud images (Ubuntu, Debian, etc.)

- Create VM templates from cloud images

- Configure cloud-init settings

- Customize templates (packages, scripts)

- Store templates in Proxmox

**Configuration Model**:

```yaml

# Template configuration

proxmox_templates:
  - name: ubuntu-2404-template
    vmid: 9000
    image_url: "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
    image_checksum: "sha256:..."
    memory: 2048
    cores: 2
    storage: local-lvm
    cloudinit:
      user: ubuntu
      packages:
        - qemu-guest-agent
        - cloud-init
      runcmd:
        - systemctl enable qemu-guest-agent
        - systemctl start qemu-guest-agent

```

---

### 8. `docker`

**Manages**: Docker installation and configuration

**Scope**:

- Docker CE installation

- Docker daemon configuration

- Docker Compose installation

- User group membership

**Responsibilities**:

- Add Docker APT repository

- Install Docker CE packages

- Configure Docker daemon

- Add users to docker group

- Install Docker Compose

**Configuration Model**:

```yaml
docker_users:
  - admin
  - developer

docker_daemon_options:
  log-driver: "json-file"
  log-opts:
    max-size: "10m"
    max-file: "3"

```

---

## Role Implementation Patterns

### Pattern 1: Infisical Secrets Integration

All roles that need secrets should retrieve them from Infisical:

```yaml

# roles/proxmox_access/tasks/secrets.yml

---

- name: Retrieve Proxmox root password from Infisical
  include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'PROXMOX_PASSWORD'
    secret_var_name: 'proxmox_password'
    infisical_project_id: "{{ infisical_project_id }}"
    infisical_env: "{{ infisical_env }}"
    infisical_path: "{{ infisical_path }}"

- name: Retrieve Proxmox username from Infisical
  include_tasks: "{{ playbook_dir }}/../tasks/infisical-secret-lookup.yml"
  vars:
    secret_name: 'PROXMOX_USERNAME'
    secret_var_name: 'proxmox_username'

```

### Pattern 2: Task File Organization

Break complex roles into focused task files:

```yaml

# roles/proxmox_cluster/tasks/main.yml

---

- name: Include prerequisite checks
  include_tasks: prerequisites.yml

- name: Include secret retrieval
  include_tasks: secrets.yml
  when: requires_secrets | default(false)

- name: Include primary tasks
  include_tasks: cluster_setup.yml

- name: Include verification
  include_tasks: verify.yml
  when: verify_after_changes | default(true)

```

### Pattern 3: Idempotent Shell Commands

When shell commands are necessary, ensure idempotency:

```yaml

- name: Create VLAN interface
  shell: |
    if ! ip link show {{ vlan_interface }} >/dev/null 2>&1; then
      ip link add link {{ parent_interface }} name {{ vlan_interface }} type vlan id {{ vlan_id }}
      ip link set {{ vlan_interface }} up
      echo "created"
    else
      echo "exists"
    fi
  register: vlan_create
  changed_when: "'created' in vlan_create.stdout"

```

### Pattern 4: Native Module Preference

Prefer native modules when available:

```yaml

# ✅ Good: Use native module

- name: Create Proxmox group
  community.proxmox.proxmox_group:
    name: "{{ item.name }}"
    state: present
    comment: "{{ item.comment }}"
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_password: "{{ proxmox_api_password }}"
  loop: "{{ proxmox_groups }}"

# ❌ Bad: Use shell when module exists

- name: Create Proxmox group
  command: pveum group add {{ item.name }}
  loop: "{{ proxmox_groups }}"

```

### Pattern 5: Declarative State Management

Define desired state, let the role converge to it:

```yaml

# Input: Desired state

system_users:
  - name: user1
    state: present
  - name: user2
    state: absent

# Role logic:

- name: Create present users
  user:
    name: "{{ item.name }}"
    state: present
  loop: "{{ system_users }}"
  when: item.state == 'present'

- name: Remove absent users
  user:
    name: "{{ item.name }}"
    state: absent
  loop: "{{ system_users }}"
  when: item.state == 'absent'

```

### Pattern 6: Error Handling

Explicit error handling with clear messages:

```yaml

- name: Join cluster
  command: pvecm add {{ primary_node_ip }} --use_ssh
  register: cluster_join
  failed_when:
    - cluster_join.rc != 0
    - "'already in a cluster' not in cluster_join.stderr"
  changed_when: cluster_join.rc == 0

- name: Display join result
  debug:
    msg: |
      Cluster join status: {{ 'Already member' if 'already in a cluster' in cluster_join.stderr else 'Successfully joined' }}

```

### Pattern 7: Conditional Execution

Use when conditions for role flexibility:

```yaml

# roles/proxmox_ceph/tasks/main.yml

---

- name: Initialize CEPH cluster
  include_tasks: init.yml
  when:
    - inventory_hostname == groups[cluster_group][0]
    - not ceph_initialized | default(false)

- name: Create monitors on all nodes
  include_tasks: monitors.yml
  when: ceph_monitors_enabled | default(true)

```

---

## Role Dependencies

Define role dependencies in `meta/main.yml`:

```yaml

# roles/proxmox_cluster/meta/main.yml

---
dependencies:
  - role: proxmox_repository
    vars:
      ensure_packages_updated: true

  - role: proxmox_network
    vars:
      ensure_corosync_network: true

```

**Note**: Use dependencies sparingly. Prefer explicit role ordering in playbooks for clarity.

---

## Role Documentation

Each role must have a README.md:

````text

# Role Name

Brief description of what this role manages.

## Requirements

- Proxmox VE 9.x

- Root access

- Specific prerequisites

## Role Variables

    ```yaml

## Required variables

```

variable_name: description

```text

```

# Optional variables

```text

```

optional_var: default_value

    ```text

## Dependencies

List of role dependencies.

## Example Playbook

```

    ```yaml
- hosts: proxmox
      roles:
  - role: role_name
          vars:
            variable: value
    ```

## Testing

How to test this role.

## License

MIT

## Author

Virgo-Core Team

````

---

## Configuration Organization

### Cluster-Specific Configuration

Store cluster-specific configuration in `group_vars/`:

```yaml

## group_vars/matrix_cluster.yml

---
cluster_name: "Matrix"
node_ids:
  foxtrot: 5
  golf: 6
  hotel: 7

proxmox_bridges: [...]
ceph_osds: {...}

```

### Global Configuration

Store global defaults in `group_vars/all.yml`:

```yaml

## group_vars/all.yml

---
infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
infisical_env: 'prod'

proxmox_version: "9.0"
ceph_version: "squid"

```

### Host-Specific Overrides

Store host-specific overrides in `host_vars/`:

```yaml

## host_vars/foxtrot.yml

---
node_id: 5
management_ip: 192.168.3.5
corosync_ip: 192.168.8.5

```

---

## Testing Roles

### Syntax Check

```bash
ansible-playbook --syntax-check playbooks/test-role.yml

```

### Check Mode (Dry Run)

```bash
ansible-playbook playbooks/test-role.yml --check --diff

```

### Role-Specific Testing

```yaml

## playbooks/test-system-user.yml

---

- name: Test system_user role
  hosts: localhost
  connection: local

  roles:

  - role: system_user
      vars:
        system_users:

    - name: testuser
            state: present
            shell: /bin/bash

```

### Ansible-lint

```bash
cd ansible
uv run ansible-lint roles/role_name/

```

---

## References

- [Ansible Philosophy](./ansible-philosophy.md)

- [Ansible Design Patterns](./ansible-design-patterns.md)

- [Ansible Playbook Design](./ansible-playbook-design.md)

- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)

---

**This document defines the authoritative structure and patterns for Ansible roles in Virgo-Core.**
