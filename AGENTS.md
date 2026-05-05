# CLAUDE.md

Agent guidance for Virgo-Core. Keep this file short and operational; link to canonical files instead of duplicating facts that drift.

## What this repo is

Virgo-Core is IaC/config management for the Matrix Proxmox cluster:

- OpenTofu provisions VM templates and NetBox VM configs under `terraform/`.
- Ansible configures Proxmox hosts, networking, access, clustering, templates, LXC, tuning, and CEPH under `ansible/`.
- Matrix nodes are Foxtrot, Golf, and Hotel.

## Canonical sources

- Tool pins: `.mise.toml` — do not hardcode tool versions in docs or guidance.
- Python compatibility: `pyproject.toml` and per-script inline metadata.
- Ansible dependencies: `ansible/requirements.yml`.
- Ansible inventory/config: `ansible/inventory/` and `ansible/ansible.cfg`.
- Terraform module defaults: upstream `Triangulum-Prime//terraform-bgp-vm` docs/defaults.
- Project docs index: `documentation/README.md`.

## Non-negotiable conventions

- Use `tofu`, not `terraform`.
- Run Ansible through `uv run`.
- Prefer `mise run <task>` for repo automation; check `.mise.toml` before inventing commands.
- Do not commit plaintext secrets. Use Infisical/local env only as intended.
- Do not repeat upstream module defaults in Terraform configs; specify only overrides.
- Keep docs pointed at canonical files instead of copying tool versions, role lists, or command details.

## Terraform/OpenTofu

Current root configs:

- `terraform/netbox-template/` — creates image/template VMs with `vm_type = "image"`.
- `terraform/netbox-vm/` — clones VMs with `vm_type = "clone"`.

Both use `github.com/basher83/Triangulum-Prime//terraform-bgp-vm?ref=v1.0.0`. Examples may lag; verify module sources before treating example docs as current.

## Ansible

Roles live under `ansible/roles/`; inspect the role defaults/tasks for truth before changing docs or examples.

Operational patterns:

- Run from `ansible/` when using its `ansible.cfg`, or pass `-i ansible/inventory/...` explicitly from repo root.
- Inventory should use hostnames matching SSH config entries, not duplicated IP/key data.
- SSH config is local and modular under `~/.ssh/config.d/`; keys are managed via 1Password.

## Documentation hygiene

When updating docs:

- Prefer “installed/managed by mise; see `.mise.toml`” over hardcoded versions.
- Prefer links to role defaults/tasks over copied variable tables unless generated.
- Mark planned architecture as planned; do not present NetBox/PowerDNS automation as implemented unless code exists.
- Validate paths and commands against the repo before publishing.

## Useful docs

- `documentation/README.md` — start here / documentation index.
- `documentation/core/infrastructure.md` — infrastructure reference.
- `documentation/core/goals.md` — goals and roadmap.
- `documentation/core/netbox-powerdns.md` — NetBox/PowerDNS architecture.
- `docs/archive/2025-11-v1.0/ansible-migration-plan.md` — historical Ansible migration plan.
