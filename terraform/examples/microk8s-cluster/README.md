# MicroK8s Cluster Deployment Example

This example demonstrates deploying a multi-node MicroK8s Kubernetes cluster using the `vm`
module with Terraform's `for_each` pattern. This approach eliminates the need for a separate
cluster-specific module by leveraging composition over abstraction.

## Key Concept: Composition Over Abstraction

**Why no cluster module?** This example shows that multi-VM deployments are better achieved
through **composition** (using `for_each` with the base `vm` module) rather than creating an
abstraction layer (a separate cluster module).

### Benefits of the for_each Pattern

✅ **Maximum Flexibility** - Full access to all vm module capabilities
✅ **Clear Logic** - Deployment-specific configuration visible in one place
✅ **Easy Customization** - Per-node overrides without fighting module constraints
✅ **DRY Principle** - Reuses the vm module without duplication
✅ **Terraform Best Practices** - Native for_each is more idiomatic than wrapper modules

## Overview

This deployment creates:

- 3 Ubuntu VMs (microk8s-1, microk8s-2, microk8s-3)
- 4 CPU cores and 8GB RAM per node (customizable per-node)
- 50GB disk per node (customizable per-node)
- Network configuration with VLAN support (dual NIC capable)
- Cloud-init for initial setup with SSH key injection
- **Cross-node cloning** - Clone from one Proxmox node, deploy to multiple nodes

## 🏗️ Architecture Pattern

### The for_each Pattern

```hcl
# Define nodes in locals
locals {
  nodes = {
    "vm-1" = { pve_node = "pve1", ip_address = "192.168.1.11", ... }
    "vm-2" = { pve_node = "pve2", ip_address = "192.168.1.12", ... }
  }
}

# Deploy using for_each
module "cluster_vms" {
  source   = "../../../modules/vm"
  for_each = local.nodes

  vm_name  = each.key
  pve_node = each.value.pve_node
  # ... map each.value attributes to vm module variables
}
```

### Why This Pattern Works

1. **Native Terraform** - Uses built-in for_each, not custom abstraction
2. **Visible Configuration** - All cluster logic is in the deployment, not hidden in a module
3. **Flexible** - Can use vm module for templates, clones, or images
4. **Scalable** - Add nodes by adding entries to the map

## 📚 Prerequisites

1. **Proxmox Template** - A VM template must exist (default ID: 2000)
   - Ubuntu 22.04 LTS recommended
   - Cloud-init enabled
   - QEMU guest agent installed

2. **Network Configuration** - Ensure the network bridge and VLAN are configured in Proxmox

3. **Terraform** - Version >= 1.0

4. **Provider Authentication** - Set Proxmox credentials via environment variables:

   ```bash
   export PROXMOX_VE_USERNAME="root@pam"
   export PROXMOX_VE_PASSWORD="your-password"
   # OR use API token
   export PROXMOX_VE_API_TOKEN="user@realm!token-id=secret"
   ```

## 🚀 Usage

### 1. Configure Variables

Copy the example variables file and customize:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
proxmox_endpoint = "https://proxmox.local:8006"
template_id      = 2000
template_node    = "lloyd"
datastore        = "local-lvm"

network_bridge  = "vmbr0"
vlan_id         = 30
network_cidr    = "24"
network_gateway = "192.168.30.1"

ssh_public_keys = [
  "ssh-ed25519 AAAAC3... user@host"
]
```

### 2. Review Node Configuration

Edit `main.tf` to customize nodes:

```hcl
locals {
  nodes = {
    "microk8s-1" = {
      pve_node   = "holly"
      ip_address = "192.168.30.101"
      cpu_cores  = 4
      memory     = 8192
      disk_size  = 50
    }
    # Add more nodes here
  }
}
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Deploy the Cluster

```bash
terraform plan
terraform apply
```

### 5. Access the Cluster

Terraform outputs connection details:

```bash
terraform output cluster_ips
terraform output ssh_commands
terraform output cluster_inventory
```

## 🎨 Customization Examples

### Add More Nodes

Simply add entries to the `locals.nodes` map:

```hcl
locals {
  nodes = {
    "microk8s-1" = { ... }
    "microk8s-2" = { ... }
    "microk8s-3" = { ... }
    "microk8s-4" = {
      pve_node   = "holly"
      ip_address = "192.168.30.104"
      cpu_cores  = 8     # More powerful worker
      memory     = 16384
      disk_size  = 100
    }
  }
}
```

### Per-Node Customization

Different resources per node:

```hcl
locals {
  nodes = {
    "master" = {
      pve_node   = "pve1"
      ip_address = "192.168.30.10"
      cpu_cores  = 4
      memory     = 8192
      disk_size  = 50
    }
    "worker-gpu" = {
      pve_node   = "pve2"
      ip_address = "192.168.30.21"
      cpu_cores  = 8
      memory     = 32768
      disk_size  = 200
    }
  }
}
```

### Dual NIC Configuration

Enable secondary network interface:

```hcl
# In terraform.tfvars
enable_secondary_nic       = true
network_bridge_secondary   = "vmbr1"
vlan_id_secondary          = null

# In main.tf locals
locals {
  nodes = {
    "microk8s-1" = {
      pve_node             = "holly"
      ip_address           = "192.168.30.101"  # Primary
      ip_address_secondary = "192.168.2.101"   # Secondary
      # ...
    }
  }
}
```

### Cross-Node Cloning

Deploy VMs across multiple Proxmox nodes from a single template:

```hcl
# Template lives on 'lloyd'
template_node = "lloyd"

# VMs deployed to different nodes
locals {
  nodes = {
    "vm-1" = { pve_node = "holly", ... }  # Clones from lloyd → holly
    "vm-2" = { pve_node = "mable", ... }  # Clones from lloyd → mable
    "vm-3" = { pve_node = "lloyd", ... }  # Uses local template
  }
}
```

## 📤 Outputs

The example provides comprehensive outputs:

```bash
# Node IP addresses
terraform output cluster_ips

# VM IDs
terraform output cluster_ids

# SSH commands
terraform output ssh_commands

# Ansible inventory (JSON)
terraform output -json cluster_inventory

# Human-readable summary
terraform output cluster_summary
```

## 🔧 Advanced Patterns

### Conditional Node Deployment

Use Terraform expressions to conditionally include nodes:

```hcl
locals {
  # Define all possible nodes
  all_nodes = {
    "master-1" = { ... }
    "master-2" = { ... }
    "worker-1" = { ... }
    "worker-2" = { ... }
  }

  # Deploy only specific nodes based on variable
  nodes = var.deploy_workers ? local.all_nodes : {
    for k, v in local.all_nodes : k => v if !startswith(k, "worker")
  }
}
```

### Dynamic Resource Sizing

Size nodes based on role:

```hcl
locals {
  # Resource profiles
  profiles = {
    master = { cpu_cores = 4, memory = 8192, disk_size = 50 }
    worker = { cpu_cores = 8, memory = 16384, disk_size = 100 }
  }

  nodes = {
    "master-1" = merge(local.profiles.master, {
      pve_node   = "pve1"
      ip_address = "192.168.30.11"
    })
    "worker-1" = merge(local.profiles.worker, {
      pve_node   = "pve2"
      ip_address = "192.168.30.21"
    })
  }
}
```

## 🔗 Integration with Ansible

Export inventory for Ansible automation:

```bash
# Export to Ansible inventory
terraform output -json cluster_inventory > ../../../../ansible/inventory/microk8s.json

# Or use YAML format with jq
terraform output -json cluster_inventory | yq -P > ../../../../ansible/inventory/microk8s.yml
```

Then configure MicroK8s:

```bash
cd ../../../../ansible
ansible-playbook -i inventory/microk8s.yml playbooks/microk8s-deploy.yml
```

## 🧹 Cleanup

To destroy the cluster:

```bash
terraform destroy
```

## Troubleshooting

### Template Not Found

Ensure the template exists and the ID is correct:

```bash
qm list | grep template
```

### Network Connectivity Issues

- Verify VLAN configuration in Proxmox
- Check bridge and gateway settings
- Ensure firewall rules allow traffic

### Cloud-init Not Running

- Verify qemu-guest-agent is installed in template
- Check cloud-init logs: `cloud-init status --long`

### Cross-Node Cloning Fails

- Ensure template exists on source node
- Verify network connectivity between Proxmox nodes
- Check storage permissions on target nodes

## 📖 Pattern Comparison

### Anti-pattern: Wrapper Module

```hcl
# Constraining abstraction - NOT RECOMMENDED
module "cluster" {
  source = "../modules/vm-cluster"  # Hardcoded to clone-only
  nodes  = var.nodes
}
```

### Best Practice: Composition with for_each

```hcl
# Flexible composition - RECOMMENDED
module "cluster_vms" {
  source   = "../modules/vm"
  for_each = local.nodes

  vm_type = "clone"  # Could be "image" for templates
  # Full control over vm module
}
```

## 📚 Related Documentation

- [vm Module Documentation](../../../modules/vm/README.md)
- [Proxmox VM Provisioning Guide](../../../../docs/terraform/proxmox-vm-provisioning-guide.md)
- [Terraform for_each Documentation](https://www.terraform.io/language/meta-arguments/for_each)

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
| <a name="module_cluster_vms"></a> [cluster\_vms](#module\_cluster\_vms) | ../../../modules/vm | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cloud_init_datastore"></a> [cloud\_init\_datastore](#input\_cloud\_init\_datastore) | Datastore for cloud-init drive | `string` | `"local"` | no |
| <a name="input_datastore"></a> [datastore](#input\_datastore) | Datastore for VM disks | `string` | `"local-lvm"` | no |
| <a name="input_display_type"></a> [display\_type](#input\_display\_type) | Display type for VMs (module default is 'std', common override is 'serial0') | `string` | `"serial0"` | no |
| <a name="input_dns_servers"></a> [dns\_servers](#input\_dns\_servers) | List of DNS servers | `list(string)` | <pre>[<br/>  "1.1.1.1",<br/>  "8.8.8.8"<br/>]</pre> | no |
| <a name="input_enable_secondary_nic"></a> [enable\_secondary\_nic](#input\_enable\_secondary\_nic) | Enable secondary network interface for all cluster nodes | `bool` | `true` | no |
| <a name="input_environment"></a> [environment](#input\_environment) | Deployment environment (determines VM ID offset to prevent collisions) | `string` | `"staging"` | no |
| <a name="input_network_bridge"></a> [network\_bridge](#input\_network\_bridge) | Network bridge for VMs | `string` | `"vmbr0"` | no |
| <a name="input_network_bridge_secondary"></a> [network\_bridge\_secondary](#input\_network\_bridge\_secondary) | Secondary network bridge for VMs | `string` | `"vmbr1"` | no |
| <a name="input_network_cidr"></a> [network\_cidr](#input\_network\_cidr) | Network CIDR suffix (e.g., '24' for /24) | `string` | `"24"` | no |
| <a name="input_network_gateway"></a> [network\_gateway](#input\_network\_gateway) | Network gateway IP address | `string` | `"192.168.30.1"` | no |
| <a name="input_proxmox_endpoint"></a> [proxmox\_endpoint](#input\_proxmox\_endpoint) | Proxmox API endpoint URL | `string` | `"https://proxmox.local:8006"` | no |
| <a name="input_proxmox_insecure"></a> [proxmox\_insecure](#input\_proxmox\_insecure) | Allow insecure TLS connections to Proxmox | `bool` | `true` | no |
| <a name="input_ssh_public_keys"></a> [ssh\_public\_keys](#input\_ssh\_public\_keys) | List of SSH public keys for VM access | `list(string)` | `[]` | no |
| <a name="input_start_on_boot"></a> [start\_on\_boot](#input\_start\_on\_boot) | Start VMs automatically on Proxmox node boot (module default is true) | `bool` | `true` | no |
| <a name="input_start_on_deploy"></a> [start\_on\_deploy](#input\_start\_on\_deploy) | Start VMs immediately after deployment (module default is true) | `bool` | `true` | no |
| <a name="input_template_id"></a> [template\_id](#input\_template\_id) | VM template ID to clone from | `number` | `2000` | no |
| <a name="input_template_node"></a> [template\_node](#input\_template\_node) | Proxmox node where the template is located (for cross-node cloning) | `string` | `"lloyd"` | no |
| <a name="input_vlan_id"></a> [vlan\_id](#input\_vlan\_id) | VLAN ID for network isolation (null for no VLAN) | `number` | `30` | no |
| <a name="input_vlan_id_secondary"></a> [vlan\_id\_secondary](#input\_vlan\_id\_secondary) | VLAN ID for secondary network interface (null for no VLAN) | `number` | `null` | no |
| <a name="input_vm_username"></a> [vm\_username](#input\_vm\_username) | Username for VMs | `string` | `"ubuntu"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_cluster_ids"></a> [cluster\_ids](#output\_cluster\_ids) | Map of node names to their VM IDs |
| <a name="output_cluster_inventory"></a> [cluster\_inventory](#output\_cluster\_inventory) | Ansible-friendly inventory output with hostnames and IPs |
| <a name="output_cluster_ips"></a> [cluster\_ips](#output\_cluster\_ips) | Map of node names to their primary IPv4 addresses (with fallback to configured IPs) |
| <a name="output_cluster_macs"></a> [cluster\_macs](#output\_cluster\_macs) | Map of node names to their MAC addresses |
| <a name="output_cluster_nodes"></a> [cluster\_nodes](#output\_cluster\_nodes) | Map of all cluster nodes with their details |
| <a name="output_cluster_summary"></a> [cluster\_summary](#output\_cluster\_summary) | Human-readable cluster summary |
| <a name="output_ssh_commands"></a> [ssh\_commands](#output\_ssh\_commands) | SSH commands to connect to each node |

<!-- END_TF_DOCS -->

## 📝 License

Copyright 2025 RalZareck. Licensed under Apache 2.0.
