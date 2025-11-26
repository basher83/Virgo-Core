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

provider "proxmox" {
  endpoint = var.proxmox_endpoint
  insecure = var.proxmox_insecure

  # Authentication handled via environment variables or API token
  # PROXMOX_VE_USERNAME, PROXMOX_VE_PASSWORD
  # or PROXMOX_VE_API_TOKEN
}
