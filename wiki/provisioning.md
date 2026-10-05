---
title: "VM, template and LXC provisioning"
created: "2026-09-11"
updated: "2026-09-11"
type: "concept"
tags: ["virgo-core"]
sources: ["terraform/netbox-vm/main.tf", "terraform/netbox-template/main.tf", "ansible/roles/proxmox_template/README.md", "ansible/roles/proxmox_lxc/README.md"]
confidence: "medium"
source_revision: "166734f0c4ad5169d7140b5177e315118edfa578"
---

# VM, template and LXC provisioning

## OpenTofu routes

`terraform/netbox-vm/main.tf` uses `vm_type = "clone"`, supplies the source template, disk/network configuration and cloud-init user/public keys. `terraform/netbox-template/main.tf` uploads a cloud-init snippet and uses `vm_type = "image"` with template mode and a cloud-image source. Both reference `github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=v1.0.0`. [Sources: both main.tf files]

These files depend on external module/provider behavior. Their directory names do not establish a functioning NetBox synchronization service. Consult actual provider configuration, variables, state/backend setup and the external module before planning changes.

## Ansible template route

The `proxmox_template` README describes a second route: validate configuration, retrieve keys if enabled, require keys, render cloud-init, invoke a shell builder, and verify the resulting template. It documents the `ansible` default user and key-only authentication. That is a VM-template workflow, not a bare-metal installation procedure. [Source: proxmox_template/README.md]

## LXC route

The `proxmox_lxc` README describes `present`/`absent` lifecycle, unprivileged containers by default, optional API-secret lookup, public-key injection, and optional TUN support for VPN use. TUN capability does not itself enroll a container into Tailscale or manage tailnet policy. The documented certificate-validation default is false; review the executable defaults and target trust requirements before use. [Source: proxmox_lxc/README.md]

## Selecting a route

Choose an existing route by required outcome and established ownership, not simply because it can create something. The wiki does not choose between overlapping template routes, relocate Terraform state, or recommend running creation/destruction commands as exploration.

Related: [[architecture]], [[ansible-roles]], [[known-gaps]].

## Pinned sources

- [terraform/netbox-vm/main.tf](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/terraform/netbox-vm/main.tf)
- [terraform/netbox-template/main.tf](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/terraform/netbox-template/main.tf)
- [ansible/roles/proxmox_template/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_template/README.md)
- [ansible/roles/proxmox_lxc/README.md](https://github.com/basher83/Virgo-Core/blob/166734f0c4ad5169d7140b5177e315118edfa578/ansible/roles/proxmox_lxc/README.md)
