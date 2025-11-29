# Proxmox Tuning Roles Design

**Date**: 2025-11-28
**Status**: Approved
**Author**: Claude + basher83

## Overview

Migrate ProxMenux's proven post-install optimizations to idempotent Ansible roles, allowing
Virgo-Core to manage Proxmox tuning as infrastructure-as-code.

### Background

The target cluster currently runs ProxMenux, which provides interactive shell-based system
optimizations. This design extracts the most valuable optimizations into proper Ansible roles
that can coexist with the existing ProxMenux installation until a full migration is complete.

### Scope (Phase 1 - Essentials)

1. **Extend `proxmox_repository` role** - Add subscription banner removal with APT hook persistence
2. **New `proxmox_tuning` role** - System optimization with preset profiles:
   - Sysctl tuning (kernel panic, memory, file limits)
   - Journald optimization (size limits, compression, log levels)

### Out of Scope (Future Phases)

- Network TCP tuning
- Logrotate optimization
- System limits (PAM/ulimits)
- Security hardening (rpcbind)
- ProxMenux removal/cleanup

## Design Principles

- **Idempotent**: Safe to run repeatedly with no unintended changes
- **Profile-based**: Single variable selects a tuning profile (`minimal`, `balanced`, `aggressive`)
- **Override-friendly**: Individual values can be overridden via variables
- **Coexistent**: Works alongside existing ProxMenux installation
- **Check-mode compatible**: Full `--check` support for dry runs
- **Verified**: Includes verification tasks to confirm settings are applied

## Component 1: `proxmox_repository` Extension

### Subscription Banner Removal

Add new task file: `ansible/roles/proxmox_repository/tasks/subscription_banner.yml`

**What it does**:

1. Modifies `/usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js` to disable the nag
2. Removes the gzipped version (forces browser to use modified file)
3. Installs APT hook at `/etc/apt/apt.conf.d/85-no-subscription-nag` to reapply after updates

**New variables in `defaults/main.yml`**:

```yaml
# Subscription banner removal
remove_subscription_banner: true
```

**Integration with existing role** - Add to `tasks/main.yml`:

```yaml
- name: Remove subscription nag banner
  ansible.builtin.include_tasks: subscription_banner.yml
  when: remove_subscription_banner | bool
```

**Files created/modified by this task**:

- `/usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js` (modified)
- `/etc/apt/apt.conf.d/85-no-subscription-nag` (created)

**Idempotency approach**:

- Use `replace` module with regex to modify JS (checks before modifying)
- APT hook file uses `copy` with `content` - only writes if changed
- Handler restarts `pveproxy` service only when JS actually changes

## Component 2: `proxmox_tuning` Role

### Directory Structure

```text
ansible/roles/proxmox_tuning/
├── defaults/
│   └── main.yml              # Default values and feature toggles
├── vars/
│   └── profiles/
│       ├── minimal.yml       # Conservative settings
│       ├── balanced.yml      # ProxMenux defaults (recommended)
│       └── aggressive.yml    # Maximum optimization
├── handlers/
│   └── main.yml              # Reload sysctl, restart journald
├── meta/
│   └── main.yml              # Role metadata
├── tasks/
│   ├── main.yml              # Entry point, profile selection
│   ├── sysctl.yml            # Kernel/memory/limits tuning
│   ├── journald.yml          # Journal size/compression config
│   └── verify.yml            # Verification tasks
├── templates/
│   ├── 99-proxmox-tuning.conf.j2   # Sysctl drop-in
│   └── journald.conf.j2            # Journald config
└── README.md                 # Documentation
```

### Task Flow

`tasks/main.yml`:

```yaml
---
- name: Load tuning profile
  ansible.builtin.include_vars:
    file: "profiles/{{ proxmox_tuning_profile }}.yml"
  when: proxmox_tuning_profile != 'custom'

- name: Apply sysctl tuning
  ansible.builtin.include_tasks: sysctl.yml
  when: proxmox_tuning_sysctl_enabled | bool

- name: Apply journald optimization
  ansible.builtin.include_tasks: journald.yml
  when: proxmox_tuning_journald_enabled | bool

- name: Verify applied settings
  ansible.builtin.include_tasks: verify.yml
  when: proxmox_tuning_verify | default(true) | bool
```

### Profile Definitions

#### Profile: `balanced` (default, matches ProxMenux)

```yaml
# Sysctl - Kernel behavior
sysctl_kernel_panic: 10              # Reboot 10s after panic
sysctl_kernel_panic_on_oops: 1       # Treat oops as panic

# Sysctl - Memory management
sysctl_vm_swappiness: 10             # Prefer RAM over swap
sysctl_vm_dirty_ratio: 15            # % RAM for dirty pages
sysctl_vm_dirty_background_ratio: 5  # Background flush threshold
sysctl_vm_max_map_count: 65530       # Memory mappings (containers)

# Sysctl - File limits
sysctl_fs_inotify_max_user_watches: 1048576
sysctl_fs_inotify_max_user_instances: 1048576
sysctl_fs_file_max: 9223372036854775807

# Journald
journald_system_max_use: "64M"
journald_runtime_max_use: "60M"
journald_max_level_store: "warning"
journald_compress: "yes"
journald_forward_to_syslog: "no"
```

#### Profile: `minimal` (conservative)

- Same kernel panic settings (safety critical)
- `swappiness: 30` (less aggressive)
- `journald_system_max_use: "128M"` (more log retention)
- Lower inotify limits (256k)

#### Profile: `aggressive` (maximum optimization)

- `swappiness: 1` (almost never swap)
- `journald_system_max_use: "32M"` (minimal logs)
- Maximum inotify limits (2M)

### Implementation Details

#### Sysctl Tasks (`tasks/sysctl.yml`)

```yaml
---
- name: Deploy sysctl tuning configuration
  ansible.builtin.template:
    src: 99-proxmox-tuning.conf.j2
    dest: /etc/sysctl.d/99-proxmox-tuning.conf
    owner: root
    group: root
    mode: '0644'
  notify: Reload sysctl

- name: Ensure core dump directory exists
  ansible.builtin.file:
    path: /var/crash
    state: directory
    mode: '0755'
  when: sysctl_kernel_panic | int > 0
```

#### Journald Tasks (`tasks/journald.yml`)

```yaml
---
- name: Deploy optimized journald configuration
  ansible.builtin.template:
    src: journald.conf.j2
    dest: /etc/systemd/journald.conf
    owner: root
    group: root
    mode: '0644'
  notify: Restart journald

- name: Vacuum existing journal to new size limit
  ansible.builtin.command:
    cmd: journalctl --vacuum-size={{ journald_system_max_use }}
  changed_when: false
  when: not ansible_check_mode
```

#### Handlers (`handlers/main.yml`)

```yaml
---
- name: Reload sysctl
  ansible.builtin.command: sysctl --system
  changed_when: true
  listen: "reload sysctl settings"

- name: Restart journald
  ansible.builtin.systemd:
    name: systemd-journald
    state: restarted
```

#### Verification Tasks (`tasks/verify.yml`)

```yaml
---
- name: Verify sysctl settings applied
  when:
    - not ansible_check_mode
    - proxmox_tuning_sysctl_enabled | bool
  block:
    - name: Check vm.swappiness value
      ansible.builtin.command: sysctl -n vm.swappiness
      register: verify_swappiness
      changed_when: false
      failed_when: verify_swappiness.stdout | int != sysctl_vm_swappiness

    - name: Check kernel.panic value
      ansible.builtin.command: sysctl -n kernel.panic
      register: verify_panic
      changed_when: false
      failed_when: verify_panic.stdout | int != sysctl_kernel_panic

- name: Verify journald configuration
  when:
    - not ansible_check_mode
    - proxmox_tuning_journald_enabled | bool
  block:
    - name: Check journald is running
      ansible.builtin.systemd:
        name: systemd-journald
        state: started
      check_mode: true
      register: journald_status
      failed_when: journald_status.status.ActiveState != "active"
```

### Role Metadata (`meta/main.yml`)

```yaml
---
galaxy_info:
  role_name: proxmox_tuning
  namespace: virgo_core
  author: basher83
  description: >-
    System tuning for Proxmox VE nodes including kernel parameters,
    memory optimization, and journald configuration.
  license: MIT
  min_ansible_version: "2.14"
  platforms:
    - name: Debian
      versions:
        - bookworm
        - bullseye
  galaxy_tags:
    - proxmox
    - tuning
    - sysctl
    - performance

dependencies: []
```

### Default Variables (`defaults/main.yml`)

```yaml
---
# Profile selection: minimal, balanced, aggressive, or custom
proxmox_tuning_profile: balanced

# Feature toggles
proxmox_tuning_sysctl_enabled: true
proxmox_tuning_journald_enabled: true
proxmox_tuning_verify: true

# Override individual values (takes precedence over profile)
# sysctl_vm_swappiness: 10
# journald_system_max_use: "64M"
```

## Playbook Integration

### Option A: Add to Existing Cluster Init

Extend `playbooks/initialize-matrix-cluster.yml`:

```yaml
- name: Apply Proxmox tuning
  hosts: matrix_cluster
  become: true
  roles:
    - role: proxmox_repository
      vars:
        remove_subscription_banner: true
    - role: proxmox_tuning
      vars:
        proxmox_tuning_profile: balanced
```

### Option B: Standalone Playbook

Create `playbooks/tune-cluster.yml`:

```yaml
---
- name: Apply Proxmox system tuning
  hosts: proxmox_clusters
  become: true

  roles:
    - role: proxmox_repository
      vars:
        remove_subscription_banner: true

    - role: proxmox_tuning
      vars:
        proxmox_tuning_profile: balanced
```

Usage:

```bash
# Check mode first
uv run ansible-playbook playbooks/tune-cluster.yml --check --diff

# Apply
uv run ansible-playbook playbooks/tune-cluster.yml
```

## Testing Strategy

1. **Check mode validation**: Run with `--check --diff` to preview changes
2. **Idempotency test**: Run twice, second run should report zero changes
3. **Integration with `test-roles.yml`**: Add both roles to existing test framework
4. **Verification tasks**: Built-in verification confirms settings are applied

### Test Commands

```bash
# Lint the new role
mise run ansible-lint

# Test in check mode
TAGS=proxmox_tuning CHECK=1 mise run ansible:test-roles

# Full idempotency test
mise run ansible:test-roles  # Run twice, compare output
```

## Migration Path

1. **Phase 1 (this design)**: Deploy Ansible roles alongside ProxMenux
2. **Phase 2**: Validate settings match between both systems
3. **Phase 3**: Disable ProxMenux optimizations, rely solely on Ansible
4. **Phase 4**: Remove ProxMenux from cluster

## Future Enhancements (Phase 2+)

After Phase 1 is stable, consider adding:

- Network TCP tuning (`/etc/sysctl.d/99-network.conf`)
- Logrotate optimization (`/etc/logrotate.conf`)
- System limits (PAM/ulimits in `/etc/security/limits.d/`)
- Security hardening (disable rpcbind, SSH tuning)
- Log2RAM for SSD protection (conditional on disk type)

## References

- [ProxMenux Repository](https://github.com/MacRimi/ProxMenux)
- [ProxMenux auto_post_install.sh](https://github.com/MacRimi/ProxMenux/blob/main/scripts/auto_post_install.sh)
- Virgo-Core ansible-best-practices skill
