# proxmox_template

Create Proxmox VM templates from Ubuntu cloud images with cloud-init customization.

## Features

- Ubuntu 24.04 cloud image support
- Cloud-init vendor-data for user creation and SSH key injection
- Automatic user creation with passwordless sudo
- QEMU guest agent installation
- Dual NIC support with VLAN tagging
- UEFI (OVMF) and legacy BIOS support
- Infisical integration for SSH key management
- Dry-run mode for testing
- Fail-fast validation (no silent failures)

## Requirements

- Proxmox VE 8.x or 9.x
- Ubuntu 24.04 cloud image downloaded to Proxmox node
- SSH keys configured (see SSH Key Configuration below)
- `infisical.vault` collection (if using Infisical for SSH keys)

## SSH Key Configuration (REQUIRED)

SSH keys are mandatory. The role will fail immediately if no keys are configured.
Password authentication is disabled by design.

Configure SSH keys using one of these methods:

### Option 1: Direct Configuration

```yaml
proxmox_template_ssh_keys:
  - "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... user@host"
  - "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... user2@host"
```

### Option 2: Infisical Vault

```yaml
proxmox_template_use_infisical: true
proxmox_template_infisical_path: "/matrix"
proxmox_template_infisical_secret_name: "ANSIBLE_SSH_KEYS"
```

The Infisical secret should contain newline-separated public keys:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... key1@host
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... key2@host
```

## Execution Flow

The role executes in this order:

1. **validate.yml** - Validates required variables and configuration
2. **secrets.yml** - Retrieves SSH keys from Infisical (if enabled)
3. **SSH key check** - Fails immediately if no SSH keys are available
4. **prepare_cloudinit.yml** - Renders vendor-data template with user and SSH keys
5. **build_template.yml** - Executes build-template.sh to create the VM template
6. **verify.yml** - Verifies template was created successfully

If any step fails, the role stops immediately with a clear error message.

## Role Variables

### Required Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_id` | Unique VM ID for template | `9000` |
| `proxmox_template_name` | Template name | `ubuntu-2404-template` |
| `proxmox_template_image_path` | Path to cloud image | `/var/lib/vz/template/iso/ubuntu-24.04-server-cloudimg-amd64.img` |
| `proxmox_template_ssh_keys` | List of SSH public keys (required if not using Infisical) | `[]` |

### Hardware Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_bios` | BIOS type (`seabios` or `ovmf`) | `ovmf` |
| `proxmox_template_cpu_cores` | CPU cores | `2` |
| `proxmox_template_cpu_sockets` | CPU sockets | `1` |
| `proxmox_template_cpu_type` | CPU type | `x86-64-v2-AES` |
| `proxmox_template_machine` | Machine type (`q35` or `pc`) | `q35` |
| `proxmox_template_memory` | Memory in MB | `2048` |

### Storage Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_storage` | Storage backend | `local-lvm` |
| `proxmox_template_scsihw` | SCSI controller | `virtio-scsi-pci` |
| `proxmox_template_disk_resize` | Additional disk size (e.g., `8G`) | `""` |

### Network Configuration (Primary - net0)

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_net_bridge` | Network bridge | `vmbr0` |
| `proxmox_template_net_type` | Network type | `virtio` |
| `proxmox_template_net_vlan` | VLAN tag | `""` |
| `proxmox_template_net_ip` | IP config (`dhcp` or `x.x.x.x/xx`) | `dhcp` |
| `proxmox_template_net_gateway` | Gateway (static IP only) | `""` |

### Network Configuration (Secondary - net1)

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_net2_bridge` | Second bridge (empty = disabled) | `""` |
| `proxmox_template_net2_type` | Second NIC type | `virtio` |
| `proxmox_template_net2_vlan` | Second NIC VLAN | `""` |
| `proxmox_template_net2_ip` | Second NIC IP | `dhcp` |
| `proxmox_template_net2_gateway` | Second NIC gateway | `""` |

### DNS Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_dns` | DNS servers (space-separated) | `""` |
| `proxmox_template_searchdomain` | DNS search domain | `""` |

### Cloud-init Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_user` | Default user created by cloud-init | `ansible` |
| `proxmox_template_user_gecos` | User description | `Ansible Automation User` |
| `proxmox_template_timezone` | Timezone | `America/New_York` |
| `proxmox_template_vendor_file` | Vendor-data filename | `vendor-data.yaml` |

### Infisical Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_use_infisical` | Enable Infisical for SSH keys | `false` |
| `proxmox_template_infisical_path` | Infisical secret path | `/matrix` |
| `proxmox_template_infisical_secret_name` | Secret name | `ANSIBLE_SSH_KEYS` |
| `proxmox_template_infisical_env` | Infisical environment | `prod` |

### Operational Flags

| Variable | Description | Default |
|----------|-------------|---------|
| `proxmox_template_dry_run` | Test mode (no changes) | `false` |
| `proxmox_template_skip_verify` | Skip verification | `false` |
| `proxmox_template_cleanup_vendor_data` | Remove vendor-data after | `false` |
| `proxmox_template_no_log` | Suppress sensitive output | `true` |

## Usage Examples

### Basic Usage

```yaml
- name: Create VM Template
  hosts: foxtrot
  become: true
  roles:
    - role: proxmox_template
      vars:
        proxmox_template_id: 9100
        proxmox_template_name: "ubuntu-2404-base"
        proxmox_template_ssh_keys:
          - "ssh-ed25519 AAAAC3... user@host"
```

### With Infisical SSH Keys

```yaml
- name: Create VM Template with Infisical
  hosts: "{{ target_host | default('foxtrot') }}"
  become: true
  roles:
    - role: proxmox_template
      vars:
        proxmox_template_id: 9100
        proxmox_template_name: "ubuntu-2404-infisical"
        proxmox_template_use_infisical: true
        proxmox_template_infisical_path: "/matrix"
```

### Dual NIC with VLANs

```yaml
- name: Create Dual-NIC Template
  hosts: foxtrot
  become: true
  roles:
    - role: proxmox_template
      vars:
        proxmox_template_id: 9200
        proxmox_template_name: "ubuntu-2404-k8s"
        proxmox_template_net_bridge: "vmbr0"
        proxmox_template_net2_bridge: "vmbr1"
        proxmox_template_net2_vlan: "2"
        proxmox_template_ssh_keys:
          - "ssh-ed25519 AAAAC3... user@host"
```

### Dry Run Mode

```bash
uv run ansible-playbook playbooks/create-template.yml \
  -e "proxmox_template_dry_run=true"
```

## Cloud Image Download

Download the Ubuntu 24.04 cloud image to your Proxmox node:

```bash
cd /var/lib/vz/template/iso/
wget https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img
```

## What Gets Created

The template includes:

- User account (`ansible` by default) with:
  - Passwordless sudo access
  - SSH key authentication only (password disabled)
  - Member of `users` and `sudo` groups
- QEMU guest agent (enabled and started)
- Package updates applied on first boot
- Automatic reboot after cloud-init completes

## Dependencies

- `infisical.vault` collection (when using Infisical)

## License

MIT

## Author

basher83
