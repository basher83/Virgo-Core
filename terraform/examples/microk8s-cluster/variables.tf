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
# = Proxmox Configuration =====================================================
# =============================================================================

variable "proxmox_endpoint" {
  description = "Proxmox API endpoint URL"
  type        = string
  default     = "https://proxmox.local:8006"
}

variable "proxmox_insecure" {
  description = "Allow insecure TLS connections to Proxmox"
  type        = bool
  default     = true
}

# =============================================================================
# = Environment Configuration =================================================
# =============================================================================

variable "environment" {
  description = "Deployment environment (determines VM ID offset to prevent collisions)"
  type        = string
  default     = "staging"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# =============================================================================
# = Template Configuration ====================================================
# =============================================================================

variable "template_id" {
  description = "VM template ID to clone from"
  type        = number
  default     = 2000
}

variable "template_node" {
  description = "Proxmox node where the template is located (for cross-node cloning)"
  type        = string
  default     = "lloyd"
}

variable "datastore" {
  description = "Datastore for VM disks"
  type        = string
  default     = "local-lvm"
}

# =============================================================================
# = Network Configuration =====================================================
# =============================================================================

variable "network_bridge" {
  description = "Network bridge for VMs"
  type        = string
  default     = "vmbr0"
}

variable "vlan_id" {
  description = "VLAN ID for network isolation (null for no VLAN)"
  type        = number
  default     = 30
}

variable "network_cidr" {
  description = "Network CIDR suffix (e.g., '24' for /24)"
  type        = string
  default     = "24"
}

variable "network_gateway" {
  description = "Network gateway IP address"
  type        = string
  default     = "192.168.30.1"
}

# =============================================================================
# = Secondary Network Configuration (Optional) ================================
# =============================================================================

variable "enable_secondary_nic" {
  description = "Enable secondary network interface for all cluster nodes"
  type        = bool
  default     = true
}

variable "network_bridge_secondary" {
  description = "Secondary network bridge for VMs"
  type        = string
  default     = "vmbr1"
}

variable "vlan_id_secondary" {
  description = "VLAN ID for secondary network interface (null for no VLAN)"
  type        = number
  default     = null
}

# =============================================================================
# = Hardware Configuration ====================================================
# =============================================================================

variable "display_type" {
  description = "Display type for VMs (module default is 'std', common override is 'serial0')"
  type        = string
  default     = "serial0"
}

# Note: CPU cores and memory are defined per-node in locals.nodes in main.tf
# Note: vm_bios, vm_machine, vm_os, cpu_type, qemu_agent_*, disk_*, efi_*,
#       network_model, network_mtu, network_firewall removed - all module defaults

# =============================================================================
# = Cloud-init Configuration ==================================================
# =============================================================================

variable "cloud_init_datastore" {
  description = "Datastore for cloud-init drive"
  type        = string
  default     = "local"
}

variable "dns_servers" {
  description = "List of DNS servers"
  type        = list(string)
  default     = ["1.1.1.1", "8.8.8.8"]
}

variable "vm_username" {
  description = "Username for VMs"
  type        = string
  default     = "ubuntu"
}

# Note: cloud_init_interface removed - module defaults to "ide2" (Proxmox convention)

# =============================================================================
# = SSH Configuration =========================================================
# =============================================================================

variable "ssh_public_keys" {
  description = "List of SSH public keys for VM access"
  type        = list(string)
  default     = []
}

# =============================================================================
# = Start Configuration =======================================================
# =============================================================================

variable "start_on_deploy" {
  description = "Start VMs immediately after deployment (module default is true)"
  type        = bool
  default     = true
}

variable "start_on_boot" {
  description = "Start VMs automatically on Proxmox node boot (module default is true)"
  type        = bool
  default     = true
}

# Note: boot_order, boot_up_delay, boot_down_delay removed - module defaults to 0
