# Documentation Enhancement Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform Virgo-Core Mintlify site from landing page with broken links to comprehensive getting-started through advanced reference documentation.

**Architecture:** Three-phase implementation: (1) Fix docs.json paths to expose existing docs, (2) Create getting-started tutorials, (3) Enhance role documentation with visuals and integration examples. Preserves existing subdirectory structure.

**Tech Stack:** Mintlify (documentation platform), Markdown/MDX, Elements of Style principles

---

## Phase 1: Foundation Fix (2-4 hours)

### Task 1: Update docs.json Navigation Paths

**Files:**

- Modify: `docs.json:15-46`
- Test: Manual verification on live site

**Step 1: Read current docs.json**

```bash
cat docs.json
```

Expected: See navigation with paths like `documentation/goals`

**Step 2: Update Getting Started paths**

Edit `docs.json` at lines 22-26:

```json
{
  "group": "Getting Started",
  "pages": [
    "index",
    "documentation/core/goals",
    "documentation/core/infrastructure"
  ]
}
```

**Step 3: Update Ansible Architecture paths**

Edit `docs.json` at lines 28-36 (remove archived docs):

```json
{
  "group": "Ansible Architecture",
  "pages": [
    "documentation/design/ansible-philosophy",
    "documentation/design/ansible-role-design",
    "documentation/design/ansible-playbook-design"
  ]
}
```

**Step 4: Update Integration & Testing paths**

Edit `docs.json` at lines 38-44 (remove archived docs):

```json
{
  "group": "Integration & Testing",
  "pages": [
    "documentation/core/netbox-powerdns",
    "documentation/core/references"
  ]
}
```

**Step 5: Verify JSON syntax**

```bash
python3 -c "import json; json.load(open('docs.json'))"
```

Expected: No output (valid JSON)

**Step 6: Commit docs.json changes**

```bash
git add docs.json
git commit -m "fix(docs): Update navigation paths to match subdirectory structure

- Fix Getting Started paths (core/ subdirectory)
- Fix Ansible Architecture paths (design/ subdirectory)
- Fix Integration paths (core/ subdirectory)
- Remove archived document references

Fixes all 404 errors by matching actual file locations"
```

### Task 2: Extract Insights from Archived Docs

**Files:**

- Read: `documentation/archive/2025-11-v1.0/testing-validation-results.md`
- Read: `documentation/archive/2025-11-v1.0/ansible-migration-completion.md`
- Modify: `documentation/design/ansible-philosophy.md` (add metrics)

**Step 1: Extract testing metrics**

Read `documentation/archive/2025-11-v1.0/testing-validation-results.md`, note:

- Total bugs found and fixed: 15
- Idempotency validation: Perfect across 3 nodes
- Test coverage metrics

**Step 2: Extract migration insights**

Read `documentation/archive/2025-11-v1.0/ansible-migration-completion.md`, note:

- 6-phase migration approach proven effective
- Key lessons learned
- Success metrics

**Step 3: Add battle-tested callout to ansible-philosophy.md**

Add after the introduction section (around line 20):

```markdown
> **Battle-Tested:** This architecture proved itself during v1.0.0 development.
> Comprehensive testing discovered and fixed 15 bugs, achieving perfect idempotency
> across the 3-node Matrix cluster. The 6-phase migration approach completed
> successfully with zero regressions.
```

**Step 4: Commit insight extraction**

```bash
git add documentation/design/ansible-philosophy.md
git commit -m "docs: Add battle-tested metrics to ansible-philosophy

Extract validation results from archived testing documentation:
- 15 bugs found and fixed during comprehensive testing
- Perfect idempotency validated on 3-node Matrix cluster
- Proven 6-phase migration approach"
```

### Task 3: Update index.mdx Links

**Files:**

- Modify: `index.mdx:40-50` (Quick Links section)

**Step 1: Read current index.mdx**

```bash
grep -A 10 "Quick Links" index.mdx
```

Expected: See links to archived docs (testing-validation-results, ansible-migration-completion)

**Step 2: Replace Quick Links section**

Replace the Quick Links section with:

```mdx
## Quick Links

[**Ansible Architecture**
Learn about the role-based automation design](documentation/ansible-philosophy)

[**Infrastructure Roadmap**
See planned features and development timeline](documentation/brainstorming/next-features-2025-11)

[**GitHub Repository**
View the source code and releases](https://github.com/basher83/Virgo-Core)
```

**Step 3: Commit index.mdx updates**

```bash
git add index.mdx
git commit -m "docs: Update homepage Quick Links section

- Remove links to archived documents
- Add link to ansible-philosophy (active design doc)
- Add link to roadmap (next-features-2025-11)
- Keep GitHub repository link"
```

### Task 4: Verify Phase 1 Complete

**Step 1: Check git status**

```bash
git status
```

Expected: Clean working tree, 3 commits ahead

**Step 2: Review commit log**

```bash
git log --oneline -3
```

Expected: Three commits for docs.json, insights, and index.mdx

**Step 3: Push to remote (optional)**

```bash
git push origin main
```

**Step 4: Test on live Mintlify site**

Visit <https://themothership.mintlify.app/> and verify:

- All navigation links work (no 404s)
- 7 reference docs accessible
- Homepage Quick Links updated

---

## Phase 2: Getting Started Content (6-10 hours)

### Task 5: Create Directory Structure

**Files:**

- Create: `documentation/getting-started/` (directory)

**Step 1: Create getting-started directory**

```bash
mkdir -p documentation/getting-started
```

**Step 2: Verify directory created**

```bash
ls -la documentation/
```

Expected: See `getting-started/` directory

**Step 3: Commit directory structure**

```bash
git add documentation/getting-started/
git commit --allow-empty -m "docs: Create getting-started directory structure

Prepare for Phase 2 tutorial content"
```

### Task 6: Write prerequisites.md

**Files:**

- Create: `documentation/getting-started/prerequisites.md`

**Step 1: Create prerequisites.md with header**

```markdown
# Prerequisites

Complete this checklist before deploying Virgo-Core to ensure you have the required hardware, network, and software.

## Hardware Requirements
```

**Step 2: Add hardware checklist section**

```markdown
## Hardware Requirements

Verify you have 3+ identical nodes meeting these specifications:

- [ ] **CPU**: 8+ cores (16 cores recommended for CEPH)
- [ ] **RAM**: 32GB+ (64GB recommended for production)
- [ ] **Storage**:
  - 1x boot drive (SSD, 120GB+)
  - 2x NVMe drives for CEPH OSDs (500GB+ each)
- [ ] **Network**:
  - 1x 1GbE+ management interface
  - 2x 10GbE interfaces for CEPH storage networks

### Validation

Test node specifications:

```bash

## Check CPU cores

ssh root@proxmox-node-1 'nproc'

## Expected: 8 or higher

## Check RAM

ssh root@proxmox-node-1 'free -h | grep Mem'

## Expected: 32Gi or higher

## Check storage devices

ssh root@proxmox-node-1 'lsblk'

## Expected: 3 drives (1 boot + 2 NVMe)

## Check network interfaces

ssh root@proxmox-node-1 'ip link show'

## Expected: 3+ interfaces
```


```text

**Step 3: Add network requirements section**

```markdown
## Network Requirements

Configure these networks before deployment:

- [ ] **Management Network**: 192.168.3.0/24 (example)
  - Node IPs: 192.168.3.11, .12, .13
  - Gateway configured
  - DNS configured
- [ ] **CEPH Public Network**: 192.168.5.0/24
  - Dedicated for CEPH client traffic
  - MTU 9000 (jumbo frames)
- [ ] **CEPH Private Network**: 192.168.7.0/24
  - Dedicated for CEPH replication
  - MTU 9000 (jumbo frames)
- [ ] **Jumbo Frames**: Switches support MTU 9000 on CEPH networks

### Validation

Test network connectivity:

```bash

## Test management network

ping -c 3 192.168.3.11

## Test MTU 9000 on CEPH network

ping -M do -s 8972 -c 3 192.168.5.11

## Expected: 0% packet loss
```


```text

**Step 4: Add software prerequisites section**

```markdown
## Software Prerequisites

### Proxmox Nodes

- [ ] **Proxmox VE 9.x** installed on all nodes
- [ ] **SSH access** as root to all nodes
- [ ] **SSH keys** generated on development machine

### Development Machine

- [ ] **mise** installed: `curl https://mise.run | sh`
- [ ] **uv** (installed via mise)
- [ ] **Git** configured
- [ ] **Infisical CLI** installed and authenticated

### Validation

Test software versions:

```bash

## Check Proxmox version

ssh root@proxmox-node-1 'pveversion'

## Expected: pve-manager/9.x

## Check SSH access

ssh root@proxmox-node-1 'hostname'

## Expected: node hostname

## Check mise

mise --version

## Expected: 2024.x or higher

## Check Git

git --version

## Expected: 2.x or higher
```


```text

**Step 5: Add Infisical setup section**

```markdown
## Credentials & Secrets

- [ ] **Infisical account** created at https://infisical.com
- [ ] **Infisical project** created for cluster secrets
- [ ] **Infisical CLI** authenticated

### Infisical Setup

1. Create Infisical account and project
2. Install Infisical CLI:

```bash

## macOS

brew install infisical/get-cli/infisical

## Linux

curl -1sLf '<https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh>' | sudo -E bash
sudo apt-get update && sudo apt-get install -y infisical
```

3. Authenticate:

```bash
infisical login
```

4. Test access:

```bash
infisical secrets

## Expected: See secrets list (may be empty)
```


```text

**Step 6: Add completion summary**

```markdown
## Prerequisites Complete

If all checkboxes are checked and validations pass, you're ready to proceed to installation.

**Next Step:** [Installation Guide](installation.md)

## Troubleshooting

### SSH Connection Fails

**Symptom**: `ssh: connect to host X.X.X.X port 22: Connection refused`

**Solutions**:
- Verify node IP address is correct
- Check SSH service running: `systemctl status sshd`
- Verify firewall allows SSH: `iptables -L | grep 22`

### Jumbo Frames Not Working

**Symptom**: `ping -M do -s 8972` fails with "message too long"

**Solutions**:
- Verify switch supports MTU 9000
- Check interface MTU: `ip link show | grep mtu`
- Configure interface MTU: Edit `/etc/network/interfaces`

### Infisical Authentication Fails

**Symptom**: `infisical login` returns authentication error

**Solutions**:
- Verify correct email/password
- Check internet connectivity
- Try browser-based authentication
```

**Step 7: Commit prerequisites.md**

```

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```text

```bash
git add documentation/getting-started/prerequisites.md
git commit -m "docs: Add comprehensive prerequisites checklist

Create detailed hardware, network, and software requirements with:

- Hardware specifications (CPU, RAM, storage, network)
- Network configuration requirements (management, CEPH networks)
- Software prerequisites (Proxmox, mise, Infisical)
- Validation commands for each requirement
- Troubleshooting section for common issues

Provides complete pre-flight checklist for new deployments"
```

## Task 7: Write installation.md

**Files:**

- Create: `documentation/getting-started/installation.md`

**Step 1: Create installation.md with overview**

```markdown

## Installation

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
```

**Step 2: Add repository clone section**

```markdown

## Step 1: Clone Repository

Clone the Virgo-Core repository:

```bash
cd ~/dev/infra-as-code
git clone <https://github.com/basher83/Virgo-Core.git>
cd Virgo-Core
```

**Verify**:

```bash
ls -la

## Expected: See .mise.toml, ansible/, terraform/, etc
```

```text

**Step 3: Add mise installation section**

```markdown

## Step 2: Install mise

Install mise (tool version manager):

```bash
curl <https://mise.run> | sh
```

Add to shell profile:

```bash

## For bash

echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc

## For zsh

echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc
source ~/.zshrc
```

**Verify**:

```bash
mise --version

## Expected: 2024.x.x or higher
```

```text

**Step 4: Add dependencies installation section**

```markdown

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

## Check uv

uv --version

## Expected: 0.x.x

## Check Python

python3 --version

## Expected: 3.13.x

## Check Ansible

ansible --version

## Expected: 2.x.x

## Check OpenTofu

tofu --version

## Expected: 1.10.x
```

```text

**Step 5: Add Infisical configuration section**

```markdown

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

## Expected: See secrets list (configured in Infisical dashboard)
```

```text

**Step 6: Add SSH configuration section**

```markdown

## Step 5: Configure SSH Access

Generate SSH key if needed:

```bash
ssh-keygen -t ed25519 -C "<your-email@example.com>"
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

## Expected: Node hostname (no password prompt)
```

```text

**Step 7: Add validation section**

```markdown

## Installation Complete

Verify all tools installed:

```bash
mise doctor

## Expected: All tools available

mise list

## Expected: Show installed tools and versions
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

```text

**Step 8: Commit installation.md**

```bash
git add documentation/getting-started/installation.md
git commit -m "docs: Add development environment installation guide

Create step-by-step installation instructions:

- Repository cloning
- mise installation and configuration
- Dependencies installation (uv, Ansible, OpenTofu)
- Infisical CLI setup
- SSH key configuration
- Validation commands
- Troubleshooting common issues

Estimated time: 15-20 minutes"
```

## Task 8: Write first-deployment.md (Part 1: Structure)

**Files:**

- Create: `documentation/getting-started/first-deployment.md`

**Step 1: Create first-deployment.md with header**

```markdown

## First Deployment: Zero to Cluster in 60 Minutes

Deploy a production-ready 3-node Proxmox cluster with CEPH storage in 60 minutes.

**Time Required**: 50-70 minutes

**Prerequisites**:

- [Prerequisites](prerequisites.md) complete
- [Installation](installation.md) complete

## Overview

This tutorial deploys the Matrix cluster with:

- 3 Proxmox nodes (Foxtrot, Golf, Hotel)
- Cluster formation with corosync
- CEPH distributed storage (12 OSDs, 12TB usable)
- Network configuration (management + CEPH networks)

## Deployment Phases

1. **Inventory Configuration** (10 min) - Configure nodes and networks
2. **Network Setup** (15 min) - Configure bridges and VLANs
3. **Cluster Formation** (10 min) - Join nodes to cluster
4. **CEPH Deployment** (15 min) - Deploy distributed storage
5. **Verification** (10 min) - Validate deployment

Total: 60 minutes
```

**Step 2: Add Phase 1: Inventory Configuration**

```markdown

## Phase 1: Inventory Configuration (10 minutes)

Configure your cluster nodes and network settings.

### Step 1: Copy example inventory

```bash
cp ansible/inventory/proxmox.yml.example ansible/inventory/proxmox.yml
```

### Step 2: Edit inventory

Edit `ansible/inventory/proxmox.yml`:

```yaml
all:
  children:
    proxmox_clusters:
      children:
        matrix_cluster:
          hosts:
            foxtrot:
              ansible_host: 192.168.3.11
              node_id: 11
            golf:
              ansible_host: 192.168.3.12
              node_id: 12
            hotel:
              ansible_host: 192.168.3.13
              node_id: 13
```

### Step 3: Configure cluster variables

Edit `ansible/inventory/group_vars/matrix_cluster.yml`:

```yaml
cluster_name: matrix

network_config:
  management:
    cidr: "192.168.3.{{ node_id }}/24"
    gateway: "192.168.3.1"
  ceph_public:
    cidr: "192.168.5.{{ node_id }}/24"
  ceph_private:
    cidr: "192.168.7.{{ node_id }}/24"
```

### Step 4: Validate inventory

```bash
uv run ansible-inventory --list
```

**Expected**: JSON output showing 3 nodes with correct IPs

**What Happens Next**: Ansible will use this inventory to configure all 3 nodes

```text

**Step 3: Commit first-deployment.md part 1**

```bash
git add documentation/getting-started/first-deployment.md
git commit -m "docs: Add first-deployment tutorial (part 1)

Add Zero to Cluster tutorial structure:

- Overview and time estimates
- Phase breakdown (5 phases, 60 minutes)
- Phase 1: Inventory configuration with examples

Part 1 of 5 - inventory setup"
```

### Task 9: Write first-deployment.md (Part 2: Network Setup)

**Files:**

- Modify: `documentation/getting-started/first-deployment.md`

**Step 1: Add Phase 2: Network Setup section**

```markdown

## Phase 2: Network Setup (15 minutes)

Configure network bridges, VLANs, and MTU for CEPH networks.

### What Will Happen

The `configure-network` playbook will:

- Create network bridges (vmbr0, vmbr1, vmbr2)
- Configure VLAN interfaces
- Set MTU to 9000 on CEPH networks
- **Network restart may briefly disconnect SSH** (~10 seconds)

### Step 1: Dry-run network configuration

```bash
CHECK=1 mise run ansible:configure-network
```

**Expected Output**:

```text
PLAY [Configure Proxmox Network] ******

TASK [proxmox_network : Create bridges] ******
changed: [foxtrot]
changed: [golf]
changed: [hotel]

PLAY RECAP ******
foxtrot: ok=12 changed=8
golf: ok=12 changed=8
hotel: ok=12 changed=8
```

**Review**: Check what would change before applying

### Step 2: Apply network configuration

```bash
mise run ansible:configure-network
```

**Expected**: Same output as dry-run, but changes actually applied

**Duration**: 5-10 minutes

### Step 3: Verify network configuration

```bash

## Check bridges created

ssh root@192.168.3.11 'ip link show | grep vmbr'

## Expected: vmbr0, vmbr1, vmbr2

## Check MTU 9000 on CEPH networks

ssh root@192.168.3.11 'ip link show vmbr1 | grep mtu'

## Expected: mtu 9000

## Test jumbo frames

ping -M do -s 8972 -c 3 192.168.5.11

## Expected: 0% packet loss
```

**Checkpoint**: All nodes should have bridges configured with correct MTU

```text

**Step 2: Commit first-deployment.md part 2**

```bash
git add documentation/getting-started/first-deployment.md
git commit -m "docs: Add first-deployment Phase 2 (network setup)

Add network configuration phase:

- What will happen explanation
- Dry-run before apply
- Network bridge creation
- MTU configuration
- Verification commands

Part 2 of 5 - network configuration"
```

## Task 10: Write first-deployment.md (Part 3-5)

**Files:**

- Modify: `documentation/getting-started/first-deployment.md`

**Step 1: Add Phase 3: Cluster Formation**

```markdown

## Phase 3: Cluster Formation (10 minutes)

Form Proxmox cluster and join nodes.

### What Will Happen

The `init-cluster` playbook will:

- Create cluster on first node (Foxtrot)
- Join Golf and Hotel to cluster
- Configure Corosync for cluster communication
- **No service disruption expected**

### Step 1: Initialize cluster

```bash
mise run ansible:init-cluster
```

**Expected Output**:

```text
TASK [proxmox_cluster : Create cluster] ******
changed: [foxtrot]

TASK [proxmox_cluster : Join nodes] ******
changed: [golf]
changed: [hotel]

PLAY RECAP ******
foxtrot: ok=8 changed=4
golf: ok=6 changed=2
hotel: ok=6 changed=2
```

**Duration**: 5-10 minutes

### Step 2: Verify cluster status

```bash
ssh root@192.168.3.11 'pvecm status'
```

**Expected Output**:

```text

## Cluster information

## -------------------

---

Name:             matrix
Config Version:   3
Transport:        knet
Secure auth:      on

## Quorum information

## ------------------

---

Date:             Mon Nov 19 12:34:56 2025
Quorum provider:  corosync_votequorum
Nodes:            3
Node ID:          0x00000001
Ring ID:          1.5
Quorate:          Yes

## Membership information

## ----------------------

---

Nodeid      Votes Name
0x00000001      1 foxtrot (local)
0x00000002      1 golf
0x00000003      1 hotel
```

**Checkpoint**: All 3 nodes should appear in cluster, status "Quorate: Yes"

```text

**Step 2: Add Phase 4: CEPH Deployment**

```markdown

## Phase 4: CEPH Deployment (15 minutes)

Deploy CEPH distributed storage across all nodes.

### What Will Happen

The `deploy-ceph` playbook will:

- Install CEPH packages on all nodes
- Create monitors (1 per node)
- Create managers (1 per node)
- Create OSDs (4 per node = 12 total)
- Create default storage pool
- **CPU/network intensive during OSD creation**

### Step 1: Deploy CEPH

```bash
mise run ansible:deploy-ceph
```

**Expected Output**:

```text
TASK [proxmox_ceph : Install CEPH] ******
changed: [foxtrot]
changed: [golf]
changed: [hotel]

TASK [proxmox_ceph : Create monitors] ******
changed: [foxtrot]
changed: [golf]
changed: [hotel]

TASK [proxmox_ceph : Create OSDs] ******
changed: [foxtrot] (4 OSDs)
changed: [golf] (4 OSDs)
changed: [hotel] (4 OSDs)

PLAY RECAP ******
foxtrot: ok=24 changed=16
golf: ok=24 changed=16
hotel: ok=24 changed=16
```

**Duration**: 10-15 minutes (OSD creation is slow)

### Step 2: Verify CEPH status

```bash
ssh root@192.168.3.11 'ceph -s'
```

**Expected Output**:

```text
  cluster:
    id:     xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum foxtrot,golf,hotel (age 2m)
    mgr: foxtrot(active, since 1m), standbys: golf, hotel
    osd: 12 osds: 12 up (since 1m), 12 in (since 1m)

  data:
    pools:   1 pools, 128 pgs
    objects: 0 objects, 0 B
    usage:   60 GiB used, 12 TiB / 12 TiB avail
    pgs:     128 active+clean
```

**Checkpoint**: HEALTH_OK, 12 OSDs up and in

```text

**Step 3: Add Phase 5: Verification**

```markdown

## Phase 5: Verification (10 minutes)

Validate complete deployment.

### Cluster Health Checks

**Check 1: Cluster Status**

```bash
ssh root@192.168.3.11 'pvecm status'
```

Expected: 3 nodes, Quorate: Yes

**Check 2: CEPH Health**

```bash
ssh root@192.168.3.11 'ceph -s'
```

Expected: HEALTH_OK, 12 OSDs

**Check 3: Network MTU**

```bash
ssh root@192.168.3.11 'ip link show vmbr1 | grep mtu'
```

Expected: mtu 9000

**Check 4: Storage Pools**

```bash
ssh root@192.168.3.11 'pvesm status'
```

Expected: See CEPH pool listed and available

### Complete Verification Checklist

- [ ] All 3 nodes in cluster (`pvecm status`)
- [ ] Cluster quorate (3/3 votes)
- [ ] CEPH health OK (`ceph -s`)
- [ ] 12 OSDs up and in
- [ ] Jumbo frames working (MTU 9000)
- [ ] SSH access to all nodes working

## Deployment Complete! 🎉

Your Matrix cluster is production-ready with:

- ✅ 3-node Proxmox cluster
- ✅ CEPH distributed storage (12TB usable)
- ✅ High-performance network (jumbo frames)
- ✅ Production-grade configuration

**Next Steps**:

- Deploy your first VM
- Configure additional storage pools
- Set up monitoring

**Troubleshooting**: See [Troubleshooting Basics](troubleshooting-basics.md)

```text

**Step 4: Commit first-deployment.md completion**

```bash
git add documentation/getting-started/first-deployment.md
git commit -m "docs: Complete first-deployment tutorial (phases 3-5)

Add remaining deployment phases:

- Phase 3: Cluster formation with verification
- Phase 4: CEPH deployment with expected timings
- Phase 5: Complete verification checklist

Tutorial complete - full Zero to Cluster in 60 minutes workflow"
```

### Task 11: Update docs.json for Phase 2 Content

**Files:**

- Modify: `docs.json:22-26`

**Step 1: Add getting-started pages to docs.json**

Edit `docs.json` Getting Started group:

```json
{
  "group": "Getting Started",
  "pages": [
    "index",
    "documentation/getting-started/prerequisites",
    "documentation/getting-started/installation",
    "documentation/getting-started/first-deployment",
    "documentation/core/goals",
    "documentation/core/infrastructure"
  ]
}
```

**Step 2: Verify JSON syntax**

```bash
python3 -c "import json; json.load(open('docs.json'))"
```

Expected: No output (valid JSON)

**Step 3: Commit docs.json update**

```bash
git add docs.json
git commit -m "docs: Add getting-started pages to navigation

Add Phase 2 tutorial pages:

- prerequisites.md
- installation.md
- first-deployment.md

Places tutorials before goals/infrastructure for better UX"
```

---

## Phase 3: Enhanced Role Documentation (8-10 hours)

### Task 12: Create Roles Directory

**Files:**

- Create: `documentation/roles/` (directory)

**Step 1: Create roles directory**

```bash
mkdir -p documentation/roles
```

**Step 2: Commit directory**

```bash
git add documentation/roles/
git commit --allow-empty -m "docs: Create roles directory for Phase 3

Prepare for enhanced role documentation"
```

### Task 13: Create system_user Role Documentation

**Files:**

- Create: `documentation/roles/system_user.md`
- Read: `ansible/roles/system_user/README.md` (source material)

**Step 1: Create system_user.md header**

```markdown

## system_user Role

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
```

**Step 2: Add quick start example**

```markdown

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

```text

**Step 3: Add configuration reference**

```markdown

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

  - "ssh-ed25519 AAAA... <ci-server@example.com>"
  - "ssh-ed25519 BBBB... <backup-key@example.com>"
    sudo: nopasswd
    groups:
  - docker
  - libvirt
    state: present
```

```text

**Step 4: Add integration examples**

```markdown

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

```text

**Step 5: Add troubleshooting section**

```markdown

## Troubleshooting

### SSH Key Not Working

**Symptom**: SSH authentication fails after adding key

**Diagnosis**:

```bash

## Check authorized_keys file

ssh root@node 'cat /home/username/.ssh/authorized_keys'

## Check file permissions

ssh root@node 'ls -la /home/username/.ssh/'

## Expected: .ssh/ directory 700, authorized_keys 600
```

**Solutions**:

- Verify key format (must be valid SSH public key)
- Check key not commented out
- Ensure home directory exists

### Sudo Access Not Working

**Symptom**: User cannot sudo

**Diagnosis**:

```bash

## Check sudoers file

ssh root@node 'cat /etc/sudoers.d/username'
```

**Solutions**:

- Verify `sudo: nopasswd` or `sudo: password` set
- Check sudoers syntax: `visudo -c`

## See Also

- [proxmox_access](proxmox_access.md) - Proxmox user and token management
- [Ansible User Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html)

```text

**Step 6: Commit system_user.md**

```bash
git add documentation/roles/system_user.md
git commit -m "docs: Add enhanced system_user role documentation

Create comprehensive role guide with:

- Quick start example
- Complete configuration reference table
- Integration patterns (proxmox_access, Infisical)
- Troubleshooting section
- Cross-references to related roles

Enhanced from existing README with additional examples"
```

## Task 14: Create Roles Index in docs.json

**Files:**

- Modify: `docs.json` (add Ansible Roles group)

**Step 1: Add Ansible Roles navigation group**

After the "Getting Started" group, add:

```json
{
  "group": "Ansible Roles",
  "pages": [
    "documentation/roles/system_user",
    "documentation/roles/proxmox_access",
    "documentation/roles/proxmox_network",
    "documentation/roles/proxmox_repository",
    "documentation/roles/proxmox_cluster",
    "documentation/roles/proxmox_ceph"
  ]
}
```

**Step 2: Verify JSON syntax**

```bash
python3 -c "import json; json.load(open('docs.json'))"
```

**Step 3: Commit navigation update**

```bash
git add docs.json
git commit -m "docs: Add Ansible Roles navigation group

Add new navigation group for role documentation (Phase 3)
Currently includes system_user, prepared for remaining 5 roles"
```

### Task 15-19: Create Remaining Role Documentation

**Note**: Tasks 15-19 follow the same pattern as Task 13:

- Read existing `ansible/roles/<role>/README.md`
- Create enhanced `documentation/roles/<role>.md`
- Add configuration tables
- Add integration examples
- Add troubleshooting
- Commit each role individually

**Roles to document**:

1. `proxmox_access.md` (based on 580-line README)
2. `proxmox_network.md` (based on 480-line README)
3. `proxmox_repository.md` (based on 99-line README)
4. `proxmox_cluster.md` (based on 156-line README)
5. `proxmox_ceph.md` (based on 290-line README)

Each commit message follows pattern:

```text
docs: Add enhanced <role> role documentation

Create comprehensive role guide with examples, configuration reference,
integration patterns, and troubleshooting.

Enhanced from existing README with additional context.
```

---


## Verification & Deployment

### Task 20: Final Verification

**Step 1: Verify all files created**

```bash
find documentation/ -name "*.md" -newer docs/plans/2025-11-19-documentation-enhancement-design.md
```

Expected: 10 new files (4 getting-started + 6 roles)

**Step 2: Verify docs.json valid**

```bash
python3 -c "import json; json.load(open('docs.json'))"
```

Expected: No errors

**Step 3: Check git status**

```bash
git status
```

Expected: Clean working tree (all changes committed)

**Step 4: Review commit history**

```bash
git log --oneline --since="1 day ago"
```

Expected: ~20 commits (Phase 1: 4, Phase 2: 5, Phase 3: 10, Setup: 1)

### Task 21: Deploy to Mintlify

**Step 1: Push to remote**

```bash
git push origin main
```

**Step 2: Wait for Mintlify build**

Mintlify auto-deploys from main branch. Check build status:

<https://dashboard.mintlify.com/>

Expected: Build succeeds

**Step 3: Test live site**

Visit <https://themothership.mintlify.app/>

Verify:

- [ ] All navigation links work (no 404s)
- [ ] Getting Started section visible
- [ ] Ansible Roles section visible
- [ ] Prerequisites page loads
- [ ] First deployment tutorial complete
- [ ] All 6 role pages accessible

**Step 4: Verify search works**

Search for "CEPH" on site

Expected: Find references in multiple docs

### Task 22: Create Completion Summary

**Step 1: Generate metrics**

```bash

## Count new documentation lines

find documentation/getting-started documentation/roles -name "*.md" -exec wc -l {} + | tail -1

## Count commits

git log --oneline --since="1 day ago" | wc -l
```

**Step 2: Document completion**

Create `docs/plans/2025-11-19-implementation-complete.md`:

```markdown

## Documentation Enhancement - Implementation Complete

**Date**: 2025-11-19
**Status**: ✅ Complete
**Duration**: [Actual time]

## Deliverables

### Phase 1: Foundation Fix

- ✅ Fixed docs.json navigation paths
- ✅ Extracted insights from archived docs
- ✅ Updated homepage links
- **Impact**: 7 reference docs now accessible (0 404s)

### Phase 2: Getting Started Content

- ✅ prerequisites.md (hardware, network, software checklists)
- ✅ installation.md (development environment setup)
- ✅ first-deployment.md (Zero to Cluster in 60 minutes)
- ✅ Updated docs.json navigation
- **Impact**: Complete onboarding path for new users

### Phase 3: Enhanced Role Documentation

- ✅ system_user.md
- ✅ proxmox_access.md
- ✅ proxmox_network.md
- ✅ proxmox_repository.md
- ✅ proxmox_cluster.md
- ✅ proxmox_ceph.md
- **Impact**: Comprehensive reference for all 6 production roles

## Metrics

- **Documentation lines added**: [X,XXX]
- **Files created**: 10
- **Files modified**: 3
- **Commits**: [~20]
- **Total effort**: [X hours]

## Site Transformation

**Before**:

- Homepage only
- 10 broken navigation links (404s)
- No getting-started content

**After**:

- Complete getting-started through advanced reference
- 16 accessible documentation pages
- Zero 404 errors
- Searchable, navigable structure

## Verification

Site URL: <https://themothership.mintlify.app/>

All acceptance criteria met:

- ✅ All navigation links work
- ✅ New users can deploy cluster following tutorial
- ✅ All 6 roles documented comprehensively
- ✅ Search functionality works
- ✅ Cross-references enable discovery

**Status**: Ready for v2.0.0 🎉
```

**Step 3: Commit completion summary**

```bash
git add docs/plans/2025-11-19-implementation-complete.md
git commit -m "docs: Add implementation completion summary

Document Phase 1-3 deliverables, metrics, and verification.

All three phases complete:

- Phase 1: Foundation fix (404s resolved)
- Phase 2: Getting-started content (onboarding path)
- Phase 3: Enhanced role docs (comprehensive reference)

Site transformed from landing page to complete documentation."
```

---

## Implementation Complete

This plan provides bite-sized tasks (2-5 minutes each) for implementing all three phases of the documentation enhancement project.

**Total Tasks**: 22
**Estimated Time**: 16-24 hours
**Commits**: ~20 atomic commits

Each task includes:

- Exact file paths
- Complete code/content
- Verification commands
- Clear commit messages

The plan is ready for execution using `superpowers:executing-plans` or `superpowers:subagent-driven-development`.
