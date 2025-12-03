---
title: First Deployment
description: Deploy a production-ready 3-node Proxmox cluster with CEPH storage in 60 minutes
---

# First Deployment: Zero to Cluster in 60 Minutes

Deploy a production-ready 3-node Proxmox cluster with CEPH storage in 60 minutes.

**Time Required**: 50-70 minutes

**Prerequisites**:

- [Prerequisites](prerequisites.md) complete
- [Installation](installation.md) complete

## Overview

This tutorial deploys the Matrix cluster with:

- 3 Proxmox nodes (Foxtrot, Golf, Hotel)
- Cluster formation with corosync
- CEPH distributed storage (12 OSDs, 12TB usable)
- Network configuration (management + CEPH networks)

## Deployment Phases

1. **Inventory Configuration** (10 min) - Configure nodes and networks
2. **Network Setup** (15 min) - Configure bridges and VLANs
3. **Cluster Formation** (10 min) - Join nodes to cluster
4. **CEPH Deployment** (15 min) - Deploy distributed storage
5. **Verification** (10 min) - Validate deployment

Total: 60 minutes

## Phase 1: Inventory Configuration (10 minutes)

Configure your cluster nodes and network settings.

### Step 1: Copy example inventory

```bash
cp ansible/inventory/proxmox.yml.example ansible/inventory/proxmox.yml
```

### Step 2: Edit inventory

Edit `ansible/inventory/proxmox.yml`:

```yaml
all:
  children:
    proxmox_clusters:
      children:
        matrix_cluster:
          hosts:
            foxtrot:
              ansible_host: 192.168.3.11
              node_id: 11
            golf:
              ansible_host: 192.168.3.12
              node_id: 12
            hotel:
              ansible_host: 192.168.3.13
              node_id: 13
```

### Step 3: Configure cluster variables

Edit `ansible/inventory/group_vars/matrix_cluster.yml`:

```yaml
cluster_name: matrix

network_config:
  management:
    cidr: "192.168.3.{{ node_id }}/24"
    gateway: "192.168.3.1"
  ceph_public:
    cidr: "192.168.5.{{ node_id }}/24"
  ceph_private:
    cidr: "192.168.7.{{ node_id }}/24"
```

### Step 4: Validate inventory

```bash
uv run ansible-inventory --list
```

**Expected**: JSON output showing 3 nodes with correct IPs

**What Happens Next**: Ansible will use this inventory to configure all 3 nodes

## Phase 2: Network Setup (15 minutes)

Configure network bridges, VLANs, and MTU for CEPH networks.

### What Will Happen

The `configure-network` playbook will:

- Create network bridges (vmbr0, vmbr1, vmbr2)
- Configure VLAN interfaces
- Set MTU to 9000 on CEPH networks
- **Network restart may briefly disconnect SSH** (~10 seconds)

### Step 1: Dry-run network configuration

```bash
CHECK=1 mise run ansible:configure-network
```

**Expected Output**:

```text
PLAY [Configure Proxmox Network] ******

TASK [proxmox_network : Create bridges] ******
changed: [foxtrot]
changed: [golf]
changed: [hotel]

PLAY RECAP ******
foxtrot: ok=12 changed=8
golf: ok=12 changed=8
hotel: ok=12 changed=8
```

**Review**: Check what would change before applying

### Step 2: Apply network configuration

```bash
mise run ansible:configure-network
```

**Expected**: Same output as dry-run, but changes actually applied

**Duration**: 5-10 minutes

### Step 3: Verify network configuration

```bash
# Check bridges created
ssh root@192.168.3.11 'ip link show | grep vmbr'
# Expected: vmbr0, vmbr1, vmbr2

# Check MTU 9000 on CEPH networks
ssh root@192.168.3.11 'ip link show vmbr1 | grep mtu'
# Expected: mtu 9000

# Test jumbo frames
ping -M do -s 8972 -c 3 192.168.5.11
# Expected: 0% packet loss
```

**Checkpoint**: All nodes should have bridges configured with correct MTU

## Phase 3: Cluster Formation (10 minutes)

Form Proxmox cluster and join nodes.

### What Will Happen

The `init-cluster` playbook will:

- Create cluster on first node (Foxtrot)
- Join Golf and Hotel to cluster
- Configure Corosync for cluster communication
- **No service disruption expected**

### Step 1: Initialize cluster

```bash
mise run ansible:init-cluster
```

**Expected Output**:

```text
TASK [proxmox_cluster : Create cluster] ******
changed: [foxtrot]

TASK [proxmox_cluster : Join nodes] ******
changed: [golf]
changed: [hotel]

PLAY RECAP ******
foxtrot: ok=8 changed=4
golf: ok=6 changed=2
hotel: ok=6 changed=2
```

**Duration**: 5-10 minutes

### Step 2: Verify cluster status

```bash
ssh root@192.168.3.11 'pvecm status'
```

**Expected Output**:

```text
Cluster information
-------------------
Name:             matrix
Config Version:   3
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Mon Nov 19 12:34:56 2025
Quorum provider:  corosync_votequorum
Nodes:            3
Node ID:          0x00000001
Ring ID:          1.5
Quorate:          Yes

Membership information
----------------------
Nodeid      Votes Name
0x00000001      1 foxtrot (local)
0x00000002      1 golf
0x00000003      1 hotel
```

**Checkpoint**: All 3 nodes should appear in cluster, status "Quorate: Yes"

## Phase 4: CEPH Deployment (15 minutes)

Deploy CEPH distributed storage across all nodes.

### What Will Happen

The `deploy-ceph` playbook will:

- Install CEPH packages on all nodes
- Create monitors (1 per node)
- Create managers (1 per node)
- Create OSDs (4 per node = 12 total)
- Create default storage pool
- **CPU/network intensive during OSD creation**

### Step 1: Deploy CEPH

```bash
mise run ansible:deploy-ceph
```

**Expected Output**:

```text
TASK [proxmox_ceph : Install CEPH] ******
changed: [foxtrot]
changed: [golf]
changed: [hotel]

TASK [proxmox_ceph : Create monitors] ******
changed: [foxtrot]
changed: [golf]
changed: [hotel]

TASK [proxmox_ceph : Create OSDs] ******
changed: [foxtrot] (4 OSDs)
changed: [golf] (4 OSDs)
changed: [hotel] (4 OSDs)

PLAY RECAP ******
foxtrot: ok=24 changed=16
golf: ok=24 changed=16
hotel: ok=24 changed=16
```

**Duration**: 10-15 minutes (OSD creation is slow)

### Step 2: Verify CEPH status

```bash
ssh root@192.168.3.11 'ceph -s'
```

**Expected Output**:

```text
  cluster:
    id:     xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum foxtrot,golf,hotel (age 2m)
    mgr: foxtrot(active, since 1m), standbys: golf, hotel
    osd: 12 osds: 12 up (since 1m), 12 in (since 1m)

  data:
    pools:   1 pools, 128 pgs
    objects: 0 objects, 0 B
    usage:   60 GiB used, 12 TiB / 12 TiB avail
    pgs:     128 active+clean
```

**Checkpoint**: HEALTH_OK, 12 OSDs up and in

## Phase 5: Verification (10 minutes)

Validate complete deployment.

### Cluster Health Checks

#### Check 1: Cluster Status

```bash
ssh root@192.168.3.11 'pvecm status'
```

Expected: 3 nodes, Quorate: Yes

#### Check 2: CEPH Health

```bash
ssh root@192.168.3.11 'ceph -s'
```

Expected: HEALTH_OK, 12 OSDs

#### Check 3: Network MTU

```bash
ssh root@192.168.3.11 'ip link show vmbr1 | grep mtu'
```

Expected: mtu 9000

#### Check 4: Storage Pools

```bash
ssh root@192.168.3.11 'pvesm status'
```

Expected: See CEPH pool listed and available

### Complete Verification Checklist

- [ ] All 3 nodes in cluster (`pvecm status`)
- [ ] Cluster quorate (3/3 votes)
- [ ] CEPH health OK (`ceph -s`)
- [ ] 12 OSDs up and in
- [ ] Jumbo frames working (MTU 9000)
- [ ] SSH access to all nodes working

## Deployment Complete

Your Matrix cluster is production-ready with:

- 3-node Proxmox cluster
- CEPH distributed storage (12TB usable)
- High-performance network (jumbo frames)
- Production-grade configuration

**Next Steps**:

- Deploy your first VM
- Configure additional storage pools
- Set up monitoring

**Troubleshooting**: See [Troubleshooting Basics](troubleshooting-basics.md)
