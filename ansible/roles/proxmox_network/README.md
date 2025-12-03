# Ansible Role: proxmox_network

Manages Proxmox VE network infrastructure including bridges, VLANs, interfaces, and MTU configuration.

## Description

This role configures Proxmox VE networking with these capabilities:

- Creates and configures Linux bridges (vmbr0, vmbr1, etc.)
- Enables VLAN-aware bridges and creates VLAN subinterfaces
- Configures jumbo frames for storage networks
- Configures IP addresses and gateways
- Runs multiple times without changes (idempotent)
- Verifies configuration after changes

## Requirements

- Proxmox VE 8.x or 9.x
- Ansible 2.15+
- `community.general` collection (provides `interfaces_file` module)

## Role Variables

### Bridge Configuration

```yaml
proxmox_bridges:
  - name: vmbr0                        # Bridge interface name
    interface: enp4s0                  # Physical interface to bridge
    address: "192.168.3.5/24"          # IP address with CIDR
    gateway: 192.168.3.1               # Default gateway (optional)
    vlan_aware: true                   # Enable VLAN filtering (optional)
    vlan_ids: [9]                      # VLAN IDs: list [9, 10] or range "2-4094" (optional)
    mtu: 1500                          # MTU size (optional)
    comment: "Management network"      # Documentation (optional)
```

### VLAN Configuration

```yaml
proxmox_vlans:
  - id: 9                              # VLAN ID
    raw_device: vmbr0                  # Parent interface
    address: "192.168.8.5/24"          # IP address with CIDR
    comment: "Corosync network"        # Documentation (optional)
```

### Control Variables

```yaml
proxmox_network_backup: true           # Backup config before changes
proxmox_network_reload: true           # Auto-reload network
proxmox_network_verify: true           # Verify configuration
proxmox_network_dry_run: false         # Check mode without applying
proxmox_network_interfaces_file: "/etc/network/interfaces"
proxmox_network_default_mtu: 1500      # Standard MTU
proxmox_network_jumbo_mtu: 9000        # Jumbo frames MTU
```

## Dependencies

None.

## Example Playbooks

### Basic Bridge Configuration

```yaml
---

- name: Configure Network Bridges
  hosts: proxmox_nodes
  become: true
  gather_facts: true

  roles:
    - role: proxmox_network
      vars:
        proxmox_bridges:
          - name: vmbr0
            interface: enp4s0
            address: "192.168.3.{{ node_id }}/24"
            gateway: 192.168.3.1
            comment: "Management network"

```

### VLAN-Aware Bridge

```yaml
---

- name: Enable VLAN Support on Bridge
  hosts: doggos_cluster
  become: true

  roles:
    - role: proxmox_network
      vars:
        proxmox_bridges:
          - name: vmbr1
            interface: enp5s0
            address: "192.168.5.{{ node_id }}/24"
            vlan_aware: true
            vlan_ids: "2-4094"
            comment: "VLAN-aware bridge"

```

The `vlan_ids` parameter accepts three formats:

- String range: `"2-4094"` (full VLAN range)
- List of integers: `[9, 10, 20]` (specific VLANs)
- List of strings: `["9", "10"]`

The role converts lists to comma-separated strings.

### Complete Network Configuration (Matrix Cluster)

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
          # Management bridge with VLAN support

          - name: vmbr0
            interface: enp4s0
            address: "192.168.3.{{ node_id }}/24"
            gateway: 192.168.3.1
            vlan_aware: true
            vlan_ids: [9]
            comment: "Management network"

          # CEPH Public network (jumbo frames)

          - name: vmbr1
            interface: enp5s0f0np0
            address: "192.168.5.{{ node_id }}/24"
            mtu: "{{ proxmox_network_jumbo_mtu }}"
            comment: "CEPH Public network"

          # CEPH Private network (jumbo frames)

          - name: vmbr2
            interface: enp5s0f1np1
            address: "192.168.7.{{ node_id }}/24"
            mtu: "{{ proxmox_network_jumbo_mtu }}"
            comment: "CEPH Private network"

        proxmox_vlans:
          # Corosync cluster network

          - id: 9
            raw_device: vmbr0
            address: "192.168.8.{{ node_id }}/24"
            comment: "Corosync network"

```

## Usage

### Standard Deployment

```bash
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml playbooks/configure-network.yml

```

### Dry Run (Check Mode)

```bash
uv run ansible-playbook playbooks/configure-network.yml \
  -e "proxmox_network_dry_run=true" \
  --check --diff

```

### Single Host

```bash
uv run ansible-playbook playbooks/configure-network.yml \
  --limit foxtrot

```

### With Tags

```bash

# Only configure bridges

uv run ansible-playbook playbooks/configure-network.yml \
  --tags bridges

# Only configure VLANs

uv run ansible-playbook playbooks/configure-network.yml \
  --tags vlans

# Verify only (no changes)

uv run ansible-playbook playbooks/configure-network.yml \
  --tags verify

```

## Task Organization

The role organizes tasks into modular files:

- `tasks/main.yml` - Entry point, orchestrates other tasks
- `tasks/prerequisites.yml` - Validation and checks
- `tasks/bridges.yml` - Bridge configuration
- `tasks/vlans.yml` - VLAN subinterface configuration
- `tasks/reload.yml` - Network reload logic
- `tasks/verify.yml` - Post-configuration verification

## Handlers

- `Reload network interfaces` - Triggered when configuration changes

## Tags

- `proxmox_network` - All tasks
- `prerequisites` - Prerequisite checks only
- `bridges` - Bridge configuration only
- `vlans` - VLAN configuration only
- `reload` - Network reload only
- `verify` - Verification only
- `debug` - Debug output

## Network Configuration Behavior

### Backup

The role creates a backup of `/etc/network/interfaces` before the first change when `proxmox_network_backup: true` (default). The role stores backups as `/etc/network/interfaces.<timestamp>`. Subsequent changes in the same run skip backup creation.

### Reload

Network configuration changes trigger the `Reload network interfaces` handler, which executes `ifreload -a` to apply changes without restarting the entire networking stack.

**Warning**: Network reload may briefly interrupt connectivity. Exercise caution on remote hosts.

### Idempotency

The role uses the `community.general.interfaces_file` module, which operates idempotently. Running the role multiple times with identical configuration produces no changes.

## Verification

Post-configuration verification checks:

1. Bridge status: confirms bridges are up and configured
2. VLAN status: confirms VLAN interfaces exist
3. VLAN filtering: confirms VLAN filtering is enabled on bridges

Verification failures appear in output but do not fail the play.

## Safety Features

### Prerequisites Check

The role validates:

- Proxmox VE installation (`/etc/pve` exists)
- Network configuration file exists
- `ifreload` command availability

### Dry Run Mode

Set `proxmox_network_dry_run: true` to skip actual configuration changes:

```yaml

- role: proxmox_network
  vars:
    proxmox_network_dry_run: true

```

### Backup Before Changes

The role enables automatic backup by default (`proxmox_network_backup: true`).

## Advanced Configuration

### Using Group Variables

For cluster-wide consistency:

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

For node-specific configuration:

```yaml

# host_vars/foxtrot.yml

proxmox_bridges:
  - name: vmbr3
    interface: enp6s0
    address: "10.0.0.5/24"
    comment: "Special network on Foxtrot only"

```

## Troubleshooting

### Configuration Not Applied

**Problem**: Changes made but network not updated

**Solution**: Reload manually:

```bash
ssh root@node ifreload -a
```

### Bridge Not Creating

**Problem**: Bridge configuration failing

**Check**:

1. Physical interface exists: `ip link show enp4s0`
2. Interface not in use: `bridge link show`
3. Network file syntax: `ifup -a --no-act`

### VLAN Not Working

**Problem**: VLAN interface not accessible

**Check**:

1. Parent bridge has `bridge-vlan-aware yes`

2. VLAN ID in `bridge-vids` range

3. Kernel module loaded: `lsmod | grep 8021q`

### Network Connectivity Lost

**Problem**: Lost SSH access after network reload

**Recovery**:

1. Access via Proxmox console (web UI)
2. Check interface status: `ip addr show`
3. Restore backup: `cp /etc/network/interfaces.<timestamp> /etc/network/interfaces`
4. Reload: `ifreload -a`

### Verification Failures

**Problem**: Verification shows bridges/VLANs missing

**Check**:

1. Review reload output for errors
2. Check system logs: `journalctl -u networking`
3. Verify manually: `ip addr show`

## Migration from Old Playbook

This role replaces `proxmox-enable-vlan-bridging.yml`. Migration steps:

### Old Playbook

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

### New Role-Based Approach

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

**Benefits**:

- Declarative configuration
- Easier to extend
- Better validation
- Automatic verification

## Best Practices

1. Test in dry run mode first:

   ```bash
   uv run ansible-playbook playbooks/configure-network.yml \
     -e "proxmox_network_dry_run=true" --check
   ```

2. Start with one node:

   ```bash
   uv run ansible-playbook playbooks/configure-network.yml --limit foxtrot
   ```

3. Keep backups enabled unless you have a specific reason to disable them

4. Use group_vars for cluster-wide network configuration

5. Document network topology in comments for each bridge/VLAN

6. Test connectivity after changes:

   ```bash
   ansible -i inventory/proxmox.yml matrix_cluster -m ping
   ```

## References

- [Proxmox VE Network Configuration](https://pve.proxmox.com/wiki/Network_Configuration)
- [VLAN Configuration](https://pve.proxmox.com/wiki/VLAN)
- [Ansible interfaces_file Module](https://docs.ansible.com/ansible/latest/collections/community/general/interfaces_file_module.html)

## License

MIT

## Author Information

Created by the Virgo-Core team for managing Proxmox VE infrastructure.

For issues or contributions, see the project repository.
