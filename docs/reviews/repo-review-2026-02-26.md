# Virgo-Core Repository Review

**Date:** 2026-02-26
**Scope:** Full repository audit covering security, code quality, Terraform/OpenTofu, CI/CD, and documentation
**Review Method:** Multi-agent deep dive with manual synthesis

---

## Executive Summary

Virgo-Core is a well-structured Infrastructure as Code repository that has achieved its v1.0.0 milestone with 9 production-ready Ansible roles, working Terraform/OpenTofu modules, and a solid CI/CD pipeline. The codebase demonstrates strong engineering practices: consistent naming, proper secrets management via Infisical, comprehensive documentation, and good use of `no_log` for sensitive operations.

This review identified **87 findings** across 5 domains. The most impactful areas for improvement are: (1) tightening Terraform state management and provider version constraints, (2) expanding CI/CD parallelism and caching, (3) resolving a Python version mismatch across tool configs, (4) fixing conflicting inventory files, and (5) adding missing Ansible role tests and tags (6 of 9 roles lack tags). No critical security vulnerabilities were found — secrets handling through Infisical is well-implemented.

### Finding Summary

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | 2 | Terraform state backend, Python version mismatch |
| High | 7 | Command injection surface, CI permissions, provider pinning, CI caching, `.cursor` corruption, conflicting inventory, Tailscale auth key exposure |
| Medium | 23 | Variable validation, tfvars drift, markdown lint coverage, pre-commit gaps, token handling, missing tags (x6), variable collisions, idempotency gaps |
| Low | 28 | Documentation drift, default values, naming conventions, missing convenience tasks, stale files |
| Info | 25 | Positive findings — things done well |

### Detailed Sub-Reports

For full findings with line-by-line analysis, see:
- **[detailed/security-audit.md](detailed/security-audit.md)** — Complete security audit with 19 findings
- **[detailed/ansible-quality.md](detailed/ansible-quality.md)** — Per-role code quality analysis with 43 findings

---

## 1. Security Audit

### 1.1 Secrets Management — STRONG

**Positive Findings:**
- Infisical integration is well-designed with a reusable lookup pattern (`ansible/tasks/infisical-secret-lookup.yml`) that validates inputs, uses `no_log: true`, and delegates to localhost
- `.gitignore` properly excludes `terraform.tfvars`, `*.auto.tfvars`, `.vault_pass.txt`, `.envrc`, and Omni Provider secrets
- No hardcoded secrets, passwords, or API keys found anywhere in the codebase
- Terraform environment export files are created with `mode: 0600` (`ansible/roles/proxmox_access/tasks/env_export.yml:9`)
- `proxmox_no_log: true` is consistently applied across sensitive operations

**Findings:**

| ID | Severity | File | Finding |
|----|----------|------|---------|
| S-1 | Medium | `ansible/roles/proxmox_access/tasks/secrets.yml:17` | Debug message exposes username: `"Proxmox API credentials retrieved for {{ proxmox_api_user }}"`. While not a password leak, exposing the API username in logs aids reconnaissance. **Recommendation:** Remove the debug task or gate it behind a verbose flag. |
| S-2 | Low | `ansible/roles/proxmox_access/templates/terraform_env.sh.j2:6` | `PROXMOX_VE_INSECURE=true` is hardcoded in the template. This disables TLS verification for all exported environments. **Recommendation:** Make it a variable: `export PROXMOX_VE_INSECURE={{ proxmox_validate_certs | ternary('false', 'true') }}` |
| S-3 | Low | `.infisical.json` | Infisical workspace ID (`7b832220-...`) is committed. While not a secret, it reduces the attack surface to avoid exposing project IDs. **Recommendation:** Consider adding to `.gitignore` if the ID is sensitive in your threat model. |

### 1.2 Access Control & Permissions — GOOD

**Positive Findings:**
- `sudoers.j2` template properly documents the security requirement for absolute paths in sudo rules
- User creation in `system_user` role correctly sets `.ssh` directory to `0700`
- ACL management uses the `community.proxmox.proxmox_access_acl` module for idempotent operations

**Findings:**

| ID | Severity | File | Finding |
|----|----------|------|---------|
| S-4 | Medium | `ansible/roles/system_user/templates/sudoers.j2:9` | `NOPASSWD:ALL` grants unrestricted root access. While documented as intentional, there is no validation that `sudo_rules` entries use absolute paths (only a comment warns about it). **Recommendation:** Add a validation task in `sudo_config.yml` that asserts all `sudo_rules` entries start with `/`. |
| S-5 | Medium | `ansible/roles/proxmox_access/tasks/tokens.yml:17` | Token creation command constructs arguments via Jinja2 string interpolation. While `item.comment` is user-controlled, the `pveum` command is not run through a shell, mitigating injection risk. However, a comment with special characters could cause unexpected behavior. **Recommendation:** Quote the comment: `"{{ item.item.comment | quote }}"` |
| S-6 | Low | `ansible/ansible.cfg:15` | `host_key_checking = False` disables SSH host key verification globally. Acceptable for a homelab but should be documented as a conscious decision. |

### 1.3 Input Validation — ADEQUATE

**Findings:**

| ID | Severity | File | Finding |
|----|----------|------|---------|
| S-7 | High | `ansible/roles/proxmox_ceph/tasks/osd_create.yml:26,69` | OSD creation uses `ansible.builtin.command` with device paths from variables. While `command` (not `shell`) mitigates injection, device paths like `/dev/nvme1n1` are not validated before being passed to `pveceph osd create` and `ceph-volume lvm batch`. **Recommendation:** Add a validation task asserting device paths match `/dev/[a-z]+[0-9]*`. |
| S-8 | Medium | `ansible/roles/proxmox_template/tasks/build_template.yml:37` | The `_build_template_cmd` fact concatenates many variables into a command string. While executed via `ansible.builtin.command` (not shell), the sheer number of unvalidated variables increases the surface area. The `proxmox_template_dns` variable is passed with quotes (`"{{ proxmox_template_dns }}"`) which is good. |
| S-9 | Low | `ansible/roles/proxmox_lxc/defaults/main.yml:109` | `proxmox_lxc_password` is stored as a default variable (empty string). If a user sets this, it will appear in Ansible logs unless `no_log` is used in every task referencing it. The role does use `no_log: "{{ proxmox_lxc_no_log }}"` in `create.yml`, which is correct. |

### 1.4 Network Security — APPROPRIATE FOR HOMELAB

**Positive Findings:**
- VLAN-aware bridging properly configured with explicit VLAN ID lists (not wide-open ranges)
- Dedicated CEPH networks (public `192.168.5.0/24`, private `192.168.7.0/24`) with jumbo frames (MTU 9000)
- Corosync traffic isolated on VLAN 9 (`192.168.8.0/24`)
- SSH hardening variables defined globally (`group_vars/all.yml`): key-only auth, no empty passwords, no X11 forwarding

**Findings:**

| ID | Severity | File | Finding |
|----|----------|------|---------|
| S-10 | Low | `ansible/inventory/group_vars/all.yml:25` | `ssh_permit_root_login: "yes"` allows root SSH (key-only). While common in Proxmox environments, consider `prohibit-password` for defense in depth. |
| S-11 | Info | `ansible/inventory/group_vars/matrix_cluster.yml` | Network configuration is well-segmented with management, CEPH public, CEPH private, and corosync on separate bridges/VLANs. |

### 1.5 CI/CD Security

| ID | Severity | File | Finding |
|----|----------|------|---------|
| S-12 | High | `.github/workflows/validate.yml` | **Missing `permissions` block.** Without explicit permissions, the workflow inherits the repository default token scope, which may be overly broad. **Recommendation:** Add `permissions: contents: read` after line 9. |
| S-13 | Info | `.github/workflows/validate.yml:16,19` | GitHub Actions are properly pinned to full SHA hashes. |
| S-14 | Info | `.pre-commit-config.yaml` | Includes `detect-private-key` and `detect-aws-credentials` hooks. |

---

## 2. Ansible Code Quality

### 2.1 Role Architecture — WELL-DESIGNED

All 9 roles follow a consistent pattern: `defaults/main.yml` for public API, `tasks/main.yml` as entry point with conditional includes, `handlers/main.yml` for service operations, and `meta/main.yml` for metadata. This is textbook Ansible role design.

**Strengths:**
- Every role has a README with usage examples
- Consistent use of `noqa: var-naming[no-role-prefix]` annotations for public API variables
- Proper separation: roles are components, playbooks are workflows (as documented in the design philosophy)
- Good use of `run_once: true` and `delegate_to` for cluster-aware operations

### 2.2 Role-Specific Findings

#### proxmox_ceph

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-1 | Medium | `tasks/osd_create.yml` | Old file `tasks/osd_create_OLD.yml` still exists in the repository. **Recommendation:** Remove deprecated file. |
| A-2 | Low | `tasks/main.yml` | No `block/rescue` pattern around the OSD creation sequence. If OSD creation partially fails mid-way, there is no automatic rollback. **Recommendation:** Add block/rescue around `osd_prepare.yml` and `osd_create.yml` includes. |
| A-3 | Low | `defaults/main.yml:6-7` | Network CIDRs hardcoded as defaults (`192.168.5.0/24`, `192.168.7.0/24`). These are cluster-specific. **Recommendation:** Move to empty defaults with documentation, override in group_vars (which is already done for Matrix). |

#### proxmox_cluster

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-4 | Low | `tasks/cluster_join.yml:33` | `pvecm add` requires SSH trust between nodes. If SSH keys haven't been exchanged yet (via `ssh_keys.yml`), this task fails cryptically. **Recommendation:** Add an explicit SSH connectivity check before the join attempt. |
| A-5 | Info | `tasks/cluster_join.yml:31-63` | Excellent use of `block/rescue` pattern for cluster join operations. |

#### proxmox_network

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-6 | Medium | `tasks/bridges.yml:87-91` | The changed-flag detection uses a massive `when` condition spanning one line. **Recommendation:** Simplify using a list of registered results: `when: [proxmox_network_bridge_ports_result, ...] | select('changed') | list | length > 0` |
| A-7 | Low | `tasks/bridges.yml` | Six sequential `community.general.interfaces_file` tasks configure different bridge properties. These cannot be easily consolidated due to module limitations, but could benefit from a loop with a dict of property→value mappings. |

#### proxmox_template

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-8 | Medium | `tasks/build_template.yml:37` | The `_build_template_cmd` fact is a single massive line (~500+ chars) constructing a command with 20+ conditional arguments. **Recommendation:** Build the command as a list of arguments in a separate task, then join them. This improves readability and maintainability. |
| A-9 | Info | `files/build-template.sh` | Well-engineered shell script with proper error handling (`set -euo pipefail`), cleanup traps, dry-run support, logging, and color output. |

#### proxmox_lxc

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-10 | Medium | `tasks/create.yml:4-27` | API credentials are passed as individual parameters to every task (`api_host`, `api_user`, `api_token_id`, `api_token_secret`). This is duplicated between create and start tasks. **Recommendation:** Define a `proxmox_lxc_api_params` dict in defaults and use `<<: *api_params` or a shared variable. |
| A-11 | Low | `defaults/main.yml:76` | `proxmox_lxc_nameserver: "1.1.1.1"` hardcodes Cloudflare DNS. While documented with a good comment about Tailscale MagicDNS, it should be empty by default with documentation. |

#### proxmox_repository

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-12 | Info | `tasks/main.yml` | Clean conditional task inclusion. Every sub-task is gated by a boolean flag. |

#### proxmox_tuning

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-13 | Info | Role design with profile-based configuration (`vars/profiles/minimal.yml`, `balanced.yml`, `aggressive.yml`) is excellent. Allows users to select a tuning profile without understanding individual parameters. |

#### system_user

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-14 | Low | `tasks/create_users.yml:16-22` | `.ssh` directory is only created when `ssh_keys` is defined. If a user later adds SSH keys through another mechanism, the directory may not exist. **Recommendation:** Always create `.ssh` for users with `create_home: true`. |

### 2.3 Playbook Quality

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-15 | Medium | `ansible/playbooks/.deprecated/` | 4 deprecated playbooks exist but aren't clearly marked as superseded. **Recommendation:** Add a README in `.deprecated/` explaining which roles replace each playbook. |
| A-16 | Low | Various playbooks | No consistent tagging strategy across playbooks. Three roles (`proxmox_lxc`, `proxmox_network`, `proxmox_template`) have proper tags, but there is no documented tag taxonomy. |

### 2.4 Inventory Issues

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-19 | High | `ansible/inventory/hosts.yml`, `ansible/inventory/proxmox.yml` | **Two conflicting inventory files.** Same hosts (lloyd/mable/holly) appear in `doggos_cluster` (hosts.yml) and `quantum_cluster` (proxmox.yml). Alpha/bravo are in `standalone` (hosts.yml) and `nexus_cluster` (proxmox.yml). **Recommendation:** Consolidate into single inventory file. |
| A-20 | Medium | `ansible/inventory/group_vars/` | `doggos_cluster.yml` and `quantum_cluster.yml` define conflicting cluster names for the same hosts. |

### 2.5 Playbook Issues

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-21 | High | `ansible/playbooks/deploy-omni-provider.yml:93` | Tailscale auth key passed on command line: `tailscale up --auth-key={{ tailscale_auth_key }}`. Visible in process listings and Ansible logs. **Recommendation:** Add `no_log: true`. Pass via environment variable. |
| A-22 | Medium | `ansible/playbooks/system-upgrade.yml` | `run_once: true` with `serial: 1` may unset the CEPH noout flag after first node instead of last. |
| A-23 | Medium | `ansible/playbooks/destroy-osds.yml` | Hardcodes `hosts: foxtrot` and specific OSD IDs. Should be parameterized. |

### 2.6 Configuration Issues

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-24 | Medium | `ansible/ansible.cfg:53` | Global `become = True` forces privilege escalation everywhere, conflicting with `delegate_to: localhost` tasks. **Recommendation:** Remove global become, set per-play. |

### 2.7 Cross-Cutting: Missing Tags

**6 of 9 roles have no tags in main.yml.** Three roles (`proxmox_lxc`, `proxmox_network`, `proxmox_template`) have proper tags. This is the single most impactful consistency improvement.

### 2.8 Missing Functionality

| ID | Severity | File | Finding |
|----|----------|------|---------|
| A-17 | Medium | All roles | **No Molecule tests.** The roles are tested manually (documented in goals.md) but have no automated test infrastructure. **Recommendation:** Add Molecule scenarios for at least `system_user` and `proxmox_repository` as starting points. |
| A-18 | Low | `ansible/requirements.yml` | Collection version constraints use `>=` (e.g., `>=11.4.0`). This could pull breaking changes. **Recommendation:** Use pessimistic constraints (`>=11.4.0,<12.0.0`). |
| A-25 | Low | `ansible/inventory/group_vars/all.yml` | SSH hardening variables (`ssh_password_authentication`, etc.) defined but no role applies them. |
| A-26 | Low | `ansible/inventory/group_vars/all.yml` | `system_ntp_servers` defined but no role configures NTP/chrony. |

---

## 3. Terraform/OpenTofu Review

### 3.1 State Management — CRITICAL

| ID | Severity | File | Finding |
|----|----------|------|---------|
| T-1 | Critical | `terraform/netbox-template/provider.tf`, `terraform/netbox-vm/provider.tf` | **No backend configuration.** State defaults to local filesystem, risking state loss, no locking, and sensitive data in unprotected files. The `.gitignore` mentions "managed by Scalr" but no Scalr configuration exists. **Recommendation:** Add a backend block (Scalr cloud, S3-compatible, or at minimum `backend "local"` with an explicit path). |
| T-2 | Medium | `.gitignore:19` | `.terraform.lock.hcl` is excluded. HashiCorp/OpenTofu recommends committing lock files for reproducible provider resolution. **Recommendation:** Remove this exclusion and commit lock files, or document the Scalr-managed decision. |

### 3.2 Provider Configuration

| ID | Severity | File | Finding |
|----|----------|------|---------|
| T-3 | High | All `provider.tf` files | Provider version constraint `>= 0.84.1` is too permissive. Allows any future version including major releases with breaking changes. **Recommendation:** Use `~> 0.84` to allow patches but block breaking changes. |
| T-4 | Medium | All `provider.tf` files | OpenTofu version constraint `>= 1.0` is too loose. `.mise.toml` installs `1.11.1`. **Recommendation:** Tighten to `>= 1.8, < 2.0`. |
| T-5 | Medium | `terraform/netbox-vm/variables.tf:14` | `proxmox_insecure` defaults to `true`. **Recommendation:** Default to `false` with a warning comment about self-signed certificates. |

### 3.3 Variable Issues

| ID | Severity | File | Finding |
|----|----------|------|---------|
| T-6 | Medium | `terraform/netbox-vm/terraform.tfvars.example` | References deleted variables: `cpu_type`, `boot_order`, `boot_up_delay`, `boot_down_delay`. Running `tofu plan -var-file=terraform.tfvars.example` would produce warnings. **Recommendation:** Remove stale entries. |
| T-7 | Medium | `terraform/netbox-vm/variables.tf:247-256` | `ssh_public_keys` has `default = []` but validation requires `length > 0`. The default value itself fails validation. **Recommendation:** Remove the default to make it required, or remove the validation. |
| T-8 | Medium | `terraform/netbox-template/provider.tf:33-37` | `ssh_username` variable is defined in `provider.tf` instead of `variables.tf`. **Recommendation:** Move to `variables.tf` per convention. |
| T-9 | Low | `terraform/netbox-vm/variables.tf:177` | `enable_secondary_nic` defaults to `true`. Surprising for single-VM deployments. **Recommendation:** Default to `false`. |
| T-10 | Low | `terraform/netbox-vm/variables.tf:8` | `proxmox_endpoint` has a default of `"https://proxmox.local:8006"` while `netbox-template/variables.tf:7` correctly has no default. **Recommendation:** Remove the default for consistency. |

### 3.4 Example Code

| ID | Severity | File | Finding |
|----|----------|------|---------|
| T-11 | Medium | `terraform/examples/*/main.tf` | Example module sources reference a non-existent local path `../../../modules/vm`. **Recommendation:** Update to use the external GitHub module with version pinning. |
| T-12 | Low | `terraform/examples/template-with-custom-cloudinit/` | Nearly identical to `terraform/netbox-template/`. **Recommendation:** Differentiate or remove. |

### 3.5 Missing Functionality

| ID | Severity | File | Finding |
|----|----------|------|---------|
| T-13 | Low | All Terraform configs | No `.tflint.hcl` configuration file despite TFLint being in `.mise.toml`. **Recommendation:** Create a `.tflint.hcl` with at minimum the Terraform ruleset plugin. |
| T-14 | Low | README files | Several broken links in `terraform/netbox-vm/README.md` referencing non-existent paths (`../../../modules/vm/README.md`, `../../../../docs/terraform/`). |

### 3.6 Positive Findings

- Module sources correctly pinned to `?ref=v1.0.0`
- Excellent inline documentation explaining DRY principle and why values are omitted
- Authentication via environment variables (not hardcoded)
- `.gitignore` properly excludes `.tfstate`, `.terraform/`, and `.tfvars`

---

## 4. CI/CD & DevOps Tooling

### 4.1 GitHub Actions

| ID | Severity | File | Finding |
|----|----------|------|---------|
| D-1 | High | `.github/workflows/validate.yml` | **No CI caching.** Every run installs mise tools, Python dependencies, and Ansible collections from scratch. **Recommendation:** Add `actions/cache` for `~/.local/share/mise`, `.venv/`, and Ansible collections. |
| D-2 | Medium | `.github/workflows/validate.yml` | All 9 lint/validate steps run sequentially in a single job. Independent checks (Terraform fmt, YAML lint, shell lint, markdown lint) could run in parallel jobs. **Recommendation:** Split into parallel jobs with a final status-check job. |
| D-3 | Low | `.github/workflows/validate.yml` | No `timeout-minutes` on the job. A hung step could run for up to 6 hours. **Recommendation:** Add `timeout-minutes: 15`. |

### 4.2 Pre-commit Configuration

| ID | Severity | File | Finding |
|----|----------|------|---------|
| D-4 | Medium | `.pre-commit-config.yaml:38` | `rumdl` only lints `README.md` (root). All other markdown files are excluded. **Recommendation:** Expand the `files` pattern to include `documentation/**/*.md`. |
| D-5 | Medium | `.pre-commit-config.yaml` | Missing `check-toml` hook. The repo heavily uses TOML (`.mise.toml`, `cliff.toml`, `.rumdl.toml`, `pyproject.toml`). |
| D-6 | Low | `.pre-commit-config.yaml` | Missing `no-commit-to-branch` hook to prevent direct commits to `main`. |
| D-7 | Low | `.pre-commit-config.yaml` | `terraform_validate` and `terraform_tflint` hooks are absent from pre-commit despite running in CI. |

### 4.3 Python Environment

| ID | Severity | File | Finding |
|----|----------|------|---------|
| D-8 | Critical | `.mise.toml:19`, `.python-version:1`, `pyproject.toml:7` | **Python version mismatch.** `.mise.toml` specifies `3.14.2`, `.python-version` says `3.13`, `pyproject.toml` requires `>=3.13`. **Recommendation:** Align all files to a single version. If 3.14 is intentional, update `.python-version`; if 3.13 is the target, downgrade `.mise.toml`. |
| D-9 | Low | `pyproject.toml:1` | Comment says "MicroK8s deployment" — stale from a previous project focus. |
| D-10 | Low | `pyproject.toml` | No `[tool.ruff]` configuration. Ruff uses defaults without target Python version or additional rule sets. |

### 4.4 Scripts Quality

| ID | Severity | File | Finding |
|----|----------|------|---------|
| D-11 | Medium | `scripts/validator.py:475` | Deprecated module detection has a false positive: `docker_container` in the DEPRECATED set would incorrectly flag `community.docker.docker_container` because it checks `mod.split(".")[-1]`. **Recommendation:** Only match short names when the module has no namespace: `mod in DEPRECATED and "." not in mod`. |
| D-12 | Low | `scripts/firecrawl_sdk_research.py:319` | Uses `datetime.now()` without timezone. **Recommendation:** Use `datetime.now(timezone.utc)`. |
| D-13 | Low | `scripts/firecrawl_sdk_research.py:285-301` | `asyncio.gather(*tasks)` fires all scrape requests simultaneously with no rate limiting. **Recommendation:** Add `asyncio.Semaphore(3)`. |

### 4.5 Tool Configuration

| ID | Severity | File | Finding |
|----|----------|------|---------|
| D-14 | Medium | `.mise.toml:213` | `shellcheck` task only searches `scripts/` directory, missing root-level `conductor-setup.sh`. **Recommendation:** Use `find . -name '*.sh' -not -path './.venv/*' -not -path './.git/*'`. |
| D-15 | High | `.cursor/rules/mintlify.mdc` | **Corrupted content.** Hundreds of lines of empty nested code blocks starting around line 178. **Recommendation:** Clean up or regenerate the file. |
| D-16 | Medium | `.github/copilot-instructions.md:99` | States "NO automated testing in CI" — this is incorrect, `validate.yml` provides CI testing. **Recommendation:** Update the statement. |
| D-17 | Low | `.devcontainer/devcontainer.json` | No `postCreateCommand` to run setup automatically. **Recommendation:** Add `"postCreateCommand": "mise install && mise run setup"`. |
| D-18 | Low | `conductor-setup.sh:46-48` | Uses `cd ansible` which fails if script is not run from project root. **Recommendation:** Use `pushd`/`popd` or absolute paths. |

---

## 5. Documentation & Architecture

### 5.1 Documentation Completeness — STRONG

**Positive Findings:**
- Comprehensive `documentation/README.md` serves as an effective index with "Start Here" guide
- `documentation/core/goals.md` clearly tracks achievements with checkboxes
- `documentation/core/infrastructure.md` provides detailed hardware, network, and storage specs
- Every Ansible role has a README
- Elements of Style principles documented and followed

### 5.2 Documentation Gaps

| ID | Severity | File | Finding |
|----|----------|------|---------|
| DOC-1 | Medium | `documentation/README.md` | References files that don't exist at their referenced paths: `brainstorming/next-features-2025-11.md`, `brainstorming/documentation-audit-2025-11.md`. These exist under `docs/brainstorming/` not `documentation/brainstorming/` — a path mismatch in the README. **Recommendation:** Fix the paths in the README to reference the correct location. |
| DOC-2 | Medium | `documentation/README.md:101-112` | Mintlify section says "Status: Infrastructure configured, ready for content population" and describes a `mintlify/` subdirectory structure that doesn't exist within `documentation/`. **Recommendation:** Create the directory structure or update the status. |
| DOC-3 | Low | Role documentation | `documentation/roles/` contains docs for 6 roles but the repo has 9 roles. Missing: `proxmox_template`, `proxmox_tuning`, `proxmox_lxc`. **Recommendation:** Add documentation for the missing roles. |
| DOC-4 | Low | Getting Started guides | `documentation/getting-started/` has `prerequisites.md`, `installation.md`, `first-deployment.md` but these may need updating for the current state of the project (post v1.0.0). |

### 5.3 Architecture Evaluation — SOLID

**Strengths:**
- Clean separation: Ansible for configuration, Terraform for provisioning
- Role-based architecture with clear component boundaries
- Multi-cluster inventory design (Matrix, Doggos clusters + standalone hosts)
- Consistent variable naming pattern: `proxmox_<role>_<setting>` for role-prefixed vars
- Secrets flow is well-designed: Infisical → Ansible → Environment vars → Terraform

**Areas for Growth:**

| ID | Severity | File | Finding |
|----|----------|------|---------|
| DOC-5 | Low | Overall architecture | No architecture diagram exists. The relationship between clusters, roles, playbooks, and Terraform modules would benefit from a visual representation. |
| DOC-6 | Low | `ansible/inventory/group_vars/all.yml:2` | Comment references `nexus_cluster` and `quantum_cluster` — these groups exist in `proxmox.yml` (not `hosts.yml`), so the comment is technically correct since `ansible.cfg` loads the entire `inventory/` directory. However, this is confusing given the split inventory situation (see A-19). **Recommendation:** Resolve as part of inventory consolidation (A-19). |

### 5.4 Functionality Opportunities

Based on `goals.md`, `infrastructure.md`, and `netbox-powerdns.md`, the following planned features could expand the project:

| Priority | Opportunity | Description |
|----------|-------------|-------------|
| High | **NetBox Integration Role** | `netbox-powerdns.md` describes a comprehensive IPAM/DNS architecture, but no Ansible role exists to configure NetBox or PowerDNS. This is the clear v2.0.0 target. |
| High | **Backup Automation** | `group_vars/all.yml` references a PBS server (`192.168.30.200`, status: unreachable). A `proxmox_backup` role for PBS integration would close this gap. |
| Medium | **Monitoring Stack** | No monitoring/alerting automation exists. A role deploying Prometheus + Grafana (leveraging CEPH manager's Prometheus module already enabled) would provide observability. |
| Medium | **Doggos Cluster Configuration** | `doggos_cluster` exists in inventory but has no group_vars. Likely needs the same configuration treatment as Matrix. |
| Low | **TrueNAS Storage Integration** | `group_vars/all.yml` references `truenas_server` but no role manages NFS/iSCSI integration with Proxmox. |
| Low | **SSH Hardening Role** | SSH variables are defined in `group_vars/all.yml` but no role applies them. A lightweight `ssh_hardening` role could enforce the configuration. |

---

## 6. Code Simplification Opportunities

| ID | Area | File | Suggestion |
|----|------|------|------------|
| CS-1 | Ansible | `proxmox_lxc/tasks/create.yml` | Extract repeated API credential parameters into a shared dict variable to reduce duplication between create/start/destroy tasks. |
| CS-2 | Ansible | `proxmox_network/tasks/bridges.yml:87-91` | Replace the massive single-line `when` condition with a list filter: `when: registered_results \| select('changed') \| list \| length > 0` |
| CS-3 | Ansible | `proxmox_template/tasks/build_template.yml:37` | Build the template command as a list variable instead of a single fact with 20+ inline conditionals. |
| CS-4 | Terraform | `terraform/examples/` | Remove or differentiate the near-duplicate example that mirrors `netbox-template/`. |
| CS-5 | Scripts | `scripts/validator.py:270-285` | Replace string-prefix heuristic for task boundary detection with proper YAML structure parsing. |
| CS-6 | CI/CD | `.github/workflows/validate.yml` | Parallelize independent lint jobs to reduce CI wall-clock time. |

---

## 7. Top Recommendations (Prioritized)

### Must-Do (Critical/High)

1. **Add Terraform backend configuration** for state management — even `backend "local"` with an explicit path is better than implicit default (T-1)
2. **Consolidate conflicting inventory files** — `hosts.yml` and `proxmox.yml` have overlapping groups (A-19)
3. **Add `permissions: contents: read`** to `validate.yml` workflow (S-12)
4. **Resolve Python version mismatch** across `.mise.toml`, `.python-version`, and `pyproject.toml` (D-8)
5. **Tighten provider version constraints** from `>= 0.84.1` to `~> 0.84` (T-3)
6. **Add CI caching** for mise tools, Python venv, and Ansible collections (D-1)
7. **Fix Tailscale auth key exposure** — add `no_log: true` in deploy-omni-provider.yml (A-21)
8. **Clean up corrupted `.cursor/rules/mintlify.mdc`** (D-15)

### Should-Do (Medium)

9. **Add tags to all 6 roles** missing them — follow `proxmox_lxc` as the model (A-27)
10. Fix `terraform.tfvars.example` drift — remove references to deleted variables (T-6)
11. Fix `ssh_public_keys` default/validation conflict (T-7)
12. Add Molecule test infrastructure for at least 2 roles (A-17)
13. Fix input validation for pveum commands — use `argv` form (S-7)
14. Expand markdown linting coverage beyond `README.md` (D-4)
15. Add `check-toml` pre-commit hook (D-5)
16. Fix broken example module source paths (T-11)
17. Make proxmox_access role updates idempotent (PA-2)
18. Remove global `become = True` from ansible.cfg (A-24)
19. Use `module_defaults` in proxmox_lxc to reduce API parameter duplication (A-10)
20. Update incorrect statement in `copilot-instructions.md` about CI (D-16)
21. Fix `validator.py` deprecated module false positive (D-11)
22. Rename generic `validate_certs` variable in proxmox_repository (PR-2)

### Nice-to-Have (Low)

23. Delete deprecated playbooks and `osd_create_OLD.yml` (A-1, A-15)
24. Create missing role documentation for `proxmox_template`, `proxmox_tuning`, `proxmox_lxc` (DOC-3)
25. Add architecture diagram (DOC-5)
26. Update `group_vars/all.yml` comment to reflect actual clusters (DOC-6)
27. Add `no-commit-to-branch` pre-commit hook (D-6)
28. Add `devcontainer.json` postCreateCommand (D-17)
29. Create `.tflint.hcl` configuration (T-13)
30. Commit `.terraform.lock.hcl` files (T-2)
31. Add timeout-minutes to CI workflow (D-3)
32. Use pessimistic constraints for Ansible collection versions (A-18)
33. Create SSH hardening and NTP configuration roles (A-25, A-26)

---

## Appendix: Files Reviewed

### Security
- `.gitignore`, `.infisical.json`
- `ansible/tasks/infisical-secret-lookup.yml`
- `ansible/roles/proxmox_access/` (all tasks, templates, defaults)
- `ansible/roles/system_user/` (all tasks, templates, defaults)
- `ansible/roles/proxmox_ceph/tasks/osd_create.yml`
- `.github/workflows/validate.yml`
- `.pre-commit-config.yaml`

### Ansible
- All 9 roles: `proxmox_ceph`, `proxmox_cluster`, `proxmox_network`, `proxmox_template`, `proxmox_access`, `system_user`, `proxmox_tuning`, `proxmox_lxc`, `proxmox_repository`
- All playbooks in `ansible/playbooks/`
- `ansible/inventory/` (hosts.yml, all group_vars)
- `ansible/ansible.cfg`, `ansible/requirements.yml`, `ansible/.ansible-lint`

### Terraform
- `terraform/netbox-template/` (all .tf files)
- `terraform/netbox-vm/` (all .tf files, terraform.tfvars.example, outputs.tf)
- `terraform/examples/` (both example directories)
- `terraform/README.md`

### CI/CD & Scripts
- `.github/workflows/` (both workflow files)
- `.pre-commit-config.yaml`
- `scripts/validator.py`, `scripts/firecrawl_sdk_research.py`
- `conductor-setup.sh`
- `.mise.toml`, `renovate.json`, `.yamllint`, `.rumdl.toml`, `cliff.toml`
- `.devcontainer/devcontainer.json`
- `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/mintlify.mdc`

### Documentation
- `documentation/` (all files)
- Root `README.md`, `ansible/README.md`, `scripts/README.md`
- All role READMEs
- `documentation/core/goals.md`, `documentation/core/infrastructure.md`
