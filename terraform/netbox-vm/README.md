# Single VM Deployment Example

This example demonstrates deploying a single VM using the `vm` module with the
**template-clone** approach - the fastest and most reliable method for single VM deployments.

## Overview

This deployment creates a single Ubuntu VM with:

- Customizable CPU, memory, and disk resources
- Static IP configuration with optional VLAN support
- Cloud-init for automated initial setup
- QEMU guest agent for IP retrieval and graceful shutdown
- Configurable lifecycle management (prevent accidental deletion)

**Perfect for**: Application servers, databases, development environments, jumpboxes, Docker hosts, or any single-VM workload.

## Prerequisites

1. **Proxmox Template**: A VM template must exist (default ID: 2000)

   - Ubuntu 22.04 LTS or similar cloud image
   - Cloud-init enabled
   - QEMU guest agent installed

2. **Network Configuration**: Ensure network bridge exists in Proxmox

3. **Terraform**: Version >= 1.0 (tofu)

4. **Provider Authentication**: Set Proxmox credentials via environment variables:

   ```bash
   export PROXMOX_VE_USERNAME="root@pam"
   export PROXMOX_VE_PASSWORD="your-password"
   # OR use API token
   export PROXMOX_VE_API_TOKEN="user@realm!token-id=secret"
   ```

5. **SSH Key**: At least one SSH public key for VM access

## Quick Start

### 1. Configure Variables

Copy the example variables file and customize:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your environment details:

```hcl
proxmox_endpoint = "https://proxmox.local:8006"
proxmox_node     = "pve"

vm_name        = "my-app-server"
template_id    = 2000

cpu_cores = 4
memory    = 8192
disk_size = 50

ip_address      = "192.168.1.100"
network_gateway = "192.168.1.1"

ssh_public_keys = [
  "ssh-rsa AAAAB3Nza... user@hostname",
]
```

### 2. Initialize Terraform

```bash
tofu init
```

### 3. Review the Plan

```bash
tofu plan
```

### 4. Deploy the VM

```bash
tofu apply
```

### 5. Access the VM

After deployment, Terraform outputs connection information:

```text
Outputs:

connection_info = <<EOT
VM Deployment Complete
======================
VM Name: my-app-server
VM ID:   101
Node:    pve
IP:      192.168.1.100

SSH Access:
ubuntu@192.168.1.100

Quick Commands:
- SSH:    ssh ubuntu@192.168.1.100
- Ping:   ping 192.168.1.100
EOT

ssh_command = "ssh ubuntu@192.168.1.100"
```

Connect to your VM:

```bash
ssh ubuntu@192.168.1.100
```

## Common Use Cases

### Development Server

**Configuration**:

```hcl
vm_name   = "dev-server"
cpu_cores = 2
memory    = 4096
disk_size = 32
vm_tags   = ["terraform", "development"]
```

**Use for**: Development work, testing, experimentation

### Database Server

**Configuration**:

```hcl
vm_name   = "postgres-db"
cpu_cores = 8
memory    = 16384
disk_size = 100
vm_tags   = ["terraform", "database", "postgres"]
prevent_destroy = true  # Prevent accidental deletion
```

**Use for**: PostgreSQL, MySQL, MongoDB, Redis

### Web Server

**Configuration**:

```hcl
vm_name   = "web-server"
cpu_cores = 4
memory    = 8192
disk_size = 50
vm_tags   = ["terraform", "webserver", "nginx"]
```

**Use for**: Nginx, Apache, application servers

### Jumpbox / Bastion Host

**Configuration**:

```hcl
vm_name   = "jumpbox"
cpu_cores = 2
memory    = 2048
disk_size = 20
vm_tags   = ["terraform", "jumpbox", "bastion"]
boot_order = 1  # Start early during boot
```

**Use for**: SSH gateway, secure network access

### Docker Host

**Configuration**:

```hcl
vm_name   = "docker-host"
cpu_cores = 8
memory    = 32768
disk_size = 200
vm_tags   = ["terraform", "docker", "containers"]
```

**Use for**: Docker containers, Docker Compose applications

### CI/CD Runner

**Configuration**:

```hcl
vm_name   = "gitlab-runner"
cpu_cores = 8
memory    = 16384
disk_size = 100
vm_tags   = ["terraform", "ci", "gitlab"]
```

**Use for**: GitLab Runner, Jenkins agent, GitHub Actions runner

## Configuration Options

### Hardware Resources

Adjust CPU, memory, and disk based on workload:

```hcl
cpu_cores = 4      # 1-128 cores
cpu_type  = "host" # Best performance
memory    = 8192   # 512 MB - 512 GB
disk_size = 50     # 1 GB - 32 TB
```

### Network Configuration

#### Standard Network (No VLAN)

```hcl
network_bridge  = "vmbr0"
vlan_id         = null
ip_address      = "192.168.1.100"
network_cidr    = "24"
network_gateway = "192.168.1.1"
```

#### VLAN-Isolated Network

```hcl
network_bridge  = "vmbr0"
vlan_id         = 30
ip_address      = "192.168.30.100"
network_cidr    = "24"
network_gateway = "192.168.30.1"
```

### DNS Configuration

Custom DNS settings:

```hcl
dns_domain = "example.local"
dns_servers = ["8.8.8.8", "1.1.1.1"]
```

### Lifecycle Management

#### Production VM (Protected)

```hcl
prevent_destroy = true  # Prevent accidental deletion
```

#### Development VM (Flexible)

```hcl
prevent_destroy = false  # Allow easy cleanup
```

### Boot Configuration

#### High Priority VM (Boot Early)

```hcl
start_on_boot  = true
boot_order     = 1    # Lower = higher priority
boot_up_delay  = 0
boot_down_delay = 0
```

#### Delayed Start VM

```hcl
start_on_boot  = true
boot_order     = 10
boot_up_delay  = 30   # Wait 30 seconds before starting
boot_down_delay = 10
```

## Advanced Features

### Multiple SSH Keys

```hcl
ssh_public_keys = [
  "ssh-rsa AAAAB3... admin@laptop",
  "ssh-ed25519 AAAAC3... admin@desktop",
  "ssh-rsa AAAAB3... ci-deploy@server",
]
```

### VM Tagging

Organize VMs with tags:

```hcl
vm_tags = ["terraform", "production", "webserver", "nginx", "team-a"]
```

### Custom VM ID

Specify a custom VM ID:

```hcl
vm_id = 150  # Must be unique in Proxmox
```

### Custom Description

Add detailed description:

```hcl
vm_description = "Production web server for example.com - Deployed via Terraform"
```

## Terraform Documentation

The following sections are auto-generated by terraform-docs.

<!-- BEGIN_TF_DOCS -->

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_proxmox"></a> [proxmox](#requirement\_proxmox) | >= 0.84.1 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_single_vm"></a> [single\_vm](#module\_single\_vm) | github.com/basher83/Triangulum-Prime//terraform-bgp-vm | v1.0.0 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cloud_init_datastore"></a> [cloud\_init\_datastore](#input\_cloud\_init\_datastore) | Datastore for cloud-init drive (must support snippets) | `string` | `"local"` | no |
| <a name="input_cpu_cores"></a> [cpu\_cores](#input\_cpu\_cores) | Number of CPU cores (override module default of 2) | `number` | `4` | no |
| <a name="input_datastore"></a> [datastore](#input\_datastore) | Datastore for VM disks and EFI | `string` | `"local-lvm"` | no |
| <a name="input_disk_size"></a> [disk\_size](#input\_disk\_size) | Disk size in GB | `number` | `32` | no |
| <a name="input_display_type"></a> [display\_type](#input\_display\_type) | Display type for the VM (module default is 'std', common override is 'serial0') | `string` | `"serial0"` | no |
| <a name="input_dns_domain"></a> [dns\_domain](#input\_dns\_domain) | DNS domain for the VM | `string` | `null` | no |
| <a name="input_dns_servers"></a> [dns\_servers](#input\_dns\_servers) | List of DNS servers | `list(string)` | <pre>[<br/>  "1.1.1.1",<br/>  "8.8.8.8"<br/>]</pre> | no |
| <a name="input_enable_secondary_nic"></a> [enable\_secondary\_nic](#input\_enable\_secondary\_nic) | Enable secondary network interface | `bool` | `true` | no |
| <a name="input_ip_address"></a> [ip\_address](#input\_ip\_address) | Static IP address for the VM (without CIDR notation) | `string` | n/a | yes |
| <a name="input_ip_address_secondary"></a> [ip\_address\_secondary](#input\_ip\_address\_secondary) | Static IP address for secondary NIC (without CIDR notation) | `string` | `"192.168.2.100"` | no |
| <a name="input_memory"></a> [memory](#input\_memory) | Memory in MB (override module default of 2048) | `number` | `4096` | no |
| <a name="input_network_bridge"></a> [network\_bridge](#input\_network\_bridge) | Network bridge for the VM | `string` | `"vmbr0"` | no |
| <a name="input_network_bridge_secondary"></a> [network\_bridge\_secondary](#input\_network\_bridge\_secondary) | Secondary network bridge for the VM | `string` | `"vmbr1"` | no |
| <a name="input_network_cidr"></a> [network\_cidr](#input\_network\_cidr) | Network CIDR suffix (e.g., '24' for /24) | `string` | `"24"` | no |
| <a name="input_network_cidr_secondary"></a> [network\_cidr\_secondary](#input\_network\_cidr\_secondary) | Network CIDR suffix for secondary NIC (e.g., '24' for /24) | `string` | `"24"` | no |
| <a name="input_network_gateway"></a> [network\_gateway](#input\_network\_gateway) | Network gateway IP address | `string` | n/a | yes |
| <a name="input_proxmox_endpoint"></a> [proxmox\_endpoint](#input\_proxmox\_endpoint) | Proxmox API endpoint URL | `string` | `"https://proxmox.local:8006"` | no |
| <a name="input_proxmox_insecure"></a> [proxmox\_insecure](#input\_proxmox\_insecure) | Allow insecure TLS connections to Proxmox | `bool` | `true` | no |
| <a name="input_proxmox_node"></a> [proxmox\_node](#input\_proxmox\_node) | Proxmox node name where VM will be deployed | `string` | `"pve"` | no |
| <a name="input_ssh_public_keys"></a> [ssh\_public\_keys](#input\_ssh\_public\_keys) | List of SSH public keys for VM access | `list(string)` | `[]` | no |
| <a name="input_start_on_boot"></a> [start\_on\_boot](#input\_start\_on\_boot) | Start VM automatically when Proxmox node boots (module default is true) | `bool` | `true` | no |
| <a name="input_start_on_deploy"></a> [start\_on\_deploy](#input\_start\_on\_deploy) | Start VM immediately after deployment (module default is true) | `bool` | `true` | no |
| <a name="input_template_id"></a> [template\_id](#input\_template\_id) | VM template ID to clone from | `number` | `2000` | no |
| <a name="input_vlan_id"></a> [vlan\_id](#input\_vlan\_id) | VLAN ID for network isolation (null for no VLAN, module default) | `number` | `null` | no |
| <a name="input_vlan_id_secondary"></a> [vlan\_id\_secondary](#input\_vlan\_id\_secondary) | VLAN ID for secondary network interface (null for no VLAN, module default) | `number` | `null` | no |
| <a name="input_vm_description"></a> [vm\_description](#input\_vm\_description) | Description of the VM | `string` | `"Single VM deployed via Terraform"` | no |
| <a name="input_vm_id"></a> [vm\_id](#input\_vm\_id) | VM ID (optional, auto-assigned if not specified) | `number` | `null` | no |
| <a name="input_vm_name"></a> [vm\_name](#input\_vm\_name) | Name of the VM | `string` | `"my-vm"` | no |
| <a name="input_vm_tags"></a> [vm\_tags](#input\_vm\_tags) | Tags for the VM | `list(string)` | <pre>[<br/>  "terraform",<br/>  "single-vm"<br/>]</pre> | no |
| <a name="input_vm_username"></a> [vm\_username](#input\_vm\_username) | Username for the VM (created via cloud-init) | `string` | `"ubuntu"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_all_ip_addresses"></a> [all\_ip\_addresses](#output\_all\_ip\_addresses) | All IPv4 addresses assigned to the VM |
| <a name="output_all_mac_addresses"></a> [all\_mac\_addresses](#output\_all\_mac\_addresses) | All MAC addresses assigned to the VM |
| <a name="output_ansible_inventory"></a> [ansible\_inventory](#output\_ansible\_inventory) | Ansible inventory entry for this VM |
| <a name="output_connection_info"></a> [connection\_info](#output\_connection\_info) | Human-readable connection information |
| <a name="output_ip_address"></a> [ip\_address](#output\_ip\_address) | Primary IPv4 address of the VM |
| <a name="output_mac_address"></a> [mac\_address](#output\_mac\_address) | MAC address of the VM's primary network interface |
| <a name="output_ssh_command"></a> [ssh\_command](#output\_ssh\_command) | SSH command to connect to the VM |
| <a name="output_vm_id"></a> [vm\_id](#output\_vm\_id) | The VM ID in Proxmox |
| <a name="output_vm_name"></a> [vm\_name](#output\_vm\_name) | The VM name |
| <a name="output_vm_node"></a> [vm\_node](#output\_vm\_node) | The Proxmox node where the VM is deployed |

<!-- END_TF_DOCS -->## Outputs

This deployment provides several useful outputs:

### Basic Information

- `vm_id` - Proxmox VM ID
- `vm_name` - VM hostname
- `vm_node` - Proxmox node location
- `ip_address` - Primary IP address

### Connection Information

- `ssh_command` - Ready-to-use SSH command
- `connection_info` - Human-readable summary

### Automation Support

- `ansible_inventory` - JSON format for Ansible
- `all_ip_addresses` - All IPs (for multi-interface VMs)
- `all_mac_addresses` - MAC addresses

### Example Output Usage

```bash
# Get SSH command
tofu output -raw ssh_command

# Get Ansible inventory
tofu output -json ansible_inventory > inventory.json

# Get IP address
tofu output -raw ip_address
```

## Post-Deployment

### Verify VM is Running

```bash
# Get VM info
VM_IP=$(tofu output -raw ip_address)

# Test connectivity
ping -c 3 $VM_IP

# SSH into VM
ssh ubuntu@$VM_IP
```

### Configure with Ansible

```bash
# Generate Ansible inventory
tofu output -json ansible_inventory | jq -r '.all.hosts | keys[]' > hosts.txt

# Run Ansible playbook
ansible-playbook -i hosts.txt playbook.yml
```

### Install Software

```bash
ssh ubuntu@$(tofu output -raw ip_address)

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker (example)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu
```

## Cleanup

To destroy the VM:

```bash
tofu destroy
```

**Note**: If `prevent_destroy = true`, you must first set it to `false` before destroying.

## Troubleshooting

### Template Not Found

**Error**: `Error: unable to find template with ID 2000`

**Solution**:

```bash
# List templates on Proxmox
ssh root@proxmox 'qm list | grep template'

# Update template_id in terraform.tfvars
template_id = 9000  # Your actual template ID
```

### IP Address Not Assigned

**Error**: Output shows `ip_address = "N/A"`

**Causes**:

1. QEMU guest agent not running
2. VM still booting
3. Network configuration issue

**Solution**:

```bash
# Wait a few seconds and re-run
tofu refresh

# Check guest agent in VM
ssh ubuntu@<ip> 'systemctl status qemu-guest-agent'

# Restart guest agent
sudo systemctl restart qemu-guest-agent
```

### SSH Connection Refused

**Causes**:

1. VM still booting
2. Firewall blocking SSH
3. Cloud-init still running

**Solution**:

```bash
# Wait for cloud-init to complete
ssh ubuntu@<ip> 'cloud-init status --wait'

# Check SSH service
ssh ubuntu@<ip> 'systemctl status ssh'

# Check firewall
ssh ubuntu@<ip> 'sudo ufw status'
```

### Network Configuration Issues

**Error**: Cannot reach VM on network

**Solution**:

1. Verify network bridge exists: `ssh root@proxmox 'ip link show vmbr0'`
2. Check VLAN configuration if using VLANs
3. Verify gateway is correct
4. Check Proxmox firewall rules

### Disk Space Issues

**Error**: `no space left on device`

**Solution**:

```bash
# Check datastore space
ssh root@proxmox 'df -h'

# Check specific datastore
ssh root@proxmox 'pvesm status'

# Change datastore in terraform.tfvars
datastore = "other-datastore"
```

## Module Features Demonstrated

This example showcases:

- ✅ Single VM deployment via template-clone
- ✅ Static IP configuration
- ✅ VLAN support
- ✅ Cloud-init integration
- ✅ QEMU guest agent
- ✅ Lifecycle management
- ✅ Resource customization
- ✅ Comprehensive outputs
- ✅ Ansible integration support

## Scaling to Multiple VMs

If you need to deploy multiple VMs, consider:

1. **Similar VMs**: Use the [vm-cluster module](../microk8s-cluster/)
2. **Different VMs**: Create multiple module blocks in `main.tf`:

```hcl
module "web_server" {
  source = "../../../modules/vm"
  # ... configuration
}

module "db_server" {
  source = "../../../modules/vm"
  # ... configuration
}
```

## Related Documentation

- [vm Module Documentation](../../../modules/vm/README.md)
- [vm-cluster Module Documentation](../../../modules/vm-cluster/README.md)
- [Proxmox VM Provisioning Guide](../../../../docs/terraform/proxmox-vm-provisioning-guide.md)
- [CLAUDE.md Project Documentation](../../../../CLAUDE.md)

## Best Practices

1. **Use Templates**: Always clone from templates for consistency
2. **Tag Your VMs**: Use meaningful tags for organization
3. **Set Descriptions**: Document VM purpose
4. **Protect Production**: Set `prevent_destroy = true` for critical VMs
5. **Use Static IPs**: Easier for automation and monitoring
6. **Enable Guest Agent**: Required for IP address detection
7. **Regular Backups**: Use Proxmox backup features
8. **Version Control**: Keep terraform.tfvars in private repo or use secrets management

## Security Considerations

1. **SSH Keys Only**: Never use password authentication
2. **Firewall Configuration**: Configure UFW or iptables in cloud-init
3. **VLAN Isolation**: Use VLANs for network segmentation
4. **Regular Updates**: Automate system updates
5. **Minimal Exposure**: Only expose necessary ports
6. **Secrets Management**: Use Infisical, Vault, or similar for sensitive data

## License

Copyright 2025 RalZareck. Licensed under Apache 2.0.
