# ADR-0001: PowerDNS over UniFi DNS

**Status**: Accepted
**Date**: 2025-11-30

## Context

The infrastructure needed programmable DNS that could:

- Integrate with Proxmox SDN across multiple clusters
- Sync with NetBox as the source of truth for IPAM
- Support infrastructure-as-code workflows via Ansible/Terraform
- Avoid circular dependencies (DNS must not depend on clusters it serves)

The UDMP-Max (OS 4.4.6/Network 10.0.160) has a local DNS feature that was evaluated as a potential solution.

## Decision

Use **PowerDNS with NetBox integration** instead of UniFi DNS for authoritative DNS.

PowerDNS will run on the infrastructure cluster (Quantum) and serve DNS for all Proxmox clusters. UniFi DNS remains available for rare edge cases or local overrides only.

## Consequences

**Benefits:**

- Full REST API enables automation and infrastructure-as-code
- Native NetBox plugin syncs IPAM data to DNS records
- Proxmox SDN plugins enable automatic VM/LXC DNS registration
- Running on separate cluster avoids circular dependencies
- Supports zone transfers, DNSSEC, and advanced DNS features

**Trade-offs:**

- Additional infrastructure to deploy and maintain
- Must ensure PowerDNS VM is highly available
- Requires network connectivity from all clusters to Quantum

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| UniFi DNS (UDMP-Max) | Gateway-scoped only; no Proxmox SDN integration; limited API; creates hardware dependency |
| Pi-hole/AdGuard | Designed for ad-blocking, not authoritative DNS; limited API |
| BIND | Complex configuration; less native integration with NetBox |
| CoreDNS | Kubernetes-focused; requires custom plugins for NetBox sync |
