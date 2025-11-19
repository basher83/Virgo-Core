# Next Features for Virgo-Core

**Date**: 2025-11-18
**Status**: Planning
**Source**: ProxSpray analysis gaps, project goals review

## Executive Summary

Virgo-Core achieved v1.0.0 with production-ready Ansible roles and complete cluster automation. This document identifies the next features to implement, prioritized by value and effort.

## Completed Milestones

The v1.0.0 release delivered:

- 6 production Ansible roles with zero lint violations
- Perfect idempotency across Matrix cluster
- Automated CEPH deployment (12 OSDs)
- Comprehensive documentation (3,600 lines)
- Mintlify documentation infrastructure

Virgo-Core surpasses ProxSpray in automated OSD creation, secrets management (Infisical), modern tooling (uv/mise), and native Ansible modules.

## Identified Gaps

### ProxSpray Features Not Implemented

**Inventory Organization**
- No `group_vars/` directory for cluster-specific variables
- No `host_vars/` directory for node-specific overrides
- Current structure uses single `inventory/proxmox.yml` file

**Network Services**
- No DHCP server automation for VM networks
- No automated firewall/NAT configuration
- No iptables persistence

**Deployment Scenarios**
- No single-node CEPH support for dev/test clusters
- No HAProxy load balancer automation
- No public-facing infrastructure patterns

### Architectural Goals

**NetBox + PowerDNS Integration**
- Architecture documented in `netbox-powerdns.md`
- Implementation not started
- No automatic DNS record creation for VMs
- No IPAM synchronization

**VM Provisioning Pipeline**
- Manual workflow: template → VM → DNS → configuration
- No integrated automation
- No single-command deployment

**Documentation**
- Mintlify site configured but empty
- No getting-started guides
- No architecture diagrams
- No troubleshooting documentation

## Recommended Projects

### High Value, Low Effort

#### 1. Inventory Reorganization

**Objective**: Improve multi-cluster variable management.

**Implementation**:
```text
ansible/inventory/
├── hosts.yml                    # Current inventory
├── group_vars/
│   ├── all.yml                  # Global variables
│   ├── matrix_cluster.yml       # Matrix-specific config
│   ├── doggos_cluster.yml       # Doggos-specific config
│   └── nexus_cluster.yml        # Nexus-specific config
└── host_vars/
    ├── foxtrot.yml              # Node-specific overrides
    ├── golf.yml
    └── hotel.yml
```

**Benefits**:
- Cleaner variable organization
- Environment-specific configuration
- Node-level customization
- Standard Ansible pattern

**Effort**: 2-4 hours

#### 2. Mintlify Documentation Content

**Objective**: Populate documentation site with comprehensive guides.

**Content Needed**:
- Getting started guide
- Role usage tutorials
- Architecture diagrams
- API reference
- Troubleshooting guides
- Common workflows

**Benefits**:
- Easier onboarding
- Professional documentation
- Searchable knowledge base
- Reduced support burden

**Effort**: 8-12 hours

### High Value, Medium Effort

#### 3. NetBox + PowerDNS Integration

**Objective**: Implement automated DNS and IPAM synchronization.

**Architecture**: Already documented in `netbox-powerdns.md`.

**Components**:

**DNS Automation**:
- Auto-create DNS records when VMs deploy
- Sync records on VM changes
- Delete records when VMs destroy
- Reverse DNS automation

**IPAM Integration**:
- Query NetBox for available IPs
- Reserve IPs during VM creation
- Update NetBox with VM metadata
- Track IP usage automatically

**Implementation Path**:
1. Create `roles/netbox_ipam/` role
2. Create `roles/powerdns_records/` role
3. Integrate with OpenTofu VM deployment
4. Add Ansible post-provisioning hooks

**Benefits**:
- Single source of truth for infrastructure
- Eliminate manual DNS management
- Prevent IP conflicts
- Audit trail for IP assignments

**Effort**: 16-24 hours

#### 4. VM Provisioning Pipeline

**Objective**: Streamline template → VM → DNS → configuration workflow.

**Current Workflow**:
```bash
# Manual, multi-step process
cd terraform/netbox-vm
tofu init
tofu plan
tofu apply

# Separate DNS update
# Manual Ansible provisioning
```

**Target Workflow**:
```bash
# Single command deployment
mise run vm:deploy --name web01 --cluster matrix --template ubuntu-22.04
```

**Pipeline Stages**:
1. Query NetBox for next available IP
2. Reserve IP in NetBox
3. Deploy VM via OpenTofu
4. Create DNS records in PowerDNS
5. Run Ansible provisioning playbook
6. Update NetBox with final metadata

**Implementation**:
- Create Python orchestration script
- Integrate with existing tools
- Add error handling and rollback
- Comprehensive logging

**Benefits**:
- One-command VM deployment
- Consistent provisioning
- Reduced human error
- Faster iteration

**Effort**: 20-32 hours

### Nice to Have

#### 5. DHCP/NAT Automation

**Objective**: Automate network services on Proxmox hosts.

**Scope**:
- ISC DHCP server installation
- DHCP configuration per bridge
- iptables NAT rules
- Persistent iptables configuration

**Use Case**: Internal VM networks need DHCP from Proxmox hosts.

**Note**: May not be needed if using NetBox IPAM with static assignments.

**Effort**: 8-12 hours

#### 6. Backup and Disaster Recovery

**Objective**: Automate backup procedures and disaster recovery.

**Components**:
- Proxmox Backup Server integration
- CEPH snapshot management
- VM backup scheduling
- Disaster recovery playbooks
- Restoration testing automation

**Benefits**:
- Data protection
- Quick recovery
- Tested procedures
- Compliance support

**Effort**: 24-40 hours

## Priority Ranking

| Rank | Feature | Value | Effort | ROI |
|------|---------|-------|--------|-----|
| 1 | Inventory Reorganization | High | Low | Highest |
| 2 | Mintlify Content | High | Low | Highest |
| 3 | NetBox + PowerDNS | High | Medium | High |
| 4 | VM Provisioning Pipeline | High | Medium | High |
| 5 | Backup/DR | Medium | High | Medium |
| 6 | DHCP/NAT | Low | Medium | Low |

## Implementation Sequence

### Phase 1: Foundation (Week 1)
- Reorganize inventory structure
- Migrate variables to group_vars/host_vars
- Test existing playbooks with new structure

### Phase 2: Documentation (Week 2)
- Create getting-started guide
- Document each role with examples
- Add architecture diagrams
- Write troubleshooting guide

### Phase 3: Integration (Weeks 3-4)
- Implement NetBox IPAM role
- Implement PowerDNS automation
- Test DNS record creation
- Validate IPAM synchronization

### Phase 4: Automation (Weeks 5-6)
- Build VM provisioning pipeline
- Create orchestration script
- Integrate all components
- Add error handling

## Success Criteria

**Inventory Reorganization**:
- All existing playbooks work unchanged
- Variables logically organized
- Documentation updated

**Mintlify Documentation**:
- Comprehensive getting-started guide
- All roles documented with examples
- Troubleshooting section complete
- Searchable and navigable

**NetBox + PowerDNS**:
- DNS records auto-created for new VMs
- IPAM reserves IPs automatically
- Bi-directional synchronization working
- Integration tested on Matrix cluster

**VM Provisioning Pipeline**:
- Single command deploys complete VM
- All services integrated (NetBox, DNS, Ansible)
- Error handling and rollback working
- Documentation complete

## Next Steps

1. Review priorities with stakeholders
2. Select first project to implement
3. Create detailed implementation plan
4. Begin development

## Additional Exploration

Beyond this document, consider exploring:

**Community Projects**:
- CEPH-ansible (official Ceph automation)
- HomelabOS (application deployment patterns)
- Ansible-NAS (service orchestration)

**New Ansible Collections**:
- Recent `community.general.proxmox_*` modules
- Updated `community.proxmox` features
- CEPH-specific collections

**Terraform Providers**:
- Telmate/proxmox provider patterns
- Community best practices
- Advanced provisioning techniques

---

**This document provides a clear roadmap for Virgo-Core's next development phase, building on the solid v1.0.0 foundation.**
