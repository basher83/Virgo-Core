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
