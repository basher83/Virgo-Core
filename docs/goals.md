# Goals

This document outlines the roadmap and objectives for Virgo-Core infrastructure automation.

> **Note**: For detailed infrastructure specifications, see [infrastructure.md](infrastructure.md)

## Core Goals

- [ ] Ansible collection to fully manage Proxmox VE 9.x homelab

  - [ ] PVE networking configuration
    - [ ] Manage `/etc/network/interfaces`
    - [ ] Manage corosync configuration `/etc/corosync/corosync.conf`
    - [ ] Manage hosts configuration `/etc/hosts`
    - [ ] VLAN configuration
    - [ ] DHCP configuration
    - [ ] DNS configuration

  - [ ] PVE storage configuration
    - [ ] CEPH cluster configuration and management
      - [ ] Each node has a monitor
      - [ ] Each node has a manager
      - [ ] Each node has 4 OSDs (2 OSDs per NVMe × 2 NVMes per node)

## Infrastructure Gotchas

- [ ] Ensure Unifi Controller has jumbo frames enabled for high-bandwidth ports (CEPH networks)

## Related Documentation

- [infrastructure.md](infrastructure.md) - Detailed infrastructure specifications
- [ansible-migration-plan.md](ansible-migration-plan.md) - Ansible role development plan
- [netbox-powerdns.md](netbox-powerdns.md) - NetBox and PowerDNS integration
