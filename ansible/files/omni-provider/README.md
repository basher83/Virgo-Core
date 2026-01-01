# Omni Provider Files

Configuration files for Sidero Omni Proxmox infrastructure provider.

## Deployment

Deployed to LXC container `omni-provider` (VMID 200) on Foxtrot via:

```bash
uv run ansible-playbook -i inventory/hosts.yml playbooks/deploy-omni-provider.yml --tags docker,compose
```

Files are copied to `/opt/omni-provider/` in the container.

## Files

| File | Purpose | Contains Secrets |
|------|---------|------------------|
| `compose.yml` | Docker Compose definition | No |
| `config.yaml` | Proxmox API connection config | Yes (API token) |
| `.env` | Omni service account key | Yes (PGP key) |

## Container Details

- **Host**: Foxtrot (192.168.3.5)
- **VMID**: 200
- **IP**: 192.168.3.10/24
- **Tailscale**: 100.76.91.16 / omni-provider.tailfb3ea.ts.net
- **App Directory**: /opt/omni-provider

## Secrets

Secret files are gitignored. To deploy, you need local copies with valid credentials.

Required secrets:

- `config.yaml`: Proxmox API token (`terraform@pam!automation`)
- `.env`: `OMNI_INFRA_PROVIDER_KEY` from Omni dashboard

## TODO

- [ ] Template `config.yaml` to pull Proxmox token from Infisical `/matrix/PROXMOX_API_TOKEN`
- [ ] Store Omni service account key in Infisical `/matrix/OMNI_INFRA_PROVIDER_KEY`
- [ ] Update playbook to render templates instead of copying static files
