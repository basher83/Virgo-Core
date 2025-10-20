# Copyright 2025 RalZareck
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# =============================================================================
# = VM Outputs ================================================================
# =============================================================================

output "vm_id" {
  description = "The VM ID in Proxmox"
  value       = module.single_vm.vm_id
}

output "vm_name" {
  description = "The VM name"
  value       = module.single_vm.vm_name
}

output "vm_node" {
  description = "The Proxmox node where the VM is deployed"
  value       = module.single_vm.vm_node
}

output "ip_address" {
  description = "Primary IPv4 address of the VM"
  value       = try(module.single_vm.ipv4_addresses[1][0], module.single_vm.ipv4_addresses[0][0], "N/A")
}

output "all_ip_addresses" {
  description = "All IPv4 addresses assigned to the VM"
  value       = module.single_vm.ipv4_addresses
}

output "mac_address" {
  description = "MAC address of the VM's primary network interface"
  value       = try(module.single_vm.mac_addresses[0], "N/A")
}

output "all_mac_addresses" {
  description = "All MAC addresses assigned to the VM"
  value       = module.single_vm.mac_addresses
}

output "ssh_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh ${var.vm_username}@${try(module.single_vm.ipv4_addresses[1][0], module.single_vm.ipv4_addresses[0][0], "N/A")}"
}

output "connection_info" {
  description = "Human-readable connection information"
  value       = <<-EOT
    VM Deployment Complete
    ======================
    VM Name: ${module.single_vm.vm_name}
    VM ID:   ${module.single_vm.vm_id}
    Node:    ${module.single_vm.vm_node}
    IP:      ${try(module.single_vm.ipv4_addresses[1][0], module.single_vm.ipv4_addresses[0][0], "N/A")}

    SSH Access:
    ${var.vm_username}@${try(module.single_vm.ipv4_addresses[1][0], module.single_vm.ipv4_addresses[0][0], "N/A")}

    Quick Commands:
    - SSH:    ssh ${var.vm_username}@${try(module.single_vm.ipv4_addresses[1][0], module.single_vm.ipv4_addresses[0][0], "N/A")}
    - Ping:   ping ${try(module.single_vm.ipv4_addresses[1][0], module.single_vm.ipv4_addresses[0][0], "N/A")}
  EOT
}

output "ansible_inventory" {
  description = "Ansible inventory entry for this VM"
  value = {
    all = {
      hosts = {
        (module.single_vm.vm_name) = {
          ansible_host = try(module.single_vm.ipv4_addresses[1][0], module.single_vm.ipv4_addresses[0][0], "N/A")
          ansible_user = var.vm_username
          vm_id        = module.single_vm.vm_id
          pve_node     = module.single_vm.vm_node
        }
      }
    }
  }
}
