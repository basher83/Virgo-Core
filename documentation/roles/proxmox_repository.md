---
title: proxmox_repository Role
description: Manage Proxmox VE and CEPH APT repository configuration, package updates, and kernel management
---

# proxmox_repository Role

Manage Proxmox VE and CEPH APT repository configuration.

**Use Cases**: Enable community repositories, configure CEPH storage, automate package updates, clean old kernels

**Dependencies**: Proxmox VE 9.x on Debian Bookworm

**Battle-Tested**: Production deployment on Matrix cluster (3 nodes), validated CEPH Squid repositories

## Overview

The `proxmox_repository` role provides declarative repository management:

- Disable enterprise repositories (requires subscription)
- Enable no-subscription repositories for community users
- Configure CEPH release repositories (Squid for PVE 9.x)
- Install and upgrade Proxmox packages safely
- Remove old kernels automatically
- Manage APT cache efficiently

## Quick Start

Enable community repositories on Proxmox cluster:

```yaml
---
- name: Configure Proxmox repositories
  hosts: proxmox_nodes
  become: true

  roles:
    - role: proxmox_repository
      vars:
        proxmox_enterprise_repo: false
        proxmox_no_subscription_repo: true
        ceph_repo_enabled: true
```

Run:

```bash
cd ansible
uv run ansible-playbook playbooks/configure-repositories.yml
```

Expected: Enterprise repo disabled, no-subscription repo enabled, CEPH Squid repo configured

## Configuration Reference

### Proxmox Version

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `proxmox_version` | string | `"9.0"` | Proxmox VE major version |

### Repository Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `proxmox_enterprise_repo` | bool | `false` | Enable enterprise repository (requires subscription) |
| `proxmox_no_subscription_repo` | bool | `true` | Enable community repository (free) |
| `proxmox_test_repo` | bool | `false` | Enable test repository (unstable, not recommended) |

### CEPH Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ceph_version` | string | `"squid"` | CEPH release codename (Squid for PVE 9.x) |
| `ceph_repo_enabled` | bool | `true` | Enable CEPH repository |

**CEPH Version Matrix**:

- Proxmox VE 9.x: CEPH Squid (19.x)
- Proxmox VE 8.x: CEPH Reef (18.x)

### Package Management

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `proxmox_packages` | list | See below | Proxmox packages to install |
| `auto_update_packages` | bool | `false` | Upgrade to latest versions (use during upgrades) |
| `auto_remove_old_kernels` | bool | `false` | Clean up old kernels after upgrade |

**Default Packages**:

```yaml
proxmox_packages:
  - proxmox-ve
  - pve-kernel
  - postfix
  - open-iscsi
```

### APT Cache

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `update_apt_cache` | bool | `true` | Update cache before package operations |

## Common Patterns

### Community Installation

Configure repositories for subscription-free installation:

```yaml
---
- name: Setup community repositories
  hosts: proxmox_nodes
  become: true

  roles:
    - role: proxmox_repository
      vars:
        proxmox_enterprise_repo: false
        proxmox_no_subscription_repo: true
        ceph_repo_enabled: true
        auto_update_packages: false
```

### Enterprise Installation

Configure repositories with enterprise subscription:

```yaml
---
- name: Setup enterprise repositories
  hosts: proxmox_nodes
  become: true

  roles:
    - role: proxmox_repository
      vars:
        proxmox_enterprise_repo: true
        proxmox_no_subscription_repo: false
        ceph_repo_enabled: true
        auto_update_packages: false
```

### Upgrade to Latest

Upgrade Proxmox packages during maintenance:

```yaml
---
- name: Upgrade Proxmox packages
  hosts: proxmox_nodes
  become: true
  serial: 1

  roles:
    - role: proxmox_repository
      vars:
        auto_update_packages: true
        auto_remove_old_kernels: true
```

Run nodes serially to maintain cluster availability during upgrades.

### CEPH Storage Only

Configure CEPH repositories without Proxmox changes:

```yaml
---
- name: Configure CEPH repositories
  hosts: ceph_nodes
  become: true

  roles:
    - role: proxmox_repository
      vars:
        proxmox_enterprise_repo: false
        proxmox_no_subscription_repo: true
        ceph_version: "squid"
        ceph_repo_enabled: true
        auto_update_packages: false
```

## Advanced Usage

### Group Variables

Define cluster-wide repository configuration:

```yaml
# group_vars/matrix_cluster.yml
proxmox_version: "9.0"
proxmox_enterprise_repo: false
proxmox_no_subscription_repo: true
ceph_version: "squid"
ceph_repo_enabled: true
```

### Test Repositories

Enable test repositories for development clusters:

```yaml
proxmox_test_repo: true
proxmox_no_subscription_repo: true
```

**Warning**: Test repositories contain unstable packages. Do not enable in production.

### Custom Package List

Install additional packages alongside Proxmox:

```yaml
proxmox_packages:
  - proxmox-ve
  - pve-kernel
  - postfix
  - open-iscsi
  - zfsutils-linux
  - smartmontools
```

### Selective Execution

Run specific configuration tasks:

```bash
# Update cache only
uv run ansible-playbook playbooks/configure-repositories.yml --tags cache

# Configure repositories without updates
uv run ansible-playbook playbooks/configure-repositories.yml --tags repos

# Single host only
uv run ansible-playbook playbooks/configure-repositories.yml --limit foxtrot
```

## Major Version Upgrades

Follow this procedure for major version upgrades (e.g., PVE 8.x to 9.x):

### Pre-Upgrade

1. Review [Proxmox upgrade documentation](https://pve.proxmox.com/wiki/Upgrade_from_8_to_9)
2. Run pre-upgrade checker:

   ```bash
   ssh root@node pve8to9 --full
   ```

3. Backup cluster configuration:

   ```bash
   ssh root@node vzdump --compress zstd --mode snapshot
   ```

4. Verify cluster health:

   ```bash
   ssh root@node pvecm status
   ```

### Upgrade Process

1. Update playbook for new version:

   ```yaml
   ---
   - name: Upgrade to Proxmox VE 9.x
     hosts: proxmox_nodes
     become: true
     serial: 1

     roles:
       - role: proxmox_repository
         vars:
           proxmox_version: "9.0"
           ceph_version: "squid"
           auto_update_packages: true
           auto_remove_old_kernels: true
   ```

2. Run upgrade:

   ```bash
   uv run ansible-playbook playbooks/upgrade-proxmox.yml
   ```

3. Reboot after kernel updates:

   ```bash
   ssh root@node reboot
   ```

4. Verify cluster health:

   ```bash
   ssh root@node pvecm status
   ssh root@node pveversion
   ```

### Post-Upgrade

1. Update CEPH if deployed:

   ```bash
   ssh root@node ceph versions
   ```

2. Verify all services:

   ```bash
   ssh root@node systemctl status pve-cluster
   ssh root@node systemctl status pvedaemon
   ssh root@node systemctl status pveproxy
   ```

3. Check for deprecated features:

   ```bash
   ssh root@node pve8to9 --full
   ```

## Testing

Validate configuration before deployment:

```bash
# Syntax check
uv run ansible-playbook playbooks/configure-repositories.yml --syntax-check

# Dry run (check mode)
uv run ansible-playbook playbooks/configure-repositories.yml --check --diff

# Single node test
uv run ansible-playbook playbooks/configure-repositories.yml --limit foxtrot

# Full cluster deployment
uv run ansible-playbook playbooks/configure-repositories.yml
```

## Troubleshooting

### Repository Configuration Failed

**Symptom**: APT configuration changes fail

**Diagnosis**:

```bash
# Check repository files
ssh root@node ls -la /etc/apt/sources.list.d/

# Verify repository URLs
ssh root@node apt-cache policy
```

**Solutions**:

- Verify network connectivity to repository servers
- Check repository files for syntax errors
- Confirm Proxmox version matches repository configuration

### Package Update Failed

**Symptom**: `apt upgrade` fails during package update

**Diagnosis**:

```bash
# Check for held packages
ssh root@node apt-mark showhold

# Check for dependency conflicts
ssh root@node apt-get -s upgrade
```

**Solutions**:

- Review package hold list: `apt-mark unhold <package>`
- Resolve conflicts manually before automation
- Check for third-party repositories causing conflicts

### CEPH Repository Not Found

**Symptom**: CEPH packages unavailable

**Diagnosis**:

```bash
# Check CEPH repository configuration
ssh root@node cat /etc/apt/sources.list.d/ceph.list

# Test repository connectivity
ssh root@node apt-get update
```

**Solutions**:

- Verify CEPH version matches Proxmox version
- Check repository URL is correct for CEPH release
- Confirm network can reach CEPH repository servers

### Old Kernels Not Removed

**Symptom**: Old kernels remain after cleanup

**Diagnosis**:

```bash
# List installed kernels
ssh root@node dpkg -l | grep pve-kernel

# Check current kernel
ssh root@node uname -r
```

**Solutions**:

- Verify `auto_remove_old_kernels: true` is set
- Manually remove: `apt-get autoremove --purge`
- Check for pinned kernel versions

### APT Cache Errors

**Symptom**: Cache update fails with errors

**Diagnosis**:

```bash
# Update cache manually
ssh root@node apt-get update

# Check for GPG key errors
ssh root@node apt-key list
```

**Solutions**:

- Import missing GPG keys: `wget -qO - <url> | apt-key add -`
- Remove stale repository entries
- Fix repository file permissions

## Best Practices

1. **Disable enterprise repo on community installations**:

   ```yaml
   proxmox_enterprise_repo: false
   proxmox_no_subscription_repo: true
   ```

2. **Match CEPH version to Proxmox version**:

   - PVE 9.x: CEPH Squid
   - PVE 8.x: CEPH Reef

3. **Update cache before package operations**:

   ```yaml
   update_apt_cache: true
   ```

4. **Upgrade nodes serially in clusters**:

   ```yaml
   serial: 1
   ```

5. **Test on single node before cluster-wide deployment**:

   ```bash
   uv run ansible-playbook playbooks/configure-repositories.yml --limit foxtrot
   ```

6. **Clean old kernels after successful upgrades**:

   ```yaml
   auto_remove_old_kernels: true
   ```

7. **Review upgrade documentation before major versions**

## See Also

- [Proxmox VE Package Repositories](https://pve.proxmox.com/wiki/Package_Repositories) - Official repository documentation
- [Upgrade from 8.x to 9.x](https://pve.proxmox.com/wiki/Upgrade_from_8_to_9) - Major version upgrade guide
- [CEPH Releases](https://docs.ceph.com/en/latest/releases/) - CEPH version compatibility
