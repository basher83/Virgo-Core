# IPAM & DNS Stack Design

**Date:** 2025-11-25
**Status:** Approved
**Author:** Claude + User collaboration

## Overview

Deploy a unified NetBox (IPAM) + PowerDNS (authoritative DNS) stack on a single
VM using Docker Compose. NetBox serves as the source of truth for IP addresses,
automatically syncing DNS records to PowerDNS when IPs are created or modified.

## Design Drivers

- **Simplicity** - Minimal moving parts, easy to maintain
- **Docker-native** - Leverage Docker Compose for service orchestration
- **Ansible-only** - Single tool for VM provisioning and configuration
- **PBS backup** - VM-level backups via Proxmox Backup Server

## Architecture

### Stack Overview

```text
┌──────────────────────────────────────────────────────────────┐
│                        Docker VM                              │
│                    Ubuntu 24.04 LTS                           │
│              4 cores, 8GB RAM, 64GB disk                      │
│                                                               │
│  ┌─ NetBox Stack (netbox-docker) ─────────────────────────┐  │
│  │  netbox (:8080)                                        │  │
│  │  netbox-worker                                         │  │
│  │  netbox-housekeeping                                   │  │
│  │  postgres-netbox (:5432)                               │  │
│  │  redis                                                 │  │
│  │  Plugin: netbox-powerdns-sync                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                            │                                  │
│                            │ (PowerDNS API calls)             │
│                            ▼                                  │
│  ┌─ PowerDNS Stack ───────────────────────────────────────┐  │
│  │  pdns-auth (:53 DNS, :8081 API)                        │  │
│  │  pdns-admin (:9191)                                    │  │
│  │  postgres-pdns (:5433)                                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌─ Traefik (:80, :443) ──────────────────────────────────┐  │
│  │  Routes:                                               │  │
│  │    netbox.domain → netbox:8080                         │  │
│  │    pdns-admin.domain → pdns-admin:9191                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Exposed Ports: 53/udp+tcp (DNS), 80/443 (Traefik)           │
└──────────────────────────────────────────────────────────────┘
```

### Container Inventory

| Container | Image | Purpose | Port |
|-----------|-------|---------|------|
| netbox | netbox/netbox | IPAM web UI and API | 8080 |
| netbox-worker | netbox/netbox | Background task processing | - |
| netbox-housekeeping | netbox/netbox | Scheduled maintenance | - |
| postgres-netbox | postgres:16 | NetBox database | 5432 |
| redis | redis:7-alpine | NetBox caching/queues | 6379 |
| pdns-auth | powerdns/pdns-auth | Authoritative DNS server | 53, 8081 |
| pdns-admin | powerdnsadmin/pda | PowerDNS web management | 9191 |
| postgres-pdns | postgres:16 | PowerDNS database | 5433 |
| traefik | traefik:v3 | Reverse proxy, TLS termination | 80, 443 |

**Total:** 9 containers

### Design Decision: Separate PostgreSQL Instances

The official netbox-docker bundles its own PostgreSQL. Rather than override this
to share a database with PowerDNS, we use two separate PostgreSQL containers:

- `postgres-netbox` - NetBox database (bundled with netbox-docker)
- `postgres-pdns` - PowerDNS database (dedicated)

**Rationale:** Simpler configuration, uses netbox-docker defaults, isolates
failure domains. Resource overhead is minimal.

## Integration Flow

The `netbox-powerdns-sync` plugin watches NetBox for IP/device changes and
pushes records to PowerDNS via REST API.

```text
User creates IP in NetBox (with dns_name field)
                │
                ▼
┌───────────────────────────────┐
│  NetBox post-save signal      │
│  triggers netbox-powerdns-sync│
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Plugin matches zone rules:   │
│  - IP dns_name field          │
│  - Device/VM name             │
│  - Tag-based matching         │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  PowerDNS API call            │
│  POST /api/v1/servers/        │
│    localhost/zones/{zone}/    │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  A/AAAA/PTR records created   │
│  in PowerDNS                  │
└───────────────────────────────┘
```

### Day-to-Day Workflow

1. Create/update IP address in NetBox with `dns_name` field populated
2. Plugin automatically creates corresponding DNS record in PowerDNS
3. Delete IP in NetBox triggers plugin to remove DNS record
4. PowerDNS-Admin available for zone management and troubleshooting

### PowerDNS-Admin Role

- Initial zone setup (forward and reverse zones)
- SOA and NS record configuration
- Manual overrides when needed
- Zone content inspection and troubleshooting

## Deployment

### Ansible-Only Approach

Single tool handles VM provisioning through stack deployment. No Terraform
state files to manage.

### Playbook Structure

```text
ansible/playbooks/deploy-ipam-stack.yml
  │
  ├── Phase 1: Template Management
  │     ├── Check if Ubuntu 24.04 template exists
  │     ├── If not: Download cloud image
  │     ├── Create VM from image
  │     ├── Configure cloud-init defaults
  │     └── Convert to template
  │
  ├── Phase 2: VM Creation
  │     ├── Clone from template
  │     ├── Set resources (4 cores, 8GB RAM, 64GB disk)
  │     ├── Apply cloud-init (static IP, SSH keys, hostname)
  │     ├── Start VM
  │     └── Wait for SSH ready
  │
  ├── Phase 3: Docker Setup
  │     └── Install Docker CE + Compose plugin
  │
  ├── Phase 4: Stack Deployment
  │     ├── Create directory structure
  │     ├── Deploy docker-compose.yml from template
  │     ├── Deploy environment/config files
  │     ├── Pull container images
  │     └── docker compose up -d
  │
  └── Phase 5: Validation
        ├── Container health checks
        ├── NetBox UI accessible
        ├── PowerDNS API responding
        └── DNS resolution test
```

### Role Structure

```text
ansible/roles/
├── proxmox_template/        # Template creation from cloud image
│   └── (pattern from Supernova proxmox-build-template.yml)
├── proxmox_vm_clone/        # Clone template to VM
└── docker_ipam_stack/       # NetBox + PowerDNS deployment
    ├── tasks/
    │   ├── main.yml
    │   ├── docker.yml
    │   ├── compose.yml
    │   └── configure.yml
    ├── templates/
    │   ├── docker-compose.yml.j2
    │   ├── netbox.env.j2
    │   ├── pdns.conf.j2
    │   └── traefik.yml.j2
    ├── defaults/main.yml
    └── handlers/main.yml
```

### Inventory Configuration

```yaml
# inventory/group_vars/ipam_servers.yml
ipam_vm_name: "netbox-pdns"
ipam_vm_id: 300
ipam_vm_cores: 4
ipam_vm_memory: 8192
ipam_vm_disk: 64
ipam_vm_ip: "192.168.x.x/24"
ipam_vm_gateway: "192.168.x.1"
ipam_vm_dns: "192.168.x.x"
ipam_vm_template_id: 9000

# Domain configuration
ipam_domain: "homelab.local"
netbox_hostname: "netbox"
pdns_admin_hostname: "pdns-admin"

# PowerDNS zones (created in pdns-admin)
pdns_forward_zones:
  - "homelab.local"
pdns_reverse_zones:
  - "168.192.in-addr.arpa"
```

### Secrets (Infisical)

| Secret | Purpose |
|--------|---------|
| `NETBOX_SECRET_KEY` | Django secret key |
| `NETBOX_DB_PASSWORD` | PostgreSQL password for NetBox |
| `PDNS_DB_PASSWORD` | PostgreSQL password for PowerDNS |
| `PDNS_API_KEY` | PowerDNS REST API authentication |
| `PDNS_ADMIN_SECRET` | PowerDNS-Admin secret key |

### Idempotency

- Template creation skipped if template ID exists
- VM creation skipped if VM ID exists
- Docker Compose stack updated in place on re-run
- Configuration files only updated when changed

## Backup Strategy

- **VM-level:** Proxmox Backup Server schedules for entire VM
- **Recovery:** Restore VM from PBS snapshot, all data intact
- **RPO:** Depends on PBS schedule (recommend daily minimum)

## Post-Deployment Setup

Manual steps after Ansible deployment:

1. **NetBox initial setup**
   - Create admin superuser
   - Configure site and regions
   - Define IP prefixes
   - Install/enable netbox-powerdns-sync plugin

2. **PowerDNS zone setup (via pdns-admin)**
   - Create forward zone(s)
   - Create reverse zone(s)
   - Configure SOA and NS records

3. **Plugin configuration**
   - Configure PowerDNS API endpoint in NetBox
   - Set zone matching rules
   - Test with sample IP creation

## Future Considerations

- **DNSSEC:** Both PowerDNS and netbox-plugin-dns support DNSSEC
- **HA:** Could add PowerDNS secondary for redundancy
- **Monitoring:** Prometheus metrics from PowerDNS `/metrics` endpoint
- **Migration:** Option to move to netbox-plugin-dns for full DNS management in NetBox

## Related Documentation

- [PowerDNS Ansible Research](../research/powerdns-ansible-roles.md)
- [NetBox PowerDNS Integration Research](../research/netbox-powerdns-integration.md)
- [PowerDNS Setup Guide](../research/powerdns-setup-guide.md)

## References

- [netbox-docker](https://github.com/netbox-community/netbox-docker)
- [PowerDNS Authoritative](https://doc.powerdns.com/authoritative/)
- [netbox-powerdns-sync](https://github.com/ArnesSI/netbox-powerdns-sync)
- [PowerDNS-Admin](https://github.com/PowerDNS-Admin/PowerDNS-Admin)
