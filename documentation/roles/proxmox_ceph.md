---
title: proxmox_ceph Role
description: Deploy and manage CEPH distributed storage with automated OSD creation, pool configuration, and health verification
---

# proxmox_ceph Role

Deploy and manage CEPH distributed storage for Proxmox VE clusters with automated OSD creation, pool configuration, and health verification.

**Use Cases**: Deploy CEPH storage, create OSDs automatically, configure pools with replication, manage CRUSH rules, verify cluster health

**Dependencies**: Requires `proxmox_repository`, `proxmox_cluster`, and `proxmox_network` roles

**Battle-Tested**: Production deployment on Matrix cluster (12 OSDs, 24TB raw capacity, 8TB usable), automated OSD creation from declarative configuration

## Overview

The `proxmox_ceph` role manages the complete CEPH storage lifecycle:

- Install CEPH packages (Squid for PVE 9.x)
- Initialize CEPH cluster
- Deploy monitors (MON) on all nodes
- Deploy managers (MGR) on all nodes
- Create OSDs automatically from declarative configuration
- Configure CEPH pools with replication settings
- Manage CRUSH rules for data placement
- Verify cluster health and functionality

**Key Innovation**: Automated OSD creation from declarative configuration. ProxSpray requires manual OSD setup; this role creates
OSDs automatically from YAML definitions, supporting multiple OSDs per disk, separate DB and WAL devices, and CRUSH device class
assignment.

## Quick Start

Deploy CEPH on three-node cluster:

```yaml
---
- name: Deploy CEPH storage
  hosts: matrix_cluster
  become: true

  vars:
    ceph_network: "192.168.5.0/24"
    ceph_cluster_network: "192.168.7.0/24"

    ceph_osds:
      foxtrot:
        - device: /dev/nvme1n1
          partitions: 2
          crush_device_class: nvme
        - device: /dev/nvme2n1
          partitions: 2
          crush_device_class: nvme

      golf:
        - device: /dev/nvme1n1
          partitions: 2
          crush_device_class: nvme
        - device: /dev/nvme2n1
          partitions: 2
          crush_device_class: nvme

      hotel:
        - device: /dev/nvme1n1
          partitions: 2
          crush_device_class: nvme
        - device: /dev/nvme2n1
          partitions: 2
          crush_device_class: nvme

    ceph_pools:
      - name: vm_ssd
        pg_num: 128
        pgp_num: 128
        size: 3
        min_size: 2
        application: rbd
        crush_rule: replicated_rule

  roles:
    - role: proxmox_ceph
```

Run:

```bash
cd ansible
uv run ansible-playbook playbooks/deploy-ceph.yml
```

Expected: CEPH cluster initialized, 12 OSDs created, pools configured, health verified

## Configuration Reference

### CEPH Version

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ceph_version` | string | `"squid"` | CEPH release (Squid for PVE 9.x) |

### Network Configuration

| Variable | Required | Type | Description |
|----------|----------|------|-------------|
| `ceph_network` | Yes | string | Public network CIDR for client traffic |
| `ceph_cluster_network` | Yes | string | Private network CIDR for replication traffic |

Best Practice: Use dedicated high-speed networks (10GbE minimum) for CEPH, separate public and private networks for security and performance.

### Cluster Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `cluster_group` | string | `"all"` | Ansible inventory group containing cluster nodes |

### OSD Configuration

| Variable | Required | Type | Description |
|----------|----------|------|-------------|
| `ceph_osds` | Yes | dict | OSD definitions per node |
| `ceph_osds.<hostname>` | Yes | list | List of OSD definitions for this node |
| `ceph_osds.<hostname>[].device` | Yes | string | Block device path (e.g., `/dev/nvme1n1`) |
| `ceph_osds.<hostname>[].partitions` | Yes | int | Number of OSDs to create on this device |
| `ceph_osds.<hostname>[].db_device` | No | string | Separate device for BlueStore DB (null = use same device) |
| `ceph_osds.<hostname>[].wal_device` | No | string | Separate device for BlueStore WAL (null = use same device) |
| `ceph_osds.<hostname>[].crush_device_class` | Yes | string | CRUSH device class (nvme, ssd, hdd) |

**WARNING**: OSD creation destroys all data on specified devices. Back up your data before running this role. Verify device
paths carefully. A single typo destroys data. Test in non-production environment first.

### Pool Configuration

| Variable | Required | Type | Description |
|----------|----------|------|-------------|
| `ceph_pools` | No | list | Pool definitions |
| `├─ name` | Yes | string | Pool name (e.g., `vm_ssd`, `vm_containers`) |
| `├─ pg_num` | Yes | int | Number of placement groups |
| `├─ pgp_num` | Yes | int | Number of PGs for placement |
| `├─ size` | Yes | int | Replica count (3 = three copies) |
| `├─ min_size` | Yes | int | Minimum replicas required for I/O |
| `├─ application` | Yes | string | Pool application type (rbd, cephfs, rgw) |
| `└─ crush_rule` | Yes | string | CRUSH rule name (e.g., `replicated_rule`) |

PG Calculation: `(OSDs * 100) / replica_size`, round to nearest power of 2.

Example: 12 OSDs with 3x replication = `(12 * 100) / 3 = 400`, round to 256 or 512.

### Feature Toggles

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `install_ceph_packages` | bool | `true` | Install CEPH packages |
| `initialize_ceph` | bool | `true` | Initialize CEPH cluster |
| `deploy_monitors` | bool | `true` | Deploy MON daemons |
| `deploy_managers` | bool | `true` | Deploy MGR daemons |
| `deploy_osds` | bool | `true` | Create OSDs from configuration |
| `create_pools` | bool | `true` | Create CEPH pools |
| `verify_ceph_health` | bool | `true` | Verify cluster health after deployment |

## Common Patterns

### Matrix Cluster Configuration

Three nodes, two 4TB NVMe drives per node, two OSDs per drive:

```yaml
---
- name: Deploy Matrix CEPH Storage
  hosts: matrix_cluster
  become: true

  vars:
    ceph_version: "squid"
    ceph_network: "192.168.5.0/24"
    ceph_cluster_network: "192.168.7.0/24"
    cluster_group: "matrix_cluster"

    ceph_osds:
      foxtrot:
        - device: /dev/nvme1n1
          partitions: 2
          db_device: null
          wal_device: null
          crush_device_class: nvme
        - device: /dev/nvme2n1
          partitions: 2
          db_device: null
          wal_device: null
          crush_device_class: nvme

      golf:
        - device: /dev/nvme1n1
          partitions: 2
          crush_device_class: nvme
        - device: /dev/nvme2n1
          partitions: 2
          crush_device_class: nvme

      hotel:
        - device: /dev/nvme1n1
          partitions: 2
          crush_device_class: nvme
        - device: /dev/nvme2n1
          partitions: 2
          crush_device_class: nvme

    ceph_pools:
      - name: vm_ssd
        pg_num: 128
        pgp_num: 128
        size: 3
        min_size: 2
        application: rbd
        crush_rule: replicated_rule

      - name: vm_containers
        pg_num: 64
        pgp_num: 64
        size: 3
        min_size: 2
        application: rbd
        crush_rule: replicated_rule

  roles:
    - role: proxmox_ceph
```

Capacity: 12 OSDs, ~24TB raw capacity, ~8TB usable with 3x replication.

### Separate DB and WAL Devices

Use fast NVMe for BlueStore database and WAL:

```yaml
ceph_osds:
  foxtrot:
    - device: /dev/sda
      partitions: 1
      db_device: /dev/nvme0n1p1
      wal_device: /dev/nvme0n1p2
      crush_device_class: hdd
```

Best Practice: Use fast NVMe for DB/WAL when using HDD for data. This dramatically improves performance.

### Group Variables Configuration

Define cluster-wide configuration centrally:

```yaml
# group_vars/matrix_cluster.yml
ceph_version: "squid"
ceph_network: "192.168.5.0/24"
ceph_cluster_network: "192.168.7.0/24"
cluster_group: "matrix_cluster"

ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

  golf:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

  hotel:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme

ceph_pools:
  - name: vm_ssd
    pg_num: 128
    pgp_num: 128
    size: 3
    min_size: 2
    application: rbd
    crush_rule: replicated_rule
```

Simplified playbook:

```yaml
---
- name: Deploy CEPH storage
  hosts: matrix_cluster
  become: true
  roles:
    - proxmox_ceph
```

### Mixed Device Classes

Combine different storage types in one cluster:

```yaml
ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/sda
      partitions: 1
      crush_device_class: ssd
    - device: /dev/sdb
      partitions: 1
      crush_device_class: hdd
```

Create pools targeting specific device classes using CRUSH rules.

## Advanced Usage

### Adding OSDs to Running Cluster

Add new disks to existing CEPH cluster:

```yaml
# Update group_vars/matrix_cluster.yml
ceph_osds:
  foxtrot:
    # Existing OSDs
    - device: /dev/nvme1n1
      partitions: 2
      crush_device_class: nvme
    - device: /dev/nvme2n1
      partitions: 2
      crush_device_class: nvme
    # New OSD
    - device: /dev/nvme3n1
      partitions: 2
      crush_device_class: nvme
```

Run playbook:

```bash
uv run ansible-playbook playbooks/deploy-ceph.yml --limit foxtrot
```

Role automatically skips existing OSDs and creates only new ones.

### Selective Deployment

Deploy only specific components:

```yaml
---
- name: Deploy only MON and MGR
  hosts: matrix_cluster
  become: true

  vars:
    install_ceph_packages: true
    initialize_ceph: true
    deploy_monitors: true
    deploy_managers: true
    deploy_osds: false
    create_pools: false
    verify_ceph_health: false

  roles:
    - role: proxmox_ceph
```

### Verify Without Changes

Check configuration before deployment:

```bash
uv run ansible-playbook playbooks/deploy-ceph.yml --check --diff
```

## CEPH Operations

### View Cluster Status

```bash
# Overall cluster status
ceph -s

# Detailed health information
ceph health detail

# OSD topology and status
ceph osd tree

# Pool details and statistics
ceph osd pool ls detail

# Cluster disk usage
ceph df
```

### Manage OSDs

```bash
# List all OSDs
pveceph osd ls

# OSD disk usage breakdown
ceph osd df

# Mark OSD out for maintenance
ceph osd out <osd-id>

# Mark OSD back in after maintenance
ceph osd in <osd-id>

# Remove failed OSD from cluster
ceph osd out <osd-id>
ceph osd purge <osd-id> --yes-i-really-mean-it
```

### Monitor Performance

```bash
# Watch cluster events live
ceph -w

# Check slow operations
ceph health detail | grep slow

# Monitor IOPS and throughput
ceph osd perf

# Check PG statistics
ceph pg stat

# View client I/O statistics
ceph iostat
```

### Manage Pools

```bash
# List all pools
ceph osd pool ls

# View pool configuration
ceph osd pool get <pool-name> all

# Adjust PG count
ceph osd pool set <pool-name> pg_num 256

# Enable pool application
ceph osd pool application enable <pool-name> rbd
```

## Troubleshooting

### OSD Creation Fails

**Symptom**: Role fails to create OSDs

**Diagnosis**:

```bash
# Check if device already has OSDs
ceph osd tree

# Verify device exists and is not mounted
lsblk /dev/nvme1n1

# Check for existing partitions
parted /dev/nvme1n1 print

# View CEPH logs
journalctl -u ceph-osd@* -n 100
```

**Solutions**:

- Ensure device path correct and device exists
- Verify device not mounted or in use
- Check device has no existing filesystem
- Use `pveceph createosd` manually to diagnose issues
- Destroy existing data with `ceph-volume lvm zap /dev/nvme1n1`

### CEPH Health Warnings

**Symptom**: `ceph -s` shows HEALTH_WARN

**Diagnosis**:

```bash
# View detailed health status
ceph health detail

# Check for PG issues
ceph pg dump_stuck

# Verify OSD status
ceph osd tree

# Check mon quorum
ceph quorum_status -f json-pretty
```

**Common Warnings and Fixes**:

- `too few PGs per OSD`: Increase PG count with `ceph osd pool set <pool> pg_num <number>`
- `clock skew detected`: Synchronize time on all nodes with NTP
- `mon is allowing insecure global_id reclaim`: Normal during initial setup, resolves automatically
- `OSD down`: Check OSD logs, restart with `systemctl restart ceph-osd@<id>`

### Performance Issues

**Symptom**: Slow I/O or high latency

**Diagnosis**:

```bash
# Check for slow operations
ceph health detail | grep slow

# Monitor real-time performance
ceph osd perf

# Check network bandwidth
iperf3 -c 192.168.7.6 -p 5201

# Verify disk performance
fio --name=test --size=10G --rw=randwrite --bs=4k --direct=1 --filename=/dev/nvme1n1
```

**Solutions**:

- Enable jumbo frames (MTU 9000) on CEPH networks
- Verify 10GbE or faster network for CEPH traffic
- Check disk I/O with `iostat` and `iotop`
- Tune BlueStore settings for workload
- Consider separate DB/WAL devices for HDD OSDs
- Verify no network packet loss with `ping` and `mtr`

### PG Stuck or Degraded

**Symptom**: Placement groups stuck in degraded, undersized, or inactive states

**Diagnosis**:

```bash
# List stuck PGs
ceph pg dump_stuck

# View specific PG details
ceph pg <pg-id> query

# Check PG mapping
ceph pg map <pg-id>
```

**Solutions**:

```bash
# Repair specific PG
ceph pg repair <pg-id>

# Force backfill on stuck PG
ceph pg force-backfill <pg-id>

# Deep scrub to fix inconsistencies
ceph pg deep-scrub <pg-id>
```

### Mon Quorum Lost

**Symptom**: Monitor quorum lost, cluster inaccessible

**Diagnosis**:

```bash
# Check mon status
systemctl status ceph-mon@$(hostname -s)

# View mon logs
journalctl -u ceph-mon@$(hostname -s) -n 100

# Check network connectivity to other mons
ping -c 3 192.168.5.6
```

**Emergency Recovery**:

```bash
# Stop all mon services
systemctl stop ceph-mon.target

# Extract monmap from surviving mon
ceph-mon -i $(hostname -s) --extract-monmap /tmp/monmap

# Remove failed mon from monmap
monmaptool /tmp/monmap --rm <failed-mon-name>

# Inject monmap back
ceph-mon -i $(hostname -s) --inject-monmap /tmp/monmap

# Start mon service
systemctl start ceph-mon@$(hostname -s)
```

### Idempotency Issues

**Symptom**: Role fails on repeated runs

**Background**: Two critical idempotency bugs fixed in November 2025:

**Bug 13: Destructive OSD Zap Logic** (`tasks/osd_prepare.yml`)

- **Issue**: Zap task attempted to destroy active OSDs when variable check failed
- **Impact**: "umount: /var/lib/ceph/osd/ceph-0: target is busy" errors on re-runs
- **Fix**: Added `osd_count_check_successful` flag and defensive fallback (defaults to 999 to prevent zapping)
- **Result**: Safe OSD handling - zapping occurs only when explicitly safe (check succeeds AND zero OSDs exist)

**Bug 14: Cluster Quorum Verification** (via `proxmox_cluster` role)

- **Issue**: Quorum verification failed when running with `--limit` on subset of nodes
- **Impact**: Playbook failed on single-node idempotency tests
- **Fix**: Added `cluster_status.rc == 0` condition to skip quorum checks when pvecm status fails
- **Result**: Playbook completes successfully on partial cluster runs

**Idempotency Test Results**:

- Before fixes: `failed=1` (75-104 tasks completed)
- After fixes: `ok=104 changed=3 failed=0 skipped=32` (full idempotency achieved)

**Commit**: `d4af18b` - fix(ansible): Critical idempotency bugs in OSD zap and cluster quorum checks

## Best Practices

1. **Use dedicated high-speed networks**: 10GbE minimum for CEPH traffic

   ```yaml
   ceph_network: "192.168.5.0/24"          # 10GbE public network
   ceph_cluster_network: "192.168.7.0/24"  # 10GbE private network
   ```

2. **Enable jumbo frames**: MTU 9000 on CEPH networks for best performance

   ```bash
   # Configure in proxmox_network role
   ip link set vmbr1 mtu 9000
   ip link set vmbr2 mtu 9000
   ```

3. **Use odd number of nodes**: Three, five, or seven nodes for proper quorum

   ```yaml
   # Good: 3 nodes, can survive 1 failure
   cluster_group: "matrix_cluster"  # 3 nodes

   # Bad: 2 nodes, no quorum on failure
   cluster_group: "small_cluster"  # 2 nodes
   ```

4. **Separate public and private networks**: Isolate client and replication traffic

   ```yaml
   ceph_network: "192.168.5.0/24"          # Client traffic
   ceph_cluster_network: "192.168.7.0/24"  # Replication traffic
   ```

5. **Calculate PG numbers correctly**: `(OSDs * 100) / replica_size`, round to power of 2

   ```yaml
   # 12 OSDs, 3x replication: (12 * 100) / 3 = 400 → 256 or 512
   pg_num: 128
   ```

6. **Use NVMe or SSD for best performance**: Avoid HDD for latency-sensitive workloads

   ```yaml
   crush_device_class: nvme  # Best performance
   crush_device_class: ssd   # Good performance
   crush_device_class: hdd   # Capacity-focused
   ```

7. **Test in non-production first**: OSD creation destroys data

   ```bash
   # Test on dev cluster first
   uv run ansible-playbook playbooks/deploy-ceph.yml --check
   ```

8. **Back up before deployment**: Save VM and container data

   ```bash
   # Backup before running role
   vzdump --all --compress gzip --storage backups
   ```

## Important Warnings

## Destructive Operations Warning

OSD creation destroys all data on specified devices. This operation is PERMANENT and IRREVERSIBLE.

Before running this role:

- Back up all data on target devices
- Verify device paths carefully
- Test in non-production environment
- Confirm network configuration complete
- Ensure Proxmox cluster already formed

**Device Path Verification**:

```bash
# List all block devices before running role
lsblk

# Verify specific device
ls -la /dev/nvme1n1

# Check for existing data
blkid /dev/nvme1n1
```

**CRITICAL**: A single typo in device path destroys the wrong disk. Double-check all paths.

**PERMANENT CHANGES**: The role modifies:

- Block devices specified in `ceph_osds` (data destroyed)
- `/etc/pve/ceph.conf` - CEPH configuration
- `/etc/pve/priv/ceph.*` - CEPH authentication keys
- `/var/lib/ceph/` - CEPH daemon data

## Integration Patterns

### Complete Infrastructure Setup

Deploy full Proxmox infrastructure in sequence:

```yaml
---
- name: Deploy Proxmox Infrastructure
  hosts: matrix_cluster
  become: true

  roles:
    - role: proxmox_repository
    - role: proxmox_network
    - role: proxmox_cluster
    - role: proxmox_ceph
```

### Separate Cluster and Storage Deployment

Split into two playbooks for better control:

```yaml
# playbooks/01-cluster-setup.yml
---
- name: Initialize Cluster
  hosts: matrix_cluster
  become: true
  roles:
    - proxmox_repository
    - proxmox_network
    - proxmox_cluster

# playbooks/02-storage-setup.yml
---
- name: Deploy CEPH Storage
  hosts: matrix_cluster
  become: true
  roles:
    - proxmox_ceph
```

Run sequentially:

```bash
uv run ansible-playbook playbooks/01-cluster-setup.yml
uv run ansible-playbook playbooks/02-storage-setup.yml
```

### Post-Deployment Verification

Add verification tasks after CEPH deployment:

```yaml
---
- name: Deploy and verify CEPH
  hosts: matrix_cluster
  become: true

  roles:
    - role: proxmox_ceph

  post_tasks:
    - name: Wait for CEPH to stabilize
      ansible.builtin.pause:
        seconds: 60

    - name: Verify CEPH health
      ansible.builtin.command: ceph -s
      register: ceph_status
      changed_when: false

    - name: Display CEPH status
      ansible.builtin.debug:
        var: ceph_status.stdout_lines

    - name: Verify all OSDs up
      ansible.builtin.command: ceph osd tree
      register: osd_tree
      changed_when: false

    - name: Display OSD topology
      ansible.builtin.debug:
        var: osd_tree.stdout_lines
```

## Testing

### Syntax Check

```bash
# Validate playbook syntax
uv run ansible-playbook playbooks/deploy-ceph.yml --syntax-check
```

### Dry Run

```bash
# Check mode without changes
uv run ansible-playbook playbooks/deploy-ceph.yml --check
```

### Full Execution

```bash
# Run on cluster
uv run ansible-playbook playbooks/deploy-ceph.yml
```

### Verify Results

```bash
# Check CEPH status on all nodes
ansible matrix_cluster -a "ceph -s"

# Verify OSD count
ansible matrix_cluster -a "ceph osd tree"

# Check pool configuration
ansible matrix_cluster -a "ceph osd pool ls detail"

# Verify health
ansible matrix_cluster -a "ceph health detail"
```

## See Also

- [Proxmox VE CEPH](https://pve.proxmox.com/wiki/Ceph) - Official CEPH documentation
- [CEPH Documentation](https://docs.ceph.com/) - Upstream CEPH documentation
- [Proxmox Cluster Role](proxmox_cluster.md) - Cluster formation prerequisite
- [Proxmox Network Role](proxmox_network.md) - Network configuration prerequisite
