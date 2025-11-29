# proxmox_tuning

System tuning for Proxmox VE nodes including kernel parameters, memory optimization,
and journald configuration.

## Overview

This role applies proven system optimizations based on [ProxMenux](https://github.com/MacRimi/ProxMenux)
post-install settings. It provides three preset profiles for different use cases:

- **minimal**: Conservative settings, safe for any system
- **balanced**: Recommended for most Proxmox deployments (default)
- **aggressive**: Maximum optimization for dedicated hosts

## Requirements

- Proxmox VE 7.x or 8.x (Debian Bullseye or Bookworm)
- Ansible 2.14+

## Role Variables

### Profile Selection

```yaml
# Choose a profile: minimal, balanced, aggressive, or custom
proxmox_tuning_profile: balanced
```

### Feature Toggles

```yaml
proxmox_tuning_sysctl_enabled: true    # Apply sysctl tuning
proxmox_tuning_journald_enabled: true  # Apply journald optimization
proxmox_tuning_bbr_enabled: true       # Enable TCP BBR congestion control
proxmox_tuning_ksm_enabled: true       # Enable KSM memory deduplication
proxmox_tuning_verify: true            # Run verification tasks
```

### Overriding Individual Values

You can override any value from the profile:

```yaml
proxmox_tuning_profile: balanced
sysctl_vm_swappiness: 5  # Override just this value
```

### All Available Variables

#### Sysctl - Kernel Behavior

| Variable | Default (balanced) | Description |
|----------|-------------------|-------------|
| `sysctl_kernel_panic` | `10` | Seconds before reboot after panic |
| `sysctl_kernel_panic_on_oops` | `1` | Treat kernel oops as panic |

#### Sysctl - Memory Management

| Variable | Default (balanced) | Description |
|----------|-------------------|-------------|
| `sysctl_vm_swappiness` | `10` | Preference for swapping (0-100) |
| `sysctl_vm_dirty_ratio` | `15` | Max % of RAM for dirty pages |
| `sysctl_vm_dirty_background_ratio` | `5` | % of RAM before background flush |
| `sysctl_vm_max_map_count` | `65530` | Max memory mappings per process |

#### Sysctl - File Limits

| Variable | Default (balanced) | Description |
|----------|-------------------|-------------|
| `sysctl_fs_inotify_max_user_watches` | `1048576` | Max inotify watches per user |
| `sysctl_fs_inotify_max_user_instances` | `1048576` | Max inotify instances per user |
| `sysctl_fs_file_max` | `9223372036854775807` | Max open files system-wide |

#### Journald Settings

| Variable | Default (balanced) | Description |
|----------|-------------------|-------------|
| `journald_system_max_use` | `64M` | Max persistent journal size |
| `journald_runtime_max_use` | `60M` | Max runtime journal size |
| `journald_max_level_store` | `warning` | Minimum level to store |
| `journald_compress` | `yes` | Enable journal compression |
| `journald_forward_to_syslog` | `no` | Forward to syslog |

#### KSM (Kernel Samepage Merging)

| Variable | Default (balanced) | Description |
|----------|-------------------|-------------|
| `ksm_pages_to_scan` | `100` | Pages to scan per sleep interval |
| `ksm_sleep_millisecs` | `20` | Milliseconds between scan batches |

## Dependencies

None.

## Example Playbook

### Basic Usage

```yaml
- hosts: proxmox_clusters
  become: true
  roles:
    - role: proxmox_tuning
```

### With Custom Profile

```yaml
- hosts: proxmox_clusters
  become: true
  roles:
    - role: proxmox_tuning
      vars:
        proxmox_tuning_profile: aggressive
```

### With Overrides

```yaml
- hosts: proxmox_clusters
  become: true
  roles:
    - role: proxmox_tuning
      vars:
        proxmox_tuning_profile: balanced
        sysctl_vm_swappiness: 5
        journald_system_max_use: "128M"
```

### Disable Specific Features

```yaml
- hosts: proxmox_clusters
  become: true
  roles:
    - role: proxmox_tuning
      vars:
        proxmox_tuning_sysctl_enabled: true
        proxmox_tuning_journald_enabled: false  # Skip journald
```

## Profile Comparison

| Setting | minimal | balanced | aggressive |
|---------|---------|----------|------------|
| `vm.swappiness` | 30 | 10 | 1 |
| `vm.dirty_ratio` | 20 | 15 | 10 |
| `journald_system_max_use` | 128M | 64M | 32M |
| `journald_max_level_store` | info | warning | warning |
| `inotify_max_user_watches` | 256K | 1M | 2M |
| `ksm_pages_to_scan` | 50 | 100 | 200 |
| `ksm_sleep_millisecs` | 50 | 20 | 10 |

## Files Modified

This role creates or modifies the following files:

- `/etc/sysctl.d/99-proxmox-tuning.conf` - Sysctl settings (including TCP BBR)
- `/etc/systemd/journald.conf` - Journald configuration
- `/etc/ksmtuned.conf` - KSM tuning daemon configuration
- `/var/crash/` - Core dump directory (created if kernel panic enabled)

## Verification

The role includes verification tasks that run after applying settings (unless
`proxmox_tuning_verify: false`). These confirm that:

- Sysctl values are actually applied
- TCP BBR congestion control is active
- Journald service is running
- KSM tuning service is running and KSM is enabled

## License

MIT

## Author

basher83 - Virgo-Core project
