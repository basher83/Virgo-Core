1. Proxmox Infrastructure Management Skill

Why: The repository is heavily focused on Proxmox VE cluster management with multiple
playbooks for template building, user creation, VLAN configuration, and VM
provisioning. A dedicated skill would provide:

-   Best practices for Proxmox API interactions
-   Template creation patterns and cloud-init configurations
-   Storage pool and datastore management guidance
-   QEMU guest agent integration patterns
-   Common pitfalls and troubleshooting for Proxmox + Terraform/Ansible

2. NetBox + PowerDNS Integration Skill

Why: This is a stated goal in docs/netbox-powerdns.md but not yet implemented. A
skill would provide:

-   NetBox IPAM best practices and data modeling
-   PowerDNS sync plugin configuration patterns
-   DNS naming convention automation (e.g., docker-01-nexus.spaceships.work)
-   Integration patterns between NetBox, PowerDNS, and Terraform
-   Common IPAM workflows for homelab environments

3. Ansible Playbook Refactoring & Best Practices Skill

Why: Looking at the playbooks, they're functional but could benefit from:

-   Role vs. playbook organization guidance
-   Variable precedence and organization patterns
-   Proper use of ansible.builtin vs. community modules
-   Idempotency patterns and changed_when/failed_when best practices
-   Testing strategies (molecule, ansible-lint)
-   Secrets management patterns with Infisical integration

4. OpenTofu/Terraform Module Development Skill

Why: The repository uses an external VM module but may need to:

-   Develop custom modules for NetBox integration
-   Create reusable modules for common Proxmox patterns
-   Module composition and dependency management
-   State management and workspace strategies
-   Testing and validation patterns for infrastructure code

5. Network Automation & VLAN Management Skill

Why: The cluster has complex networking (4 interfaces, VLANs, CEPH networks, jumbo
frames). A skill would help with:

-   VLAN-aware bridge configuration patterns
-   Network interface bonding/teaming
-   MTU configuration for CEPH storage networks
-   Corosync network separation best practices
-   Proxmox network troubleshooting

6. CEPH Storage Cluster Management Skill

Why: The goals document mentions CEPH cluster configuration (monitors, managers,
OSDs). A skill would provide:

-   CEPH deployment patterns for Proxmox
-   OSD configuration on NVMe drives (2 OSDs per drive)
-   Monitor and manager placement strategies
-   Performance tuning for homelab CEPH
-   Common CEPH issues and recovery procedures

7. Infrastructure Testing & Validation Skill

Why: No clear testing strategy exists for infrastructure changes. A skill would help
with:

-   Smoke testing patterns for Proxmox deployments
-   Terraform/OpenTofu testing frameworks (terratest, kitchen-terraform)
-   Ansible playbook testing with molecule
-   Integration testing for multi-component deployments
-   Rollback strategies and disaster recovery testing

8. Homelab Infrastructure-as-Code Patterns Skill

Why: General IaC skill specifically tailored to homelab constraints:

-   Cost-effective architecture patterns
-   Resource optimization for limited hardware
-   Documentation and knowledge management
-   Version control strategies for infrastructure
-   Migration strategies (from manual → automated)
-   Homelab-specific security considerations

Priority Ranking:

Tier 1 (Immediate Value):

1. Proxmox Infrastructure Management
2. NetBox + PowerDNS Integration
3. Ansible Playbook Refactoring & Best Practices

Tier 2 (Strategic Value):

4. Network Automation & VLAN Management
5. OpenTofu/Terraform Module Development
6. CEPH Storage Cluster Management

Tier 3 (Nice to Have):

7. Infrastructure Testing & Validation
8. Homelab Infrastructure-as-Code Patterns

These skills would complement the existing agents (ansible-research, commit-craft,
git-workflow) by providing domain-specific expertise for the technologies and
workflows central to this repository's mission.
