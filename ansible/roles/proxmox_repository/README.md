# proxmox_repository

Manages Proxmox VE and CEPH APT repository configuration.

## Description

This role configures APT repositories for Proxmox VE and CEPH, including:

- Disabling Proxmox Enterprise repositories (requires subscription)
- Enabling no-subscription repositories for community users
- Configuring CEPH repositories (Squid for PVE 9.x)
- Installing and updating Proxmox packages
- Cleaning up old kernels

## Requirements

- Proxmox VE 9.x
- Root access or sudo privileges
- Debian Bookworm (Debian 12)

## Role Variables

```yaml
# Proxmox VE version
proxmox_version: "9.0"

# Repository configuration
proxmox_enterprise_repo: false          # Disable enterprise repo (no subscription)
proxmox_no_subscription_repo: true      # Enable no-subscription repo
proxmox_test_repo: false                # Disable test repo (unstable)

# CEPH version
ceph_version: "squid"                   # CEPH Squid for PVE 9.x
ceph_repo_enabled: true                 # Enable CEPH repository

# Package management
proxmox_packages:
  - proxmox-ve
  - pve-kernel
  - postfix
  - open-iscsi

# Automatic operations
auto_update_packages: false             # Upgrade to latest versions
auto_remove_old_kernels: false          # Clean up old kernels

# APT cache
update_apt_cache: true                  # Update cache before operations
```

## Dependencies

None

## Example Playbook

```yaml
---
- name: Configure Proxmox repositories
  hosts: proxmox
  become: true

  roles:
    - role: proxmox_repository
      vars:
        proxmox_enterprise_repo: false
        auto_update_packages: true
```

## Upgrade Notes

For major version upgrades (e.g., PVE 8.x ’ 9.x):

1. Review Proxmox upgrade documentation
2. Set `auto_update_packages: true` to upgrade packages
3. Reboot after kernel updates
4. Verify cluster health after upgrade

## Testing

```bash
# Syntax check
ansible-playbook --syntax-check playbooks/configure-repositories.yml

# Check mode (dry run)
ansible-playbook playbooks/configure-repositories.yml --check --diff

# Run on single node
ansible-playbook playbooks/configure-repositories.yml --limit foxtrot
```

## License

MIT

## Author

Virgo-Core Team
