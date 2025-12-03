# Inventory Reorganization Checklist

**Date**: 2025-11-18
**Purpose**: Gather cluster topology information for inventory reorganization
**Status**: Information Gathering

## Overview

Creating comprehensive `group_vars/` structure for 3 Proxmox clusters with different topologies:

- **Nexus**: Original cluster, hot mess of everything, local storage
- **Matrix**: Production 3-node cluster, CEPH storage (ALREADY CONFIGURED ✅)
- **Doggos**: 3x Minisforum MS-01s, formerly Vault/Nomad/k8s, now idle, NFS+local storage

## Confirmed Global Settings ✅

- [x] `ansible_user`: ansible
- [x] `system_timezone`: America/New_York
- [x] `system_ntp_servers`: Google/Cloudflare
- [x] `ssh_*`: To be determined based on security requirements

---

## Nexus Cluster Information Needed

### Basic Configuration

- [x] **Node IDs**
  - alpha: `50`
  - bravo: `30`
  - **Question**: Do these match IP octet patterns like Matrix does?
  - **Answer**: Yes, they match the IP octet patterns like Matrix does.

- [x] **Cluster Name**
  - Formal name: `nexus`
  - **Question**: Should this stay "nexus" or rename to something else?
  - **Answer**: This should stay "nexus".

### Network Topology

- [x] **Management Network**
  - Bridge name: `vmbr0`
  - Physical interface: `enp1s0`
  - IP addressing pattern: `192.168.30.50/24`
  - Gateway: `192.168.30.1`
  - VLAN-aware? No
  - **Question**: Same network topology as Matrix (vmbr0, vmbr1, vmbr2) or different?
  - **Answer**: Different, Nexus has a single network.

- [x] **Additional Bridges** (if any)
  - **Answer**: N/A - Nexus uses only vmbr0 (management)

- [x] **VLANs** (if any)
  - **Answer**: N/A - No VLANs configured

- [x] **MTU Settings**
  - Jumbo frames enabled? No
  - MTU value: `1500`
  - **Question**: Any special MTU requirements?
  - **Answer**: No, standard MTU.

### Storage Configuration

#### Alpha Node

- [x] **Storage Type**
  - Primary: Local + NFS
  - ZFS: No (no pools available)
  - LVM: Yes (LVM-thin in use)
  - Local storage backend: LVM-thin (`local-lvm` using thin pool `data` in VG `pve`)

- [x] **Storage Locations**
  - Boot disk: `/dev/sda` (with EFI partition on `/dev/sda2`)
  - VM storage:
    - Primary: LVM-thin volume `pve/data` (3.49 TB, 3.67% used)
    - Additional: NFS mount TrueNAS and swarm
  - LXC storage:
    - Primary: LVM-thin `local-lvm`
    - Additional: NFS mounts
  - Backup location:
    - `/var/lib/vz` (local directory - 94GB total, 37% used)
    - NFS pbs at `/mnt/pve/pbs` (13TB, 18% used)
    - NFS TrueNAS at `/mnt/pve/TrueNAS` (11TB, 3% used)
    - Proxmox Backup Server `pbs-real` at `192.168.30.200` (currently unreachable)

- [x] **Shared Storage**
  - NFS mounts: Yes (3 active mounts)
  - NFS server: `192.168.30.6` (TrueNAS)
  - Mount points:
    - `/mnt/pve/pbs` - backups, ISOs, templates, images (13TB)
    - `/mnt/pve/TrueNAS` - backups, templates, ISOs, images (11TB)
    - `/mnt/pve/swarm` - container images and rootdirs (11TB)

#### Bravo Node

- [x] **Storage Type**
  - Primary: Local + NFS (not local only)
  - ZFS: No (no pools available)
  - LVM: Yes (LVM-thin configured)
  - Local storage backend: LVM-thin (`local-lvm` using thin pool on VG `pve`)

- [x] **Storage Locations**
  - Boot disk: `/dev/sda` (10.9TB)
  - VM storage: `local-lvm` (LVM-thin pool on `/dev/sda3`, VG: `pve`, thin pool: `data`)
  - LXC storage: `local-lvm` (same thin pool as VMs)
  - Backup locations:
    - Local: `/var/lib/vz` (local storage)
    - NFS: `/mnt/pve/TrueNAS` and `/mnt/pve/pbs`
    - PBS (currently inactive): `pbs-real` at `192.168.30.200`

- [x] **Shared Storage**
  - NFS mounts: Yes (3 NFS mounts)
  - NFS server: `192.168.30.6` (TrueNAS)
  - Mount points:
    - `/mnt/pve/TrueNAS` ← `/mnt/DataLake/NFSshare` (backups, ISOs, templates, images)
    - `/mnt/pve/swarm` ← `/mnt/DataLake/swarm` (images, rootdir)
    - `/mnt/pve/pbs` ← `/mnt/DataLake/pbs` (backups, ISOs, images, templates)

### Hardware Details

- [x] **Physical Interfaces** Alpha
  - Management NIC: `enp1s0` (bridged to `vmbr0` with IP `192.168.30.50`)
  - Speed: 2.5GbE (2500Mb/s Full Duplex)
  - Additional NICs: 5 additional Intel I225-V 2.5GbE controllers:
    - `enp2s0` (DOWN, available)
    - `enp3s0` (DOWN, available)
    - `enp4s0` (DOWN, available)
    - `enp5s0` (DOWN, available)
    - `enp6s0` (DOWN, available)
  - Hardware: 6x Intel Corporation Ethernet Controller I225-V (rev 03) - all 2.5GbE capable
  - Current Configuration: Only `enp1s0` is active and bridged to `vmbr0` for management traffic. The remaining 5 NICs are configured but not in use.

- [x] **Physical Interfaces** Bravo
  - Management NIC: `enp130s0f1` (bridged to `vmbr0` with IP `192.168.30.30/24`)
  - Speed: 1GbE (currently running at 1000Mb/s)
  - Additional NICs:
    - `enp130s0f0` - Intel X550 (supports up to 10GbE, currently DOWN, bridged to `vmbr1`)
    - `eno1` - Broadcom BCM5720 (1GbE, currently DOWN)
    - `eno2` - Broadcom BCM5720 (1GbE, currently DOWN)
  - Network Hardware Summary:
    - 2x Broadcom BCM5720 Gigabit Ethernet (`eno1`, `eno2`)
    - 2x Intel X550 Ethernet Controllers (`enp130s0f0`, `enp130s0f1`) - 10GbE capable
    - Active management on Intel X550 port at 1GbE speed

- [x] **Node Differences**

#### Alpha Node

- **Hostname**: `alpha`
- **Hardware**:
  - Vendor: Protectli
  - Model: VP4630
- **CPU**:
  - Model: Intel Core i3-10110U @ 2.10GHz (Comet Lake, 10th Gen)
  - Cores: 2 cores / 4 threads
  - Speed: 400 MHz - 4.1 GHz (turbo)
  - Architecture: x86_64
- **Memory**:
  - Total RAM: 64 GB (2x 32GB)
  - Type: DDR4
  - Speed: 3200 MT/s (running at 2667 MT/s)
  - Manufacturer: Crucial
  - Current Usage: 6.9 GB used, 55 GB available
- **Storage**:
  - Primary: 3.6TB Samsung SSD 870 EVO 4TB (SATA)
  - Secondary: 1.8TB Kingston SNV2S2000G (NVMe)
  - Additional: 14.6GB eMMC storage
- **Network**:
  - NICs: 6x Intel I225-V 2.5GbE controllers
- **Software**:
  - OS: Debian GNU/Linux
  - Proxmox VE: 8.4.0 (manager 8.4.14)
  - Kernel: 6.8.12-15-pve

#### Bravo Node

- **Hostname**: `bravo`
- **Vendor/Model**:
  - Manufacturer: Dell Inc.
  - Model: PowerEdge T430
  - Serial Number: GN23XM2
  - Chassis: Server
- **CPU**:
  - Model: Intel Xeon E5-2680 v4 @ 2.40GHz
  - Sockets: 2
  - Cores per socket: 14 (28 total cores)
  - Threads: 56 (2 threads per core, hyperthreading enabled)
  - Max frequency: 3.3 GHz
  - Architecture: x86_64
- **RAM**:
  - Total: 256 GB (251 GiB)
  - Type: DDR4
  - Configuration: 8x 32GB modules
  - Maximum capacity: 1536 GB (12 slots available)
  - Currently available: 217 GiB
- **Operating System**:
  - OS: Debian GNU/Linux 12 (bookworm)
  - Kernel: Linux 6.8.12-15-pve (Proxmox VE)
  - Firmware: 2.16.0

### Cluster-Specific Settings

- [x] **Cluster Formation**
  - Is this a Proxmox cluster? Yes
  - If yes, cluster name in Proxmox: `nexus`
  - Corosync network: `192.168.30.0/24`
  - **Question**: Is Nexus a proper Proxmox cluster or standalone nodes?
  - **Answer**: Yes, Nexus is a proper Proxmox cluster.

- [x] **Special Configuration**
  - LXC-heavy workload settings: No
  - Custom kernel parameters: None
  - Memory overcommit ratio: Default
  - **Answer**: No special tuning for LXC workloads

---

## Doggos Cluster Information Needed

### Basic Configuration

- [x] **Node IDs**
  - holly: `3`
  - lloyd: `2`
  - mable: `4`
  - **Answer**: Confirmed - matches IP addressing pattern

- [x] **Cluster Name**
  - Current name: `doggos`
  - Future name: `quantum`
  - **Answer**: Will be renamed to "quantum"

### Network Topology

#### Lloyd Node

- [x] **Management Network**
  - Bridge name: `vmbr0`
  - Physical interface: `enp87s0`
  - IP addressing pattern: `192.168.10.2/24`
  - Gateway: `192.168.10.1`
  - VLAN-aware: Yes
  - VLAN IDs: 2-4094

- [x] **Additional Bridges**
  - Bridge 2 name: `vmbr1` (purpose: secondary network on `192.168.11.0/24`)
  - Physical interface: `enp2s0f0np0`
  - IP: `192.168.11.2/24`
  - VLAN-aware: Yes
  - **Answer**: Doggos uses 2 bridges (`vmbr0` + `vmbr1`)

- [x] **VLANs**
  - VLAN-aware enabled on both bridges
  - Supports VLAN IDs 2-4094
  - No specific VLANs currently configured in the interfaces file
  - **Answer**: VLAN capability enabled, no specific VLANs actively configured

- [x] **MTU Settings**
  - Jumbo frames enabled: No
  - MTU value: `1500` (standard on all interfaces)
  - Note: `Tailscale0` uses MTU `1280`

### Storage Configuration

#### Lloyd Node

- [x] **Local Storage**
  - Storage type: LVM-thin (primary) + dir (secondary)
  - Boot disk: `nvme0n1` (953.9GB)
  - VM storage: `local-lvm` (LVM-thin on `pve/data`)
  - Directory storage: `local` at `/var/lib/vz`

- [x] **NFS Storage**
  - NFS server: `192.168.30.6` (NAS)
  - NFS export: `/mnt/DataLake/nomad-volumes`
  - Mount point: `/mnt/pve/nomad-volumes`
  - Usage: VMs, LXCs, ISOs, backups, snippets, templates
  - Size: ~10.6TB total available

- [x] **Storage Layout**
  - VMs: `local-lvm` (primary) / NFS (available)
  - LXCs: `local-lvm` (primary) / NFS (available)
  - Backups: local, NFS, PBS (currently offline at `192.168.30.200`)
  - ISOs/Templates: local, NFS

### Hardware Details

#### Lloyd Node (Minisforum MS-01)

- [x] **Configuration**
  - CPU: Intel Core i9-13900H (14 cores, 20 threads)
  - RAM: 32GB (31GiB usable)
  - Boot disk: 1TB NVMe (`nvme0n1` - 953.9GB)
  - Additional storage: None detected (single NVMe only)
  - Network: 4x physical NICs (2x 2.5GbE likely, 2x 10GbE SFP+)
    - `enp87s0` (active on `vmbr0`)
    - `enp88s0` (unused)
    - `enp2s0f0np0` (active on `vmbr1`)
    - `enp2s0f1np1` (unused)
    - `wlp89s0` (WiFi - unused)

**Note**: The PBS (Proxmox Backup Server) at `192.168.30.200` is currently unreachable.

- [x] **Node-Specific Differences** (if any)
  - holly: Identical to lloyd
  - lloyd: Reference configuration (documented above)
  - mable: Identical to lloyd
  - **Answer**: All three MS-01s are identically configured

### Cluster-Specific Settings

- [x] **Cluster Formation**
  - Is this a Proxmox cluster: Yes
  - Cluster name in Proxmox: `quantum` (will be renamed from doggos)
  - Corosync network: `<subnet>` or N/A
  - **Question**: Proper Proxmox cluster or standalone nodes?

- [ ] **Former Workload Configuration**
  - Vault cluster network: `<details if still configured>`
  - Nomad/Consul network: `<details if still configured>`
  - k8s network: `<details if still configured>`
  - **Question**: Should we preserve any of the old network config or start fresh?

- [ ] **Idle State Goals**
  - Keep cluster running but empty? Yes/No
  - Minimal resource usage mode? Yes/No
  - Future plans: `<what will Doggos become>`
  - **Question**: What's the intended future use for Doggos?

---

## Additional Configuration Questions

### SSH Settings (Global)

- [x] **SSH Hardening**
  - Port: `22`
  - Password authentication: No (disabled)
  - Root login: Yes (via key only, password auth disabled)
  - X11 forwarding: No (recommended)
  - **Answer**: Standard hardening with key-only auth

- [x] **Allowed Users/Groups**
  - SSH allowed users: `all` (controlled via keys)
  - SSH allowed groups: `all`
  - **Answer**: No specific user restrictions

### Infisical Configuration

- [x] **Per-Cluster Paths**
  - Nexus Infisical path: `/nexus`
  - Matrix Infisical path: `/matrix`
  - Quantum Infisical path: `/quantum` (renamed from /doggos)
  - **Answer**: Confirmed - /nexus, /matrix, /quantum

### hosts.yml Migration

- [ ] **Review hosts.yml unique bits**
  - Anything in `hosts.yml` not in `proxmox.yml`? `<list>`
  - Comments to preserve? `<list>`
  - Format preferences to keep? `<list>`
  - **Question**: Review `hosts.yml` for unique content to preserve

---

## Implementation Checklist (After Info Gathered)

### Phase 1: Create group_vars Structure

- [ ] Create `group_vars/all.yml` with global settings
- [ ] Create `group_vars/proxmox_clusters.yml` with shared Proxmox settings
- [ ] Create `group_vars/nexus_cluster.yml` with Nexus config
- [ ] Create `group_vars/doggos_cluster.yml` with Doggos config
- [ ] Verify `group_vars/matrix_cluster.yml` is complete

### Phase 2: Update Inventory

- [ ] Add `node_id` to all hosts in `proxmox.yml`
- [ ] Add any missing host variables
- [ ] Test inventory with `ansible-inventory --list`

### Phase 3: Validation

- [ ] Test `ansible-ping` on all clusters
- [ ] Verify `group_vars` loading with `ansible-inventory --host <hostname>`
- [ ] Confirm templating works (`node_id` expansion)

### Phase 4: Documentation

- [ ] Update `ansible/README.md` with new inventory structure
- [ ] Document variable precedence for team
- [ ] Archive `hosts.yml` with explanation

### Phase 5: Testing

- [ ] Run existing playbooks against new inventory structure
- [ ] Verify no regressions
- [ ] Test with check mode on all clusters

---

## Notes

### From User

- Nexus: "hot mess of everything" - lots of LXCs, handful of VMs, local storage
- Doggos: 3x Minisforum MS-01s, formerly Vault/Nomad/Consul/k8s, now idle
- Matrix: ✅ Already fully configured in `group_vars/matrix_cluster.yml`

### Design Decisions

- Following ansible-best-practices skill patterns
- Using `node_id` templating pattern from Matrix cluster
- Minimal `host_vars` (only `node_id`), everything else in `group_vars`
- Role-prefixed variables throughout
- Empty list defaults for safety

### Reference

- Skill: ansible-best-practices (variable management patterns)
- Example: `group_vars/matrix_cluster.yml` (excellent reference)
- Standard: geerlingguy role patterns (universal approach)

---

## Questions Summary (Quick Reference)

Copy this section to quickly answer all questions:

### Nexus

1. Node IDs: alpha=?, bravo=?
2. Network bridges: How many? Names?
3. Storage backend: dir/LVM/ZFS?
4. Cluster or standalone?
5. Hardware: Identical nodes or different?

### Doggos

1. Node IDs: holly=?, lloyd=?, mable=?
2. Future cluster name: ?
3. Network topology: How many bridges? VLANs?
4. NFS details: Server IP, what mounts?
5. Storage layout: What goes local vs NFS?
6. Hardware: All MS-01s identical?
7. Future purpose: What will Doggos become?

### Global

1. SSH port and hardening settings?
2. SSH access restrictions?
3. Infisical path structure confirmed?
4. Review `hosts.yml` for unique content?

---

**Next Steps**: Fill in the blanks above, then we'll generate the complete `group_vars` structure following ansible-best-practices patterns!
