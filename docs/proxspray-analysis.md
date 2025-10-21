# ProxSpray Analysis: Patterns for Virgo-Core Integration

**Document Version:** 1.1
**Analysis Date:** 2025-10-20
**Last Updated:** 2025-10-20
**ProxSpray Repository:** https://github.com/ankraio/proxspray
**ProxSpray Version Analyzed:** Latest (Proxmox VE 8+, Ansible 2.18+)

---

## Important Note on Role Design

**This document includes an initial recommendation for a `proxmox_terraform` role which has been superseded by the Virgo-Core design standards.**

The correct approach is documented in:
- [Ansible Philosophy](./ansible-philosophy.md) - Core design principles (Roles = Components, not Tasks)
- [Ansible Role Design](./ansible-role-design.md) - Proper role structure with `proxmox_access` + `system_user` separation
- [Ansible Playbook Design](./ansible-playbook-design.md) - How to orchestrate roles for workflows
- [Ansible Migration Plan](./ansible-migration-plan.md) - Step-by-step migration guide

**Key Correction**:
- ❌ **Wrong**: `proxmox_terraform` role (task-oriented, conflates concerns)
- ✅ **Correct**: `proxmox_access` role (manages Proxmox API access) + `system_user` role (manages Linux users)
- ✅ **Orchestration**: `setup-terraform-automation.yml` playbook combines both roles

ProxSpray makes this same mistake with their `proxmox_terraform` role - we are improving on their design by properly separating concerns.

---

## Executive Summary

**ProxSpray** is a production-ready Ansible automation tool for deploying Proxmox VE clusters with integrated CEPH storage, advanced networking, and automated infrastructure provisioning. This analysis identifies patterns, implementations, and architectural decisions from ProxSpray that can enhance Virgo-Core's capabilities, while highlighting Virgo-Core's existing strengths that should be preserved.

### Key Findings

- **ProxSpray excels at**: Role-based architecture, cluster automation, CEPH setup, network interface management
- **Virgo-Core excels at**: Secrets management (Infisical), modern Python tooling (uv/mise), code quality (pre-commit), native Ansible modules
- **Recommended approach**: Adopt ProxSpray's role structure and automation patterns while maintaining Virgo-Core's modern tooling and security practices

---

## Repository Comparison

### Architectural Overview

| Aspect | ProxSpray | Virgo-Core | Winner |
|--------|-----------|------------|--------|
| **Structure** | Role-based playbooks | Individual playbooks | ProxSpray |
| **Secrets Management** | Hardcoded/vault variables | Infisical integration | Virgo-Core |
| **Python Tooling** | requirements.txt only | uv + pyproject.toml | Virgo-Core |
| **Task Automation** | None | mise task runner | Virgo-Core |
| **Code Quality** | None | pre-commit hooks | Virgo-Core |
| **Cluster Setup** | Fully automated | Manual/partial | ProxSpray |
| **CEPH Setup** | Automated (monitors/managers) | Not implemented | ProxSpray |
| **Network Setup** | Automated (bridges/VLAN/DHCP) | Partial automation | ProxSpray |
| **Testing** | None | ansible-lint configured | Virgo-Core |
| **Documentation** | Basic README | Comprehensive docs + CLAUDE.md | Virgo-Core |
| **Terraform Integration** | Automated user/token setup | Similar implementation | Tie |

### Directory Structure Comparison

#### ProxSpray Structure

```text
proxspray/
├── inventory-example/          # Multi-environment support
│   ├── inventory
│   ├── group_vars/all.yml
│   └── host_vars/
├── roles/                      # Modular, reusable roles
│   ├── admin/                  # User management
│   ├── proxmox/                # Repository management
│   ├── proxmox_cluster/        # Cluster formation + CEPH
│   ├── proxmox_interfaces/     # Network automation
│   ├── proxmox_terraform/      # Terraform user setup
│   ├── proxmox_ceph/           # CEPH storage
│   └── [8 more roles]
├── playbook.yml                # Main orchestration
└── setup-terraform-user.yml    # Standalone playbook
```

#### Virgo-Core Structure

```text
ansible/
├── playbooks/                  # Task-specific playbooks
│   ├── proxmox-build-template.yml
│   ├── proxmox-create-terraform-user.yml
│   ├── proxmox-enable-vlan-bridging.yml
│   ├── install-docker.yml
│   └── add-system-user.yml
├── inventory/
│   └── proxmox.yml             # Cluster definitions
├── tasks/
│   └── infisical-secret-lookup.yml
├── templates/
│   └── sudoers.j2
├── requirements.yml            # Galaxy collections
└── ansible.cfg
```

**Analysis**: ProxSpray's role-based structure provides better reusability and composition, while Virgo-Core's playbook approach is simpler but less maintainable at scale.

---

## ProxSpray Strengths to Emulate

### 1. Role-Based Architecture

**Pattern**: Decompose complex operations into focused, reusable roles with clear responsibilities.

#### ProxSpray Implementation

```yaml
# playbook.yml - Orchestration layer
- name: Setup Proxmox Infrastructure
  hosts: proxmox
  become: true
  roles:
    - role: proxmox                # Repository management
      tags: proxmox
    - role: proxmox_interfaces     # Network configuration
      tags: proxmox_interfaces
    - role: proxmox_terraform      # Terraform user setup
      tags: proxmox_terraform

- name: Setup Proxmox Cluster and Storage
  hosts: proxmox
  become: true
  roles:
    - role: proxmox_cluster        # Cluster formation
      tags: proxmox_cluster
    - role: proxmox_ceph           # CEPH storage
      tags: proxmox_ceph
```

#### Role Structure Example (`roles/proxmox_cluster/`)

```text
roles/proxmox_cluster/
├── tasks/
│   ├── main.yml              # Entry point with conditionals
│   ├── cluster_setup.yml     # Multi-node cluster formation
│   ├── ceph_setup.yml        # CEPH initialization
│   ├── production_setup.yml  # Production hardening
│   └── single_node.yml       # Single-node configuration
├── defaults/
│   └── main.yml              # Default variables
└── handlers/
    └── main.yml              # Service handlers
```

**Why This Matters for Virgo-Core**:
- Current playbooks duplicate logic (e.g., user creation, network config)
- Roles enable composition for different cluster types (nexus_cluster, doggos_cluster, matrix_cluster)
- Easier testing and maintenance with focused responsibilities

**Recommended Virgo-Core Roles**:

```text
ansible/roles/
├── proxmox_base/              # Repository, package management
├── proxmox_networking/        # Network interfaces, VLAN, bridges
├── proxmox_cluster/           # Cluster formation, corosync
├── proxmox_ceph/              # CEPH monitors, managers, OSDs
├── proxmox_terraform/         # Terraform user + API token
├── proxmox_templates/         # Cloud-init template creation
└── system_users/              # Admin user management
```

---

### 2. Comprehensive Cluster Automation

**Pattern**: Fully automate cluster formation with idempotency checks, error handling, and support for both new clusters and existing deployments.

#### ProxSpray Cluster Setup (`roles/proxmox_cluster/tasks/cluster_setup.yml`)

**Key Features**:
1. **Hostname resolution verification** before cluster creation
2. **Idempotent cluster status checks** (detect existing cluster membership)
3. **Automated /etc/hosts management** for all cluster nodes
4. **SSH key distribution** for passwordless cluster joins
5. **Certificate management** with automatic updates
6. **Service restart orchestration** (pve-cluster, corosync, pvedaemon, pveproxy)
7. **Firewall configuration** for cluster communication ports

**Critical Pattern - Cluster Status Detection**:

```yaml
# roles/proxmox_cluster/tasks/cluster_setup.yml:125-143
- name: Check existing cluster status
  ansible.builtin.command:
    cmd: pvecm status
  register: cluster_status
  failed_when: false
  changed_when: false

- name: Set cluster facts
  ansible.builtin.set_fact:
    is_cluster_member: "{{ cluster_status.rc == 0 and (cluster_nodes_check.stdout_lines | length > 1 or proxmox_cluster_name in cluster_status.stdout) }}"
    is_first_node: "{{ inventory_hostname == groups['proxmox'][0] }}"
    in_target_cluster: "{{ cluster_status.rc == 0 and proxmox_cluster_name in cluster_status.stdout }}"

# Only create cluster on first node if not already in target cluster
- name: Create new cluster on first node
  ansible.builtin.command:
    cmd: "pvecm create {{ proxmox_cluster_name }}"
  become: true
  when:
    - is_first_node
    - not in_target_cluster
```

**Pattern Benefits**:
- Safe to run repeatedly without breaking existing clusters
- Supports adding nodes to existing clusters
- Handles misconfigurations gracefully

**Virgo-Core Gap**: Current playbooks lack cluster formation automation. Matrix cluster was configured manually.

**Recommendation**: Create `roles/proxmox_cluster/` with:
- `cluster_setup.yml` - Cluster initialization and node joining
- `corosync_config.yml` - Corosync network configuration (VLAN 9)
- `cluster_verification.yml` - Health checks and quorum validation

---

### 3. Network Interface Automation

**Pattern**: Declarative network configuration with automated bridge creation, VLAN tagging, DHCP services, and firewall rules.

#### ProxSpray Network Configuration (`roles/proxmox_interfaces/`)

**Configuration Model** (`inventory-example/group_vars/all.yml`):

```yaml
# Declarative interface definitions
proxmox_interfaces:
  - name: vmbr1
    cidr: "192.168.10.0/24"
    vlan: 4000               # Creates vmbr0.4000 VLAN interface
  - name: vmbr2
    cidr: "192.168.20.0/24"
```

**Automated Operations**:

1. **Bridge Interface Creation**:

```yaml
# roles/proxmox_interfaces/tasks/main.yml:7-22
- name: Create Proxmox bridge interfaces in /etc/network/interfaces
  ansible.builtin.blockinfile:
    path: /etc/network/interfaces
    marker: "# {mark} ANSIBLE MANAGED BLOCK - {{ item.name }}"
    block: |
      auto {{ item.name }}
      iface {{ item.name }} inet static
          address {{ item.cidr }}
          bridge-ports {% if item.vlan is defined %}vmbr0.{{ item.vlan }}{% else %}none{% endif %}
          bridge-stp off
          bridge-fd 0
          {% if item.vlan is defined %}bridge-vlan-aware yes{% endif %}
    create: yes
  loop: "{{ proxmox_interfaces }}"
```

2. **Runtime Configuration** (idempotent):

```yaml
# Create VLAN interface if needed
- name: Create VLAN interface if needed
  ansible.builtin.shell: |
    if ! ip link show vmbr0.{{ item.vlan }} >/dev/null 2>&1; then
      ip link add link vmbr0 name vmbr0.{{ item.vlan }} type vlan id {{ item.vlan }}
      ip link set vmbr0.{{ item.vlan }} up
    fi
  loop: "{{ proxmox_interfaces }}"
  when: item.vlan is defined
```

3. **DHCP Server Configuration**:

```yaml
# Install and configure ISC DHCP server
- name: Install ISC DHCP server package
  ansible.builtin.apt:
    name: isc-dhcp-server
    update_cache: yes
    state: present

- name: Deploy dhcpd.conf for ISC DHCP server
  ansible.builtin.template:
    src: dhcpd.conf.j2
    dest: /etc/dhcp/dhcpd.conf
```

4. **Firewall and NAT**:

```yaml
# Enable NAT for internal networks
- name: Enable NAT for each internal interface via vmbr0
  ansible.builtin.iptables:
    table: nat
    chain: POSTROUTING
    source: "{{ item.cidr }}"
    out_interface: "vmbr0"
    jump: MASQUERADE
  loop: "{{ proxmox_interfaces }}"

# Persist iptables rules
- name: Save IPv4 iptables rules
  ansible.builtin.shell: iptables-save > /etc/iptables/rules.v4
```

**Virgo-Core Gap**: Current implementation only enables VLAN bridging; lacks automated bridge creation, DHCP, and firewall setup.

**Recommendation for Virgo-Core**:

Create `roles/proxmox_networking/` with Matrix-specific configuration:

```yaml
# Matrix cluster network configuration
proxmox_interfaces:
  - name: vmbr0
    cidr: "192.168.3.{{ node_id }}/24"
    gateway: "192.168.3.1"
    bridge_ports: "enp4s0"
    vlan_aware: true
    vlan_ids: "9"
    comment: "Management network"

  - name: vmbr1
    cidr: "192.168.5.{{ node_id }}/24"
    bridge_ports: "enp5s0f0np0"
    mtu: 9000
    comment: "CEPH Public network"

  - name: vmbr2
    cidr: "192.168.7.{{ node_id }}/24"
    bridge_ports: "enp5s0f1np1"
    mtu: 9000
    comment: "CEPH Private network"

  - name: vlan9
    cidr: "192.168.8.{{ node_id }}/24"
    vlan_raw_device: "vmbr0"
    comment: "Corosync network"
```

---

### 4. CEPH Storage Automation

**Pattern**: Automated CEPH cluster initialization with monitors, managers, and declarative pool configuration.

#### ProxSpray CEPH Setup (`roles/proxmox_ceph/tasks/ceph_setup.yml`)

**Key Operations**:

1. **CEPH Initialization**:

```yaml
- name: Initialize Ceph cluster on first node
  ansible.builtin.shell: |
    pveceph install --repository no-subscription
    pveceph init --network {{ ceph_network }}
  when:
    - is_ceph_first_node
    - not ceph_configured
```

2. **Monitor Creation** (all nodes):

```yaml
- name: Create initial Ceph monitor on first node
  ansible.builtin.command:
    cmd: "pveceph mon create"
  when:
    - is_ceph_first_node
    - not ceph_configured

- name: Create Ceph monitors on other nodes
  ansible.builtin.command:
    cmd: "pveceph mon create"
  when:
    - not is_ceph_first_node
    - not ceph_configured
```

3. **Manager Creation** (all nodes):

```yaml
- name: Create Ceph manager on first node
  ansible.builtin.command:
    cmd: "pveceph mgr create"
  when:
    - is_ceph_first_node
    - not ceph_configured
```

4. **Single-Node Configuration Support**:

```yaml
# Disable safety checks for single-node deployments
- name: Configure Ceph for single node
  ansible.builtin.shell: |
    ceph config set global mon_allow_pool_size_one true
    ceph config set global osd_crush_chooseleaf_type 0
  when:
    - groups['proxmox'] | length == 1
    - not ceph_configured
```

**Configuration Model** (`inventory-example/group_vars/all.yml`):

```yaml
# Multi-node cluster (production)
ceph_cluster_enabled: true
ceph_network: "192.168.10.0/24"
ceph_pools:
  - name: vm_data
    pg_num: 32
    size: 3       # Replicate across 3 nodes
    min_size: 2   # Minimum 2 replicas required

# Single-node cluster (development)
ceph_pools:
  - name: vm_data
    pg_num: 32
    size: 1       # No replication
    min_size: 1
```

**ProxSpray Weakness**: OSD creation left as manual step with debug message:

```yaml
- name: Create OSD on available disks (manual step required)
  ansible.builtin.debug:
    msg: |
      To create OSDs, run manually:
      {% for line in available_disks.stdout_lines %}
      pveceph osd create {{ line.split()[0] }}
      {% endfor %}
```

**Virgo-Core Gap**: No CEPH automation implemented. Manual configuration performed.

**Recommendation for Matrix Cluster**:

Create `roles/proxmox_ceph/` with **fully automated OSD creation** (improve on ProxSpray):

```yaml
# Matrix cluster CEPH configuration
ceph_network: "192.168.5.0/24"          # Public network (vmbr1)
ceph_cluster_network: "192.168.7.0/24"  # Private network (vmbr2)

# Node-specific OSD configuration
ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      db_device: null
      partitions: 2  # Create 2 OSDs per NVMe
    - device: /dev/nvme2n1
      db_device: null
      partitions: 2
  golf:
    - device: /dev/nvme1n1
      partitions: 2
    - device: /dev/nvme2n1
      partitions: 2
  hotel:
    - device: /dev/nvme1n1
      partitions: 2
    - device: /dev/nvme2n1
      partitions: 2

# Pool configuration
ceph_pools:
  - name: vm_ssd
    pg_num: 128
    pgp_num: 128
    size: 3
    min_size: 2
    application: rbd
```

**Implementation Tasks**:

```yaml
# roles/proxmox_ceph/tasks/osd_setup.yml
- name: Create partitions on CEPH disks
  community.general.parted:
    device: "{{ item.device }}"
    number: "{{ partition_num }}"
    state: present
    part_end: "{{ partition_size }}"
  loop: "{{ ceph_osds[inventory_hostname_short] }}"
  loop_control:
    index_var: partition_num

- name: Create CEPH OSDs
  ansible.builtin.command:
    cmd: "pveceph osd create {{ item.device }}{{ partition_num }}"
  loop: "{{ ceph_osds[inventory_hostname_short] }}"
```

---

### 5. Terraform User and API Token Automation

**Pattern**: API-driven user creation with automated token generation and environment file export.

#### ProxSpray Implementation (`roles/proxmox_terraform/tasks/main.yml`)

**Key Features**:
1. **API-based authentication** using Proxmox ticket system
2. **Automated user creation** with error handling for existing users
3. **API token generation** with automatic deletion/recreation
4. **Environment file export** for Terraform integration
5. **Idempotent operations** with status code handling

**Authentication Pattern**:

```yaml
- name: Get Proxmox authentication ticket
  ansible.builtin.uri:
    url: "https://localhost:8006/api2/json/access/ticket"
    method: POST
    body_format: form-urlencoded
    body:
      username: "{{ proxmox_api_user }}"
      password: "{{ proxmox_api_password }}"
    validate_certs: false
    status_code: [200, 401]
  register: proxmox_auth

- name: Set authentication headers
  ansible.builtin.set_fact:
    proxmox_auth_headers:
      Cookie: "PVEAuthCookie={{ proxmox_auth.json.data.ticket }}"
      CSRFPreventionToken: "{{ proxmox_auth.json.data.CSRFPreventionToken }}"
```

**User and Token Creation**:

```yaml
- name: Create terraform user in Proxmox
  ansible.builtin.uri:
    url: "https://localhost:8006/api2/json/access/users"
    method: POST
    headers: "{{ proxmox_auth_headers }}"
    body:
      userid: "terraform@pve"
      password: "{{ terraform_user_password }}"
    status_code: [200, 500]  # 500 = user exists

- name: Create API token
  ansible.builtin.uri:
    url: "https://localhost:8006/api2/json/access/users/terraform@pve/token/terraform-token"
    method: POST
    headers: "{{ proxmox_auth_headers }}"
    body:
      privsep: "0"  # No privilege separation
    status_code: [200, 400, 500]
  register: terraform_token_result
```

**Environment File Export**:

```yaml
- name: Store terraform API token locally
  ansible.builtin.copy:
    content: |
      export TF_VAR_proxmox_url="https://localhost:8006/api2/json"
      export TF_VAR_proxmox_token_id="terraform@pve!terraform-token"
      export TF_VAR_proxmox_token_secret="{{ terraform_api_token }}"
    dest: "{{ lookup('env', 'HOME') }}/tmp/.proxmox-terraform/proxmox-{{ inventory_hostname_short }}"
    mode: '0600'
```

**Virgo-Core Comparison**: Similar implementation but uses:
- **Community.proxmox modules** for better idempotency (group, ACL management)
- **Infisical secrets** instead of hardcoded passwords
- **More comprehensive role/permission configuration**
- **PAM realm** user creation for SSH + API access

**Verdict**: Virgo-Core's implementation is **superior** due to native modules and secrets management.

**Recommendation**: Maintain Virgo-Core's approach but add ProxSpray's environment file export pattern for easier Terraform integration.

---

### 6. Multi-Environment Inventory Structure

**Pattern**: Template-based inventory system supporting multiple deployment environments with shared and environment-specific variables.

#### ProxSpray Inventory Structure

```text
inventory-example/
├── inventory                # Host definitions
├── group_vars/
│   └── all.yml             # Shared variables
├── host_vars/
│   ├── srv01.example.com.yml
│   ├── srv02.example.com.yml
│   └── srv03.example.com.yml
└── README.md               # Setup instructions

# Usage for multiple environments
inventory/
├── production/
│   ├── inventory
│   ├── group_vars/all.yml
│   └── host_vars/
├── staging/
│   ├── inventory
│   └── group_vars/all.yml
└── development/
    ├── inventory
    └── group_vars/all.yml
```

**Inventory File** (`inventory-example/inventory`):

```ini
[all]
srv01.example.com ansible_host=192.168.1.101
srv02.example.com ansible_host=192.168.1.102
srv03.example.com ansible_host=192.168.1.103

[proxmox]
srv01.example.com
srv02.example.com
srv03.example.com

[public_nodes]
# Public-facing infrastructure

[haproxy]
# Load balancer nodes
```

**Virgo-Core Current Structure** (`ansible/inventory/proxmox.yml`):

```yaml
all:
  children:
    nexus_cluster:
      hosts:
        alpha:
        bravo:
    doggos_cluster:
      hosts:
        holly:
        lloyd:
        mable:
    matrix_cluster:
      hosts:
        foxtrot:
        golf:
        hotel:
```

**Analysis**:
- Virgo-Core uses YAML format (cleaner, more readable)
- Virgo-Core has multiple clusters in one inventory (good for multi-cluster management)
- ProxSpray's template approach is better for onboarding and documentation

**Recommendation**: Maintain Virgo-Core's YAML format but add:

```text
ansible/
├── inventory/
│   ├── proxmox.yml              # Current multi-cluster inventory
│   ├── group_vars/
│   │   ├── all.yml              # Global variables
│   │   ├── matrix_cluster.yml   # Matrix-specific config
│   │   ├── doggos_cluster.yml   # Doggos-specific config
│   │   └── nexus_cluster.yml    # Nexus-specific config
│   └── host_vars/
│       ├── foxtrot.yml          # Node-specific overrides
│       ├── golf.yml
│       └── hotel.yml
└── inventory-example/
    └── README.md                # Setup guide for new clusters
```

---

### 7. Repository and Package Management

**Pattern**: Clean repository configuration with automatic package updates and cleanup.

#### ProxSpray Implementation (`roles/proxmox/tasks/main.yml`)

**Key Operations**:

1. **Remove conflicting repositories**:

```yaml
- name: Remove duplicate/existing repository files
  ansible.builtin.file:
    path: "{{ item }}"
    state: absent
  loop:
    - /etc/apt/sources.list.d/pve-community.list
    - /etc/apt/sources.list.d/pve-no-subscription.list
    - /etc/apt/sources.list.d/ceph.list
    - /etc/apt/sources.list.d/pve-enterprise.list
```

2. **Disable enterprise repositories**:

```yaml
# Handle both .list and .sources formats
- name: Disable Proxmox Enterprise repository (.sources format)
  ansible.builtin.command:
    cmd: mv /etc/apt/sources.list.d/pve-enterprise.sources /etc/apt/sources.list.d/pve-enterprise.sources.disabled
  args:
    creates: /etc/apt/sources.list.d/pve-enterprise.sources.disabled
```

3. **Add no-subscription repositories via templates**:

```yaml
- name: Add Proxmox VE No-Subscription repository
  ansible.builtin.template:
    src: pve-no-subscription.list.j2
    dest: /etc/apt/sources.list.d/pve-no-subscription.list
  notify: update apt cache
```

**Template** (`roles/proxmox/templates/pve-no-subscription.list.j2`):

```jinja2
# Proxmox VE No-Subscription Repository
deb http://download.proxmox.com/debian/pve {{ ansible_distribution_release }} pve-no-subscription
```

4. **Install latest packages**:

```yaml
- name: Install latest Proxmox VE packages
  ansible.builtin.apt:
    name:
      - proxmox-ve
      - postfix
      - open-iscsi
    state: latest
    update_cache: yes
```

**Virgo-Core Gap**: No automated repository management role.

**Recommendation**: Create `roles/proxmox_base/` for:
- Repository configuration (no-subscription repos for Proxmox VE 9.x)
- Base package installation
- System updates and cleanup
- Kernel parameter configuration

---

### 8. Admin User Management

**Pattern**: Declarative user creation with SSH key management and sudo configuration.

#### ProxSpray Implementation (`roles/admin/`)

**Configuration Model**:

```yaml
# group_vars/all.yml
admin_users:
  - name: admin
    public_key: "ssh-rsa AAAAB3... admin@example.com"
    sudo: true
    shell: /bin/bash
    groups: []
```

**Tasks** (`roles/admin/tasks/main.yml`):

```yaml
- name: Create admin users
  ansible.builtin.user:
    name: "{{ item.name }}"
    shell: "{{ item.shell | default('/bin/bash') }}"
    groups: "{{ item.groups | default([]) | join(',') }}"
    append: true
    create_home: true
  loop: "{{ admin_users }}"

- name: Add SSH public keys
  ansible.posix.authorized_key:
    user: "{{ item.name }}"
    state: present
    key: "{{ item.public_key }}"
  loop: "{{ admin_users }}"
  when: item.public_key is defined

- name: Configure passwordless sudo
  ansible.builtin.lineinfile:
    path: /etc/sudoers.d/admin-users
    line: "{{ item.name }} ALL=(ALL) NOPASSWD:ALL"
    create: true
    validate: 'visudo -cf %s'
    mode: '0440'
  loop: "{{ admin_users }}"
  when: item.sudo | default(false)
```

**Virgo-Core Comparison**: Has `playbooks/add-system-user.yml` but less comprehensive than role-based approach.

**Recommendation**: Convert to `roles/system_users/` with:
- Support for multiple user types (admin, service accounts, developers)
- SSH key management from files or Infisical
- Flexible sudo rules configuration
- User group management

---

## Virgo-Core Strengths to Preserve

### 1. Infisical Secrets Management

**Implementation**: `ansible/tasks/infisical-secret-lookup.yml`

```yaml
- name: Retrieve secret from Infisical
  ansible.builtin.shell: |
    infisical secrets get {{ secret_name }} \
      --projectId {{ infisical_project_id }} \
      --env {{ infisical_env }} \
      --path {{ infisical_path }} \
      --plain
  register: infisical_secret
  changed_when: false
  no_log: true

- name: Set secret as Ansible variable
  ansible.builtin.set_fact:
    "{{ secret_var_name }}": "{{ infisical_secret.stdout }}"
  no_log: true
```

**Why This Is Critical**:
- ProxSpray hardcodes passwords in variables (`terraform_user_password: "terraform123!"`)
- Virgo-Core's Infisical integration provides:
  - Centralized secrets management
  - Audit logging
  - Automatic rotation support
  - Environment-specific secrets (dev/staging/prod)

**Integration Recommendation**: Add Infisical lookups to **all** new roles:

```yaml
# roles/proxmox_cluster/defaults/main.yml
proxmox_admin_password: "{{ lookup('infisical', 'PROXMOX_PASSWORD') }}"
ceph_admin_keyring: "{{ lookup('infisical', 'CEPH_ADMIN_KEYRING') }}"
```

---

### 2. Modern Python Tooling (uv + pyproject.toml)

**Virgo-Core**: `pyproject.toml` with `uv` for dependency management

```toml
[project]
dependencies = [
    "ansible>=11.1.0",
    "infisical-python>=2.3.3",
]

[tool.uv]
dev-dependencies = [
    "ansible-lint>=24.12.2",
    "yamllint>=1.35.1",
]
```

**ProxSpray**: Only `requirements.txt` with `ansible>=2.10`

**Advantages of uv**:
- Lockfile for reproducible builds (`uv.lock`)
- Faster dependency resolution
- Better dependency conflict detection
- Dev dependencies separation
- Python version management

**Recommendation**: Maintain `uv` for all Python dependencies. Do **not** regress to `requirements.txt`.

---

### 3. Mise Task Runner

**Virgo-Core**: `.mise.toml` with comprehensive task automation

```toml
[tasks.ansible-ping]
description = "Test connectivity to all Proxmox hosts"
run = "cd ansible && uv run ansible all -i inventory/proxmox.yml -m ping"

[tasks.full-check]
description = "Run all validation checks"
depends = ["fmt-all", "validate-all", "lint-all", "docs-check", "infisical-scan"]
```

**ProxSpray**: No task automation. Users must remember complex commands.

**Advantages**:
- Consistent command interface across developers
- Self-documenting (`mise tasks`)
- Dependency management between tasks
- Tool version management

**Recommendation**: Create mise tasks for new role operations:

```toml
[tasks."cluster:init"]
description = "Initialize Proxmox cluster on Matrix nodes"
run = "cd ansible && uv run ansible-playbook -i inventory/proxmox.yml playbooks/cluster-init.yml --limit matrix_cluster"

[tasks."ceph:deploy"]
description = "Deploy CEPH storage on Matrix cluster"
run = "cd ansible && uv run ansible-playbook -i inventory/proxmox.yml playbooks/ceph-deploy.yml --limit matrix_cluster"
```

---

### 4. Pre-commit Hooks and Code Quality

**Virgo-Core**: `.pre-commit-config.yaml` with multiple checks

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: check-yaml
      - id: detect-private-key

  - repo: local
    hooks:
      - id: mise-terraform-fmt
        name: Terraform Format
        entry: mise run fmt
```

**ProxSpray**: No code quality automation.

**Advantages**:
- Prevents common errors (YAML syntax, trailing whitespace)
- Security scanning (private keys, AWS credentials)
- Automatic formatting
- Runs on every commit

**Recommendation**: Add ansible-specific hooks:

```yaml
repos:
  - repo: https://github.com/ansible/ansible-lint
    rev: v24.12.2
    hooks:
      - id: ansible-lint
        files: \.(yaml|yml)$
        args: [--profile=production]
```

---

### 5. Community.proxmox Native Modules

**Virgo-Core**: Uses native Ansible modules where available

```yaml
# ansible/playbooks/proxmox-create-terraform-user.yml:173-183
- name: Create terraform-users group in Proxmox
  community.proxmox.proxmox_group:
    name: "{{ proxmox_group_name }}"
    state: present
    comment: "Group for Terraform automation users"
    api_host: "{{ proxmox_api_host }}"
    api_user: "{{ proxmox_api_user }}"
    api_password: "{{ proxmox_api_password }}"
  delegate_to: localhost
```

**ProxSpray**: Heavy reliance on `shell` and `command` modules

```yaml
# roles/proxmox_cluster/tasks/cluster_setup.yml:214-224
- name: Create new cluster on first node
  ansible.builtin.command:
    cmd: "pvecm create {{ proxmox_cluster_name }}"
```

**Advantages of Native Modules**:
- Better idempotency (check-mode support)
- Structured error handling
- Parameter validation
- State management (present/absent)
- API-based (no shell parsing)

**Recommendation**: Use `community.proxmox` modules wherever possible:
- `proxmox_group` - Group management
- `proxmox_access_acl` - Permission management
- `proxmox_user` - User creation (when PAM support is added)
- `proxmox_pool` - Resource pool management

**When to Use Shell/Command**:
- No native module exists (e.g., `pvecm`, `pveceph`)
- Complex operations requiring pipelines
- Temporary workarounds until modules are available

---

## ProxSpray Weaknesses to Avoid

### 1. Hardcoded Secrets

**Anti-Pattern** (`roles/proxmox_terraform/defaults/main.yml`):

```yaml
# Default variables for proxmox_terraform role
terraform_user_password: "terraform123!"  # ❌ NEVER do this
```

**Problem**:
- Secrets committed to version control
- No audit trail for access
- Difficult to rotate
- Same password across environments

**Virgo-Core Solution**: Use Infisical for all secrets

```yaml
# roles/proxmox_terraform/defaults/main.yml
terraform_user_password: "{{ lookup('infisical', 'TERRAFORM_USER_PASSWORD') }}"
```

---

### 2. Manual CEPH OSD Creation

**Anti-Pattern** (`roles/proxmox_ceph/tasks/ceph_setup.yml:115-122`):

```yaml
- name: Create OSD on available disks (manual step required)
  ansible.builtin.debug:
    msg: |
      To create OSDs, run manually:
      pveceph osd create /dev/sda
```

**Problem**:
- Defeats purpose of automation
- Error-prone manual process
- Inconsistent deployments
- No idempotency

**Virgo-Core Solution**: Fully automate OSD creation with declarative configuration

```yaml
# Matrix cluster OSD configuration
ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

# Automated creation task
- name: Create CEPH OSDs from configuration
  ansible.builtin.command:
    cmd: "pveceph osd create {{ item.device }}{{ partition_id }}"
    creates: "/var/lib/ceph/osd/ceph-{{ osd_id }}"
  loop: "{{ ceph_osds[inventory_hostname_short] }}"
```

---

### 3. Excessive Shell Command Usage

**Anti-Pattern** (`roles/proxmox_interfaces/tasks/main.yml`):

```yaml
- name: Create VLAN interface if needed
  ansible.builtin.shell: |
    if ! ip link show vmbr0.{{ item.vlan }} >/dev/null 2>&1; then
      ip link add link vmbr0 name vmbr0.{{ item.vlan }} type vlan id {{ item.vlan }}
      ip link set vmbr0.{{ item.vlan }} up
    fi
```

**Problem**:
- Limited idempotency checking
- No check-mode support
- Shell-specific syntax
- Harder to test

**Better Approach**: Use network modules when available

```yaml
- name: Create VLAN interface
  community.general.nmcli:
    conn_name: "vmbr0.{{ item.vlan }}"
    type: vlan
    vlanid: "{{ item.vlan }}"
    vlandev: vmbr0
    state: present
  when: item.vlan is defined
```

**When Shell Is Acceptable**:
- No native module exists
- Operation is truly idempotent (with conditional checks)
- Temporary until better solution available

---

### 4. Lack of Testing Infrastructure

**ProxSpray Gap**: No testing framework

**Problems**:
- No validation before production deployment
- Manual testing required
- Regression risk
- Difficult to verify changes

**Virgo-Core Advantage**: ansible-lint configured

**Recommendation**: Add comprehensive testing:

```yaml
# .mise.toml
[tasks."test:syntax"]
description = "Validate Ansible syntax"
run = "cd ansible && uv run ansible-playbook --syntax-check playbooks/*.yml"

[tasks."test:lint"]
description = "Run ansible-lint"
run = "cd ansible && uv run ansible-lint playbooks/ roles/"

[tasks."test:molecule"]
description = "Run molecule tests"
run = "cd ansible && uv run molecule test"
```

**Future Enhancement**: Add Molecule for role testing

```text
ansible/roles/proxmox_cluster/
├── molecule/
│   └── default/
│       ├── molecule.yml
│       ├── converge.yml
│       └── verify.yml
```

---

### 5. Limited Error Handling

**Anti-Pattern**: Overuse of `failed_when: false`

```yaml
- name: Join cluster on other nodes
  ansible.builtin.shell: |
    timeout 60 pvecm add {{ primary_node }}
  failed_when: false  # ❌ Silently ignores all errors
```

**Problem**:
- Hides real failures
- Makes debugging difficult
- Creates inconsistent state

**Better Approach**: Explicit error handling

```yaml
- name: Join cluster on other nodes
  ansible.builtin.shell: |
    pvecm add {{ primary_node }}
  register: cluster_join
  failed_when:
    - cluster_join.rc != 0
    - "'already in a cluster' not in cluster_join.stderr"
  changed_when: cluster_join.rc == 0
```

---

## Integration Recommendations

### Phase 1: Role Conversion (Immediate)

**Objective**: Convert existing Virgo-Core playbooks to reusable roles while maintaining Infisical integration.

#### 1.1 Create Base Role Structure

```bash
mkdir -p ansible/roles/{proxmox_base,proxmox_networking,proxmox_cluster,proxmox_ceph,proxmox_terraform,system_users}

for role in ansible/roles/*/; do
  mkdir -p "$role"/{tasks,defaults,handlers,templates,vars}
  touch "$role"/tasks/main.yml
  touch "$role"/defaults/main.yml
done
```

#### 1.2 Convert Terraform User Playbook to Role

**Source**: `ansible/playbooks/proxmox-create-terraform-user.yml`
**Target**: `ansible/roles/proxmox_terraform/`

```yaml
# ansible/roles/proxmox_terraform/tasks/main.yml
---
- name: Include Infisical secret lookups
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/secrets.yml"

- name: Include Linux user creation
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/linux_user.yml"

- name: Include Proxmox PVE user creation
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/pve_user.yml"

- name: Include API token generation
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/api_token.yml"

- name: Include environment file export
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/env_export.yml"
```

```yaml
# ansible/roles/proxmox_terraform/defaults/main.yml
---
system_username: "terraform"
system_user_shell: "/bin/bash"
proxmox_role_name: "TerraformUser"
proxmox_group_name: "terraform-users"
proxmox_token_name: "token"

# Infisical configuration
infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
infisical_env: 'prod'
infisical_path: '/{{ cluster_name }}'
```

**Usage**:

```yaml
# ansible/playbooks/setup-terraform-user.yml
---
- name: Setup Terraform User on All Clusters
  hosts: all
  roles:
    - role: proxmox_terraform
      vars:
        cluster_name: "{{ group_names | select('search', '_cluster') | first | regex_replace('_cluster$', '') }}"
```

#### 1.3 Convert Network Playbook to Role

**Source**: `ansible/playbooks/proxmox-enable-vlan-bridging.yml`
**Target**: `ansible/roles/proxmox_networking/`

**Enhance with ProxSpray's bridge automation**:

```yaml
# ansible/roles/proxmox_networking/tasks/main.yml
---
- name: Include network interface configuration
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/interfaces.yml"

- name: Include VLAN configuration
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/vlans.yml"

- name: Include bridge configuration
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/bridges.yml"

- name: Include MTU configuration
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/mtu.yml"
  when: network_jumbo_frames_enabled | default(false)
```

```yaml
# ansible/roles/proxmox_networking/defaults/main.yml
---
# Matrix cluster network configuration
network_interfaces:
  management:
    bridge: vmbr0
    physical_port: enp4s0
    address: "192.168.3.{{ node_id }}/24"
    gateway: "192.168.3.1"
    vlan_aware: true
    vlan_ids: "9"
    comment: "Management network"

  ceph_public:
    bridge: vmbr1
    physical_port: enp5s0f0np0
    address: "192.168.5.{{ node_id }}/24"
    mtu: 9000
    comment: "CEPH Public network"

  ceph_private:
    bridge: vmbr2
    physical_port: enp5s0f1np1
    address: "192.168.7.{{ node_id }}/24"
    mtu: 9000
    comment: "CEPH Private network"

# VLAN configuration
vlans:
  - id: 9
    raw_device: vmbr0
    address: "192.168.8.{{ node_id }}/24"
    comment: "Corosync network"

# Node ID mapping
node_ids:
  foxtrot: 5
  golf: 6
  hotel: 7
```

---

### Phase 2: Cluster Automation (High Priority)

**Objective**: Implement comprehensive Proxmox cluster formation for Matrix cluster.

#### 2.1 Create Cluster Role

```yaml
# ansible/roles/proxmox_cluster/tasks/main.yml
---
- name: Verify prerequisites
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/prerequisites.yml"

- name: Configure /etc/hosts
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/hosts_config.yml"

- name: Initialize cluster (first node only)
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/cluster_init.yml"
  when: inventory_hostname == groups[cluster_group][0]

- name: Join cluster (other nodes)
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/cluster_join.yml"
  when: inventory_hostname != groups[cluster_group][0]

- name: Configure corosync
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/corosync.yml"

- name: Verify cluster health
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/verify.yml"
```

#### 2.2 Matrix-Specific Configuration

```yaml
# ansible/group_vars/matrix_cluster.yml
---
cluster_name: "Matrix"
cluster_group: "matrix_cluster"

# Corosync configuration
corosync_network: "192.168.8.0/24"  # VLAN 9
corosync_ring:
  - interface: vlan9
    bindnetaddr: "192.168.8.0"
    mcastaddr: "239.192.8.1"
    mcastport: 5405

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

#### 2.3 Implementation Pattern

```yaml
# ansible/roles/proxmox_cluster/tasks/prerequisites.yml
---
- name: Check Proxmox VE is installed
  ansible.builtin.stat:
    path: /usr/bin/pvecm
  register: pvecm_binary
  failed_when: not pvecm_binary.stat.exists

- name: Verify minimum node count
  ansible.builtin.assert:
    that:
      - groups[cluster_group] | length >= 3
    fail_msg: "Matrix cluster requires at least 3 nodes for quorum"

- name: Check network connectivity
  ansible.builtin.wait_for:
    host: "{{ hostvars[item].corosync_ip }}"
    port: 22
    timeout: 10
  loop: "{{ groups[cluster_group] }}"
  delegate_to: localhost
```

```yaml
# ansible/roles/proxmox_cluster/tasks/hosts_config.yml
---
- name: Ensure cluster nodes in /etc/hosts
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: "^{{ item.management_ip }}\\s+"
    line: "{{ item.management_ip }} {{ item.hostname }} {{ item.name }}"
    state: present
  loop: "{{ cluster_nodes }}"

- name: Ensure corosync IPs in /etc/hosts
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: "^{{ item.corosync_ip }}\\s+"
    line: "{{ item.corosync_ip }} {{ item.name }}-corosync"
    state: present
  loop: "{{ cluster_nodes }}"
```

---

### Phase 3: CEPH Storage Automation (High Priority)

**Objective**: Fully automate CEPH deployment for Matrix cluster with 12 OSDs (4 per node).

#### 3.1 Create CEPH Role

```yaml
# ansible/roles/proxmox_ceph/tasks/main.yml
---
- name: Install CEPH packages
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/install.yml"

- name: Initialize CEPH cluster
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/init.yml"
  when: inventory_hostname == groups[cluster_group][0]

- name: Create CEPH monitors
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/monitors.yml"

- name: Create CEPH managers
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/managers.yml"

- name: Prepare OSD disks
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/osd_prepare.yml"

- name: Create OSDs
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/osd_create.yml"

- name: Create CEPH pools
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/pools.yml"
  when: inventory_hostname == groups[cluster_group][0]

- name: Verify CEPH health
  ansible.builtin.include_tasks: "{{ role_path }}/tasks/verify.yml"
```

#### 3.2 Matrix CEPH Configuration

```yaml
# ansible/group_vars/matrix_cluster.yml (continued)
---
# CEPH configuration
ceph_network: "192.168.5.0/24"          # vmbr1 - Public
ceph_cluster_network: "192.168.7.0/24"  # vmbr2 - Private

# OSD configuration (4 OSDs per node = 12 total)
ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      partitions: 2
      db_device: null
      wal_device: null
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      db_device: null
      wal_device: null
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
    size: 3           # Replicate across 3 nodes
    min_size: 2       # Minimum 2 replicas required
    application: rbd
    crush_rule: replicated_rule
  - name: vm_containers
    pg_num: 64
    pgp_num: 64
    size: 3
    min_size: 2
    application: rbd
```

#### 3.3 OSD Creation Implementation

```yaml
# ansible/roles/proxmox_ceph/tasks/osd_create.yml
---
- name: Check existing OSDs
  ansible.builtin.command:
    cmd: "pveceph osd ls"
  register: existing_osds
  changed_when: false
  failed_when: false

- name: Create partitions on OSD devices
  community.general.parted:
    device: "{{ item.device }}"
    number: "{{ partition_idx + 1 }}"
    state: present
    part_start: "{{ (partition_idx * 50) }}%"
    part_end: "{{ ((partition_idx + 1) * 50) }}%"
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) }}"
  loop_control:
    index_var: osd_idx
  vars:
    partition_idx: "{{ osd_idx % item.partitions }}"
  when:
    - item.partitions is defined
    - item.partitions > 1

- name: Create OSDs from partitions
  ansible.builtin.command:
    cmd: >
      pveceph osd create {{ item.0.device }}{{ item.1 + 1 }}
      {% if item.0.db_device %}--db_dev {{ item.0.db_device }}{% endif %}
      {% if item.0.wal_device %}--wal_dev {{ item.0.wal_device }}{% endif %}
  loop: "{{ ceph_osds[inventory_hostname_short] | default([]) | subelements('partitions', skip_missing=True) }}"
  register: osd_create
  changed_when: "'successfully created' in osd_create.stdout"
  failed_when:
    - osd_create.rc != 0
    - "'already in use' not in osd_create.stderr"
```

---

### Phase 4: Testing and Validation

**Objective**: Ensure all roles work correctly before production deployment.

#### 4.1 Ansible-lint Configuration

```yaml
# ansible/.ansible-lint
---
profile: production

exclude_paths:
  - .cache/
  - .venv/
  - venv/

skip_list:
  - yaml[line-length]  # Allow long lines in some cases

warn_list:
  - experimental  # Warn about experimental features
  - role-name     # Warn about role naming

enable_list:
  - no-changed-when
  - no-handler
  - fqcn-builtins
```

#### 4.2 Mise Test Tasks

```toml
# .mise.toml (additions)
[tasks."ansible:syntax"]
description = "Check Ansible playbook syntax"
run = """
cd ansible
for playbook in playbooks/*.yml; do
  echo "Checking $playbook..."
  uv run ansible-playbook --syntax-check "$playbook"
done
"""

[tasks."ansible:lint"]
description = "Run ansible-lint on playbooks and roles"
run = "cd ansible && uv run ansible-lint playbooks/ roles/"

[tasks."ansible:test-matrix"]
description = "Test Matrix cluster configuration (check mode)"
run = """
cd ansible
uv run ansible-playbook \
  -i inventory/proxmox.yml \
  playbooks/cluster-init.yml \
  --limit matrix_cluster \
  --check \
  --diff
"""
```

#### 4.3 Pre-commit Integration

```yaml
# .pre-commit-config.yaml (additions)
repos:
  - repo: https://github.com/ansible/ansible-lint
    rev: v24.12.2
    hooks:
      - id: ansible-lint
        name: Ansible Lint
        files: \.(yaml|yml)$
        args:
          - --profile=production
          - --force-color
        exclude: ^(terraform/|docs/)
```

---

### Phase 5: Documentation Updates

**Objective**: Document new roles and usage patterns.

#### 5.1 Role Documentation

```markdown
# ansible/roles/proxmox_cluster/README.md

# Proxmox Cluster Role

Automates Proxmox VE cluster formation with corosync configuration.

## Requirements

- Proxmox VE 9.x installed on all nodes
- Minimum 3 nodes for quorum
- Network connectivity between all nodes
- Root SSH access

## Role Variables

```yaml
# Required
cluster_name: "MyCluster"
cluster_group: "proxmox"
cluster_nodes:
  - name: node1
    hostname: node1.example.com
    management_ip: 192.168.1.10
    corosync_ip: 192.168.10.10
    node_id: 1
```

## Example Playbook

```yaml
- hosts: proxmox
  roles:
    - role: proxmox_cluster
      vars:
        cluster_name: "Production"
```

## Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/cluster-init.yml

# Check mode (dry run)
ansible-playbook playbooks/cluster-init.yml --check

# Run on single cluster
ansible-playbook playbooks/cluster-init.yml --limit matrix_cluster
```
```

#### 5.2 Update CLAUDE.md

```markdown
# CLAUDE.md (additions)

## Ansible Roles

This repository uses a role-based Ansible architecture for reusability and composability:

### Available Roles

- **proxmox_base**: Repository configuration, package management, base system setup
- **proxmox_networking**: Network interfaces, bridges, VLANs, MTU configuration
- **proxmox_cluster**: Cluster formation, corosync, quorum management
- **proxmox_ceph**: CEPH storage deployment (monitors, managers, OSDs, pools)
- **proxmox_terraform**: Terraform user and API token creation
- **system_users**: Admin user management with SSH keys and sudo

### Role Usage Patterns

```bash
# Initialize Matrix cluster
mise run ansible:cluster-init

# Deploy CEPH storage
mise run ansible:ceph-deploy

# Setup terraform user
ansible-playbook -i inventory/proxmox.yml playbooks/setup-terraform-user.yml --limit matrix_cluster
```

### Secrets Management

All roles integrate with Infisical for secrets:
- Proxmox passwords
- API tokens
- CEPH keyrings
- SSH private keys

Configure Infisical in `group_vars/<cluster_name>.yml`:

```yaml
infisical_project_id: 'your-project-id'
infisical_env: 'prod'
infisical_path: '/matrix-cluster'
```
```

---

## Implementation Roadmap

### Immediate (Week 1-2)

- [ ] Create role directory structure
- [ ] Convert `proxmox-create-terraform-user.yml` to role
- [ ] Convert `proxmox-enable-vlan-bridging.yml` to role
- [ ] Add ansible-lint to pre-commit hooks
- [ ] Create mise tasks for ansible operations

### High Priority (Week 3-4)

- [ ] Implement `proxmox_networking` role with Matrix config
- [ ] Implement `proxmox_cluster` role
- [ ] Test cluster formation on Matrix nodes
- [ ] Document role usage in CLAUDE.md

### Critical (Week 5-6)

- [ ] Implement `proxmox_ceph` role
- [ ] Automate CEPH monitor/manager creation
- [ ] Automate OSD creation (12 OSDs across 3 nodes)
- [ ] Create CEPH pools configuration

### Enhancement (Week 7-8)

- [ ] Add molecule testing framework
- [ ] Create CI/CD pipeline for role testing
- [ ] Add comprehensive error handling
- [ ] Performance optimization

### Long-term

- [ ] Extend to doggos_cluster and nexus_cluster
- [ ] Integrate with NetBox for IPAM
- [ ] PowerDNS automation
- [ ] Monitoring integration (Prometheus/Grafana)

---

## Conclusion

**ProxSpray** provides excellent patterns for Proxmox cluster automation, particularly in role-based architecture, network configuration, and CEPH deployment. However, it lacks modern tooling, secrets management, and comprehensive testing.

**Virgo-Core** should adopt ProxSpray's role structure and automation patterns while maintaining its superior foundations in:
- Infisical secrets management
- Modern Python tooling (uv)
- Task automation (mise)
- Code quality (pre-commit, ansible-lint)
- Native Ansible modules

### Key Takeaways

1. **Convert to Roles**: Migrate playbooks to reusable roles for better composition
2. **Maintain Security**: Keep Infisical integration; never hardcode secrets
3. **Automate Everything**: No manual steps (especially CEPH OSD creation)
4. **Use Native Modules**: Prefer `community.proxmox` over shell commands
5. **Test Thoroughly**: Add ansible-lint, molecule, and CI/CD

By combining ProxSpray's automation depth with Virgo-Core's modern engineering practices, the result will be a production-ready, maintainable, and secure infrastructure automation platform.

---

**Next Steps**: Begin with Phase 1 (Role Conversion) to establish the foundation for future automation enhancements.
