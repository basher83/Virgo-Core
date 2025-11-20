# Prerequisites

Before deploying Virgo-Core, verify you have the required hardware, network, and software.

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
# Check CPU cores
ssh root@proxmox-node-1 'nproc'
# Expected: 8 or higher

# Check RAM
ssh root@proxmox-node-1 'free -h | grep Mem'
# Expected: 32Gi or higher

# Check storage devices
ssh root@proxmox-node-1 'lsblk'
# Expected: 3 drives (1 boot + 2 NVMe)

# Check network interfaces
ssh root@proxmox-node-1 'ip link show'
# Expected: 3+ interfaces
```

## Network Requirements

Before deployment, configure these networks:

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
# Test management network
ping -c 3 192.168.3.11

# Test MTU 9000 on CEPH network
ping -M do -s 8972 -c 3 192.168.5.11
# Expected: 0% packet loss
```

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
# Check Proxmox version
ssh root@proxmox-node-1 'pveversion'
# Expected: pve-manager/9.x

# Check SSH access
ssh root@proxmox-node-1 'hostname'
# Expected: node hostname

# Check mise
mise --version
# Expected: 2024.x or higher

# Check Git
git --version
# Expected: 2.x or higher
```

## Credentials & Secrets

- [ ] **Infisical account** created at https://infisical.com
- [ ] **Infisical project** created for cluster secrets
- [ ] **Infisical CLI** authenticated

### Infisical Setup

1. Create Infisical account and project
2. Install Infisical CLI:

   ```bash
   # macOS
   brew install infisical/get-cli/infisical

   # Linux
   curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | sudo -E bash
   sudo apt-get update && sudo apt-get install -y infisical
   ```

3. Authenticate:

   ```bash
   infisical login
   ```

4. Test access:

   ```bash
   infisical secrets
   # Expected: See secrets list (may be empty)
   ```

## Prerequisites Complete

When all checkboxes are checked and validations pass, proceed to installation.

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
