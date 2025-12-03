# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) documenting significant technical decisions.

## Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| [0001](0001-powerdns-over-unifi-dns.md) | PowerDNS over UniFi DNS | Accepted | 2025-11-30 |
| [0002](0002-quantum-as-infrastructure-cluster.md) | Quantum as Infrastructure Cluster | Accepted | 2025-11-30 |

## ADR Format

Each ADR follows this structure:

```markdown
# ADR-NNNN: Title

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Supersedes**: ADR-XXXX (if applicable)

## Context

What situation led to this decision? What problem needed solving?

## Decision

What did we decide? State the decision clearly.

## Consequences

What does this mean going forward? Include both benefits and trade-offs.

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Alternative A | Reason |
| Alternative B | Reason |
```

## Status Definitions

- **Proposed** - Under discussion, not yet accepted
- **Accepted** - Decision made and in effect
- **Deprecated** - No longer applies, but kept for history
- **Superseded** - Replaced by a newer ADR (link to replacement)

## When to Write an ADR

Write an ADR when you make a decision that:

- Affects architecture or major components
- Involves choosing between multiple valid approaches
- You would want to remember "why" in 6 months
- Others would need to understand to work on the system

## Numbering

ADRs are numbered sequentially (0001, 0002, ...). Never reuse numbers, even for deprecated decisions.
