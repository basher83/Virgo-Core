terraform {
  required_version = ">= 1.0"

  required_providers {
    proxmox = {
      version = ">= 0.84.1"
      source  = "bpg/proxmox"
    }
  }
}

# =============================================================================
# = Proxmox Provider Configuration ============================================
# =============================================================================
# IMPORTANT: Template creation requires SSH access to the Proxmox host
# for image import operations. Configure provider as follows:

provider "proxmox" {
  endpoint = var.proxmox_endpoint
  insecure = var.proxmox_insecure

  # Authentication handled via environment variables or API token
  # PROXMOX_VE_USERNAME, PROXMOX_VE_PASSWORD
  # or PROXMOX_VE_API_TOKEN

  # SSH required for image import (cloud image download + import)
  ssh {
    agent    = true             # Use local SSH agent for authentication
    username = var.ssh_username # SSH user on Proxmox host (e.g., "terraform")
  }
}

variable "ssh_username" {
  type        = string
  description = "SSH username for Proxmox host (required for image import)"
  default     = "terraform"
}
