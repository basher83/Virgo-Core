# ProxMenux Integration Research

Source: [MacRimi/ProxMenux](https://github.com/MacRimi/ProxMenux)

This document tracks features from ProxMenux that have been integrated into Virgo-Core
Ansible roles, and features under consideration for future integration.

## Integration Status

### Implemented

| Feature | Source Script | Virgo-Core Role | Notes |
|---------|---------------|-----------------|-------|
| Subscription banner removal | `customizable_post_install.sh` | `proxmox_repository` | APT hook for persistence across updates |
| Journald optimization | `customizable_post_install.sh` | `proxmox_tuning` | 64M limit, compression, warning-level |
| Sysctl kernel tuning | `customizable_post_install.sh` | `proxmox_tuning` | Panic, swappiness, inotify, file limits |
| System upgrade | `global/update-pve9_2.sh` | `system-upgrade.yml` | CEPH-aware rolling upgrade |
| TCP BBR | `customizable_post_install.sh` | `proxmox_tuning` | Google BBR congestion control via sysctl |
| pigz | `customizable_post_install.sh` | `proxmox_repository` | Parallel gzip for faster vzdump backups |
| KSM tuning | `customizable_post_install.sh` | `proxmox_tuning` | Memory deduplication with profile-based settings |
| kexec | `customizable_post_install.sh` | `proxmox_tuning` | Fast reboot via `reboot-quick` script |

### High Priority - To Consider

| Feature | Description | Complexity | Value |
|---------|-------------|------------|-------|
| **IOMMU/VFIO** | PCI passthrough configuration. Detects Intel/AMD, configures GRUB/systemd-boot, loads VFIO modules, blacklists GPU drivers. | High | High |
| **ZFS ARC optimization** | Tunes ZFS ARC cache size based on available RAM. Useful for ZFS-based storage. | Low | Medium |

### Medium Priority - To Consider

| Feature | Description | Complexity | Value |
|---------|-------------|------------|-------|
| **haveged** | Entropy generation daemon. Prevents slowdowns in cryptographic operations. | Low | Medium |
| **AMD CPU fixes** | Adds `idle=nomwait` kernel parameter and KVM MSR options for AMD EPYC/Ryzen stability. | Medium | Medium |
| **Network optimization** | Additional TCP/IP sysctl tuning (buffers, queues, security hardening). | Low | Medium |
| **System utilities** | Package installation for htop, btop, iftop, iotop, tmux, etc. | Low | Low |
| **OpenVSwitch** | Virtual switching for advanced network configurations. | Medium | Low |

### Low Priority - To Consider

| Feature | Description | Complexity | Value |
|---------|-------------|------------|-------|
| **APT skip languages** | Configure APT to skip downloading translation files. Minor disk/bandwidth savings. | Low | Low |
| **Force APT IPv4** | Force APT to use IPv4 only. Useful for networks with IPv6 issues. | Low | Low |
| **Time sync** | Auto-detect timezone from IP and enable NTP. Most systems already configured. | Low | Low |
| **Bashrc customization** | Custom PS1 prompt, aliases, history format. Personal preference. | Low | Low |
| **Lynis** | Security audit tool. Useful but not automated. | Low | Low |
| **Guest agent** | Detect virtualization and install guest agent. Only relevant for nested virtualization. | Low | Low |

### Not Applicable

| Feature | Reason |
|---------|--------|
| Fail2Ban | Nodes not internet-exposed; known issues with Ansible (rapid SSH connections trigger bans, control host lockout). Risk outweighs benefit for internal-only infrastructure. |
| Ceph installation | Already handled by `proxmox_ceph` role with proper cluster awareness |
| ZFS auto-snapshot | Site-specific; would need flexible configuration |
| Kernel headers | Usually installed as-needed for specific drivers |
| Disable RPC/portmapper | May break NFS; needs careful consideration |

## Implementation Notes

### IOMMU/VFIO

Complex feature with multiple components:
1. Detect CPU vendor (Intel/AMD)
2. Add kernel parameters (`intel_iommu=on` or `amd_iommu=on`, `iommu=pt`)
3. Handle both GRUB and systemd-boot (ZFS) configurations
4. Load VFIO modules
5. Blacklist conflicting GPU drivers
6. Update initramfs

Should be optional and well-documented due to potential for breaking systems.

## Proposed Role Structure

For new features, consider:

1. **Extend `proxmox_tuning`** for:
   - ~~TCP BBR congestion control~~ ✓ Implemented
   - Network optimization (TCP/IP tuning)
   - ~~KSM tuning (memory deduplication)~~ ✓ Implemented
   - ZFS ARC optimization (if ZFS detected)

2. **Extend `proxmox_repository`** for:
   - ~~pigz installation and configuration (faster backups)~~ ✓ Implemented
   - APT optimizations (skip languages, force IPv4)

3. **New role `proxmox_passthrough`** for:
   - IOMMU/VFIO configuration
   - GPU driver blacklisting
   - Kernel parameter management (GRUB/systemd-boot)

## References

- [ProxMenux GitHub](https://github.com/MacRimi/ProxMenux)
- [ProxMenux customizable_post_install.sh](https://github.com/MacRimi/ProxMenux/blob/main/scripts/post_install/customizable_post_install.sh)
- [xshok-proxmox](https://github.com/extremeshok/xshok-proxmox) - Original inspiration for some ProxMenux features
- [Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE) - Community scripts project
