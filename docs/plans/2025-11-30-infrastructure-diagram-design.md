# Infrastructure Diagram Design

**Date**: 2025-11-30
**Status**: Approved

## Summary

Create `docs/diagrams/infrastructure-overview.md` showing cluster topology, switch connections, and current/planned services. Establish `docs/decisions/` for Architecture Decision Records.

## Goals

1. Document "where things are" for personal reference and disaster recovery
2. Show current state and planned additions with visual distinction
3. Capture permanent decisions in a discoverable location

## Infrastructure Diagram

### Location

`docs/diagrams/infrastructure-overview.md`

### Structure

1. **Quick Reference Table** - Cluster roles, nodes, current/planned state
2. **Physical Topology** - Switches and cluster connections (Mermaid)
3. **Cluster Detail** - Per-cluster nodes, storage, services (Mermaid)
4. **Legend** - Visual conventions and design principles

### Visual Conventions

| Style | Meaning |
|-------|---------|
| Solid box/line | Exists now |
| Dashed box/line | Planned |
| Blue | Infrastructure cluster (Quantum) |
| Green | Workload cluster (Matrix) |
| Gray | Legacy/mixed (Nexus) |

### Content Summary

**Quick Reference:**

| Cluster | Role | Current State | Planned |
|---------|------|---------------|---------|
| Quantum | Infrastructure | Empty | NetBox, PowerDNS |
| Matrix | Workload | Empty | Production VMs |
| Nexus | Legacy | Active | Migrate or sunset |

**Physical Topology:**

- USW-Pro-Max-24-PoE → all clusters (management)
- USW Aggregation → Matrix CEPH (10G×6 ports)
- USW Flex XG → Quantum CEPH (10G×3 ports)
- TrueNAS → Pro-Max-24 (10G SFP+)

**Design Principles:**

1. No circular dependencies - infrastructure services use local/NFS storage
2. Management plane separation - Quantum survives Matrix outages
3. Workload isolation - Matrix runs VMs without management overhead

## Decision Documentation

### Location

`docs/decisions/`

### Format (ADR)

```markdown
# ADR-NNNN: Title

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD

## Context
What situation led to this decision?

## Decision
What did we decide?

## Consequences
What does this mean going forward?

## Alternatives Considered
| Option | Rejected Because |
|--------|------------------|
```

### Initial ADRs

- `0001-powerdns-over-unifi-dns.md` - Extract from planning-30-nov-2025.md
- `0002-quantum-as-infrastructure-cluster.md` - Document cluster role assignment

### Cleanup

After extraction, archive or delete `docs/brainstorming/planning-30-nov-2025.md`.

## Implementation Steps

1. Create `docs/diagrams/infrastructure-overview.md` with full content
2. Create `docs/decisions/README.md` with index and format guide
3. Create `docs/decisions/0001-powerdns-over-unifi-dns.md`
4. Move `switch-topology-30-nov-2025.md` to permanent location or keep as-is
5. Clean up brainstorming directory

## Related Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Hardware and network specs
- [switch-topology-30-nov-2025.md](../brainstorming/switch-topology-30-nov-2025.md) - Port-level connections
- [2025-11-25-ipam-dns-stack-design.md](2025-11-25-ipam-dns-stack-design.md) - NetBox + PowerDNS design
