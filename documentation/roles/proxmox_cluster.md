---
title: proxmox_cluster Role
description: Form and configure Proxmox VE clusters with automated node joining, Corosync setup, and health verification
---

# proxmox_cluster Role

Form and configure Proxmox VE clusters with automated node joining, Corosync setup, and health verification.

**Use Cases**: Initialize multi-node clusters, join nodes to existing clusters, configure Corosync communication, verify cluster health

**Dependencies**: Requires `proxmox_repository` and `proxmox_network` roles

**Battle-Tested**: Production deployment on Matrix cluster (3 nodes: Foxtrot, Golf, Hotel), validated VLAN 9 Corosync network

## Overview

The `proxmox_cluster` role manages the complete cluster lifecycle:

- Initialize cluster on first node
- Join additional nodes to cluster
- Configure Corosync for cluster communication
- Manage `/etc/hosts` for hostname resolution
- Distribute SSH keys for passwordless access
- Verify cluster health and quorum

## Quick Start

Initialize a three-node cluster:

```yaml
---
- name: Initialize Proxmox cluster
  hosts: matrix_cluster
  become: true

  vars:
    cluster_name: "Matrix"
    cluster_nodes:
      - name: foxtrot
        hostname: foxtrot.matrix.spaceships.work
        management_ip: 192.168.3.5
        corosync_ip: 192.168.8.5
        node_id: 1
      - name: golf
        hostname: golf.matrix.spaceships.work
        management_ip: 192.168.3.6
        corosync_ip: 192.168.8.6
        node_id: 2
      - name: hotel
        hostname: hotel.matrix.spaceships.work
        management_ip: 192.168.3.7
        corosync_ip: 192.168.8.7
        node_id: 3

  roles:
    - role: proxmox_cluster
```

Run:

```bash
cd ansible
uv run ansible-playbook playbooks/initialize-cluster.yml
```

Expected: Cluster formed, nodes joined, quorum established, health verified

## Configuration Reference

### Cluster Configuration

| Variable | Required | Type | Description |
|----------|----------|------|-------------|
| `cluster_name` | Yes | string | Cluster identifier (used in Proxmox UI) |
| `cluster_group` | No | string | Ansible inventory group containing cluster nodes (default: `"all"`) |
| `cluster_nodes` | Yes | list | Node definitions with network details |
| `├─ name` | Yes | string | Node hostname (short form) |
| `├─ hostname` | Yes | string | Fully qualified domain name |
| `├─ management_ip` | Yes | string | Management network IP address |
| `├─ corosync_ip` | Yes | string | Corosync network IP address |
| `└─ node_id` | Yes | int | Unique node identifier (1-based) |

### Corosync Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `corosync_network` | string | `"192.168.8.0/24"` | Corosync network CIDR |
| `corosync_bindnetaddr` | string | `"192.168.8.0"` | Bind network address |
| `corosync_mcastaddr` | string | `"239.192.8.1"` | Multicast address |
| `corosync_mcastport` | int | `5405` | Multicast port |
| `corosync_link0_interface` | string | `"vlan9"` | Interface for corosync link0 |

### SSH Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `configure_ssh_keys` | bool | `true` | Distribute SSH keys between nodes |
| `ssh_key_type` | string | `"rsa"` | SSH key type (rsa, ed25519) |
| `ssh_key_bits` | int | `4096` | Key size for RSA keys |

### Verification

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `verify_cluster_health` | bool | `true` | Run health checks after formation |
| `expected_votes` | int | `3` | Expected number of cluster nodes |
| `manage_hosts_file` | bool | `true` | Update `/etc/hosts` with cluster nodes |

## Common Patterns

### Three-Node Cluster with Dedicated Corosync Network

Standard production configuration:

```yaml
---
- name: Configure Matrix Cluster
  hosts: matrix_cluster
  become: true

  vars:
    cluster_name: "Matrix"
    cluster_group: "matrix_cluster"
    corosync_network: "192.168.8.0/24"
    corosync_link0_interface: "vlan9"

    cluster_nodes:
      - name: foxtrot
        hostname: foxtrot.matrix.spaceships.work
        management_ip: 192.168.3.5
        corosync_ip: 192.168.8.5
        node_id: 1
      - name: golf
        hostname: golf.matrix.spaceships.work
        management_ip: 192.168.3.6
        corosync_ip: 192.168.8.6
        node_id: 2
      - name: hotel
        hostname: hotel.matrix.spaceships.work
        management_ip: 192.168.3.7
        corosync_ip: 192.168.8.7
        node_id: 3

  roles:
    - role: proxmox_cluster
```

### Group Variables Configuration

Define cluster-wide configuration centrally:

```yaml
# group_vars/matrix_cluster.yml
cluster_name: "Matrix"
cluster_group: "matrix_cluster"
corosync_network: "192.168.8.0/24"
corosync_link0_interface: "vlan9"

cluster_nodes:
  - name: foxtrot
    hostname: foxtrot.matrix.spaceships.work
    management_ip: 192.168.3.5
    corosync_ip: 192.168.8.5
    node_id: 1
  - name: golf
    hostname: golf.matrix.spaceships.work
    management_ip: 192.168.3.6
    corosync_ip: 192.168.8.6
    node_id: 2
  - name: hotel
    hostname: hotel.matrix.spaceships.work
    management_ip: 192.168.3.7
    corosync_ip: 192.168.8.7
    node_id: 3
```

Simplified playbook:

```yaml
---
- name: Initialize Proxmox cluster
  hosts: matrix_cluster
  become: true
  roles:
    - proxmox_cluster
```

### Custom SSH Configuration

Use Ed25519 keys instead of RSA:

```yaml
---
- name: Configure cluster with Ed25519 keys
  hosts: matrix_cluster
  become: true

  vars:
    ssh_key_type: "ed25519"
    # ssh_key_bits not used for Ed25519

  roles:
    - role: proxmox_cluster
```

## Advanced Usage

### Adding Nodes to Existing Cluster

Add a fourth node to running cluster:

```yaml
# Update group_vars/matrix_cluster.yml
cluster_nodes:
  - name: foxtrot
    hostname: foxtrot.matrix.spaceships.work
    management_ip: 192.168.3.5
    corosync_ip: 192.168.8.5
    node_id: 1
  - name: golf
    hostname: golf.matrix.spaceships.work
    management_ip: 192.168.3.6
    corosync_ip: 192.168.8.6
    node_id: 2
  - name: hotel
    hostname: hotel.matrix.spaceships.work
    management_ip: 192.168.3.7
    corosync_ip: 192.168.8.7
    node_id: 3
  - name: india
    hostname: india.matrix.spaceships.work
    management_ip: 192.168.3.8
    corosync_ip: 192.168.8.8
    node_id: 4
```

Run playbook targeting only new node:

```bash
uv run ansible-playbook playbooks/initialize-cluster.yml --limit india
```

### Verify Without Changes

Check cluster configuration:

```bash
uv run ansible-playbook playbooks/initialize-cluster.yml --check --diff
```

### Single Node Testing

Test on one node first:

```bash
uv run ansible-playbook playbooks/initialize-cluster.yml --limit foxtrot
```

## Cluster Operations

### View Cluster Status

```bash
# Show cluster status and quorum
pvecm status

# List all cluster nodes
pvecm nodes

# Check corosync status
corosync-cfgtool -s

# View detailed quorum information
pvecm expected
```

### Monitor Cluster Health

```bash
# Watch corosync logs
journalctl -u corosync -f

# Check cluster communication
pvecm status | grep -i quorum

# View cluster configuration
cat /etc/pve/corosync.conf
```

## Troubleshooting

### Cluster Formation Fails

**Symptom**: First node fails to create cluster

**Diagnosis**:

```bash
# Check Proxmox installation
ls -la /etc/pve

# Verify no existing cluster
pvecm status

# Check network connectivity
ping -c 3 192.168.8.5
```

**Solutions**:

- Ensure Proxmox VE 9.x installed on all nodes
- Verify no existing cluster configuration
- Confirm Corosync network configured and reachable

### Node Join Fails

**Symptom**: Additional nodes cannot join cluster

**Diagnosis**:

```bash
# Test SSH connectivity to first node
ssh root@foxtrot.matrix.spaceships.work

# Check hostname resolution
getent hosts foxtrot.matrix.spaceships.work

# Verify Corosync network reachable
ping -c 3 192.168.8.5
```

**Solutions**:

- Verify SSH keys distributed correctly
- Ensure `/etc/hosts` contains all cluster nodes
- Confirm Corosync network configured on all nodes
- Check firewall allows Corosync traffic (UDP 5405)

### Quorum Lost

**Symptom**: Cluster loses quorum when node fails

**Diagnosis**:

```bash
# Check quorum status
pvecm status | grep -i quorum

# Count expected votes
pvecm expected
```

**Emergency Recovery**:

```bash
# Set expected votes to 1 (emergency only)
pvecm expected 1
```

**Permanent Solution**:

- Use odd number of nodes (3, 5, 7) for proper quorum
- Configure QDevice for even-node clusters
- Plan maintenance to avoid multiple node failures

### Corosync Communication Issues

**Symptom**: Nodes cannot communicate via Corosync

**Diagnosis**:

```bash
# Check corosync status
systemctl status corosync

# View corosync logs
journalctl -u corosync -n 50

# Verify interface configuration
ip addr show vlan9

# Test multicast connectivity
corosync-cfgtool -s
```

**Solutions**:

- Verify VLAN interface exists and has IP
- Ensure multicast enabled on network switches
- Check MTU matches across all nodes
- Confirm firewall allows multicast traffic

### Time Synchronization Issues

**Symptom**: Cluster operations fail intermittently

**Diagnosis**:

```bash
# Check time on all nodes
timedatectl

# Verify NTP synchronization
systemctl status systemd-timesyncd
```

**Solution**:

```bash
# Configure NTP on all nodes
timedatectl set-ntp true
systemctl restart systemd-timesyncd
```

### SSH Key Distribution Fails

**Symptom**: Passwordless SSH not working between nodes

**Diagnosis**:

```bash
# Test SSH connection
ssh root@golf.matrix.spaceships.work

# Check authorized_keys
cat /root/.ssh/authorized_keys

# Verify key permissions
ls -la /root/.ssh/
```

**Solutions**:

- Ensure `.ssh` directory has permissions 700
- Verify `authorized_keys` has permissions 600
- Check SSH service running on all nodes
- Confirm no `sshd_config` restrictions

## Best Practices

1. **Use odd number of nodes**: Three, five, or seven nodes provide proper quorum

   ```yaml
   # Good: 3 nodes
   expected_votes: 3

   # Bad: 2 nodes (no quorum on failure)
   expected_votes: 2
   ```

2. **Dedicate VLAN for Corosync**: Isolate cluster traffic from other networks

   ```yaml
   corosync_link0_interface: "vlan9"  # Dedicated VLAN
   ```

3. **Synchronize time before clustering**: Configure NTP on all nodes first

   ```bash
   # Configure NTP before running role
   timedatectl set-ntp true
   ```

4. **Verify network connectivity first**: Test Corosync network before forming cluster

   ```bash
   # Ping all Corosync IPs
   ansible matrix_cluster -m ping
   ```

5. **Backup configuration before changes**: Save cluster configuration

   ```bash
   # Backup corosync.conf
   cp /etc/pve/corosync.conf /root/corosync.conf.backup
   ```

6. **Test on single node first**: Validate configuration before full deployment

   ```bash
   uv run ansible-playbook playbooks/initialize-cluster.yml --limit foxtrot --check
   ```

## Important Warnings

**WARNING**: Cluster formation is permanent. Once you create a cluster:

- You cannot remove nodes without data loss
- Changing cluster configuration requires careful planning
- Breaking the cluster destroys shared storage access

**CRITICAL**: Before forming cluster:

- Back up all VM and container data
- Verify network configuration correct
- Ensure time synchronized on all nodes
- Test SSH connectivity between nodes
- Confirm Corosync network operational

**PERMANENT CHANGES**: The role modifies:

- `/etc/pve/corosync.conf` - Cluster configuration
- `/etc/hosts` - Hostname resolution
- `/root/.ssh/authorized_keys` - SSH keys
- Cluster membership database

## Integration Patterns

### Complete Infrastructure Setup

Run all prerequisite roles first:

```yaml
---
- name: Configure Proxmox Infrastructure
  hosts: matrix_cluster
  become: true

  roles:
    - role: proxmox_repository
    - role: proxmox_network
    - role: proxmox_cluster
    - role: proxmox_ceph
```

### Separate Network and Cluster Configuration

Split into two playbooks for better control:

```yaml
# playbooks/01-configure-network.yml
---
- name: Configure Network
  hosts: matrix_cluster
  become: true
  roles:
    - proxmox_network

# playbooks/02-initialize-cluster.yml
---
- name: Initialize Cluster
  hosts: matrix_cluster
  become: true
  roles:
    - proxmox_cluster
```

Run sequentially:

```bash
uv run ansible-playbook playbooks/01-configure-network.yml
uv run ansible-playbook playbooks/02-initialize-cluster.yml
```

### Post-Cluster Verification

Add verification tasks after cluster formation:

```yaml
---
- name: Initialize and verify cluster
  hosts: matrix_cluster
  become: true

  roles:
    - role: proxmox_cluster

  post_tasks:
    - name: Wait for cluster to stabilize
      ansible.builtin.pause:
        seconds: 30

    - name: Verify cluster status
      ansible.builtin.command: pvecm status
      register: cluster_status
      changed_when: false

    - name: Display cluster status
      ansible.builtin.debug:
        var: cluster_status.stdout_lines
```

## Testing

### Syntax Check

```bash
# Validate playbook syntax
uv run ansible-playbook playbooks/initialize-cluster.yml --syntax-check
```

### Dry Run

```bash
# Check mode without changes
uv run ansible-playbook playbooks/initialize-cluster.yml --check --diff
```

### Full Execution

```bash
# Run on cluster
uv run ansible-playbook playbooks/initialize-cluster.yml
```

### Verify Results

```bash
# Check cluster status on all nodes
ansible matrix_cluster -a "pvecm status"

# Verify quorum
ansible matrix_cluster -a "pvecm expected"

# Check corosync
ansible matrix_cluster -a "corosync-cfgtool -s"
```

## See Also

- [Proxmox VE Cluster Manager](https://pve.proxmox.com/wiki/Cluster_Manager) - Official cluster documentation
- [Corosync Configuration](https://pve.proxmox.com/wiki/Corosync) - Corosync setup guide
- [Proxmox Network Role](proxmox_network.md) - Network configuration prerequisite
- [Proxmox CEPH Role](proxmox_ceph.md) - Shared storage deployment
