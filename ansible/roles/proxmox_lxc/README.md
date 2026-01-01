# proxmox_lxc

Manage Proxmox LXC containers with state-based lifecycle, Infisical secret integration, and SSH key injection.

## Features

- Create and remove LXC containers via Proxmox API
- Automatic template download from Proxmox repositories
- State management: `present` to create, `absent` to remove
- Optional Infisical integration for API token retrieval
- SSH public key injection for container access
- Configurable auto-start behavior
- Unprivileged containers by default (security best practice)
- Comprehensive input validation with configuration summary

## Requirements

- Proxmox VE 7.x or 8.x
- Ansible 2.14+
- `community.proxmox` collection
- `infisical.vault` collection (if using Infisical)
- API token with appropriate permissions on the Proxmox node

## Role Variables

### Required Variables

```yaml
# Container identity
proxmox_lxc_vmid: 100          # Unique VM ID (100-999999999)
proxmox_lxc_hostname: "myct"   # Container hostname

# API authentication (if not using Infisical)
proxmox_lxc_token_id: "ansible"
proxmox_lxc_token_secret: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Network configuration
proxmox_lxc_netif:
  net0: "name=eth0,bridge=vmbr0,ip=dhcp"
```

### API Connection

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_api_host` | `{{ ansible_host }}` | Proxmox API host |
| `proxmox_lxc_node` | `{{ inventory_hostname }}` | Target Proxmox node |
| `proxmox_lxc_api_user` | `root@pam` | API user |
| `proxmox_lxc_token_id` | `""` | API token ID |
| `proxmox_lxc_token_secret` | `""` | API token secret |
| `proxmox_lxc_validate_certs` | `false` | Validate SSL certificates |

### Container Identity

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_vmid` | `""` | Unique VM ID (required) |
| `proxmox_lxc_hostname` | `""` | Container hostname (required) |
| `proxmox_lxc_state` | `present` | `present` to create, `absent` to remove |

### Template

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_template` | `debian-12-standard_12.12-1_amd64.tar.zst` | LXC template filename |
| `proxmox_lxc_template_storage` | `local` | Storage for templates |

### Hardware

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_cores` | `1` | CPU cores |
| `proxmox_lxc_memory` | `1024` | Memory in MB |
| `proxmox_lxc_swap` | `512` | Swap in MB |

### Storage

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_rootfs_storage` | `local-lvm` | Storage for rootfs |
| `proxmox_lxc_disk_size` | `4` | Disk size in GB |

### Network

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_netif` | `{}` | Network interface configuration (required) |
| `proxmox_lxc_nameserver` | `1.1.1.1` | DNS nameserver (prevents MagicDNS inheritance from host) |

Network format examples:

```yaml
# DHCP
proxmox_lxc_netif:
  net0: "name=eth0,bridge=vmbr0,ip=dhcp"

# Static IP
proxmox_lxc_netif:
  net0: "name=eth0,bridge=vmbr0,ip=192.168.1.100/24,gw=192.168.1.1"

# Multiple NICs with VLAN
proxmox_lxc_netif:
  net0: "name=eth0,bridge=vmbr0,ip=dhcp"
  net1: "name=eth1,bridge=vmbr1,tag=100,ip=10.0.0.5/24"
```

### Container Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_unprivileged` | `true` | Run as unprivileged container |
| `proxmox_lxc_start` | `true` | Start container after creation |
| `proxmox_lxc_onboot` | `false` | Start on host boot |
| `proxmox_lxc_description` | `""` | Container description |
| `proxmox_lxc_features` | `["nesting=1"]` | Container features as list of "key=value" strings |
| `proxmox_lxc_enable_tun` | `false` | Enable TUN device for Tailscale/VPN |

### Access

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_pubkey` | `""` | SSH public key for root |
| `proxmox_lxc_password` | `""` | Root password (optional) |

### Infisical Integration

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_use_infisical` | `false` | Enable Infisical for token retrieval |
| `proxmox_lxc_infisical_path` | `/matrix` | Infisical secret path |
| `proxmox_lxc_infisical_secret_name` | `PROXMOX_API_TOKEN` | Secret name |
| `proxmox_lxc_infisical_env` | `prod` | Infisical environment |

### Operational Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `proxmox_lxc_skip_verify` | `false` | Skip post-creation verification |
| `proxmox_lxc_no_log` | `true` | Suppress sensitive output |
| `proxmox_lxc_timeout` | `300` | API timeout in seconds |

## Dependencies

None. Required collections should be installed via project `requirements.yml`.

## Example Playbook

### Basic Container Creation

```yaml
- name: Deploy LXC container
  hosts: foxtrot
  gather_facts: false
  tasks:
    - name: Create web server container
      ansible.builtin.include_role:
        name: proxmox_lxc
      vars:
        proxmox_lxc_api_host: "192.168.3.5"
        proxmox_lxc_node: "Foxtrot"
        proxmox_lxc_token_id: "ansible"
        proxmox_lxc_token_secret: "{{ vault_proxmox_token }}"
        proxmox_lxc_vmid: 100
        proxmox_lxc_hostname: "webserver"
        proxmox_lxc_cores: 2
        proxmox_lxc_memory: 2048
        proxmox_lxc_disk_size: 10
        proxmox_lxc_netif:
          net0: "name=eth0,bridge=vmbr0,ip=192.168.3.100/24,gw=192.168.3.1"
        proxmox_lxc_pubkey: "ssh-ed25519 AAAAC3... user@host"
```

### With Infisical

```yaml
- name: Deploy container with Infisical secrets
  hosts: foxtrot
  gather_facts: false
  tasks:
    - name: Create database container
      ansible.builtin.include_role:
        name: proxmox_lxc
      vars:
        proxmox_lxc_api_host: "192.168.3.5"
        proxmox_lxc_node: "Foxtrot"
        proxmox_lxc_token_id: "ansible"
        proxmox_lxc_use_infisical: true
        proxmox_lxc_infisical_path: "/matrix"
        proxmox_lxc_vmid: 101
        proxmox_lxc_hostname: "database"
        proxmox_lxc_template: "debian-12-standard_12.12-1_amd64.tar.zst"
        proxmox_lxc_netif:
          net0: "name=eth0,bridge=vmbr0,ip=dhcp"
```

### Tailscale-Ready Container

```yaml
- name: Deploy Tailscale-ready container
  hosts: foxtrot
  gather_facts: false
  tasks:
    - name: Create container with TUN device
      ansible.builtin.include_role:
        name: proxmox_lxc
      vars:
        proxmox_lxc_api_host: "192.168.3.5"
        proxmox_lxc_node: "Foxtrot"
        proxmox_lxc_token_id: "ansible"
        proxmox_lxc_token_secret: "{{ vault_proxmox_token }}"
        proxmox_lxc_vmid: 200
        proxmox_lxc_hostname: "vpn-gateway"
        proxmox_lxc_template: "ubuntu-24.04-standard_24.04-2_amd64.tar.zst"
        proxmox_lxc_netif:
          net0: "name=eth0,bridge=vmbr0,ip=192.168.3.200/24,gw=192.168.3.1"
        # Enable TUN device for Tailscale/WireGuard
        proxmox_lxc_enable_tun: true
        proxmox_lxc_features:
          - nesting=1
```

### Remove Container

```yaml
- name: Remove LXC container
  hosts: foxtrot
  gather_facts: false
  tasks:
    - name: Destroy container
      ansible.builtin.include_role:
        name: proxmox_lxc
      vars:
        proxmox_lxc_api_host: "192.168.3.5"
        proxmox_lxc_node: "Foxtrot"
        proxmox_lxc_token_id: "ansible"
        proxmox_lxc_token_secret: "{{ vault_proxmox_token }}"
        proxmox_lxc_vmid: 100
        proxmox_lxc_hostname: "webserver"
        proxmox_lxc_state: absent
```

### Multiple Containers

```yaml
- name: Deploy multiple containers
  hosts: foxtrot
  gather_facts: false
  vars:
    containers:
      - vmid: 100
        hostname: "web1"
        ip: "192.168.3.100/24"
      - vmid: 101
        hostname: "web2"
        ip: "192.168.3.101/24"
  tasks:
    - name: Create containers
      ansible.builtin.include_role:
        name: proxmox_lxc
      vars:
        proxmox_lxc_api_host: "192.168.3.5"
        proxmox_lxc_node: "Foxtrot"
        proxmox_lxc_token_id: "ansible"
        proxmox_lxc_token_secret: "{{ vault_proxmox_token }}"
        proxmox_lxc_vmid: "{{ item.vmid }}"
        proxmox_lxc_hostname: "{{ item.hostname }}"
        proxmox_lxc_netif:
          net0: "name=eth0,bridge=vmbr0,ip={{ item.ip }},gw=192.168.3.1"
      loop: "{{ containers }}"
```

## Testing

```bash
# Syntax check
uv run ansible-playbook playbooks/your-playbook.yml --syntax-check

# Lint
uv run ansible-lint ansible/roles/proxmox_lxc/

# Dry run (check mode)
uv run ansible-playbook playbooks/your-playbook.yml --check
```

## License

MIT

## Author

basher83
