# VM Template Creation from Cloud Images

This directory creates Proxmox VM templates from cloud images. Templates serve as base images for rapid VM
deployment via cloning.

## Overview

This configuration downloads cloud images and creates Proxmox VM templates with custom cloud-init configuration.
The templates provide a consistent base for deploying VMs across your Proxmox cluster.

Key features:

- Downloads cloud images directly from vendor URLs
- Uploads custom cloud-init user-data configuration
- Creates UEFI-enabled VM templates
- Supports Ubuntu, Debian, and other cloud-init compatible distributions
- Templates marked as non-startable (clone-only)

## How It Works

The configuration executes three operations:

1. **Upload cloud-init user-data** - Uploads your custom user-data.yaml to Proxmox as a snippet
2. **Download cloud image** - Fetches the cloud image from the vendor URL
3. **Create template** - Imports the image and creates a VM template with cloud-init configuration

The resulting template serves as a base for cloning VMs (see [terraform/netbox-vm](../netbox-vm)).

## Prerequisites

### Required Access

- **Proxmox API credentials** - Set via environment variables
- **SSH access to Proxmox host** - Required for image import operations
- **SSH agent running** - Must have key loaded for Proxmox host authentication

### Required Storage

- **File-based datastore** - For cloud images and snippets (typically `local`)
- **Block or file datastore** - For VM disks (e.g., `local-lvm` or CEPH)

### Proxmox Configuration

Verify the SSH user exists on your Proxmox hosts:

```bash
# Create terraform user (if needed)
ssh root@proxmox 'useradd -m -s /bin/bash terraform'

# Add your SSH key
ssh-copy-id terraform@proxmox
```

## Quick Start

### 1. Configure Variables

Copy the example configuration:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
proxmox_endpoint = "https://foxtrot.matrix.local:8006"
proxmox_node     = "foxtrot"

template_name = "ubuntu-24-04-custom-cloudinit-template"
template_id   = 2008

cloud_image_url = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
cloud_image_filename = "noble-server-cloudimg-amd64.img"

datastore = "local-lvm"
```

### 2. Customize Cloud-Init

Copy and edit the cloud-init configuration:

```bash
cp user-data.yaml.example user-data.yaml
```

Edit `user-data.yaml` to configure:

- Default users and SSH keys
- Installed packages
- System timezone
- NTP servers
- Custom scripts

**Important**: Change the default password hash in user-data.yaml before deploying.

### 3. Set Authentication

Export Proxmox credentials:

```bash
export PROXMOX_VE_USERNAME="root@pam"
export PROXMOX_VE_PASSWORD="your-password"

# OR use API token
export PROXMOX_VE_API_TOKEN="terraform@pam!token-id=secret"
```

### 4. Deploy Template

Initialize and apply:

```bash
tofu init
tofu plan
tofu apply
```

The template appears in Proxmox with a cloud icon, ready for cloning.

### 5. Verify Template

Check the template exists:

```bash
# List templates on Proxmox
ssh root@proxmox 'qm list | grep template'

# Get template details
tofu output template_id
tofu output template_name
```

## Variable Reference

### Connection Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `proxmox_endpoint` | string | required | Proxmox API URL (e.g., `https://proxmox.local:8006`) |
| `proxmox_insecure` | bool | `true` | Skip TLS verification for self-signed certificates |
| `proxmox_node` | string | required | Proxmox node name for template creation |

### Template Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `template_name` | string | `ubuntu-24-04-custom-cloudinit-template` | Template name in Proxmox |
| `template_id` | number | `2008` | VM ID (100-999999999, typically 2000-9999) |
| `template_description` | string | `Ubuntu 24.04 LTS Cloud Template...` | Template description |
| `template_tags` | list(string) | `["template", "ubuntu", ...]` | Tags for organization |

### Cloud Image Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `cloud_image_url` | string | Ubuntu 24.04 URL | Cloud image download URL |
| `cloud_image_filename` | string | `noble-server-cloudimg-amd64.img` | Filename for downloaded image |
| `cloud_image_checksum` | string | `null` | SHA256 checksum (recommended for production) |
| `cloud_image_datastore` | string | `local` | File-based datastore for image download |

### Cloud-Init Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `user_data_file` | string | `user-data.yaml` | Path to cloud-init user-data file |
| `user_data_snippet_name` | string | `user-data-custom.yaml` | Snippet name in Proxmox |
| `cloud_init_datastore` | string | `local` | Datastore for snippets |
| `dns_servers` | list(string) | `["1.1.1.1", "8.8.8.8"]` | DNS servers for network configuration |

### Storage Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `datastore` | string | `local-lvm` | Datastore for VM disks (template disk) |
| `disk_size` | number | `12` | Template disk size in GB (expand during clone) |

### Network Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `network_bridge` | string | `vmbr0` | Network bridge for template |

## Example Configurations

### Ubuntu 24.04 LTS Template

```hcl
template_name = "ubuntu-24-04-template"
template_id   = 2000

cloud_image_url = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
cloud_image_filename = "noble-server-cloudimg-amd64.img"
```

### Ubuntu 22.04 LTS Template

```hcl
template_name = "ubuntu-22-04-template"
template_id   = 2001

cloud_image_url = "https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img"
cloud_image_filename = "jammy-server-cloudimg-amd64.img"
```

### Debian 12 Template

```hcl
template_name = "debian-12-template"
template_id   = 2002

cloud_image_url = "https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-amd64.qcow2"
cloud_image_filename = "debian-12-cloudimg-amd64.qcow2"
```

### Template with Image Verification

```hcl
template_name = "ubuntu-24-04-verified-template"
template_id   = 2003

cloud_image_url = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
cloud_image_filename = "noble-server-cloudimg-amd64.img"

# Get checksum from https://cloud-images.ubuntu.com/noble/current/SHA256SUMS
cloud_image_checksum = "abc123def456..."  # SHA256 hash only, no prefix
```

## Integration with VM Deployment

After creating a template, deploy VMs by cloning:

```bash
cd ../netbox-vm
cp terraform.tfvars.example terraform.tfvars
```

Configure `terraform.tfvars` to reference your template:

```hcl
template_id = 2008  # Match the template_id from this directory
vm_name     = "my-server"
ip_address  = "192.168.1.100"
```

See [terraform/netbox-vm/README.md](../netbox-vm/README.md) for VM deployment details.

## Outputs

The configuration provides these outputs:

- `template_id` - VM ID for clone operations
- `template_name` - Template name in Proxmox
- `template_node` - Proxmox node location
- `cloud_init_file_id` - Cloud-init snippet file ID

Access outputs:

```bash
tofu output template_id
tofu output -json
```

## Troubleshooting

### SSH Authentication Failed

**Error**: `Failed to connect to Proxmox via SSH`

**Causes**:

1. SSH agent not running
2. Key not loaded in SSH agent
3. Wrong SSH username

**Solution**:

```bash
# Start SSH agent
eval $(ssh-agent)

# Add your key
ssh-add ~/.ssh/id_rsa

# Test SSH access
ssh terraform@proxmox 'hostname'

# Verify username in provider.tf matches
grep ssh_username provider.tf
```

### Cloud Image Download Failed

**Error**: `Failed to download cloud image`

**Causes**:

1. Invalid URL
2. Network connectivity issue
3. Insufficient storage space

**Solution**:

```bash
# Verify URL is accessible
curl -I "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"

# Check datastore space
ssh root@proxmox 'df -h /var/lib/vz'

# Verify datastore exists
ssh root@proxmox 'pvesm status'
```

### Wrong Datastore Type

**Error**: `Download file resource does not support the specified datastore`

**Cause**: Using block-based storage (e.g., `local-lvm`) for cloud image download

**Solution**: Cloud images require file-based storage. Use `local` for `cloud_image_datastore`:

```hcl
cloud_image_datastore = "local"     # File-based storage
datastore = "local-lvm"             # Can use block storage here
```

### Template Already Exists

**Error**: `VM ID 2008 already exists`

**Solution**:

```bash
# Remove existing template
ssh root@proxmox 'qm destroy 2008'

# OR choose different template_id
template_id = 2009
```

### Cloud-Init Snippet Upload Failed

**Error**: `Failed to upload cloud-init user-data`

**Causes**:

1. File does not exist
2. Datastore does not support snippets
3. Permissions issue

**Solution**:

```bash
# Verify file exists
ls -l user-data.yaml

# Check datastore supports snippets
ssh root@proxmox 'pvesm status -content snippets'

# Verify snippet directory exists
ssh root@proxmox 'ls -ld /var/lib/vz/snippets'
```

### Checksum Verification Failed

**Error**: `Checksum mismatch`

**Solution**:

1. Download checksum file from vendor
2. Extract hash value only (no `sha256:` prefix)
3. Update `cloud_image_checksum` variable

```bash
# Get Ubuntu checksums
curl https://cloud-images.ubuntu.com/noble/current/SHA256SUMS

# Extract hash for your image
grep 'noble-server-cloudimg-amd64.img' SHA256SUMS | awk '{print $1}'
```

## Updating Templates

Templates cannot be modified after creation. To update:

1. Create a new template with a different ID
2. Test the new template by deploying a VM
3. Update VM deployments to use the new template ID
4. Remove the old template

```bash
# Create new template
template_id = 2009  # New ID

tofu apply

# After testing, remove old template
ssh root@proxmox 'qm destroy 2008'
```

## Cloud-Init Customization

The `user-data.yaml` file configures the template's default behavior. Common customizations:

### Add Users

```yaml
users:
  - name: admin
    groups: [adm, sudo]
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ssh-rsa AAAAB3... admin@laptop
```

### Install Packages

```yaml
packages:
  - qemu-guest-agent  # Required for IP detection
  - docker.io
  - nginx
  - postgresql
```

### Run Custom Scripts

```yaml
runcmd:
  - apt update && apt upgrade -y
  - systemctl enable docker
  - curl -fsSL https://get.docker.com | sh
```

### Configure Timezone

```yaml
timezone: America/New_York
```

See [user-data.yaml.example](user-data.yaml.example) for more options.

## Best Practices

1. **Use specific cloud image versions** - Pin to dated releases for reproducibility
2. **Verify checksums in production** - Always set `cloud_image_checksum`
3. **Keep templates minimal** - Install only essential packages; customize during deployment
4. **Use small disk sizes** - Disks expand during cloning
5. **Test templates before production** - Deploy test VMs to verify configuration
6. **Version your templates** - Use sequential IDs (2000, 2001, 2002)
7. **Tag templates** - Use descriptive tags for organization
8. **Document template purpose** - Set clear descriptions

## Security Considerations

1. **Change default passwords** - Never use example password hashes
2. **Use SSH keys only** - Disable password authentication in user-data.yaml
3. **Minimal package installation** - Reduce attack surface
4. **Regular updates** - Create new templates monthly with latest images
5. **Protect credentials** - Never commit secrets to version control
6. **Secure cloud-init files** - Restrict permissions on user-data.yaml

## Module Information

This configuration uses the external module:

- **Source**: `github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=v1.0.0`
- **Module Type**: `vm_type = "image"`
- **Documentation**: See module's `DEFAULTS.md` for default values

The module handles:

- Cloud image download via Proxmox API
- Image import to Proxmox storage
- VM template creation with cloud-init
- EFI boot configuration

## Related Documentation

- [VM Deployment Guide](../netbox-vm/README.md) - How to deploy VMs from templates
- [CLAUDE.md](../../CLAUDE.md) - Project conventions and standards
- [Infrastructure Specifications](../../docs/infrastructure.md) - Hardware and network details
- [Module Repository](https://github.com/basher83/Triangulum-Prime) - External module source

## Important Notes

- **Use tofu, not terraform** - This project uses OpenTofu
- **SSH access required** - Template creation needs SSH to Proxmox host
- **File-based storage required** - Cloud images need `local` or similar
- **Templates are immutable** - Create new templates for updates
- **Module defaults apply** - Only specify overrides (see module's DEFAULTS.md)
