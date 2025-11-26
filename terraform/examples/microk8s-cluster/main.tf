# =============================================================================
# = MicroK8s Cluster Deployment Example ======================================
# =============================================================================
# This example demonstrates deploying a 3-node MicroK8s cluster using the
# vm module with for_each. This pattern eliminates the need for a separate
# cluster module by using Terraform's native for_each capability.
#
# This example follows DRY principles by:
# - Only specifying values that differ from module defaults
# - Using for_each with the vm module (Terraform best practice)
# - Not repeating module defaults (see terraform/modules/vm/DEFAULTS.md)
# - Keeping configuration minimal and focused on cluster-specific values

# =============================================================================
# = Local Values ==============================================================
# =============================================================================

locals {
  # Environment-based VM ID offsets (prevents ID collisions between environments)
  # See: docs/terraform/deployment-patterns.md#pattern-2-environment-based-vm-id-offsets
  env_offsets = {
    dev     = 2000 # dev: 2000-2999
    staging = 3000 # staging: 3000-3999
    prod    = 4000 # prod: 4000-4999
  }
  vm_id_offset = local.env_offsets[var.environment]

  # Deterministic MAC addresses (prevents MAC drift across provider updates)
  # See: docs/terraform/deployment-patterns.md#pattern-1-deterministic-mac-addressing
  # Format: 02:50:00:[VLAN]:[HOST]:[NIC] where 02 = locally administered unicast
  cluster_macs = {
    "microk8s-1" = {
      mac1 = "02:50:00:30:01:01" # Primary NIC (VLAN 30, host 01, nic 01)
      mac2 = "02:50:00:02:01:01" # Secondary NIC (VLAN 2, host 01, nic 01)
    }
    "microk8s-2" = {
      mac1 = "02:50:00:30:01:02"
      mac2 = "02:50:00:02:01:02"
    }
    "microk8s-3" = {
      mac1 = "02:50:00:30:01:03"
      mac2 = "02:50:00:02:01:03"
    }
  }

  # Define cluster nodes with their configuration
  # Only node-specific values that differ per VM
  nodes = {
    "microk8s-1" = {
      vm_id                = local.vm_id_offset + 101 # 3101 for staging, 4101 for prod
      pve_node             = "holly"
      ip_address           = "192.168.30.101"
      ip_address_secondary = var.enable_secondary_nic ? "192.168.2.101" : null
      cpu_cores            = 4
      memory               = 8192
      disk_size            = 50
    }
    "microk8s-2" = {
      vm_id                = local.vm_id_offset + 102
      pve_node             = "mable"
      ip_address           = "192.168.30.102"
      ip_address_secondary = var.enable_secondary_nic ? "192.168.2.102" : null
      cpu_cores            = 4
      memory               = 8192
      disk_size            = 50
    }
    "microk8s-3" = {
      vm_id                = local.vm_id_offset + 103
      pve_node             = "lloyd"
      ip_address           = "192.168.30.103"
      ip_address_secondary = var.enable_secondary_nic ? "192.168.2.103" : null
      cpu_cores            = 4
      memory               = 8192
      disk_size            = 50
    }
  }

  # Cluster-wide tags applied to all nodes
  cluster_tags = ["microk8s", "kubernetes", "cluster", var.environment]
}

# =============================================================================
# = MicroK8s Cluster VMs ======================================================
# =============================================================================

module "cluster_vms" {
  source   = "../../../modules/vm"
  for_each = local.nodes

  # Required: Node identification
  vm_type  = "clone"
  vm_id    = each.value.vm_id
  pve_node = each.value.pve_node
  vm_name  = each.key
  vm_tags  = concat(local.cluster_tags, ["node-${each.key}"])

  # Required: Clone configuration
  src_clone = {
    datastore_id = var.datastore
    node_name    = var.template_node
    tpl_id       = var.template_id
  }

  # Override: Production-ready CPU/memory per node
  vm_cpu = {
    cores = each.value.cpu_cores
    # type defaults to "host" - no need to specify
  }

  vm_mem = {
    dedicated = each.value.memory
    # floating/shared default to null - no need to specify
  }

  # Override: Display type if needed (default is "std")
  vm_display = var.display_type != "std" ? {
    type = var.display_type
  } : {}

  # Required: EFI disk for UEFI boot
  vm_efi_disk = {
    datastore_id = var.datastore
    # file_format, type, pre_enrolled_keys have sensible defaults
  }

  # Required: Disk configuration
  vm_disk = {
    scsi0 = {
      datastore_id = var.datastore
      size         = each.value.disk_size
      main_disk    = true
      # file_format, iothread, ssd, discard all have optimal defaults
    }
  }

  # Required: Network configuration with deterministic MAC addresses
  # Simplified - only specify what differs from defaults
  vm_net_ifaces = merge(
    {
      net0 = {
        bridge    = var.network_bridge
        vlan_id   = var.vlan_id
        mac_addr  = local.cluster_macs[each.key].mac1 # Deterministic MAC
        ipv4_addr = "${each.value.ip_address}/${var.network_cidr}"
        ipv4_gw   = var.network_gateway
        # enabled, firewall, model, mtu all have sensible defaults
      }
    },
    var.enable_secondary_nic && each.value.ip_address_secondary != null ? {
      net1 = {
        bridge    = var.network_bridge_secondary
        vlan_id   = var.vlan_id_secondary
        mac_addr  = local.cluster_macs[each.key].mac2 # Deterministic MAC
        ipv4_addr = "${each.value.ip_address_secondary}/${var.network_cidr}"
        ipv4_gw   = null
      }
    } : {}
  )

  # Required: Cloud-init configuration
  vm_init = {
    datastore_id = var.cloud_init_datastore
    # interface defaults to "ide2" (Proxmox convention) - no need to specify

    dns = {
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
