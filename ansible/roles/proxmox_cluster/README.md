# proxmox_cluster

Manages Proxmox VE cluster formation and configuration.

## Description

This role manages the complete Proxmox VE cluster lifecycle:

- Initializes the cluster on the first node
- Adds additional nodes to the cluster
- Configures Corosync for cluster communication
- Manages /etc/hosts for all cluster nodes
- Distributes SSH keys for passwordless access
- Verifies cluster health and quorum

## Requirements

- Proxmox VE 9.x installed on all nodes
- Root access or sudo privileges
- Network connectivity between all cluster nodes
- Corosync network configured (typically VLAN 9)
- All nodes must be able to resolve each other's hostnames

## Role Variables

```yaml
# Cluster configuration
cluster_name: "proxmox-cluster"       # Name of the cluster
cluster_group: "all"                  # Ansible inventory group containing cluster nodes

# Corosync configuration
corosync_network: "192.168.8.0/24"    # Corosync network CIDR
corosync_bindnetaddr: "192.168.8.0"   # Bind network address
corosync_mcastaddr: "239.192.8.1"     # Multicast address
corosync_mcastport: 5405              # Multicast port
corosync_link0_interface: "vlan9"     # Interface for corosync link0

# Cluster nodes (define in group_vars)
cluster_nodes:
  - name: foxtrot
    hostname: foxtrot.matrix.spaceships.work
    management_ip: 192.168.3.5
    corosync_ip: 192.168.8.5
    node_id: 1

# SSH configuration
configure_ssh_keys: true              # Distribute SSH keys
ssh_key_type: "rsa"                   # SSH key type (rsa, ed25519)
ssh_key_bits: 4096                    # Key size for RSA keys

# Verification
verify_cluster_health: true           # Run health checks after cluster formation
expected_votes: 3                     # Expected number of cluster nodes

# /etc/hosts management
manage_hosts_file: true               # Update /etc/hosts with cluster nodes
```

## Dependencies

Run the `proxmox_repository` and `proxmox_network` roles before this role.

## Example Playbook

```yaml
---
- name: Initialize Proxmox cluster
  hosts: matrix_cluster
  become: true

  vars:
    cluster_name: "Matrix"
    cluster_group: "matrix_cluster"
    corosync_network: "192.168.8.0/24"

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

## Important Notes

WARNING: Cluster formation is a one-time operation. Once you create a cluster:

- You cannot remove nodes without data loss
- Changing cluster configuration requires careful planning
- Back up cluster configuration before changes

Best Practices:

1. Synchronize time on all nodes (NTP)
2. Verify network connectivity on corosync network before clustering
3. Test SSH connectivity between all nodes
4. Use a dedicated VLAN for corosync
5. Start with 3 nodes for proper quorum (odd numbers preferred)

## Cluster Operations

### View Cluster Status

```bash
pvecm status        # Show cluster status and quorum
pvecm nodes         # List all cluster nodes
corosync-cfgtool -s # Check corosync status
```

### Troubleshooting

```bash
# Check corosync logs
journalctl -u corosync -f

# Verify cluster communication
pvecm expected 1    # Set expected votes (emergency only)

# Check quorum
pvecm status | grep -i quorum
```

## Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/initialize-cluster.yml

# Check mode (dry run) - safe for testing
ansible-playbook playbooks/initialize-cluster.yml --check --diff

# Run on cluster
ansible-playbook playbooks/initialize-cluster.yml
```

## License

MIT

## Author

Virgo-Core Team
