# Proxmox LXC Role Design

**Date**: 2025-12-31
**Status**: Approved
**Author**: basher83

## Overview

Design a role to manage Proxmox LXC containers.

### 1. The Role Structure

Create a directory named `roles/proxmox_lxc/` with the following layout:

```text
roles/proxmox_lxc/
├── defaults/
│   └── main.yml        # Default variables (memory, cores, etc.)
├── tasks/
│   └── main.yml        # The actual logic we wrote earlier
└── vars/
    └── main.yml        # OS-specific variables (template names)

```

---

### 2. Defining the Logic (`tasks/main.yml`)

We’ll use variables (`{{ }}`) instead of hardcoded values so the role is flexible.

```yaml
---
- name: Ensure template is available
  community.proxmox.proxmox_template:
    api_host: "{{ pve_api_host }}"
    api_user: "{{ pve_api_user | default('root@pam') }}"
    api_token_id: "{{ pve_token_id }}"
    api_token_secret: "{{ pve_token_secret }}"
    node: "{{ pve_node }}"
    storage: "{{ pve_template_storage | default('local') }}"
    template: "{{ lxc_template }}"
    state: present
    timeout: 600

- name: Provision LXC container
  community.proxmox.proxmox:
    api_host: "{{ pve_api_host }}"
    api_user: "{{ pve_api_user | default('root@pam') }}"
    api_token_id: "{{ pve_token_id }}"
    api_token_secret: "{{ pve_token_secret }}"
    vmid: "{{ lxc_vmid }}"
    node: "{{ pve_node }}"
    hostname: "{{ lxc_hostname }}"
    ostemplate: "{{ pve_template_storage | default('local') }}:vztmpl/{{ lxc_template }}"
    cores: "{{ lxc_cores | default(1) }}"
    memory: "{{ lxc_memory | default(1024) }}"
    rootfs: "{{ lxc_rootfs_storage | default('local-lvm') }}:{{ lxc_disk_size | default(4) }}"
    unprivileged: "{{ lxc_unprivileged | default(true) }}"
    netif: "{{ lxc_netif }}"
    state: present

```

---

### 3. Setting Defaults (`defaults/main.yml`)

These are the fallback values if you don't specify them in your inventory.

```yaml
---
lxc_template: "debian-12-standard_12.12-1_amd64.tar.zst"
pve_template_storage: "local"
lxc_unprivileged: true
lxc_cores: 1
lxc_memory: 1024

```

---

### 4. How to use the Role (`site.yml`)

Now your main playbook becomes incredibly clean. You can define your different containers as a list and loop through them.

```yaml
---
- name: Deploy Infrastructure
  hosts: localhost
  gather_facts: false
  vars:
    # Secrets (In a real scenario, use Ansible Vault for these!)
    pve_token_id: "ansible-token"
    pve_token_secret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

  tasks:
    - name: Deploy Omni Providers
      include_role:
        name: proxmox_lxc
      vars:
        pve_api_host: "192.168.3.5"
        pve_node: "Foxtrot"
        lxc_vmid: 100
        lxc_hostname: "omni-provider"
        lxc_netif:
          net0: "name=eth0,bridge=vmbr0,ip=192.168.3.10/24,gw=192.168.3.1"

    - name: Deploy Secondary DNS (Example)
      include_role:
        name: proxmox_lxc
      vars:
        pve_api_host: "192.168.3.6" # Different Proxmox Host
        pve_node: "Echo"
        lxc_vmid: 101
        lxc_hostname: "dns-secondary"
        lxc_netif:
          net0: "name=eth0,bridge=vmbr0,ip=192.168.3.11/24,gw=192.168.3.1"

```

---

### Benefits

1. **Separation of Concerns:** If you decide to change the Debian template version later, you only change it in **one** place (`defaults/main.yml`), and every container you deploy will automatically use the new version.
2. **Scalability:** To add a third or fourth container, you just add another `include_role` block.
3. **Cross-Network Ready:** Since `pve_api_host` is a variable, this single role can manage your Catonsville lab and any remote servers simultaneously.
