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

variable "proxmox_node" {
  description = "Proxmox node name where VM will be deployed"
  type        = string
  default     = "pve"
}

# =============================================================================
# = Template Configuration ====================================================
# =============================================================================

variable "template_id" {
  description = "VM template ID to clone from"
  type        = number
  default     = 2000

  validation {
    condition     = var.template_id > 0
    error_message = "Template ID must be a positive integer"
  }
}

variable "datastore" {
  description = "Datastore for VM disks and EFI"
  type        = string
  default     = "local-lvm"
}

# =============================================================================
# = VM Configuration ==========================================================
# =============================================================================

variable "vm_name" {
  description = "Name of the VM"
  type        = string
  default     = "my-vm"

  validation {
    condition     = can(regex("^[a-zA-Z0-9-]+$", var.vm_name))
    error_message = "VM name must contain only alphanumeric characters and hyphens"
  }
}

variable "vm_id" {
  description = "VM ID (optional, auto-assigned if not specified)"
  type        = number
  default     = null
}

variable "vm_description" {
  description = "Description of the VM"
  type        = string
  default     = "Single VM deployed via Terraform"
}

variable "vm_tags" {
  description = "Tags for the VM"
  type        = list(string)
  default     = ["terraform", "single-vm"]
}

# =============================================================================
# = Hardware Configuration ====================================================
# =============================================================================

variable "cpu_cores" {
  description = "Number of CPU cores (override module default of 2)"
  type        = number
  default     = 4

  validation {
    condition     = var.cpu_cores > 0 && var.cpu_cores <= 128
    error_message = "CPU cores must be between 1 and 128"
  }
}

variable "memory" {
  description = "Memory in MB (override module default of 2048)"
  type        = number
  default     = 4096

  validation {
    condition     = var.memory >= 512 && var.memory <= 524288
    error_message = "Memory must be between 512 MB and 512 GB"
  }
}

variable "disk_size" {
  description = "Disk size in GB"
  type        = number
  default     = 32

  validation {
    condition     = var.disk_size >= 1 && var.disk_size <= 32768
    error_message = "Disk size must be between 1 GB and 32 TB"
  }
}

variable "display_type" {
  description = "Display type for the VM (module default is 'std', common override is 'serial0')"
  type        = string
  default     = "serial0"
}

# =============================================================================
# = Network Configuration =====================================================
# =============================================================================

variable "network_bridge" {
  description = "Network bridge for the VM"
  type        = string
  default     = "vmbr0"
}

variable "vlan_id" {
  description = "VLAN ID for network isolation (null for no VLAN, module default)"
  type        = number
  default     = null
}

# Note: network_firewall removed - module defaults to false

variable "ip_address" {
  description = "Static IP address for the VM (without CIDR notation)"
  type        = string

  validation {
    condition     = can(regex("^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$", var.ip_address))
    error_message = "IP address must be a valid IPv4 address without CIDR notation"
  }
}

variable "network_cidr" {
  description = "Network CIDR suffix (e.g., '24' for /24)"
  type        = string
  default     = "24"

  validation {
    condition     = can(regex("^[0-9]{1,2}$", var.network_cidr)) && tonumber(var.network_cidr) >= 0 && tonumber(var.network_cidr) <= 32
    error_message = "network_cidr must be a number between 0 and 32"
  }
}

variable "network_gateway" {
  description = "Network gateway IP address"
  type        = string

  validation {
    condition     = can(regex("^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$", var.network_gateway))
    error_message = "network_gateway must be a valid IPv4 address"
  }
}

# =============================================================================
# = Secondary Network Configuration (Optional) ================================
# =============================================================================

variable "enable_secondary_nic" {
  description = "Enable secondary network interface"
  type        = bool
  default     = true
}

variable "network_bridge_secondary" {
  description = "Secondary network bridge for the VM"
  type        = string
  default     = "vmbr1"
}

variable "vlan_id_secondary" {
  description = "VLAN ID for secondary network interface (null for no VLAN, module default)"
  type        = number
  default     = null
}

# Note: network_firewall_secondary removed - module defaults to false

variable "ip_address_secondary" {
  description = "Static IP address for secondary NIC (without CIDR notation)"
  type        = string
  default     = "192.168.2.100"

  validation {
    condition     = can(regex("^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$", var.ip_address_secondary))
    error_message = "ip_address_secondary must be a valid IPv4 address without CIDR notation"
  }
}

variable "network_cidr_secondary" {
  description = "Network CIDR suffix for secondary NIC (e.g., '24' for /24)"
  type        = string
  default     = "24"

  validation {
    condition     = can(regex("^[0-9]{1,2}$", var.network_cidr_secondary)) && tonumber(var.network_cidr_secondary) >= 0 && tonumber(var.network_cidr_secondary) <= 32
    error_message = "network_cidr_secondary must be a number between 0 and 32"
  }
}

# =============================================================================
# = DNS Configuration =========================================================
# =============================================================================

variable "dns_domain" {
  description = "DNS domain for the VM"
  type        = string
  default     = null
}

variable "dns_servers" {
  description = "List of DNS servers"
  type        = list(string)
  default     = ["1.1.1.1", "8.8.8.8"]
}

# =============================================================================
# = Cloud-init Configuration ==================================================
# =============================================================================

variable "cloud_init_datastore" {
  description = "Datastore for cloud-init drive (must support snippets)"
  type        = string
  default     = "local"
}

variable "vm_username" {
  description = "Username for the VM (created via cloud-init)"
  type        = string
  default     = "ubuntu"
}

variable "ssh_public_keys" {
  description = "List of SSH public keys for VM access"
  type        = list(string)
  default     = []

  validation {
    condition     = length(var.ssh_public_keys) > 0
    error_message = "At least one SSH public key must be provided"
  }
}

# =============================================================================
# = Start Configuration =======================================================
# =============================================================================

variable "start_on_deploy" {
  description = "Start VM immediately after deployment (module default is true)"
  type        = bool
  default     = true
}

variable "start_on_boot" {
  description = "Start VM automatically when Proxmox node boots (module default is true)"
  type        = bool
  default     = true
}

# Note: boot_order, boot_up_delay, boot_down_delay removed - module defaults to 0
