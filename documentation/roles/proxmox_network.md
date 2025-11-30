---
title: proxmox_network Role
description: Manage Proxmox VE network infrastructure with bridges, VLANs, and jumbo frames for CEPH storage networks
---

# proxmox_network Role

Manage Proxmox VE network infrastructure with bridges, VLANs, and jumbo frames.

**Use Cases**: Configure cluster networking, enable VLAN-aware bridges, optimize storage networks with jumbo frames

**Dependencies**: Requires `community.general` collection for `interfaces_file` module

**Battle-Tested**: Production deployment on Matrix cluster (3 nodes), validated CEPH storage networks

## Overview

The `proxmox_network` role provides declarative network management:

- Create Linux bridges with physical interface binding
- Enable VLAN-aware bridges for VM network isolation
- Configure VLAN subinterfaces on existing bridges
- Configure jumbo frames (MTU 9000) for storage networks
- Manage IP addresses and default gateways
- Backup and verify network configuration automatically

## Quick Start

Configure basic management bridge:

```yaml
---
- name: Configure network bridge
  hosts: proxmox_nodes
  roles:
    - role: proxmox_network
      proxmox_bridges:
        - name: vmbr0
          interface: enp4s0
          address: "192.168.3.{{ node_id }}/24"
          gateway: 192.168.3.1
          comment: "Management network"
```

Run:

```bash
cd ansible
uv run ansible-playbook playbooks/configure-network.yml
```

Expected: Bridge `vmbr0` created, bound to `enp4s0`, IP configured, network reloaded

## Configuration Reference

### Bridge Configuration

| Variable | Required | Type | Description |
|----------|----------|------|-------------|
| `proxmox_bridges` | No | list | Bridge definitions |
| `├─ name` | Yes | string | Bridge interface name (vmbr0, vmbr1, etc.) |
| `├─ interface` | Yes | string | Physical interface to bridge |
| `├─ address` | Yes | string | IP address with CIDR notation |
| `├─ gateway` | No | string | Default gateway IP |
| `├─ vlan_aware` | No | bool | Enable VLAN filtering (default: `false`) |
| `├─ vlan_ids` | No | mixed | VLAN IDs: list `[9, 10]` or range `"2-4094"` |
| `├─ mtu` | No | int | MTU size (default: 1500) |
| `└─ comment` | No | string | Documentation string |

### VLAN Configuration

| Variable | Required | Type | Description |
|----------|----------|------|-------------|
| `proxmox_vlans` | No | list | VLAN subinterface definitions |
| `├─ id` | Yes | int | VLAN ID (1-4094) |
| `├─ raw_device` | Yes | string | Parent interface (typically a bridge) |
| `├─ address` | Yes | string | IP address with CIDR notation |
| `└─ comment` | No | string | Documentation string |

### Control Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `proxmox_network_backup` | bool | `true` | Backup `/etc/network/interfaces` before changes |
| `proxmox_network_reload` | bool | `true` | Reload network after configuration |
| `proxmox_network_verify` | bool | `true` | Verify configuration after changes |
| `proxmox_network_dry_run` | bool | `false` | Check mode without applying changes |
| `proxmox_network_interfaces_file` | string | `/etc/network/interfaces` | Network configuration file path |
| `proxmox_network_default_mtu` | int | `1500` | Standard MTU for general networks |
| `proxmox_network_jumbo_mtu` | int | `9000` | Jumbo frames MTU for storage |

## Common Patterns

### VLAN-Aware Bridge

Enable VLAN support for VM network isolation:

```yaml
proxmox_bridges:
  - name: vmbr1
    interface: enp5s0
    address: "192.168.5.{{ node_id }}/24"
    vlan_aware: true
    vlan_ids: "2-4094"
    comment: "VLAN-aware bridge for VMs"
```

**VLAN ID Formats**:

- String range: `"2-4094"` (full VLAN range)
- List of integers: `[9, 10, 20]` (specific VLANs)
- List of strings: `["9", "10"]`

The role converts lists to comma-separated strings automatically.

### Jumbo Frames for Storage

Configure CEPH networks with jumbo frames:

```yaml
proxmox_bridges:
  - name: vmbr1
    interface: enp5s0f0np0
    address: "192.168.5.{{ node_id }}/24"
    mtu: "{{ proxmox_network_jumbo_mtu }}"
    comment: "CEPH Public network"

  - name: vmbr2
    interface: enp5s0f1np1
    address: "192.168.7.{{ node_id }}/24"
    mtu: "{{ proxmox_network_jumbo_mtu }}"
    comment: "CEPH Private network"
```

### VLAN Subinterface

Create isolated network on existing bridge:

```yaml
proxmox_vlans:
  - id: 9
    raw_device: vmbr0
    address: "192.168.8.{{ node_id }}/24"
    comment: "Corosync cluster network"
```

### Complete Cluster Configuration

Full network setup for Matrix cluster:

```yaml
---
- name: Configure Matrix Cluster Network
  hosts: matrix_cluster
  become: true
  gather_facts: true

  vars:
    node_ids:
      foxtrot: 5
      golf: 6
      hotel: 7
    node_id: "{{ node_ids[inventory_hostname] }}"

  roles:
    - role: proxmox_network
      vars:
        proxmox_bridges:
          - name: vmbr0
            interface: enp4s0
            address: "192.168.3.{{ node_id }}/24"
            gateway: 192.168.3.1
            vlan_aware: true
            vlan_ids: [9]
            comment: "Management network"

          - name: vmbr1
            interface: enp5s0f0np0
            address: "192.168.5.{{ node_id }}/24"
            mtu: "{{ proxmox_network_jumbo_mtu }}"
            comment: "CEPH Public network"

          - name: vmbr2
            interface: enp5s0f1np1
            address: "192.168.7.{{ node_id }}/24"
            mtu: "{{ proxmox_network_jumbo_mtu }}"
            comment: "CEPH Private network"

        proxmox_vlans:
          - id: 9
            raw_device: vmbr0
            address: "192.168.8.{{ node_id }}/24"
            comment: "Corosync network"
```

## Advanced Usage

### Group Variables

Define cluster-wide network configuration:

```yaml
# group_vars/matrix_cluster.yml
proxmox_bridges:
  - name: vmbr0
    interface: enp4s0
    address: "192.168.3.{{ node_id }}/24"
    gateway: 192.168.3.1
    vlan_aware: true
    vlan_ids: [9]

node_ids:
  foxtrot: 5
  golf: 6
  hotel: 7

node_id: "{{ node_ids[inventory_hostname] }}"
```

### Per-Node Customization

Override configuration for specific nodes:

```yaml
# host_vars/foxtrot.yml
proxmox_bridges:
  - name: vmbr3
    interface: enp6s0
    address: "10.0.0.5/24"
    comment: "Special network on Foxtrot only"
```

### Dry Run Mode

Test configuration without applying changes:

```bash
uv run ansible-playbook playbooks/configure-network.yml \
  -e "proxmox_network_dry_run=true" \
  --check --diff
```

### Selective Execution

Run specific configuration tasks:

```bash
# Configure bridges only
uv run ansible-playbook playbooks/configure-network.yml --tags bridges

# Configure VLANs only
uv run ansible-playbook playbooks/configure-network.yml --tags vlans

# Verify configuration only
uv run ansible-playbook playbooks/configure-network.yml --tags verify

# Single host only
uv run ansible-playbook playbooks/configure-network.yml --limit foxtrot
```

## Migration from Old Playbook

Replace standalone VLAN playbook with declarative role:

**Old Approach**:

```yaml
- name: Enable VLAN-Aware Bridging
  hosts: doggos_cluster
  tasks:
    - name: Enable VLAN-aware bridging on vmbr1
      community.general.interfaces_file:
        iface: vmbr1
        option: bridge-vlan-aware
        value: "yes"
```

**New Approach**:

```yaml
- name: Configure Network
  hosts: doggos_cluster
  roles:
    - role: proxmox_network
      vars:
        proxmox_bridges:
          - name: vmbr1
            interface: enp5s0
            vlan_aware: true
            vlan_ids: "2-4094"
```

**Benefits**: Declarative configuration, automatic verification, better validation, easier extension

## Task Organization

The role uses modular task files:

- `tasks/main.yml` - Orchestrates task execution
- `tasks/prerequisites.yml` - Validates environment and dependencies
- `tasks/bridges.yml` - Configures Linux bridges
- `tasks/vlans.yml` - Configures VLAN subinterfaces
- `tasks/reload.yml` - Reloads network configuration
- `tasks/verify.yml` - Verifies configuration success

## Available Tags

- `proxmox_network` - All tasks in role
- `prerequisites` - Prerequisite validation only
- `bridges` - Bridge configuration only
- `vlans` - VLAN configuration only
- `reload` - Network reload only
- `verify` - Verification only
- `debug` - Debug output

## Behavior Details

### Automatic Backup

The role creates timestamped backups at `/etc/network/interfaces.<timestamp>` before the first change when `proxmox_network_backup: true`
(default). Subsequent changes in the same run skip backup creation.

### Network Reload

Configuration changes trigger the `Reload network interfaces` handler, which executes `ifreload -a` to apply changes without
restarting the entire networking stack.

**Warning**: Network reload may briefly interrupt connectivity. Exercise caution on remote hosts.

### Idempotency

The role uses the `community.general.interfaces_file` module, which operates idempotently. Running the role multiple times with
identical configuration produces no changes.

### Post-Configuration Verification

Verification checks run automatically when `proxmox_network_verify: true` (default):

1. Bridge status: Confirms bridges are up and configured
2. VLAN status: Confirms VLAN interfaces exist
3. VLAN filtering: Confirms VLAN filtering is enabled on bridges

Verification failures appear in output but do not fail the play.

## Safety Features

### Prerequisites Check

The role validates:

- Proxmox VE installation (`/etc/pve` exists)
- Network configuration file exists
- `ifreload` command availability

### Dry Run Mode

Set `proxmox_network_dry_run: true` to skip configuration changes while showing what would change.

### Automatic Backup

Enabled by default; backups allow recovery from configuration errors.

## Troubleshooting

### Configuration Not Applied

**Symptom**: Changes made but network not updated

**Solution**:

```bash
ssh root@node ifreload -a
```

### Bridge Not Creating

**Symptom**: Bridge configuration fails

**Diagnosis**:

```bash
# Check physical interface exists
ip link show enp4s0

# Check interface not already in use
bridge link show

# Verify network file syntax
ifup -a --no-act
```

**Solutions**:

- Verify physical interface exists
- Ensure interface not in use by another bridge
- Check `/etc/network/interfaces` syntax

### VLAN Not Working

**Symptom**: VLAN interface not accessible

**Diagnosis**:

```bash
# Check parent bridge VLAN-aware
ip -d link show vmbr0 | grep vlan_filtering

# Check VLAN module loaded
lsmod | grep 8021q

# Check VLAN interface exists
ip link show vmbr0.9
```

**Solutions**:

- Ensure parent bridge has `bridge-vlan-aware yes`
- Verify VLAN ID in `bridge-vids` range
- Confirm kernel module `8021q` loaded

### Network Connectivity Lost

**Symptom**: Lost SSH access after network reload

**Recovery**:

```bash
# Access via Proxmox console (web UI)
# Check interface status
ip addr show

# Restore from backup
cp /etc/network/interfaces.<timestamp> /etc/network/interfaces
ifreload -a
```

### Verification Failures

**Symptom**: Verification shows bridges/VLANs missing

**Diagnosis**:

```bash
# Check reload output for errors
journalctl -u networking -n 50

# Verify manually
ip addr show
ip link show
```

**Solutions**:

- Review reload output for errors
- Check system logs: `journalctl -u networking`
- Verify configuration manually

## Best Practices

1. **Test before deploying**: Use dry run mode first

   ```bash
   uv run ansible-playbook playbooks/configure-network.yml \
     -e "proxmox_network_dry_run=true" --check
   ```

2. **Start with one node**: Validate on single host before cluster-wide deployment

   ```bash
   uv run ansible-playbook playbooks/configure-network.yml --limit foxtrot
   ```

3. **Keep backups enabled**: Disable only when you have specific reason

4. **Use group_vars for consistency**: Define cluster-wide configuration centrally

5. **Document network topology**: Use comments for each bridge/VLAN

6. **Test connectivity after changes**:

   ```bash
   ansible -i inventory/proxmox.yml matrix_cluster -m ping
   ```

## See Also

- [Proxmox VE Network Configuration](https://pve.proxmox.com/wiki/Network_Configuration) - Official documentation
- [VLAN Configuration](https://pve.proxmox.com/wiki/VLAN) - VLAN setup guide
- [interfaces_file Module](https://docs.ansible.com/ansible/latest/collections/community/general/interfaces_file_module.html) - Ansible module documentation
