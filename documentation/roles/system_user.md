---
title: system_user Role
description: Manage Linux system users with SSH keys, sudo privileges, and shell configuration
---

# system_user Role

Manage Linux system users with SSH keys, sudo privileges, and shell configuration.

**Use Cases**: Create automation users, manage operator access, configure CI/CD service accounts

**Dependencies**: None (standalone role)

**Battle-Tested**: Validated on Matrix cluster (3 nodes), perfect idempotency

## Overview

The `system_user` role provides declarative user management:

- Create/remove users with specific UID/GID
- Configure SSH authorized keys (supports multiple keys per user)
- Manage sudo privileges (password/NOPASSWD)
- Set default shell and home directory
- Configure user groups and supplementary groups

## Quick Start

Create an automation user for Terraform:

```yaml
---
- name: Create Terraform automation user
  hosts: proxmox_nodes
  roles:
    - role: system_user
      system_users:
        - username: terraform
          comment: "Terraform Automation"
          shell: /bin/bash
          ssh_keys:
            - "{{ lookup('env', 'TF_SSH_KEY') }}"
          sudo: nopasswd
```

Run:

```bash
uv run ansible-playbook create-automation-user.yml
```

Expected: User `terraform` created on all nodes with SSH key and sudo access

## Configuration

### User Variables

| Variable | Required | Type | Description |
|----------|----------|------|-------------|
| `username` | Yes | string | System username (lowercase, no spaces) |
| `comment` | No | string | GECOS field (full name/description) |
| `uid` | No | int | User ID (auto-assigned if omitted) |
| `gid` | No | int | Primary group ID (matches UID if omitted) |
| `shell` | No | string | Default shell (default: `/bin/bash`) |
| `home` | No | string | Home directory (default: `/home/<username>`) |
| `ssh_keys` | No | list | SSH public keys (supports multiple) |
| `sudo` | No | string | Sudo access: `nopasswd`, `password`, or omit |
| `groups` | No | list | Supplementary groups |
| `state` | No | string | `present` or `absent` (default: `present`) |

### Example: Complete Configuration

```yaml
system_users:
  - username: deployer
    comment: "CI/CD Deploy User"
    uid: 2000
    gid: 2000
    shell: /bin/bash
    home: /home/deployer
    ssh_keys:
      - "ssh-ed25519 AAAA... ci-server@example.com"
      - "ssh-ed25519 BBBB... backup-key@example.com"
    sudo: nopasswd
    groups:
      - docker
      - libvirt
    state: present
```

## Integration Patterns

### With proxmox_access Role

Create automation user and Proxmox API token:

```yaml
---
- name: Setup Terraform automation
  hosts: proxmox_nodes
  tasks:
    - name: Create system user
      include_role:
        name: system_user
      vars:
        system_users:
          - username: terraform
            ssh_keys: ["{{ terraform_ssh_key }}"]
            sudo: nopasswd

    - name: Create Proxmox token
      include_role:
        name: proxmox_access
      vars:
        proxmox_tokens:
          - user: terraform@pam
            name: automation
            privilege_separation: true
```

### Infisical Integration

Store SSH keys in Infisical:

```yaml
vars:
  admin_ssh_key: "{{ lookup('infisical', 'ADMIN_SSH_KEY') }}"

system_users:
  - username: admin
    ssh_keys: ["{{ admin_ssh_key }}"]
```

## Troubleshooting

### SSH Key Not Working

**Symptom**: SSH authentication fails after adding key

**Diagnosis**:

```bash
# Check authorized_keys file
ssh root@node 'cat /home/username/.ssh/authorized_keys'

# Check file permissions
ssh root@node 'ls -la /home/username/.ssh/'
# Expected: .ssh/ directory 700, authorized_keys 600
```

**Solutions**:

- Verify key format (must be valid SSH public key)
- Check key not commented out
- Ensure home directory exists

### Sudo Access Not Working

**Symptom**: User cannot sudo

**Diagnosis**:

```bash
# Check sudoers file
ssh root@node 'cat /etc/sudoers.d/username'
```

**Solutions**:

- Verify `sudo: nopasswd` or `sudo: password` set
- Check sudoers syntax: `visudo -c`

## See Also

- [proxmox_access](proxmox_access.md) - Proxmox user and token management
- [Ansible User Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html)
