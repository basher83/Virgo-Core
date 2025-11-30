# ADR-0002: Quantum as Infrastructure Cluster

**Status**: Accepted
**Date**: 2025-11-30

## Context

With three Proxmox clusters available (Matrix, Nexus, Quantum), we needed to decide where to run infrastructure services like NetBox and PowerDNS.

Key constraint: **Infrastructure services must not depend on the infrastructure they manage.** Hosting NetBox/PowerDNS on a CEPH cluster they manage creates a circular dependency—the cluster needs DNS/IPAM to function, but those services need the cluster to be running.

## Decision

Designate **Quantum as the infrastructure/management cluster** and **Matrix as the workload cluster**.

- Quantum runs NetBox, PowerDNS, and other management services
- Matrix runs production VMs on CEPH storage
- Nexus remains legacy/mixed until migrated or sunset

## Consequences

**Benefits:**

- No circular dependencies—Quantum uses local/NFS storage, not CEPH
- Management plane survives workload cluster outages
- DNS and IPAM remain available during Matrix maintenance
- Clean separation of concerns between management and workload

**Trade-offs:**

- Quantum nodes (32GB RAM each) have less capacity than Matrix nodes (64GB each)
- Quantum lacks CEPH private network (only public), limiting future CEPH options
- Must maintain two clusters instead of consolidating

**Cluster Roles:**

| Cluster | Role | Storage | Services |
|---------|------|---------|----------|
| Quantum | Infrastructure | Local LVM + NFS | NetBox, PowerDNS, monitoring |
| Matrix | Workload | CEPH (24TB) | Production VMs |
| Nexus | Legacy | Local + NFS | Existing workloads (migrate over time) |

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Run everything on Matrix | Creates circular dependency; DNS/IPAM would depend on CEPH they manage |
| Single dedicated VM on Nexus | Nexus hardware is mixed; no HA; creates dependency on legacy cluster |
| Separate single node | Wastes Quantum capacity; Quantum already has 3 nodes available |
