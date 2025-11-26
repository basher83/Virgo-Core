---
title: Installation
description: Set up your development environment with mise, uv, Ansible, OpenTofu, and Infisical for Virgo-Core
---

# Installation

Set up your development environment to deploy and manage Virgo-Core infrastructure.

**Time Required**: 15-20 minutes

**Prerequisites**: Complete [Prerequisites](prerequisites.md) checklist

## Overview

This guide installs:

- **mise** - Tool version manager and task runner
- **uv** - Fast Python package manager
- **Ansible** - Infrastructure automation
- **OpenTofu** - Infrastructure as Code
- **Infisical CLI** - Secrets management

## Installation Steps

## Step 1: Clone Repository

Clone the Virgo-Core repository:

```bash
cd ~/dev/infra-as-code
git clone https://github.com/basher83/Virgo-Core.git
cd Virgo-Core
```

**Verify**:

```bash
ls -la
# Expected: See .mise.toml, ansible/, terraform/, etc.
```

## Step 2: Install mise

Install mise (tool version manager):

```bash
curl https://mise.run | sh
```

Add to shell profile:

```bash
# For bash
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc
source ~/.zshrc
```

**Verify**:

```bash
mise --version
# Expected: 2024.x.x or higher
```

## Step 3: Install Dependencies

Run mise setup to install all dependencies:

```bash
mise run setup
```

This installs:

- uv (Python package manager)
- Python 3.13+
- Ansible and collections
- OpenTofu
- All Python dependencies

**Expected Output**:

```text
✓ mise Installing mise tools...
✓ uv Installing Python packages...
✓ ansible-galaxy Installing Ansible collections...
Setup complete!
```

**Verify**:

```bash
# Check uv
uv --version
# Expected: 0.x.x

# Check Python
python3 --version
# Expected: 3.13.x

# Check Ansible
ansible --version
# Expected: 2.x.x

# Check OpenTofu
tofu --version
# Expected: 1.10.x
```

## Step 4: Configure Infisical

Authenticate with Infisical:

```bash
infisical login
```

Follow browser authentication flow.

**Set Infisical project**:

Edit `.infisical.json` with your project ID:

```json
{
  "workspaceId": "your-workspace-id",
  "defaultEnvironment": "prod"
}
```

**Verify**:

```bash
infisical secrets
# Expected: See secrets list (configured in Infisical dashboard)
```

## Step 5: Configure SSH Access

Generate SSH key if needed:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

Add SSH key to Proxmox nodes:

```bash
ssh-copy-id root@192.168.3.11
ssh-copy-id root@192.168.3.12
ssh-copy-id root@192.168.3.13
```

**Verify**:

```bash
ssh root@192.168.3.11 'hostname'
# Expected: Node hostname (no password prompt)
```

## Installation Complete

Verify all tools installed:

```bash
mise doctor
# Expected: All tools available

mise list
# Expected: Show installed tools and versions
```

**Next Step:** [First Deployment](first-deployment.md)

## Troubleshooting

### mise Installation Fails

**Symptom**: `curl https://mise.run | sh` returns error

**Solutions**:

- Check internet connectivity
- Verify curl installed: `curl --version`
- Try manual install from <https://mise.jdx.dev/installing-mise.html>

### Dependencies Installation Fails

**Symptom**: `mise run setup` fails

**Solutions**:

- Check Python version: `python3 --version` (need 3.13+)
- Clear mise cache: `rm -rf ~/.local/share/mise`
- Run with verbose: `mise run setup --verbose`

### Infisical Login Fails

**Symptom**: Browser auth fails or times out

**Solutions**:

- Check Infisical service status: <https://status.infisical.com>
- Clear Infisical cache: `rm -rf ~/.config/infisical`
- Try CLI token auth: `infisical login --token`
