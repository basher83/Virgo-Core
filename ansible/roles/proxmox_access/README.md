# Ansible Role: proxmox_access

Manage Proxmox VE access control including custom roles, groups, users, API tokens, and ACL permissions. This role is designed for infrastructure-as-code workflows, particularly Terraform/OpenTofu automation.

## Features

- ✅ **Custom Role Management**: Create Proxmox roles with granular privilege sets
- ✅ **Group Management**: Organize users into groups for easier permission management
- ✅ **User Management**: Create/manage Proxmox users (PAM and PVE realms)
- ✅ **API Token Generation**: Create API tokens for passwordless automation
- ✅ **ACL Configuration**: Grant permissions to users/groups on specific resources
- ✅ **Terraform Integration**: Export environment files for Terraform/OpenTofu
- ✅ **Infisical Secrets**: Optional integration with Infisical for credential management
- ✅ **Idempotent Operations**: Safe to run multiple times without side effects
- ✅ **State-Based**: Supports both creation and removal via `state` parameter

## Requirements

### Ansible Version
- Minimum: 2.15+
- Tested: 2.17+

### Collections
- `community.proxmox` - Proxmox VE modules
- `infisical.vault` - Secrets management (optional)
- `ansible.builtin` - Core modules

### Target Systems
- Proxmox VE 8.x or 9.x
- Debian 12 (Bookworm) or Ubuntu 22.04/24.04
- Root/sudo access on Proxmox nodes

### Prerequisites
- For PAM users: Linux users must exist first (use `system_user` role)
- For API operations: Admin credentials (root@pam or equivalent)

## Role Variables

See [defaults/main.yml](defaults/main.yml) for comprehensive variable documentation.

### Connection Variables

```yaml
# API connection settings
proxmox_api_host: "{{ ansible_default_ipv4.address }}"
proxmox_validate_certs: false
proxmox_no_log: true
```

### Infisical Configuration (Optional)

```yaml
infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
infisical_env: 'prod'
infisical_path: '/cluster-name'
```

### Role Configuration

```yaml
proxmox_roles:
  - name: TerraformUser
    privileges:
      - Datastore.Allocate
      - VM.Allocate
      - VM.Clone
      # ... more privileges
```

### Group Configuration

```yaml
proxmox_groups:
  - name: terraform-users
    comment: "Automation users"
    state: present
```

### User Configuration

```yaml
proxmox_users:
  - userid: terraform@pam
    groups:
      - terraform-users
    comment: "Terraform automation user"
    email: terraform@example.com
    state: present
```

### Token Configuration

```yaml
proxmox_tokens:
  - userid: terraform@pam
    tokenid: automation
    privsep: false  # false = inherit user permissions
    comment: "Automation token"
    state: present
```

### ACL Configuration

```yaml
proxmox_acls:
  - path: /
    type: group
    ugid: terraform-users
    roleid: TerraformUser
    state: present
```

### Terraform Export

```yaml
export_terraform_env: true
terraform_env_dir: "{{ lookup('env', 'HOME') }}/tmp/.proxmox-terraform"
```

## Dependencies

None (but works best with `system_user` role for Linux user creation).

## Example Usage

### Basic Terraform Automation Setup

```yaml
- hosts: proxmox_nodes
  become: true
  roles:
    - role: proxmox_access
      vars:
        infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
        infisical_env: 'prod'
        infisical_path: '/matrix-cluster'

        proxmox_roles:
          - name: TerraformUser
            privileges:
              - Datastore.Allocate
              - VM.Allocate
              - VM.Clone
              - VM.Config.CDROM
              - VM.Config.CPU
              - VM.Config.Disk
              - VM.PowerMgmt

        proxmox_groups:
          - name: terraform-users
            comment: "Terraform automation"

        proxmox_users:
          - userid: terraform@pam
            groups: [terraform-users]
            comment: "Terraform user"

        proxmox_tokens:
          - userid: terraform@pam
            tokenid: automation
            privsep: false

        proxmox_acls:
          - path: /
            type: group
            ugid: terraform-users
            roleid: TerraformUser

        export_terraform_env: true
```

### Complete Workflow with Linux User

```yaml
- hosts: proxmox_nodes
  become: true
  roles:
    # Step 1: Create Linux PAM user
    - role: system_user
      vars:
        system_users:
          - name: terraform
            ssh_keys:
              - "{{ lookup('file', 'files/terraform.pub') }}"
            sudo_rules:
              - /sbin/pvesm
              - /sbin/qm
            sudo_nopasswd: true

    # Step 2: Create Proxmox access
    - role: proxmox_access
      vars:
        proxmox_users:
          - userid: terraform@pam
            groups: [terraform-users]
        # ... rest of config
```

### API-Only User (PVE Realm)

```yaml
- hosts: proxmox_nodes
  become: true
  roles:
    - role: proxmox_access
      vars:
        proxmox_users:
          - userid: api_user@pve
            groups: [api-users]
            comment: "API-only user"

        proxmox_tokens:
          - userid: api_user@pve
            tokenid: readonly
            privsep: true  # Separate permissions from user

        proxmox_acls:
          - path: /
            type: user
            ugid: api_user@pve
            roleid: PVEAuditor  # Built-in read-only role
```

### Remove Access

```yaml
- hosts: proxmox_nodes
  become: true
  roles:
    - role: proxmox_access
      vars:
        proxmox_tokens:
          - userid: terraform@pam
            tokenid: automation
            state: absent

        proxmox_users:
          - userid: terraform@pam
            state: absent

        proxmox_groups:
          - name: terraform-users
            state: absent
```

## Playbook Integration

Use the provided orchestration playbook:

```bash
# Setup Terraform automation
cd ansible
uv run ansible-playbook playbooks/setup-terraform-automation.yml

# Specific cluster
uv run ansible-playbook playbooks/setup-terraform-automation.yml \
  -e "target_cluster=matrix_cluster"

# Custom configuration
uv run ansible-playbook playbooks/setup-terraform-automation.yml \
  -e "terraform_username=myuser" \
  -e "export_terraform_env=true"
```

## Terraform Integration

After running the role with `export_terraform_env: true`:

```bash
# Source the environment file
source ~/tmp/.proxmox-terraform/proxmox-foxtrot

# Use with OpenTofu/Terraform
cd terraform/netbox-vm
tofu plan
tofu apply
```

The environment file exports:
- `PROXMOX_VE_ENDPOINT` - API endpoint URL
- `PROXMOX_VE_API_TOKEN` - Full API token value
- `TF_VAR_proxmox_*` - Alternative Terraform variable format

## Task Breakdown

The role is organized into modular task files:

| Task File | Purpose | Module Used |
|-----------|---------|-------------|
| `main.yml` | Orchestration | - |
| `secrets.yml` | Retrieve Infisical credentials | `infisical.vault` |
| `roles.yml` | Create custom Proxmox roles | `pveum` command |
| `groups.yml` | Manage Proxmox groups | `community.proxmox.proxmox_group` |
| `users.yml` | Manage Proxmox users | `pveum` command |
| `tokens.yml` | Generate API tokens | `pveum` command |
| `acls.yml` | Configure ACL permissions | `community.proxmox.proxmox_access_acl` |
| `env_export.yml` | Export Terraform env files | `ansible.builtin.template` |

## Privilege Reference

Common privilege sets for different use cases:

### Terraform/IaC Automation
```yaml
privileges:
  - Datastore.Allocate
  - Datastore.AllocateSpace
  - Datastore.AllocateTemplate
  - Datastore.Audit
  - VM.Allocate
  - VM.Audit
  - VM.Clone
  - VM.Config.CDROM
  - VM.Config.Cloudinit
  - VM.Config.CPU
  - VM.Config.Disk
  - VM.Config.Memory
  - VM.Config.Network
  - VM.PowerMgmt
```

### Read-Only Monitoring
```yaml
privileges:
  - Sys.Audit
  - Datastore.Audit
  - VM.Audit
  - VM.Monitor
```

### VM Management Only
```yaml
privileges:
  - VM.PowerMgmt
  - VM.Console
  - VM.Monitor
```

See [Proxmox VE documentation](https://pve.proxmox.com/wiki/User_Management) for complete privilege list.

## Security Considerations

### Token Security

⚠️ **API tokens are shown only once during creation**

- Save token values immediately
- Store securely (use Infisical, HashiCorp Vault, etc.)
- Tokens are displayed in playbook output but can be suppressed with `proxmox_no_log: true`
- Use `privsep: true` for tokens that need different permissions than the user

### Privilege Separation

```yaml
# Option 1: Token inherits user permissions (simpler)
proxmox_tokens:
  - userid: terraform@pam
    tokenid: automation
    privsep: false

# Option 2: Token has separate permissions (more secure)
proxmox_tokens:
  - userid: terraform@pam
    tokenid: readonly
    privsep: true  # Requires separate ACL for token

proxmox_acls:
  - path: /
    type: user
    ugid: terraform@pam!readonly  # Token-specific ACL
    roleid: PVEAuditor
```

### PAM vs PVE Realm

- **PAM (@pam)**: Linux system users, requires Linux user to exist first
  - ✅ Use for SSH + API access
  - ✅ Integrates with system authentication
  - ❌ Requires Linux user management

- **PVE (@pve)**: Proxmox-only users, managed entirely in Proxmox
  - ✅ API-only access, no SSH
  - ✅ Easier to manage programmatically
  - ❌ No system-level authentication

## Idempotency

This role is fully idempotent:

- ✅ Running twice produces no changes on second run
- ✅ Checks existence before creating resources
- ✅ Uses `changed_when` and `failed_when` appropriately
- ✅ Gracefully handles "already exists" scenarios

Test idempotency:
```bash
# Run once
uv run ansible-playbook playbooks/setup-terraform-automation.yml

# Run again - should show no changes
uv run ansible-playbook playbooks/setup-terraform-automation.yml
```

## Testing

### Syntax Check
```bash
cd ansible
uv run ansible-playbook --syntax-check playbooks/setup-terraform-automation.yml
```

### Lint Check
```bash
mise run ansible-lint
```

### Dry Run (Check Mode)
```bash
uv run ansible-playbook playbooks/setup-terraform-automation.yml \
  --check --diff --limit foxtrot
```

### Verify Permissions
```bash
# SSH to node and test
ssh terraform@foxtrot

# Test sudo access
sudo pvesm status

# Test API token (on controller)
curl -k -H "Authorization: PVEAPIToken=terraform@pam!automation=<token-value>" \
  https://foxtrot.example.com:8006/api2/json/nodes
```

## Troubleshooting

### Token Creation Failed

**Error**: `pveum user token add` fails with "user does not exist"

**Solution**: Ensure Proxmox user exists first. Check with:
```bash
ssh root@node pveum user list | grep terraform
```

### PAM User Creation Failed

**Error**: `pveum user add terraform@pam` fails

**Solution**: Linux user must exist first. Run `system_user` role before `proxmox_access`.

### ACL Not Applied

**Error**: User has no permissions despite ACL configuration

**Solution**: Check role assignment:
```bash
ssh root@node pveum aclmod list
```

### Terraform Can't Connect

**Error**: Terraform fails with "authentication failed"

**Solution**:
1. Verify token was created: `pveum user token list terraform@pam`
2. Check environment file has correct token value
3. Verify token has `privsep: false` or separate ACL if `privsep: true`

## Migration from Legacy Playbook

This role replaces `proxmox-create-terraform-user.yml`:

**Old workflow**:
```bash
ansible-playbook playbooks/proxmox-create-terraform-user.yml
```

**New workflow**:
```bash
ansible-playbook playbooks/setup-terraform-automation.yml
```

The new playbook provides:
- ✅ Better separation of concerns (Linux user vs Proxmox access)
- ✅ Reusable role for other automation users
- ✅ Clearer variable structure
- ✅ Improved idempotency
- ✅ Better error handling

## Related Roles

- **system_user**: Create Linux PAM users with SSH and sudo access
- **proxmox_cluster**: Cluster formation and management (Phase 4)
- **proxmox_network**: Network configuration (Phase 3)
- **proxmox_ceph**: CEPH storage management (Phase 4)

## License

MIT

## Author Information

This role is part of the Virgo-Core infrastructure automation project.

For issues and contributions, see the main repository.
