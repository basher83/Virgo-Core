# Ansible Role: system_user

Manage Linux system users with SSH keys and sudo privileges in a declarative, idempotent manner.

## Features

- ✅ Create and manage multiple system users
- ✅ Configure SSH authorized keys
- ✅ Flexible sudo configuration (full access or specific commands)
- ✅ Remove users when no longer needed
- ✅ Idempotent - safe to run multiple times
- ✅ Validated sudoers files (prevents lockout)
- ✅ Follows Ansible best practices

## Requirements

- Ansible >= 2.10
- Target systems: Ubuntu 20.04+, Debian 10+
- Root or sudo access on target hosts

## Role Variables

### Main Variable

**`system_users`** (list, default: `[]`)

List of users to manage. Each user is a dictionary with the following keys:

| Key | Required | Type | Default | Description |
|-----|----------|------|---------|-------------|
| `name` | Yes | string | - | Username to create/manage |
| `state` | No | string | `present` | User state: `present` or `absent` |
| `comment` | No | string | `""` | User's GECOS field (full name/description) |
| `shell` | No | string | `/bin/bash` | User's default shell |
| `groups` | No | list | `[]` | Additional groups for the user |
| `create_home` | No | boolean | `true` | Create home directory |
| `ssh_keys` | No | list | `[]` | List of SSH public keys |
| `sudo_nopasswd` | No | boolean | `false` | Grant full sudo without password |
| `sudo_rules` | No | list | `[]` | Specific sudo commands allowed |

**Note:** If both `sudo_nopasswd` and `sudo_rules` are defined, `sudo_nopasswd` takes precedence.

## Example Playbooks

### Example 1: Create Admin User

```yaml
---
- name: Create Administrative User
  hosts: all
  become: true

  roles:
    - role: system_user
      vars:
        system_users:
          - name: admin
            comment: "System Administrator"
            shell: /bin/bash
            groups: [sudo]
            ssh_keys:
              - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC... admin@workstation"
            sudo_nopasswd: true
```

### Example 2: Create Service User with Limited Sudo

```yaml
---
- name: Create Terraform Automation User
  hosts: proxmox_cluster
  become: true

  roles:
    - role: system_user
      vars:
        system_users:
          - name: terraform
            comment: "Terraform automation user"
            shell: /bin/bash
            ssh_keys:
              - "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGvT... terraform@controller"
            sudo_rules:
              - "/sbin/pvesm"
              - "/sbin/qm"
              - "/usr/bin/tee /var/lib/vz/*"
```

### Example 3: Manage Multiple Users

```yaml
---
- name: Setup Development Team Users
  hosts: dev_servers
  become: true

  roles:
    - role: system_user
      vars:
        system_users:
          - name: alice
            comment: "Alice Developer"
            groups: [docker, developers]
            ssh_keys:
              - "ssh-rsa AAAAB3... alice@laptop"
            sudo_nopasswd: false

          - name: bob
            comment: "Bob DevOps"
            groups: [docker, sudo]
            ssh_keys:
              - "ssh-ed25519 AAAAC3... bob@workstation"
            sudo_nopasswd: true

          - name: olddev
            state: absent  # Remove this user
```

### Example 4: No Sudo Access

```yaml
---
- name: Create Regular User
  hosts: servers
  become: true

  roles:
    - role: system_user
      vars:
        system_users:
          - name: appuser
            comment: "Application Service Account"
            shell: /bin/sh
            create_home: true
            ssh_keys:
              - "ssh-ed25519 AAAAC3... deploy@ci-server"
            # No sudo_* variables = no sudo access
```

## Usage

### Via Playbook

```bash
# Run playbook
cd ansible
uv run ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml

# Check mode (dry run)
uv run ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml --check --diff

# Limit to specific hosts
uv run ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml --limit foxtrot
```

### Via Command Line Variables

```bash
uv run ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml \
  -e "admin_name=newuser" \
  -e "admin_ssh_key='ssh-rsa AAAAB3...'"
```

## Verification

After running the role, verify the configuration:

```bash
# Test SSH access
ssh username@hostname

# Test sudo access
ssh username@hostname sudo id

# Verify sudo configuration
ssh root@hostname sudo -l -U username
```

## Idempotency

This role is fully idempotent:

- Running it multiple times with the same configuration produces no changes
- User accounts are created only if they don't exist
- SSH keys are only added if not already present
- Sudoers files are only updated if configuration changes

```bash
# First run - creates user
uv run ansible-playbook playbook.yml
# CHANGED: 1

# Second run - no changes
uv run ansible-playbook playbook.yml
# CHANGED: 0
```

## Security Considerations

1. **SSH Keys**: Always use SSH key authentication, not passwords
2. **Sudo Access**: Grant minimal privileges needed (prefer `sudo_rules` over `sudo_nopasswd`)
3. **Sudoers Validation**: All sudoers files are validated with `visudo -cf` before installation
4. **File Permissions**: SSH directories (0700) and authorized_keys (0600) have secure permissions
5. **Idempotent Operations**: Safe to run repeatedly without side effects

## Testing

### Syntax Check

```bash
cd ansible
uv run ansible-playbook --syntax-check playbooks/create-admin-user.yml
```

### Lint Check

```bash
mise run ansible-lint
```

### Dry Run

```bash
uv run ansible-playbook -i inventory/proxmox.yml playbooks/create-admin-user.yml \
  --check --diff --limit testhost
```

## Troubleshooting

### User Already Exists

If the user already exists, the role will update their configuration (groups, shell, SSH keys, sudo) to match the desired state.

### SSH Key Not Working

1. Check key is correctly formatted (no line breaks within key)
2. Verify `~/.ssh` directory permissions (0700)
3. Verify `~/.ssh/authorized_keys` permissions (0600)
4. Check SSH daemon configuration on target host

### Sudo Not Working

1. Verify sudoers file was created: `ls -la /etc/sudoers.d/username`
2. Check sudoers file syntax: `sudo visudo -cf /etc/sudoers.d/username`
3. Test sudo: `sudo -l -U username`

### Sudoers Validation Failed

If visudo validation fails, the role will not install the broken sudoers file. Check:

1. Command paths are absolute (e.g., `/sbin/pvesm` not `pvesm`)
2. Syntax is correct in `sudo_rules`
3. No invalid characters or formatting

## Dependencies

This role has no dependencies on other roles.

## License

MIT

## Author Information

Created as part of the Virgo-Core infrastructure automation project (Phase 1: Ansible Migration to Role-Based Architecture).

## Related Documentation

- [Ansible Migration Plan](../../../docs/ansible-migration-plan.md)
- [Ansible Best Practices Skill](.claude/skills/ansible-best-practices/)
- [Repository CLAUDE.md](../../../CLAUDE.md)
