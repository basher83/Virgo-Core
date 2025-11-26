# Terraform Directory

OpenTofu configurations for VM provisioning and template creation on Proxmox VE.

## Important: Use `tofu` not `terraform`

This project uses OpenTofu, not Terraform. Always use the `tofu` command:

```bash
tofu init
tofu plan
tofu apply
```

## Overview

The terraform directory provides declarative infrastructure for:

- **Template Creation**: Download cloud images and create Proxmox VM templates
- **VM Deployment**: Clone templates to deploy single VMs or clusters
- **DRY Configuration**: Only specify values that differ from module defaults

All configurations use the external module from `github.com/basher83/Triangulum-Prime//terraform-bgp-vm` which provides two deployment modes:

- `vm_type = "image"` - Downloads cloud image and creates template
- `vm_type = "clone"` - Clones from existing template to create VMs

## Directory Structure

```text
terraform/
├── netbox-template/     # Template creation configurations
│   ├── main.tf          # Template creation with custom cloud-init
│   ├── variables.tf     # Template variables
│   └── provider.tf      # Proxmox provider configuration
│
├── netbox-vm/           # Single VM deployment configurations
│   ├── main.tf          # Single VM clone deployment
│   ├── variables.tf     # VM variables
│   ├── outputs.tf       # VM outputs (IP, SSH, Ansible inventory)
│   ├── provider.tf      # Proxmox provider configuration
│   └── README.md        # Comprehensive VM deployment guide
│
└── examples/            # Example deployment patterns
    ├── microk8s-cluster/               # Multi-node cluster with for_each
    └── template-with-custom-cloudinit/ # Custom cloud-init template
```

## Module Overview

### netbox-template

Creates Proxmox VM templates from cloud images.

**Features**:

- Downloads Ubuntu cloud images
- Configures cloud-init with custom user-data
- Creates bootable UEFI templates
- Minimal resource allocation (customize during clone)

**Use for**: Creating reusable VM templates with custom configurations

See: [netbox-template/main.tf](netbox-template/main.tf)

### netbox-vm

Deploys single VMs by cloning templates.

**Features**:

- Static IP configuration with VLAN support
- Customizable CPU, memory, disk resources
- Cloud-init for automated setup
- QEMU guest agent for IP retrieval
- Lifecycle management (prevent accidental deletion)

**Use for**: Application servers, databases, development environments, Docker hosts

See: [netbox-vm/README.md](netbox-vm/README.md) (comprehensive 557-line guide)

## External Module Reference

All configurations use the Triangulum-Prime module:

```hcl
module "vm" {
  source = "github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=v1.0.0"

  vm_type  = "clone"  # or "image" for templates
  pve_node = "proxmox-node"

  # Only specify values that differ from module defaults
  # See module's DEFAULTS.md for complete reference
}
```

**Module capabilities**:

- Creates templates from cloud images
- Clones VMs with cloud-init
- Supports multiple NICs with VLAN configuration
- Provides deterministic MAC addressing
- Supports EFI/UEFI boot
- Manages comprehensive lifecycle

**Key principle**: The module provides sensible defaults. Only override values specific to your deployment.

## Quick Start

### 1. Create a Template

```bash
cd terraform/netbox-template

# Configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your Proxmox endpoint and node

# Set Proxmox credentials
export PROXMOX_VE_USERNAME="root@pam"
export PROXMOX_VE_PASSWORD="your-password"

# Deploy the template
tofu init
tofu plan
tofu apply
```

### 2. Deploy a VM

```bash
cd terraform/netbox-vm

# Configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with VM configuration

# Deploy the VM
tofu init
tofu plan
tofu apply

# Get SSH command
tofu output -raw ssh_command
```

## Common Workflows

### Template Creation Workflow

1. **Download cloud image**: Module downloads from URL
2. **Upload custom cloud-init**: Optional user-data customization
3. **Create template**: Bootable UEFI template with cloud-init
4. **Tag and document**: Apply tags and description

Templates use minimal resources. Customize CPU and memory during cloning.

### VM Deployment Workflow

1. **Clone template**: Fast deployment from existing template
2. **Configure resources**: Set CPU, memory, disk size
3. **Network setup**: Static IP with optional VLAN
4. **Cloud-init**: SSH keys, user creation, packages
5. **Boot and access**: QEMU agent provides IP automatically

### Cluster Deployment Workflow

See [examples/microk8s-cluster](examples/microk8s-cluster/) for multi-node pattern using `for_each`.

**Pattern**:

```hcl
locals {
  nodes = {
    "node-1" = { vm_id = 101, ip = "192.168.1.101", ... }
    "node-2" = { vm_id = 102, ip = "192.168.1.102", ... }
    "node-3" = { vm_id = 103, ip = "192.168.1.103", ... }
  }
}

module "cluster" {
  source   = "github.com/basher83/Triangulum-Prime//terraform-bgp-vm"
  for_each = local.nodes

  vm_type  = "clone"
  vm_name  = each.key
  # ... per-node configuration
}
```

## Environment Variables

Required for Proxmox authentication:

```bash
# Option 1: Username/password
export PROXMOX_VE_USERNAME="root@pam"
export PROXMOX_VE_PASSWORD="your-password"

# Option 2: API token (recommended)
export PROXMOX_VE_API_TOKEN="user@realm!token-id=secret"

# Optional: Endpoint (if not in terraform.tfvars)
export PROXMOX_VE_ENDPOINT="https://proxmox.example.com:8006"
```

## Examples

### Single VM Deployment

See [netbox-vm/README.md](netbox-vm/README.md) for comprehensive examples:

- Development server (2 cores, 4GB RAM)
- Database server (8 cores, 16GB RAM)
- Web server (4 cores, 8GB RAM)
- Jumpbox/bastion (2 cores, 2GB RAM)
- Docker host (8 cores, 32GB RAM)

### Multi-Node Cluster

See [examples/microk8s-cluster](examples/microk8s-cluster/) for:

- 3-node Kubernetes cluster
- Environment-based VM ID offsets
- Deterministic MAC addressing
- Dual-NIC configuration with VLANs

### Custom Cloud-Init Template

See [examples/template-with-custom-cloudinit](examples/template-with-custom-cloudinit/) for:

- Uploading custom user-data.yaml
- Advanced cloud-init configuration
- Template creation with custom packages

## DRY Principle and Module Defaults

**Core philosophy**: The Triangulum-Prime module provides comprehensive defaults. Only specify values that differ.

**Good practice**:

```hcl
module "vm" {
  source = "github.com/basher83/Triangulum-Prime//terraform-bgp-vm"

  vm_type  = "clone"
  pve_node = "proxmox-node"

  # Only override what's needed
  vm_cpu = {
    cores = 8  # Override default 2 cores
  }

  # Don't repeat defaults like:
  # vm_bios = "ovmf"      # Already module default
  # vm_machine = "q35"    # Already module default
  # vm_os = "l26"         # Already module default
}
```

**Bad practice**:

```hcl
module "vm" {
  # Avoid repeating module defaults
  vm_bios    = "ovmf"      # Unnecessary
  vm_machine = "q35"       # Unnecessary
  vm_os      = "l26"       # Unnecessary
  # ... this makes configs verbose and harder to maintain
}
```

See module's `DEFAULTS.md` for complete reference.

## Troubleshooting

### Template Not Found

**Error**: `unable to find template with ID 2000`

**Solution**: List templates on Proxmox and update `template_id`

```bash
ssh root@proxmox 'qm list | grep template'
```

### IP Address Not Assigned

**Error**: Output shows `ip_address = "N/A"`

**Cause**: QEMU guest agent has not started or VM is still booting

**Solution**:

```bash
# Wait and refresh
tofu refresh

# Check guest agent in VM
ssh ubuntu@<ip> 'systemctl status qemu-guest-agent'
```

### SSH Connection Refused

**Cause**: VM is still booting or cloud-init is running

**Solution**:

```bash
# Wait for cloud-init
ssh ubuntu@<ip> 'cloud-init status --wait'
```

### Network Configuration Issues

**Common causes**:

- Network bridge does not exist
- Incorrect VLAN configuration
- Wrong gateway address
- Proxmox firewall blocks traffic

**Solution**: Verify bridge exists and check firewall rules

```bash
ssh root@proxmox 'ip link show vmbr0'
ssh root@proxmox 'pvesh get /nodes/<node>/network'
```

## Related Documentation

- [netbox-vm/README.md](netbox-vm/README.md) - Comprehensive VM deployment guide
- [CLAUDE.md](../CLAUDE.md) - Project conventions and technologies
- [docs/infrastructure.md](../docs/infrastructure.md) - Hardware and network specs
- [docs/goals.md](../docs/goals.md) - Project roadmap

## Best Practices

1. **Use templates**: Always clone from templates for consistency
2. **Tag VMs**: Use meaningful tags for organization
3. **Static IPs**: Easier for automation and monitoring
4. **DRY principle**: Avoid repeating module defaults
5. **Version pinning**: Use module version tags (e.g., `?ref=v1.0.0`)
6. **Protect production**: Set lifecycle policies for critical VMs
7. **Enable guest agent**: Required for IP address detection
8. **Document purpose**: Use descriptions and tags
9. **Environment variables**: Never commit credentials
10. **Use `tofu`**: Use `tofu`, not `terraform` - this project uses OpenTofu

## License

Copyright 2025 RalZareck. Licensed under Apache 2.0.
