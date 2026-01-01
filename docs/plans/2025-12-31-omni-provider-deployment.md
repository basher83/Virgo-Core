# Omni Provider LXC Deployment

**Date**: 2025-12-31
**Status**: Complete
**Author**: Claude

## Request from DevOps

Deploy an LXC container for Omni Provider on the Matrix cluster with the following specs:

| Setting | Value |
|---------|-------|
| Host | Foxtrot (192.168.3.5) |
| Deployment type | LXC |
| LXC name | omni-provider |
| VMID | 200 |
| LXC IP | 192.168.3.10/24 |
| Gateway | 192.168.3.1 |
| Resources | 1 core, 1GB RAM, 4GB disk |
| Network | vmbr0 |
| OS | Ubuntu 24.04 |
| Additional | Tailscale installed and connected |

## Completed Work

### 1. New Ansible Role: `proxmox_lxc`

Created a complete role at `ansible/roles/proxmox_lxc/` with:

- State management (present/absent)
- Infisical integration for API tokens
- TUN device configuration for Tailscale
- Nesting support for containers
- SSH key injection via pubkey parameter
- Full validation and verification

Files created:
- `defaults/main.yml` - All configuration variables
- `tasks/main.yml` - Orchestration
- `tasks/validate.yml` - Input validation
- `tasks/secrets.yml` - Infisical integration
- `tasks/template.yml` - Template download
- `tasks/create.yml` - Container creation
- `tasks/destroy.yml` - Container removal
- `tasks/configure_tun.yml` - TUN device for Tailscale
- `tasks/verify.yml` - Post-creation checks
- `meta/main.yml` - Role metadata
- `README.md` - Documentation

### 2. Terraform Automation User on Matrix

Created automation user on all 3 Matrix nodes (Foxtrot, Golf, Hotel):

- Linux user: `terraform`
- SSH key configured from Infisical `/ssh/PROD_PUB_KEY`
- Sudoers configured for Proxmox commands
- Proxmox role: `TerraformUser` with full VM/LXC permissions
- Proxmox group: `terraform-users`
- Proxmox user: `terraform@pam`
- API token: `terraform@pam!automation`

### 3. Container Deployed

The omni-provider container (VMID 200) has been:

- Created on Foxtrot
- Started and running
- TUN device configured for Tailscale
- Nesting enabled

Verified via `pct list` and `pct status 200`.

### 4. Playbook Created

`ansible/playbooks/deploy-omni-provider.yml` - Two-play playbook:
1. Deploy LXC using `proxmox_lxc` role
2. Configure Tailscale using `proxmox_pct_remote` connection

### 5. Dependencies Updated

- `ansible/requirements.yml` - Updated community.proxmox to >= 1.5.0
- `ansible/.ansible-lint` - Added mock modules for community.proxmox
- Installed `paramiko` for proxmox_pct_remote connection
- Created `ansible/files/terraform_authorized_keys` with SSH key

## Remaining Work

### 1. Complete Tailscale Installation - DONE

Container connected to Tailscale:
- IP: `100.76.91.16`
- Hostname: `omni-provider.tailfb3ea.ts.net`

Note: Had to fix DNS first (was pointing at MagicDNS before Tailscale was installed).

### 2. Store Secrets in Infisical - DONE

The Matrix cluster path `/matrix` in Infisical has been configured:

| Secret Name | Status | Description |
|-------------|--------|-------------|
| `PROXMOX_API_TOKEN` | ✅ Created | terraform@pam!automation token |
| `ANSIBLE_SSH_KEYS` | ❌ Optional | SSH public key (use /ssh/PROD_PUB_KEY instead) |

### 3. Fix Recursive Template Bug - DONE

`ansible/playbooks/setup-terraform-automation.yml` had a template recursion bug at line 117.
Fixed by removing redundant role vars that shadowed play vars (role inherits them automatically).

### 4. Update README Examples - DONE

Updated `ansible/roles/proxmox_lxc/README.md`:
- Fixed features format: `["nesting=1"]` list, not `{nesting: true}` dict
- Added `proxmox_lxc_nameserver` to Network table
- Fixed Tailscale example to use correct features format

## Credentials Reference

All secrets stored in Infisical:

| Secret | Infisical Path | Description |
|--------|----------------|-------------|
| Proxmox API Token | `/matrix/PROXMOX_API_TOKEN` | `terraform@pam!automation` token |
| SSH Public Key | `/ssh/PROD_PUB_KEY` | Automation SSH key |
| Tailscale Auth Key | Generate from Tailscale admin | Reusable auth key for device registration |

## Container Status

```bash
# Check container status
ssh foxtrot "pct status 200"

# Access container
ssh foxtrot "pct exec 200 -- bash"

# Check Tailscale status (after installation)
ssh foxtrot "pct exec 200 -- tailscale status"
```

## Files Modified

```
ansible/roles/proxmox_lxc/                    # New role (entire directory)
ansible/playbooks/deploy-omni-provider.yml   # LXC + Tailscale + Docker + Compose
ansible/playbooks/setup-terraform-automation.yml  # Fixed recursion bug
ansible/files/omni-provider/README.md        # Deployment docs
ansible/files/omni-provider/compose.yml      # Compose definition
ansible/requirements.yml
ansible/.ansible-lint
ansible/files/terraform_authorized_keys
docs/plans/2025-12-31-omni-provider-deployment.md
.gitignore                                   # Added omni-provider secrets
```
