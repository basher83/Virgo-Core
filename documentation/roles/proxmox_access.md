# proxmox_access Role

Manage Proxmox VE access control for automation and operators.

**Use Cases**: Terraform/OpenTofu automation, API tokens, operator access, team permissions

**Dependencies**: Works with system_user for PAM users (Linux user must exist first)

**Battle-Tested**: Production deployment on Matrix cluster, validated Terraform integration

## Overview

The `proxmox_access` role provides declarative access control management:

- Create custom Proxmox roles with granular privileges
- Organize users into groups for simplified permissions
- Manage users in PAM and PVE realms
- Generate API tokens for passwordless automation
- Configure ACL permissions on specific resources
- Export environment files for Terraform/OpenTofu

## Quick Start

Create Terraform automation user with API token:

```yaml
---
- name: Setup Terraform automation
  hosts: proxmox_nodes
  roles:
    - role: proxmox_access
      infisical_project_id: '7b832220-24c0-45bc-a5f1-ce9794a31259'
      infisical_env: 'prod'
      infisical_path: '/matrix-cluster'

      proxmox_roles:
        - name: TerraformUser
          privileges:
            - Datastore.Allocate
            - VM.Allocate
            - VM.Clone
            - VM.Config.Disk
            - VM.PowerMgmt

      proxmox_groups:
        - name: terraform-users
          comment: "Terraform automation"

      proxmox_users:
        - userid: terraform@pam
          groups: [terraform-users]

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

Run:

```bash
cd ansible
uv run ansible-playbook playbooks/setup-terraform-automation.yml
```

Expected: Creates user, token, permissions; exports `~/tmp/.proxmox-terraform/proxmox-foxtrot`

## Configuration Reference

### Connection Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `proxmox_api_host` | string | `{{ ansible_default_ipv4.address }}` | API endpoint |
| `proxmox_validate_certs` | bool | `false` | Validate SSL certificates |
| `proxmox_no_log` | bool | `true` | Suppress sensitive output |

### Infisical Configuration

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `infisical_project_id` | string | No | Infisical project UUID |
| `infisical_env` | string | No | Environment (prod, dev) |
| `infisical_path` | string | No | Secret path prefix |

### Role Definition

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `proxmox_roles` | list | No | Custom role definitions |
| `├─ name` | string | Yes | Role identifier |
| `├─ privileges` | list | Yes | Privilege strings (see reference below) |
| `└─ state` | string | No | `present` or `absent` (default: `present`) |

### Group Definition

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `proxmox_groups` | list | No | Group definitions |
| `├─ name` | string | Yes | Group name |
| `├─ comment` | string | No | Description |
| `└─ state` | string | No | `present` or `absent` (default: `present`) |

### User Definition

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `proxmox_users` | list | No | User definitions |
| `├─ userid` | string | Yes | Username@realm (e.g., `user@pam`, `api@pve`) |
| `├─ groups` | list | No | Group memberships |
| `├─ comment` | string | No | Description |
| `├─ email` | string | No | Email address |
| `└─ state` | string | No | `present` or `absent` (default: `present`) |

**Realms**:

- `@pam`: Linux system users (requires Linux user via system_user)
- `@pve`: Proxmox-only users (API access, no system login)

### Token Definition

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `proxmox_tokens` | list | No | API token definitions |
| `├─ userid` | string | Yes | Username@realm owning token |
| `├─ tokenid` | string | Yes | Token identifier |
| `├─ privsep` | bool | No | Privilege separation (default: `false`) |
| `├─ comment` | string | No | Description |
| `└─ state` | string | No | `present` or `absent` (default: `present`) |

**Privilege Separation**:

- `privsep: false`: Token inherits user permissions (simpler)
- `privsep: true`: Token requires separate ACL grant (more secure)

### ACL Definition

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `proxmox_acls` | list | No | Access control entries |
| `├─ path` | string | Yes | Resource path (`/`, `/vms/100`, `/storage/local`) |
| `├─ type` | string | Yes | `user` or `group` |
| `├─ ugid` | string | Yes | User ID or group name |
| `├─ roleid` | string | Yes | Role name (built-in or custom) |
| `└─ state` | string | No | `present` or `absent` (default: `present`) |

### Terraform Export

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `export_terraform_env` | bool | `false` | Export environment files |
| `terraform_env_dir` | string | `~/tmp/.proxmox-terraform` | Output directory |

## Privilege Reference

### Terraform/IaC Automation

Complete privilege set for VM provisioning:

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

Audit and monitoring without changes:

```yaml
privileges:
  - Sys.Audit
  - Datastore.Audit
  - VM.Audit
  - VM.Monitor
```

### VM Management Only

Power control and console access:

```yaml
privileges:
  - VM.PowerMgmt
  - VM.Console
  - VM.Monitor
```

See [Proxmox VE User Management](https://pve.proxmox.com/wiki/User_Management) for complete privilege list.

## Integration Patterns

### With system_user Role

Create Linux user and Proxmox access together:

```yaml
---
- name: Complete automation setup
  hosts: proxmox_nodes
  roles:
    - role: system_user
      system_users:
        - username: terraform
          ssh_keys:
            - "{{ lookup('file', 'files/terraform.pub') }}"
          sudo: nopasswd

    - role: proxmox_access
      proxmox_users:
        - userid: terraform@pam
          groups: [terraform-users]
      proxmox_tokens:
        - userid: terraform@pam
          tokenid: automation
          privsep: false
      proxmox_acls:
        - path: /
          type: group
          ugid: terraform-users
          roleid: TerraformUser
```

### API-Only User (PVE Realm)

Create user without Linux account:

```yaml
proxmox_users:
  - userid: monitoring@pve
    groups: [monitoring]
    comment: "Read-only monitoring"

proxmox_tokens:
  - userid: monitoring@pve
    tokenid: readonly
    privsep: true

proxmox_acls:
  - path: /
    type: user
    ugid: monitoring@pve
    roleid: PVEAuditor
```

### Token with Separate Permissions

Grant token different privileges than user:

```yaml
proxmox_tokens:
  - userid: admin@pam
    tokenid: restricted
    privsep: true

proxmox_acls:
  # User has full permissions
  - path: /
    type: user
    ugid: admin@pam
    roleid: Administrator

  # Token has limited permissions
  - path: /vms
    type: user
    ugid: admin@pam!restricted
    roleid: PVEVMUser
```

### Terraform Integration

After running role with `export_terraform_env: true`:

```bash
# Source environment file
source ~/tmp/.proxmox-terraform/proxmox-foxtrot

# Verify variables
echo $PROXMOX_VE_ENDPOINT
echo $PROXMOX_VE_API_TOKEN

# Run Terraform
cd terraform/netbox-vm
tofu plan
tofu apply
```

Environment file exports:

- `PROXMOX_VE_ENDPOINT`: API URL (<https://hostname:8006>)
- `PROXMOX_VE_API_TOKEN`: Full token (userid!tokenid=secret)
- `TF_VAR_proxmox_*`: Alternative variable format

### Remove Access

Clean up users and tokens:

```yaml
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

## Troubleshooting

### Token Creation Failed

**Symptom**: `pveum user token add` fails with "user does not exist"

**Diagnosis**:

```bash
ssh root@node pveum user list | grep username
```

**Solutions**:

- Verify user exists before creating token
- Check userid includes correct realm (`@pam` or `@pve`)
- For PAM users: ensure Linux user exists (run system_user role first)

### PAM User Creation Failed

**Symptom**: `pveum user add user@pam` fails

**Diagnosis**:

```bash
ssh root@node getent passwd username
```

**Solutions**:

- Create Linux user first using system_user role
- Verify username matches between Linux and Proxmox
- Check user has valid shell and home directory

### ACL Not Applied

**Symptom**: User has no permissions despite ACL configuration

**Diagnosis**:

```bash
ssh root@node pveum aclmod list
ssh root@node pveum user permissions user@pam
```

**Solutions**:

- Verify role assigned to user or group
- Check ACL path matches resource (/ for all, /vms/100 for specific VM)
- Confirm user is member of group if using group ACL
- For privsep tokens: check ACL uses `userid!tokenid` format

### Terraform Authentication Failed

**Symptom**: Terraform fails with "authentication failed"

**Diagnosis**:

```bash
# Verify token exists
ssh root@node pveum user token list userid@pam

# Test token manually
curl -k -H "Authorization: PVEAPIToken=userid@pam!tokenid=secret" \
  https://hostname:8006/api2/json/nodes
```

**Solutions**:

- Check token value in environment file matches actual token
- Verify token has `privsep: false` or separate ACL if `privsep: true`
- Confirm API endpoint URL is correct (https, port 8006)
- Check network connectivity to Proxmox API

### Idempotency Failed

**Symptom**: Role shows changes on second run

**Diagnosis**:

```bash
# Run with check mode
uv run ansible-playbook playbooks/setup-terraform-automation.yml --check
```

**Solutions**:

- Review task output for "changed" status
- Check for manual changes via Proxmox GUI
- Verify role and group definitions are complete
- Report issue if role incorrectly detects changes

## See Also

- [system_user](system_user.md) - Linux user management for PAM users
- [Proxmox VE User Management](https://pve.proxmox.com/wiki/User_Management) - Official documentation
- [API Token Documentation](https://pve.proxmox.com/wiki/Proxmox_VE_API#API_Tokens) - Token details
