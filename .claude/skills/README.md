# Virgo-Core Claude Code Skills

This directory contains **Agent Skills** that extend Claude Code's capabilities for managing Proxmox VE infrastructure, NetBox IPAM, PowerDNS automation, and Ansible configuration management.

## Available Skills

### 1. Proxmox Infrastructure Management

**Skill:** `proxmox-infrastructure`

Expert guidance for Proxmox VE cluster management, VM provisioning, and template creation.

**Use when:**
- Creating or managing Proxmox VM templates
- Provisioning VMs via Terraform
- Configuring Proxmox networking (VLANs, bonds, bridges)
- Managing CEPH storage
- Working with QEMU guest agent
- Interacting with Proxmox API

**Includes:**
- API reference (Python proxmoxer, Terraform, Ansible)
- Storage management (CEPH, LVM-thin)
- QEMU guest agent integration
- Tools: `validate_template.py`, `cluster_status.py`
- Tutorial examples

**Learn more:** [proxmox-infrastructure/SKILL.md](proxmox-infrastructure/SKILL.md)

### 2. NetBox PowerDNS Integration

**Skill:** `netbox-powerdns-integration`

NetBox IPAM and PowerDNS integration for automated DNS record management and infrastructure documentation.

**Use when:**
- Setting up NetBox IPAM
- Implementing automated DNS workflows
- Using NetBox as source of truth
- Creating DNS naming conventions
- Configuring netbox-powerdns-sync plugin
- Setting up Ansible dynamic inventory from NetBox

**Includes:**
- DNS naming conventions (`<service>-<NN>-<purpose>.<domain>`)
- Terraform NetBox provider patterns
- PowerDNS sync plugin configuration
- Ansible dynamic inventory setup
- Tools: `validate_dns_naming.py`, `dns_audit.py`
- Integration examples (Proxmox → NetBox → PowerDNS)

**Learn more:** [netbox-powerdns-integration/SKILL.md](netbox-powerdns-integration/SKILL.md)

### 3. Ansible Best Practices

**Skill:** `ansible-best-practices`

Ansible playbook patterns, idempotency, testing, and secrets management from this repository.

**Use when:**
- Refactoring Ansible playbooks
- Improving playbook idempotency
- Implementing Infisical secrets management
- Setting up Ansible testing (molecule, ansible-lint)
- Analyzing playbook complexity
- Following Ansible best practices

**Includes:**
- Infisical secrets integration patterns
- Error handling (changed_when, failed_when, blocks)
- Variable precedence guide
- Common anti-patterns to avoid
- Tools: `check_idempotency.py`, `lint-all.sh`
- Production playbook examples

**Learn more:** [ansible-best-practices/SKILL.md](ansible-best-practices/SKILL.md)

## Skills Architecture

Each skill follows a **progressive disclosure** pattern:

```
skill-name/
├── SKILL.md              # Main skill file (loaded when triggered)
├── reference/            # Deep-dive documentation (loaded as needed)
├── patterns/             # Reusable patterns and workflows
├── workflows/            # End-to-end workflow guides
├── anti-patterns/        # Common mistakes to avoid
├── tools/                # Python scripts, shell scripts, CLI tools
└── examples/             # Tutorial and integration examples
```

### Loading Levels

1. **Metadata** - Always loaded (name + description)
2. **SKILL.md** - Loaded when skill triggers
3. **Supporting files** - Loaded by Claude as needed

This design keeps the context window efficient while providing comprehensive information.

## How Skills Work

**Skills are model-invoked** - Claude decides when to use them based on:
- Skill name and description (metadata)
- User's request and context
- Task requirements

**You don't need to explicitly invoke skills** - just work naturally:

```
User: "Help me create a Proxmox template with cloud-init"
→ Claude loads proxmox-infrastructure skill automatically

User: "Set up DNS automation with NetBox"
→ Claude loads netbox-powerdns-integration skill automatically

User: "Review this Ansible playbook for idempotency"
→ Claude loads ansible-best-practices skill automatically
```

## Skills Integration

These skills work together to provide complete infrastructure automation:

**Example Workflow:**

1. **Proxmox** - Create VM from template
2. **NetBox** - Register IP with DNS name
3. **PowerDNS** - Auto-create DNS records (via sync plugin)
4. **Ansible** - Configure VM using dynamic inventory from NetBox

**See:** [netbox-powerdns-integration/examples/01-vm-with-dns/](netbox-powerdns-integration/examples/01-vm-with-dns/)

## Quick Start

### Using Skills

Skills activate automatically based on your task. Example interactions:

**Proxmox Management:**
```
You: "I need to validate my Proxmox template"
Claude: [loads proxmox-infrastructure skill]
        "I'll use the validate_template.py tool to check your template..."
```

**DNS Automation:**
```
You: "Help me set up automated DNS for my VMs"
Claude: [loads netbox-powerdns-integration skill]
        "I'll show you how to integrate Proxmox with NetBox and PowerDNS..."
```

**Ansible Best Practices:**
```
You: "Review this playbook for issues"
Claude: [loads ansible-best-practices skill]
        "I'll check for idempotency issues using check_idempotency.py..."
```

### Running Tools

Skills include working tools (Python scripts, shell scripts):

```bash
# Proxmox tools
.claude/skills/proxmox-infrastructure/tools/validate_template.py --template-id 9000
.claude/skills/proxmox-infrastructure/tools/cluster_status.py --node foxtrot

# NetBox tools
.claude/skills/netbox-powerdns-integration/tools/validate_dns_naming.py docker-01-nexus.spaceships.work

# Ansible tools
.claude/skills/ansible-best-practices/tools/check_idempotency.py playbooks/*.yml
.claude/skills/ansible-best-practices/tools/lint-all.sh
```

All Python tools use `uv` inline dependencies (no separate installation needed).

### Examples

Each skill includes tutorial examples:

**Proxmox:**
- `examples/01-basic-vm/` - Minimal VM deployment

**NetBox:**
- `examples/01-vm-with-dns/` - Full Proxmox → NetBox → PowerDNS workflow

**Ansible:**
- `examples/02-infisical-secrets/` - Production playbook with secrets

## Development

### Validating Skills

Use the skill-creator validator:

```bash
cd .claude/skills/skill-creator
python scripts/quick_validate.py ../proxmox-infrastructure
python scripts/quick_validate.py ../netbox-powerdns-integration
python scripts/quick_validate.py ../ansible-best-practices
```

### Packaging Skills

To share a skill:

```bash
cd .claude/skills/skill-creator
python scripts/package_skill.py ../proxmox-infrastructure ./dist
```

Creates `proxmox-infrastructure.zip` ready for distribution.

## Meta-Skills

This directory also includes meta-skills for Claude Code development:

- **mcp-builder** - MCP server development guide
- **skill-creator** - Skill scaffolding and validation tools

## Repository Context

These skills are designed specifically for **Virgo-Core** infrastructure:

**Hardware:**
- 3-node Proxmox cluster (Foxtrot, Golf, Hotel)
- AMD Ryzen 9 9955HX, 64GB RAM, NVMe storage
- 10GbE networking with CEPH storage

**Software Stack:**
- Proxmox VE 9.x
- OpenTofu (Terraform) for provisioning
- Ansible for configuration management
- NetBox for IPAM
- PowerDNS for DNS
- Infisical for secrets

**Naming Convention:**
```
<service>-<NN>-<purpose>.<domain>
Examples:
  docker-01-nexus.spaceships.work
  k8s-02-worker.spaceships.work
  proxmox-foxtrot-mgmt.spaceships.work
```

## Further Reading

- **Project Documentation:** [../../docs/](../../docs/)
- **Terraform Examples:** [../../terraform/](../../terraform/)
- **Ansible Playbooks:** [../../ansible/playbooks/](../../ansible/playbooks/)
- **Skills Planning:** [../../docs/skills-planning.md](../../docs/skills-planning.md)

## Contributing

When updating skills:

1. Maintain progressive disclosure structure
2. Update reference docs separately from SKILL.md
3. Test tools before committing
4. Validate with `quick_validate.py`
5. Update examples if patterns change

## Version

**Skills Version:** 0.5.0 (Initial Release)

- ✅ Core skills foundation
- ✅ Reference documentation
- ✅ Working tools
- ✅ Tutorial examples
- ⏳ Advanced examples (planned)
- ⏳ Integration testing (planned)

See [CHANGELOG.md](../../CHANGELOG.md) for release history.
