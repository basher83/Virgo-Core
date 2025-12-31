---
title: "Infrastructure Architecture"
description: "Comprehensive architecture documentation for all three Proxmox VE clusters: Matrix, Nexus, and Quantum"
---

# Infrastructure Architecture

This document provides a holistic view of all three Proxmox VE clusters managed by Virgo-Core, consolidating hardware specifications, network topology, storage configuration, and operational details into a single source of truth.

## Executive Summary

Virgo-Core manages three Proxmox VE clusters with distinct topologies, hardware configurations, and purposes:

| Cluster | Nodes | Purpose | Storage | Status |
|---------|-------|---------|---------|--------|
| **Matrix** | 3 (Foxtrot, Golf, Hotel) | Production cluster | CEPH distributed storage | Production-ready ✅ |
| **Nexus** | 2 (Alpha, Bravo) | Original cluster, mixed workloads | Local LVM-thin + NFS | Active |
| **Quantum** | 3 (Holly, Lloyd, Mable) | Currently idle | Local LVM-thin + NFS | Idle (future TBD) |

### Quick Reference

**Cluster Names & Node IDs:**

- **Matrix**: foxtrot (5), golf (6), hotel (7)
- **Nexus**: alpha (50), bravo (30)
- **Quantum**: holly (3), lloyd (2), mable (4)

**Network Subnets:**

- **Matrix**: 192.168.3.0/24 (mgmt), 192.168.5.0/24 (CEPH public), 192.168.7.0/24 (CEPH private), 192.168.8.0/24 (corosync)
- **Nexus**: 192.168.30.0/24 (management)
- **Quantum**: 192.168.10.0/24 (mgmt), 192.168.11.0/24 (secondary)

**Shared Infrastructure:**

- TrueNAS server: 192.168.30.6 (NFS storage)
- Proxmox Backup Server: 192.168.30.200 (currently unreachable)
- DNS domain: spaceships.work

## Global Configuration

All clusters share common configuration managed through Ansible `group_vars/all.yml`:

### Ansible Connection Settings

- **User**: `ansible`
- **Python**: `/usr/bin/python3`
- **Become**: Enabled via sudo
- **Become Method**: sudo

### System Configuration

- **Timezone**: America/New_York (all clusters)
- **NTP Servers**:
  - `time.google.com`
  - `time.cloudflare.com`

### SSH Hardening

- **Port**: 22
- **Password Authentication**: Disabled (key-only)
- **Root Login**: Allowed via key only
- **X11 Forwarding**: Disabled
- **DNS Lookup**: Disabled (faster connections)

### Infisical Secrets Management

Per-cluster Infisical paths for secrets management:

- **Matrix**: `/matrix`
- **Nexus**: `/nexus`
- **Quantum**: `/quantum`

**Global Settings:**

- Project ID: `7b832220-24c0-45bc-a5f1-ce9794a31259`
- Environment: `prod`

### Shared Storage

- **TrueNAS Server**: 192.168.30.6
  - Provides NFS exports for Nexus and Quantum clusters
- **Proxmox Backup Server**: 192.168.30.200
  - Status: Currently unreachable

### Common Packages

Packages installed on all Proxmox nodes:

- vim, tmux, htop
- curl, wget, git, rsync
- screen, net-tools, dnsutils

### Proxmox VE Configuration

Shared Proxmox settings (`group_vars/proxmox_clusters.yml`):

- **Target Version**: 8.x
- **Certificate Validation**: Disabled (homelab environment)
- **Default Storage Type**: LVM-thin
- **Network Management**: Backup enabled, reload enabled, verification enabled

## Matrix Cluster

**Status**: Production-ready, fully configured ✅

### Overview

Matrix is the production 3-node Proxmox VE 9.x cluster with CEPH distributed storage. All nodes have identical hardware and are fully automated via Ansible roles.

### Nodes

| Node | Node ID | Management IP | CEPH Public IP | CEPH Private IP | Corosync IP |
|------|---------|---------------|----------------|-----------------|-------------|
| Foxtrot | 5 | 192.168.3.5/24 | 192.168.5.5/24 | 192.168.7.5/24 | 192.168.8.5/24 |
| Golf | 6 | 192.168.3.6/24 | 192.168.5.6/24 | 192.168.7.6/24 | 192.168.8.6/24 |
| Hotel | 7 | 192.168.3.7/24 | 192.168.5.7/24 | 192.168.7.7/24 | 192.168.8.7/24 |

**Hostnames**: `{node}.matrix.spaceships.work` (e.g., `foxtrot.matrix.spaceships.work`)

### Hardware Configuration

All nodes have identical hardware:

**Chassis**: MINISFORUM MS-A2 (mini PC)

**Compute:**

- **CPU**: AMD Ryzen 9 9955HX
  - 16 cores / 32 threads
- **RAM**: 64GB total
  - 2× 32GB A-DATA DDR5 SODIMMs (model CBDAD5S560032G-BAD)
  - Running at 5600 MT/s (dual-channel)

**Storage:**

- **Boot Disk**: 1× 1TB Crucial P3 (nvme0n1)
  - Partitioning: EFI partition + LVM2_member
- **CEPH Storage**: 2× 4TB Samsung 990 PRO
  - nvme1n1: 3.6TB usable (2 OSDs)
  - nvme2n1: 3.6TB usable (2 OSDs)
  - Total: 4 OSDs per node = 12 OSDs cluster-wide

**Network Interfaces:**

- **Management**: Realtek RTL8125 2.5GbE (enp4s0)
- **CEPH Public**: Intel X710 10GbE SFP+ port 0 (enp5s0f0np0)
- **CEPH Private**: Intel X710 10GbE SFP+ port 1 (enp5s0f1np1)
- **Unused**: Intel I226-V Gigabit (enp3s0), MediaTek WiFi (wlp6s0)

### Network Architecture

**Bridge Configuration:**

| Bridge | Physical Interface | IP Range | MTU | Purpose |
|--------|-------------------|----------|-----|---------|
| vmbr0 | enp4s0 | 192.168.3.0/24 | 1500 | Management (VLAN-aware) |
| vmbr1 | enp5s0f0np0 | 192.168.5.0/24 | 9000 | CEPH Public network |
| vmbr2 | enp5s0f1np1 | 192.168.7.0/24 | 9000 | CEPH Private network |

**VLAN Configuration:**

- **vlan9**: Corosync network
  - Parent: vmbr0
  - IP Range: 192.168.8.0/24
  - Purpose: Cluster communication

**Network Notes:**

- Gateway: 192.168.3.1 (via vmbr0)
- Jumbo frames (MTU 9000) required for CEPH networks
- UniFi Controller must have jumbo frames enabled for CEPH ports

### Storage Architecture

**CEPH Configuration:**

- **Version**: Squid (for PVE 9.x)
- **Monitors**: 3 (1 per node)
- **Managers**: 3 (1 per node)
- **OSDs**: 12 total (4 per node)
  - 2 OSDs per NVMe drive
  - Device class: nvme

**Storage Capacity:**

- **Raw Capacity**: 24TB (12 OSDs × 2TB per OSD)
- **Usable Capacity**: ~12TB (with replication factor 3)
- **Performance**: NVMe-backed, 10GbE network, jumbo frames

**CEPH Pools:**

- **vm_ssd**: 128 PGs, size 3, min_size 2 (for VM storage)
- **vm_containers**: 64 PGs, size 3, min_size 2 (for container storage)

### Cluster Formation

- **Cluster Name**: `matrix`
- **Corosync Network**: 192.168.8.0/24 (VLAN 9)
- **Multicast Address**: 239.192.8.1
- **Multicast Port**: 5405

### Initialization

Matrix cluster initialization is automated via `ansible/playbooks/initialize-matrix-cluster.yml`, which:

1. Configures Proxmox repositories
2. Forms the cluster
3. Deploys CEPH storage

## Nexus Cluster

**Status**: Active, proper Proxmox cluster

### Overview

Nexus is the original Proxmox cluster hosting mixed LXC and VM workloads. Nodes have different hardware configurations, and storage is provided via local LVM-thin volumes plus NFS mounts from TrueNAS.

### Nodes

| Node | Node ID | Management IP |
|------|---------|---------------|
| Alpha | 50 | 192.168.30.50/24 |
| Bravo | 30 | 192.168.30.30/24 |

**Hostnames**: `{node}.nexus.spaceships.work` (inferred from naming convention)

### Hardware Configuration

#### Alpha Node

**Vendor/Model**: Protectli VP4630

**Compute:**

- **CPU**: Intel Core i3-10110U @ 2.10GHz (Comet Lake, 10th Gen)
  - 2 cores / 4 threads
  - Speed: 400 MHz - 4.1 GHz (turbo)
- **RAM**: 64GB total
  - 2× 32GB DDR4 modules (Crucial)
  - Speed: 3200 MT/s (running at 2667 MT/s)
  - Current usage: ~7GB used, 55GB available

**Storage:**

- **Primary**: 3.6TB Samsung SSD 870 EVO 4TB (SATA)
- **Secondary**: 1.8TB Kingston SNV2S2000G (NVMe)
- **Additional**: 14.6GB eMMC storage

**Network:**

- **Management**: Intel I225-V 2.5GbE (enp1s0) - Active
- **Additional NICs**: 5× Intel I225-V 2.5GbE controllers (enp2s0, enp3s0, enp4s0, enp5s0, enp6s0) - All DOWN, available

**Software:**

- **OS**: Debian GNU/Linux
- **Proxmox VE**: 8.4.0 (manager 8.4.14)
- **Kernel**: 6.8.12-15-pve

#### Bravo Node

**Vendor/Model**: Dell PowerEdge T430 (Serial: GN23XM2)

**Compute:**

- **CPU**: Intel Xeon E5-2680 v4 @ 2.40GHz
  - 2 sockets
  - 14 cores per socket (28 total cores)
  - 56 threads (hyperthreading enabled)
  - Max frequency: 3.3 GHz
- **RAM**: 256GB total (251 GiB)
  - 8× 32GB DDR4 modules
  - Maximum capacity: 1536GB (12 slots available)
  - Currently available: 217 GiB

**Storage:**

- **Boot Disk**: /dev/sda (10.9TB)
- **VM Storage**: LVM-thin pool on /dev/sda3 (VG: pve, thin pool: data)

**Network:**

- **Management**: Intel X550 1GbE (enp130s0f1) - Active
- **Additional NICs**:
  - Intel X550 10GbE (enp130s0f0) - DOWN, bridged to vmbr1
  - 2× Broadcom BCM5720 1GbE (eno1, eno2) - DOWN

**Software:**

- **OS**: Debian GNU/Linux 12 (bookworm)
- **Kernel**: Linux 6.8.12-15-pve (Proxmox VE)
- **Firmware**: 2.16.0

### Network Architecture

**Bridge Configuration:**

| Bridge | Physical Interface | IP Range | MTU | VLAN-aware |
|--------|-------------------|----------|-----|------------|
| vmbr0 | enp1s0 (alpha) / enp130s0f1 (bravo) | 192.168.30.0/24 | 1500 | No |

**Network Notes:**

- Gateway: 192.168.30.1
- Single bridge configuration (management only)
- No VLANs configured
- Standard MTU (1500)

### Storage Architecture

**Local Storage:**

- **Type**: LVM-thin
- **Storage Backend**: `local-lvm` using thin pool `data` in VG `pve`

**NFS Storage (TrueNAS at 192.168.30.6):**

| Mount Point | Export Path | Usage | Size |
|-------------|-------------|-------|------|
| /mnt/pve/pbs | /mnt/DataLake/pbs | backups, ISOs, templates, images | 13TB |
| /mnt/pve/TrueNAS | /mnt/DataLake/NFSshare | backups, templates, ISOs, images | 11TB |
| /mnt/pve/swarm | /mnt/DataLake/swarm | images, rootdir | 11TB |

**Backup Locations:**

- Local: `/var/lib/vz` (local directory)
- NFS: TrueNAS mounts
- PBS: `pbs-real` at 192.168.30.200 (currently unreachable)

### Cluster Formation

- **Cluster Name**: `nexus`
- **Corosync Network**: 192.168.30.0/24
- **Status**: Proper Proxmox cluster (not standalone nodes)

## Quantum Cluster

**Status**: Idle, future purpose TBD

### Overview

Quantum (formerly "Doggos") is a 3-node cluster of identical Minisforum MS-01 mini PCs. Previously hosted HashiCorp Vault, Nomad/Consul, and MicroK8s workloads. All workloads have been removed, and the cluster is currently idle awaiting future purpose.

### Nodes

| Node | Node ID | Management IP (vmbr0) | Secondary IP (vmbr1) |
|------|---------|----------------------|---------------------|
| Holly | 3 | 192.168.10.3/24 | 192.168.11.3/24 |
| Lloyd | 2 | 192.168.10.2/24 | 192.168.11.2/24 |
| Mable | 4 | 192.168.10.4/24 | 192.168.11.4/24 |

**Hostnames**: `{node}.quantum.spaceships.work` (inferred from naming convention)

### Hardware Configuration

All nodes have identical hardware:

**Vendor/Model**: Minisforum MS-01

**Compute:**

- **CPU**: Intel Core i9-13900H
  - 14 cores / 20 threads
- **RAM**: 32GB total (31GiB usable)

**Storage:**

- **Boot Disk**: 1TB NVMe (nvme0n1, 953.9GB)
- **Additional Storage**: None detected (single NVMe only)

**Network:**

- **Active NICs**:
  - enp87s0: Active on vmbr0 (management)
  - enp2s0f0np0: Active on vmbr1 (10GbE SFP+)
- **Unused NICs**:
  - enp88s0: Available
  - enp2s0f1np1: Available (10GbE SFP+)
  - wlp89s0: WiFi (unused)

**Note**: All three MS-01s are identically configured.

### Network Architecture

**Bridge Configuration:**

| Bridge | Physical Interface | IP Range | MTU | VLAN-aware |
|--------|-------------------|----------|-----|------------|
| vmbr0 | enp87s0 | 192.168.10.0/24 | 1500 | Yes (VLANs 2-4094) |
| vmbr1 | enp2s0f0np0 | 192.168.11.0/24 | 1500 | Yes (VLANs 2-4094) |

**Network Notes:**

- Gateway: 192.168.10.1 (via vmbr0)
- Dual bridge configuration
- VLAN capability enabled on both bridges (no specific VLANs actively configured)
- Standard MTU (1500)
- Note: Tailscale0 interface uses MTU 1280

### Storage Architecture

**Local Storage:**

- **Type**: LVM-thin (primary) + dir (secondary)
- **Boot Disk**: nvme0n1 (953.9GB)
- **VM Storage**: `local-lvm` (LVM-thin on `pve/data`)
- **Directory Storage**: `local` at `/var/lib/vz`

**NFS Storage (TrueNAS at 192.168.30.6):**

| Mount Point | Export Path | Usage | Size |
|-------------|-------------|-------|------|
| /mnt/pve/nomad-volumes | /mnt/DataLake/nomad-volumes | VMs, LXCs, ISOs, backups, snippets, templates | 10.6TB |

**Storage Layout Preferences:**

- **VMs**: Primary `local-lvm`, available `nomad-volumes`
- **LXCs**: Primary `local-lvm`, available `nomad-volumes`
- **Backups**: local, nomad-volumes, PBS (currently offline)
- **ISOs/Templates**: local, nomad-volumes

### Cluster Formation

- **Cluster Name**: `quantum` (renamed from "doggos")
- **Corosync Network**: TBD (update when Proxmox cluster configured)
- **Status**: Proper Proxmox cluster

### Former Workloads

Previously hosted:

- 4-node HashiCorp Vault cluster
- 3-node HashiCorp Nomad/Consul cluster
- 3-node MicroK8s cluster

All workloads have been removed. Cluster is now idle awaiting future purpose.

## Network Architecture

### IP Address Allocation Summary

| Subnet | Purpose | Cluster(s) | Gateway |
|--------|---------|------------|---------|
| 192.168.3.0/24 | Management | Matrix | 192.168.3.1 |
| 192.168.5.0/24 | CEPH Public | Matrix | N/A |
| 192.168.7.0/24 | CEPH Private | Matrix | N/A |
| 192.168.8.0/24 | Corosync (VLAN 9) | Matrix | N/A |
| 192.168.10.0/24 | Management | Quantum | 192.168.10.1 |
| 192.168.11.0/24 | Secondary | Quantum | N/A |
| 192.168.30.0/24 | Management | Nexus | 192.168.30.1 |

### VLAN Configuration

| Cluster | VLAN ID | Parent Bridge | IP Range | Purpose |
|---------|---------|---------------|----------|---------|
| Matrix | 9 | vmbr0 | 192.168.8.0/24 | Corosync cluster communication |
| Nexus | None | N/A | N/A | No VLANs configured |
| Quantum | 2-4094 (capability) | vmbr0, vmbr1 | N/A | VLAN-aware, no specific VLANs configured |

### DNS Naming Convention

**Domain**: `spaceships.work`

**Format**: `<service>-<number>-<cluster>.<domain>`

**Examples:**

- `docker-01-nexus.spaceships.work`
- `foxtrot.matrix.spaceships.work`
- `alpha.nexus.spaceships.work`

DNS records are automatically managed via NetBox + PowerDNS integration.

## Storage Architecture

### Matrix Cluster: CEPH Distributed Storage

**Configuration:**

- **CEPH Version**: Squid (for PVE 9.x)
- **Monitors**: 3 (1 per node)
- **Managers**: 3 (1 per node)
- **OSDs**: 12 total (4 per node, 2 per NVMe drive)

**Storage Pools:**

- **vm_ssd**: VM storage (128 PGs, replication factor 3)
- **vm_containers**: Container storage (64 PGs, replication factor 3)

**Capacity:**

- Raw: 24TB
- Usable: ~12TB (with replication factor 3)

**Performance:**

- NVMe-backed OSDs
- 10GbE network (separate public/private networks)
- Jumbo frames (MTU 9000)

### Nexus Cluster: Local + NFS Storage

**Local Storage:**

- LVM-thin volumes (`local-lvm`)
- Thin pool: `data` in VG `pve`

**NFS Storage (TrueNAS 192.168.30.6):**

- 3 NFS mounts totaling 35TB shared storage
- Used for backups, ISOs, templates, images, container rootdirs

### Quantum Cluster: Local + NFS Storage

**Local Storage:**

- LVM-thin volumes (`local-lvm`) - primary
- Directory storage (`local`) - secondary

**NFS Storage (TrueNAS 192.168.30.6):**

- 1 NFS mount: `nomad-volumes` (10.6TB)
- Used for VMs, LXCs, ISOs, backups, snippets, templates

### Shared Storage Infrastructure

**TrueNAS Server:**

- **IP**: 192.168.30.6
- **Exports**:
  - `/mnt/DataLake/pbs` → Nexus (13TB)
  - `/mnt/DataLake/NFSshare` → Nexus (11TB)
  - `/mnt/DataLake/swarm` → Nexus (11TB)
  - `/mnt/DataLake/nomad-volumes` → Quantum (10.6TB)

**Proxmox Backup Server:**

- **IP**: 192.168.30.200
- **Status**: Currently unreachable
- **Intended Use**: Centralized backups for all clusters

## Hardware Specifications

### Matrix Cluster Hardware Summary

| Component | Specification |
|-----------|---------------|
| **Chassis** | MINISFORUM MS-A2 (mini PC) |
| **CPU** | AMD Ryzen 9 9955HX (16 cores / 32 threads) |
| **RAM** | 64GB DDR5 (5600 MT/s) |
| **Boot Storage** | 1TB Crucial P3 NVMe |
| **CEPH Storage** | 2× 4TB Samsung 990 PRO NVMe (per node) |
| **Management NIC** | Realtek RTL8125 2.5GbE |
| **CEPH NICs** | 2× Intel X710 10GbE SFP+ |

### Nexus Cluster Hardware Summary

| Node | CPU | RAM | Storage | Management NIC |
|------|-----|-----|---------|----------------|
| **Alpha** | Intel i3-10110U (2C/4T) | 64GB DDR4 | 3.6TB SATA + 1.8TB NVMe | Intel I225-V 2.5GbE |
| **Bravo** | Dual Xeon E5-2680 v4 (28C/56T) | 256GB DDR4 | 10.9TB (boot) | Intel X550 1GbE |

### Quantum Cluster Hardware Summary

| Component | Specification |
|-----------|---------------|
| **Chassis** | Minisforum MS-01 (all nodes identical) |
| **CPU** | Intel Core i9-13900H (14 cores / 20 threads) |
| **RAM** | 32GB (per node) |
| **Boot Storage** | 1TB NVMe (per node) |
| **Management NIC** | enp87s0 (2.5GbE likely) |
| **Secondary NIC** | enp2s0f0np0 (10GbE SFP+) |

### Compute Resources Summary

| Cluster | Total Cores | Total Threads | Total RAM | Storage Type |
|---------|------------|---------------|-----------|--------------|
| **Matrix** | 48 | 96 | 192GB | CEPH (24TB raw) |
| **Nexus** | 30 | 60 | 320GB | Local + NFS |
| **Quantum** | 42 | 60 | 96GB | Local + NFS |

## Integration Points

### NetBox + PowerDNS

**Purpose**: Single source of truth for IPAM and automated DNS management

**Components:**

- **NetBox**: Infrastructure documentation and IPAM
- **PowerDNS**: Authoritative DNS server
- **NetBox PowerDNS Sync Plugin**: Automatic DNS record generation
- **Diode + Orb Agent**: Automated network discovery

**DNS Naming**: Records automatically generated from NetBox device inventory (e.g., `docker-01-nexus.spaceships.work`)

**Reference**: See [NetBox + PowerDNS Integration](../documentation/core/netbox-powerdns.md)

### Infisical Secrets Management

**Per-Cluster Paths:**

- Matrix: `/matrix`
- Nexus: `/nexus`
- Quantum: `/quantum`

**Usage**: Ansible roles use Infisical lookup for secrets (SSH keys, API tokens, etc.)

**Example**: `{{ lookup('infisical', 'SECRET_NAME') }}`

### Terraform/OpenTofu Integration

**Modules Used**: External module from `github.com/basher83/Triangulum-Prime//terraform-bgp-vm`

**Supported VM Types:**

- `vm_type = "image"`: Downloads cloud image and creates template
- `vm_type = "clone"`: Clones from existing template to create VMs

**Key Principle**: Only specify values that differ from module defaults

**Reference**: See [VM Deployment Guide](../terraform/netbox-vm/README.md)

### Ansible Automation

**Roles**: 6 production-ready roles managing Proxmox infrastructure:

- `system_user`: Linux user management
- `proxmox_access`: Proxmox users, tokens, ACLs
- `proxmox_network`: Network bridges, VLANs, MTU
- `proxmox_repository`: APT repository management
- `proxmox_cluster`: Cluster formation and Corosync
- `proxmox_ceph`: CEPH distributed storage deployment

**Collections**: `community.proxmox`, `infisical.vault`, `ansible.posix`, `geerlingguy.docker`

**Reference**: See [Ansible Role Design](../documentation/design/ansible-role-design.md)

## Operational Notes

### Cluster Naming Conventions

- **Cluster Names**: Lowercase (matrix, nexus, quantum)
- **Node Names**: Military phonetic alphabet (Foxtrot, Golf, Hotel, Alpha, Bravo, Holly, Lloyd, Mable)
- **Hostnames**: `{node}.{cluster}.spaceships.work`

### Node ID Patterns

Node IDs match the last octet of management IP addresses:

- **Matrix**: Node IDs 5, 6, 7 → IPs 192.168.3.{5,6,7}
- **Nexus**: Node IDs 50, 30 → IPs 192.168.30.{50,30}
- **Quantum**: Node IDs 3, 2, 4 → IPs 192.168.10.{3,2,4}

### Inventory Structure

**File**: `ansible/inventory/proxmox.yml`

**Hierarchy:**

```text
all
└── proxmox_clusters
    ├── matrix_cluster
    ├── nexus_cluster
    └── quantum_cluster
```

**Group Variables:**

- `group_vars/all.yml`: Global settings
- `group_vars/proxmox_clusters.yml`: Shared Proxmox settings
- `group_vars/matrix_cluster.yml`: Matrix-specific configuration
- `group_vars/nexus_cluster.yml`: Nexus-specific configuration
- `group_vars/quantum_cluster.yml`: Quantum-specific configuration

### Playbook References

**Matrix Cluster Initialization:**

- `ansible/playbooks/initialize-matrix-cluster.yml`: Complete Matrix cluster setup (network, cluster, CEPH)

**Common Playbooks:**

- `ansible/playbooks/system-upgrade.yml`: CEPH-aware rolling upgrades
- `ansible/playbooks/configure-network.yml`: Network configuration
- `ansible/playbooks/create-ansible-user.yml`: User management

### Tooling Conventions

- **Use `tofu` not `terraform`**: Repository migrated to OpenTofu
- **Ansible via uv**: Always prefix with `uv run` (e.g., `uv run ansible-playbook`)
- **Mise for tasks**: Use `mise run <task>` for common operations

### Related Documentation

- [Infrastructure Specifications](../documentation/core/infrastructure.md) - Detailed Matrix cluster specs
- [Goals](../documentation/core/goals.md) - Project roadmap
- [NetBox + PowerDNS](../documentation/core/netbox-powerdns.md) - DNS/IPAM integration
- [Ansible Role Design](../documentation/design/ansible-role-design.md) - Role architecture patterns
- [Ansible Playbook Design](../documentation/design/ansible-playbook-design.md) - Playbook patterns
- [Inventory Reorganization Checklist](./brainstorming/inventory-reorganization-checklist.md) - Cluster information gathering notes
