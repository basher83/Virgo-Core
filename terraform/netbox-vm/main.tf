# =============================================================================
# = Single VM Deployment Example =============================================
# =============================================================================
# This example demonstrates deploying a single VM using the vm module with
# the template-clone approach. Perfect for application servers, databases,
# development environments, or any single-VM workload.
#
# This example follows DRY principles by:
# - Only specifying values that differ from module defaults
# - Not repeating module defaults (see terraform/modules/vm/DEFAULTS.md)
# - Keeping configuration minimal and focused

# =============================================================================
# = Single VM Deployment ======================================================
# =============================================================================

module "single_vm" {
  source = "github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=v1.0.0"

  # Required: VM type and Proxmox node
  vm_type  = "clone"
  pve_node = var.proxmox_node

  # Required: Clone source
  src_clone = {
    datastore_id = var.datastore
    tpl_id       = var.template_id
  }

  # Required: VM identification
  vm_name        = var.vm_name
  vm_id          = var.vm_id
  vm_description = var.vm_description
  vm_tags        = var.vm_tags

  # Override: Production-ready CPU/memory (defaults are 2 cores / 2GB)
  vm_cpu = {
    cores = var.cpu_cores # Override for production workload
    # type defaults to "host" - no need to specify
  }

  vm_mem = {
    dedicated = var.memory # Override for production workload
    # floating/shared default to null - no need to specify
  }

  # Override: Display type if needed (default is "std")
  # Only specify if you need serial console or specific display adapter
  vm_display = var.display_type != "std" ? {
    type = var.display_type
  } : {}

  # Required: EFI disk for UEFI boot
  vm_efi_disk = {
    datastore_id = var.datastore
    # file_format defaults to "raw" - no need to specify
    # type defaults to "4m" - no need to specify
  }

  # Required: Disk configuration
  vm_disk = {
    scsi0 = {
      datastore_id = var.datastore
      size         = var.disk_size
      main_disk    = true
      # file_format, iothread, ssd, discard all have optimal defaults
    }
  }

  # Required: Network configuration
  # Note: Dual NIC support simplified - only specify what differs from defaults
  vm_net_ifaces = merge(
    {
      net0 = {
        bridge    = var.network_bridge
        vlan_id   = var.vlan_id
        ipv4_addr = "${var.ip_address}/${var.network_cidr}"
        ipv4_gw   = var.network_gateway
        # enabled, firewall, model, mtu all have sensible defaults
      }
    },
    var.enable_secondary_nic ? {
      net1 = {
        bridge    = var.network_bridge_secondary
        vlan_id   = var.vlan_id_secondary
        ipv4_addr = "${var.ip_address_secondary}/${var.network_cidr_secondary}"
        ipv4_gw   = null # Secondary NIC doesn't need a gateway
      }
    } : {}
  )

  # Required: Cloud-init configuration
  vm_init = {
    datastore_id = var.cloud_init_datastore
    # interface defaults to "ide2" (Proxmox convention) - no need to specify

    dns = {
      domain  = var.dns_domain
      servers = var.dns_servers
    }

    user = {
      name = var.vm_username
      keys = var.ssh_public_keys
    }
  }

  # Override: VM start settings (only if different from defaults)
  vm_start = {
    on_deploy = var.start_on_deploy
    on_boot   = var.start_on_boot
    # order, up_delay, down_delay default to 0 - no need to specify
  }

  # Note: The following are NOT specified because module defaults are optimal:
  # - vm_bios (defaults to "ovmf" for UEFI)
  # - vm_machine (defaults to "q35" modern chipset)
  # - vm_os (defaults to "l26" for Linux 2.6+)
  # - vm_agent (defaults to enabled with 15m timeout and trim)
  # - vm_rng (defaults to /dev/urandom for entropy)
  # - vm_serial (defaults to serial0 socket for console access)
  # See terraform/modules/vm/DEFAULTS.md for complete defaults reference
}
