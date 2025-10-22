# MicroK8s Cluster Deployment Example

This example demonstrates deploying a multi-node MicroK8s Kubernetes cluster using the `vm` module with Terraform's `for_each` pattern. This approach eliminates the need for a separate cluster-specific module by leveraging composition over abstraction.

## 🎯 Key Concept: Composition Over Abstraction

**Why no cluster module?** This example shows that multi-VM deployments are better achieved through **composition** (using `for_each` with the base `vm` module) rather than creating an abstraction layer (a separate cluster module).

### Benefits of the for_each Pattern

✅ **Maximum Flexibility** - Full access to all vm module capabilities
✅ **Clear Logic** - Deployment-specific configuration visible in one place
✅ **Easy Customization** - Per-node overrides without fighting module constraints
✅ **DRY Principle** - Reuses the vm module without duplication
✅ **Terraform Best Practices** - Native for_each is more idiomatic than wrapper modules

## 📋 Overview

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

## 🛠️ Troubleshooting

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

### ❌ Anti-pattern: Wrapper Module
```hcl
# Constraining abstraction - NOT RECOMMENDED
module "cluster" {
  source = "../modules/vm-cluster"  # Hardcoded to clone-only
  nodes  = var.nodes
}
```

### ✅ Best Practice: Composition with for_each
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

## 📝 License

Copyright 2025 RalZareck. Licensed under Apache 2.0.
