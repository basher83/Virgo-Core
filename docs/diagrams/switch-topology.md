# Switch Topology - Proxmox and TrueNAS Connections

## Overview

This document maps Proxmox cluster nodes (Matrix, Nexus, and Quantum clusters) and TrueNAS storage connections to UniFi switches and ports.

## Matrix Cluster Nodes

### Foxtrot (192.168.3.5)

- **Primary Interface**: `38:05:25:30:5b:4c`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 12 (GE)
  - **Speed**: 1 Gbps
  - **VLAN**: Matrix-MGMT (VLAN 30)

- **Secondary Interface**: `38:05:25:30:5b:4d`
  - **Switch**: USW Aggregation (1c:6a:1b:91:cf:06)
  - **Port**: SFP+ 5
  - **Speed**: 10 Gbps
  - **VLAN**: Matrix-CEPH-Public (VLAN 7)

- **Tertiary Interface**: `38:05:25:30:5b:4e`
  - **Switch**: USW Aggregation (1c:6a:1b:91:cf:06)
  - **Port**: SFP+ 6
  - **Speed**: 10 Gbps
  - **VLAN**: Matrix-CEPH-Private (VLAN 8)

### Golf (192.168.3.6)

- **Primary Interface**: `58:47:ca:7f:cd:d1`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 11 (GE)
  - **Speed**: 1 Gbps
  - **VLAN**: Matrix-MGMT (VLAN 30)

- **Secondary Interface**: `58:47:ca:7f:cd:d2`
  - **Switch**: USW Aggregation (1c:6a:1b:91:cf:06)
  - **Port**: SFP+ 4
  - **Speed**: 10 Gbps
  - **VLAN**: Matrix-CEPH-Private (VLAN 8)

- **Tertiary Interface**: `58:47:ca:7f:cd:d3`
  - **Switch**: USW Aggregation (1c:6a:1b:91:cf:06)
  - **Port**: SFP+ 3
  - **Speed**: 10 Gbps
  - **VLAN**: Matrix-CEPH-Public (VLAN 7)

### Hotel (192.168.3.7)

- **Primary Interface**: `58:47:ca:7f:df:79`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 10 (GE)
  - **Speed**: 1 Gbps
  - **VLAN**: Matrix-MGMT (VLAN 30)

- **Secondary Interface**: `58:47:ca:7f:df:7a`
  - **Switch**: USW Aggregation (1c:6a:1b:91:cf:06)
  - **Port**: SFP+ 1
  - **Speed**: 10 Gbps
  - **VLAN**: Matrix-CEPH-Public (VLAN 7)

- **Tertiary Interface**: `58:47:ca:7f:df:7b`
  - **Switch**: USW Aggregation (1c:6a:1b:91:cf:06)
  - **Port**: SFP+ 2
  - **Speed**: 10 Gbps
  - **VLAN**: Matrix-CEPH-Private (VLAN 8)

## Nexus Cluster Nodes

### Protectli (pve1.homelab.net - 192.168.30.50)

- **Interface**: `00:e0:97:1b:9a:76`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 20 (2P5GE)
  - **Speed**: 2.5 Gbps
  - **VLAN**: Homelab-Servers (VLAN 3)

### Proxmox Server (proxmoxt430.homelab.net - 192.168.30.30)

- **Interface**: `a0:36:9f:f5:f5:c1`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 19 (2P5GE)
  - **Speed**: 1 Gbps
  - **VLAN**: Homelab-Servers (VLAN 3)

## Quantum Cluster Nodes

### Lloyd (192.168.10.2)

- **Primary Interface**: `58:47:ca:79:7a:22`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 23 (2P5GE)
  - **Speed**: 2.5 Gbps
  - **VLAN**: Quantum-MGMT (VLAN 10)

- **Secondary Interface**: `58:47:ca:79:7a:20`
  - **Switch**: USW Flex XG (24:5a:4c:1b:b8:ad)
  - **Port**: Port 4 (10GE)
  - **Speed**: 10 Gbps
  - **VLAN**: Quantum-CEPH-Public (VLAN 11)

### Holly (192.168.10.3)

- **Primary Interface**: `58:47:ca:79:7a:36`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 24 (2P5GE)
  - **Speed**: 2.5 Gbps
  - **VLAN**: Quantum-MGMT (VLAN 10)

- **Secondary Interface**: `58:47:ca:79:7a:34`
  - **Switch**: USW Flex XG (24:5a:4c:1b:b8:ad)
  - **Port**: Port 3 (10GE)
  - **Speed**: 10 Gbps
  - **VLAN**: Quantum-CEPH-Public (VLAN 11)

### Mable (192.168.10.4)

- **Primary Interface**: `58:47:ca:79:78:66`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 22 (2P5GE)
  - **Speed**: 2.5 Gbps
  - **VLAN**: Quantum-MGMT (VLAN 10)

- **Secondary Interface**: `58:47:ca:79:78:64`
  - **Switch**: USW Flex XG (24:5a:4c:1b:b8:ad)
  - **Port**: Port 2 (10GE)
  - **Speed**: 10 Gbps
  - **VLAN**: Quantum-CEPH-Public (VLAN 11)

## TrueNAS Storage

### TrueNAS (nas.homelab.net - 192.168.30.6)

- **Interface**: `a0:36:9f:d7:59:54`
  - **Switch**: USW-Pro-Max-24-PoE (f4:e2:c6:ae:21:e7)
  - **Port**: Port 25 (SFP+ 1)
  - **Speed**: 10 Gbps
  - **VLAN**: Homelab-Servers (VLAN 3)
  - **SFP Module**: SFP-10G-SR (OEM, Serial: CSF102M14469)

## Switch Summary

### USW-Pro-Max-24-PoE (192.168.1.51)

- **Model**: USPM24P
- **Total Ports**: 26 (24 GE PoE + 2 SFP+)
- **Matrix Cluster Connections**:
  - Port 10: Hotel (primary, 1G)
  - Port 11: Golf (primary, 1G)
  - Port 12: Foxtrot (primary, 1G)
- **Nexus Cluster Connections**:
  - Port 19: Proxmox Server (1G)
  - Port 20: Protectli (2.5G)
- **Quantum Cluster Connections**:
  - Port 22: Mable (primary, 2.5G)
  - Port 23: Lloyd (primary, 2.5G)
  - Port 24: Holly (primary, 2.5G)
- **TrueNAS Connection**:
  - Port 25 (SFP+ 1): TrueNAS (10G)

### USW Aggregation (192.168.1.49)

- **Model**: USL8A
- **Total Ports**: 8 SFP+
- **Matrix Cluster Connections** (all 10G):
  - SFP+ 1: Hotel (secondary, CEPH-Public)
  - SFP+ 2: Hotel (tertiary, CEPH-Private)
  - SFP+ 3: Golf (tertiary, CEPH-Public)
  - SFP+ 4: Golf (secondary, CEPH-Private)
  - SFP+ 5: Foxtrot (secondary, CEPH-Public)
  - SFP+ 6: Foxtrot (tertiary, CEPH-Private)
  - SFP+ 7: Uplink to DMPX-Mothership

### USW Flex XG (192.168.1.212)

- **Model**: USFXG
- **Total Ports**: 5 (1 GE + 4 10GE)
- **Quantum Cluster Connections** (all 10G):
  - Port 1: Uplink to USW-Pro-Max-24-PoE (1G)
  - Port 2: Mable (secondary, CEPH-Public)
  - Port 3: Holly (secondary, CEPH-Public)
  - Port 4: Lloyd (secondary, CEPH-Public)

## Network VLANs

- **VLAN 30 (Matrix-MGMT)**: Management network for Matrix cluster nodes (192.168.3.0/24)
- **VLAN 7 (Matrix-CEPH-Public)**: CEPH public network for Matrix cluster (192.168.5.0/24)
- **VLAN 8 (Matrix-CEPH-Private)**: CEPH private network for Matrix cluster (192.168.7.0/24)
- **VLAN 10 (Quantum-MGMT)**: Management network for Quantum cluster nodes (192.168.10.0/24)
- **VLAN 11 (Quantum-CEPH-Public)**: CEPH public network for Quantum cluster (192.168.11.0/24)
- **VLAN 3 (Homelab-Servers)**: General server network (192.168.30.0/24)

## Notes

- **Matrix Cluster**: All Proxmox Matrix cluster nodes (Foxtrot, Golf, Hotel) have 3 network interfaces:
  1. Management (1Gbps) on USW-Pro-Max-24-PoE
  2. CEPH Public (10Gbps) on USW Aggregation
  3. CEPH Private (10Gbps) on USW Aggregation
- **Nexus Cluster**: Nexus cluster nodes (Proxmox Server, Protectli) are connected to USW-Pro-Max-24-PoE on Homelab-Servers VLAN
- **Quantum Cluster**: All Quantum cluster nodes (Lloyd, Holly, Mable) have 2 network interfaces:
  1. Management (2.5Gbps) on USW-Pro-Max-24-PoE
  2. CEPH Public (10Gbps) on USW Flex XG
- TrueNAS is connected via 10Gbps SFP+ to the main switch
- All connections are active and forwarding (STP state: forwarding)
