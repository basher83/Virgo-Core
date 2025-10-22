# =============================================================================
# = Cluster Outputs ===========================================================
# =============================================================================

output "cluster_nodes" {
  description = "Map of all cluster nodes with their details"
  value = {
    for name, vm in module.cluster_vms : name => {
      vm_id          = vm.vm_id
      vm_name        = vm.vm_name
      node           = vm.vm_node
      ipv4_addresses = vm.ipv4_addresses
      ipv6_addresses = vm.ipv6_addresses
      mac_addresses  = vm.mac_addresses
    }
  }
}

output "cluster_ips" {
  description = "Map of node names to their primary IPv4 addresses (with fallback to configured IPs)"
  value = {
    for name, vm in module.cluster_vms :
    name => vm.primary_ip # Uses enhanced output with fallback logic
  }
}

output "cluster_ids" {
  description = "Map of node names to their VM IDs"
  value = {
    for name, vm in module.cluster_vms :
    name => vm.vm_id
  }
}

output "cluster_macs" {
  description = "Map of node names to their MAC addresses"
  value = {
    for name, vm in module.cluster_vms :
    name => vm.mac_addresses
  }
}

output "cluster_inventory" {
  description = "Ansible-friendly inventory output with hostnames and IPs"
  value = {
    all = {
      hosts = {
        for name, vm in module.cluster_vms :
        name => {
          ansible_host = vm.primary_ip # Uses enhanced output with fallback
          vm_id        = vm.vm_id
          pve_node     = vm.vm_node
        }
      }
    }
  }
}

output "cluster_summary" {
  description = "Human-readable cluster summary"
  value       = <<-EOT
    Cluster Deployment Summary
    ==========================
    Total Nodes: ${length(module.cluster_vms)}

    Nodes:
    ${join("\n    ", [for name, vm in module.cluster_vms : "${name}: ${vm.primary_ip} (ID: ${vm.vm_id}, Node: ${vm.vm_node})"])}
  EOT
}

output "ssh_commands" {
  description = "SSH commands to connect to each node"
  value = {
    for name, vm in module.cluster_vms :
    name => "ssh ubuntu@${vm.primary_ip}"
  }
}
