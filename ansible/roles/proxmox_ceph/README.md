# proxmox_ceph

Manages CEPH distributed storage infrastructure for Proxmox VE.

## Description

This role provides complete CEPH cluster lifecycle management:

- CEPH package installation (Squid for PVE 9.x)
- CEPH cluster initialization
- Monitor (MON) deployment on all nodes
- Manager (MGR) deployment on all nodes
- **Automated OSD creation** from configuration (improves on ProxSpray)
- CEPH pool creation with replication settings
- CRUSH rule configuration
- Health verification

## Key Features

**Automated OSD Creation**: Unlike ProxSpray which requires manual OSD setup, this role
automatically creates OSDs based on declarative configuration, including support for:

- Multiple OSDs per disk (partitioning)
- Separate DB and WAL devices
- CRUSH device class assignment (nvme, ssd, hdd)
- Idempotent OSD creation (won't recreate existing OSDs)

## Requirements

- Proxmox VE 9.x with cluster already formed
- Root access or sudo privileges
- Dedicated CEPH networks configured (public and private)
- Unused block devices for OSD creation
- Minimum 3 nodes for proper replication

## Role Variables

```yaml
# CEPH version
ceph_version: "squid"                   # CEPH Squid for PVE 9.x

# Network configuration
ceph_network: "192.168.5.0/24"          # Public network (vmbr1)
ceph_cluster_network: "192.168.7.0/24"  # Private network (vmbr2)

# Cluster configuration
cluster_group: "all"                    # Ansible group for cluster nodes

# OSD configuration (Matrix cluster example)
ceph_osds:
  foxtrot:
    - device: /dev/nvme1n1
      partitions: 2                     # Create 2 OSDs on this device
      db_device: null                   # Use same device for DB
      wal_device: null                  # Use same device for WAL
      crush_device_class: nvme          # CRUSH device class

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

# Pool configuration
ceph_pools:
  - name: vm_ssd
    pg_num: 128                         # Placement groups
    pgp_num: 128                        # PG for placement
    size: 3                             # 3 replicas across nodes
    min_size: 2                         # Minimum 2 replicas required
    application: rbd                    # RBD application type
    crush_rule: replicated_rule         # Use replicated rule

  - name: vm_containers
    pg_num: 64
    pgp_num: 64
    size: 3
    min_size: 2
    application: rbd

# Feature toggles
install_ceph_packages: true             # Install CEPH packages
initialize_ceph: true                   # Initialize CEPH cluster
deploy_monitors: true                   # Deploy monitors
deploy_managers: true                   # Deploy managers
deploy_osds: true                       # Create OSDs
create_pools: true                      # Create pools
verify_ceph_health: true                # Verify health after deployment
```

## Dependencies

- `proxmox_repository` - CEPH repositories must be configured
- `proxmox_cluster` - Proxmox cluster must be formed first
- `proxmox_network` - CEPH networks must be configured

## Example Playbook

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

    ceph_pools:
      - name: vm_ssd
        pg_num: 128
        size: 3
        min_size: 2
        application: rbd

  roles:
    - role: proxmox_ceph
```

## Important Notes

### WARNING: Destructive Operations

- OSD creation is **destructive** - it will wipe the specified devices
- Always backup data before running this role
- Verify device paths carefully (typos can destroy data)
- Test in a non-production environment first

**Best Practices**:

1. Use dedicated high-speed networks for CEPH (10GbE minimum)
2. Enable jumbo frames (MTU 9000) on CEPH networks
3. Use odd number of nodes (3, 5, 7) for quorum
4. Separate public and private CEPH networks
5. Use NVMe or SSD devices for best performance
6. Calculate PG numbers based on OSD count: `(OSDs * 100) / replica_size`

## Matrix Cluster Configuration

For the Matrix cluster (3 nodes, 2� 4TB NVMe per node):

- **Total OSDs**: 12 (4 OSDs per node)
- **Total raw capacity**: ~24TB (2� 4TB � 3 nodes)
- **Usable capacity**: ~8TB (with 3� replication)
- **PG calculation**: `(12 OSDs * 100) / 3 = 400` � Round to nearest power of 2 = 128 or 256

## CEPH Operations

### View CEPH Status

```bash
ceph -s                 # Overall cluster status
ceph health detail      # Detailed health information
ceph osd tree           # OSD topology
ceph osd pool ls detail # Pool details
```

### Manage OSDs

```bash
pveceph osd ls          # List OSDs
ceph osd df             # OSD disk usage
ceph osd out <osd-id>   # Mark OSD out (for maintenance)
ceph osd in <osd-id>    # Mark OSD back in
```

### Troubleshooting

```bash
# Check CEPH logs
journalctl -u ceph-mon@$(hostname -s) -f
journalctl -u ceph-mgr@$(hostname -s) -f

# Repair PGs
ceph pg repair <pg-id>

# Check slow operations
ceph -w                 # Watch cluster events
```

## Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/deploy-ceph.yml

# Check mode (safe, read-only)
ansible-playbook playbooks/deploy-ceph.yml --check

# Run on cluster
ansible-playbook playbooks/deploy-ceph.yml
```

## License

MIT

## Author

Virgo-Core Team
