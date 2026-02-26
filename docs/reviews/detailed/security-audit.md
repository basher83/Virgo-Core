# Security Audit Report: Virgo-Core

**Audit Date:** 2026-02-26
**Scope:** Secrets Management, Access Control, Input Validation, CI/CD Security, General IaC Security

---

## 1. SECRETS MANAGEMENT

### Finding 1.1 -- Infisical Project ID Committed to Repository

- **Severity:** Medium
- **Files and Lines:**
  - `.infisical.json` (line 2): `"workspaceId": "7b832220-24c0-45bc-a5f1-ce9794a31259"`
  - `ansible/inventory/group_vars/all.yml` (line 36): `infisical_project_id`
  - `ansible/tasks/infisical-secret-lookup.yml` (lines 52, 64): hardcoded as default
  - `ansible/playbooks/deploy-omni-provider.yml` (line 17): hardcoded
  - `ansible/playbooks/setup-terraform-automation.yml` (line 48): hardcoded
- **Description:** The Infisical workspace/project ID is hardcoded in 6+ files and `.infisical.json` is not in `.gitignore`. While not a credential, it provides targeting information for the secrets vault.
- **Recommendation:** Add `.infisical.json` to `.gitignore`. Centralize the project ID in a single `group_vars/all.yml` location.

### Finding 1.2 -- Token Values Potentially Logged in Deprecated Playbook

- **Severity:** Medium
- **File:** `ansible/playbooks/.deprecated/proxmox-create-terraform-user.yml` (lines 196-207)
- **Description:** The deprecated playbook displays API tokens via `ansible.builtin.debug` without `no_log: true`. The active role (`proxmox_access/tasks/tokens.yml`) correctly uses `no_log`.
- **Recommendation:** Delete the deprecated playbooks since migration is complete.

### Finding 1.3 -- Terraform Environment File Directory Permissive

- **Severity:** Low
- **File:** `ansible/roles/proxmox_access/tasks/env_export.yml` (line 9)
- **Description:** Directory created with mode `0755` (world-readable). Individual files are `0600`, but directory allows listing.
- **Recommendation:** Change directory mode to `0700`.

### Finding 1.4 -- Secrets Correctly Handled (Positive)

- **Severity:** Info
- **Description:** Infisical lookup uses `no_log: true` on all steps. `.gitignore` excludes `.vault_pass.txt`, `terraform.tfvars`, `.envrc`. Pre-commit includes `detect-private-key` and `detect-aws-credentials`.

---

## 2. ACCESS CONTROL

### Finding 2.1 -- Sudo Wildcard Allows Arbitrary File Write

- **Severity:** High
- **Files:**
  - `ansible/playbooks/.deprecated/add-system-user.yml` (line 27): `"/usr/bin/tee /var/lib/vz/*"`
  - `ansible/playbooks/setup-terraform-automation.yml` (lines 63-64): restricted to `template/*` and `images/*`
- **Description:** Deprecated playbooks use broad wildcard. Active playbook is better but `tee` with sudo is inherently dangerous.
- **Recommendation:** Delete deprecated playbooks. Consider more targeted file operations.

### Finding 2.2 -- API Token with privsep=false at Root Path

- **Severity:** Medium
- **File:** `ansible/playbooks/setup-terraform-automation.yml` (line 134)
- **Description:** `privsep: false` means the token inherits full user permissions. ACL on path `/` grants cluster-wide access.
- **Recommendation:** Enable `privsep: true` and scope ACL paths more narrowly.

### Finding 2.3 -- Sudo Rules Not Validated for Absolute Paths

- **Severity:** Medium
- **File:** `ansible/roles/system_user/templates/sudoers.j2`
- **Description:** Template comments warn about absolute paths but no validation task enforces it.
- **Recommendation:** Add assertion in `sudo_config.yml` that all `sudo_rules` start with `/`.

### Finding 2.4 -- Root SSH Login Permitted

- **Severity:** Low
- **File:** `ansible/inventory/group_vars/all.yml` (line 25)
- **Description:** `ssh_permit_root_login: "yes"` across all nodes. Key-only authentication mitigates risk.
- **Recommendation:** Use `"prohibit-password"` for defense in depth.

---

## 3. INPUT VALIDATION

### Finding 3.1 -- Command Injection Surface in pveum Commands

- **Severity:** High
- **Files:**
  - `ansible/roles/proxmox_access/tasks/users.yml` (lines 12-13)
  - `ansible/roles/proxmox_access/tasks/tokens.yml` (lines 16-17)
  - `ansible/roles/proxmox_access/tasks/roles.yml` (lines 11-12)
- **Description:** `ansible.builtin.command` with folded block scalar (`>`) passes variables through string interpolation. Comment fields containing special characters could cause unexpected behavior.
- **Recommendation:** Use `argv` form of `command` module. Add validation tasks checking values against `^[a-zA-Z0-9@._-]+$`.

### Finding 3.2 -- CEPH OSD Device Paths Not Validated

- **Severity:** Medium
- **File:** `ansible/roles/proxmox_ceph/tasks/osd_create.yml` (lines 26, 69)
- **Description:** Device paths passed directly to `pveceph osd create` and `ceph-volume lvm batch` without validation.
- **Recommendation:** Assert device paths match `/dev/[a-z]+[0-9]*`.

### Finding 3.3 -- Terraform Variable Validation (Positive)

- **Severity:** Info
- **File:** `terraform/netbox-vm/variables.tf`
- **Description:** Comprehensive validation blocks for VM names, IPs, CPU, memory, disk sizes, CIDR. Well done.

---

## 4. CI/CD SECURITY

### Finding 4.1 -- Validate Workflow Missing Permissions Block

- **Severity:** High
- **File:** `.github/workflows/validate.yml`
- **Description:** No explicit `permissions:` block. Inherits default token scope.
- **Recommendation:** Add `permissions: contents: read`.

### Finding 4.2 -- GitHub Actions SHA-Pinned (Positive)

- **Severity:** Info
- **Description:** All actions pinned to commit SHAs. Best practice.

---

## 5. GENERAL IaC SECURITY

### Finding 5.1 -- TLS Verification Disabled Everywhere

- **Severity:** Medium
- **Files:** All `provider.tf` files, `proxmox_access/defaults/main.yml`, `terraform_env.sh.j2`
- **Description:** TLS certificate verification disabled for all Proxmox API connections. MITM vulnerability.
- **Recommendation:** Deploy proper certificates. Make `PROXMOX_VE_INSECURE` configurable in template.

### Finding 5.2 -- Curl-pipe-to-shell for Tailscale

- **Severity:** Medium
- **File:** `ansible/playbooks/deploy-omni-provider.yml` (line 92)
- **Description:** `curl -fsSL https://tailscale.com/install.sh | sh` plus auth key on command line.
- **Recommendation:** Download, verify checksum, then execute. Pass auth key via environment variable.

### Finding 5.3 -- Cloud Image Checksum Not Required

- **Severity:** Low
- **File:** `terraform/netbox-template/variables.tf` (lines 86-90)
- **Description:** Checksum defaults to `null`. Unverified downloads could be tampered with.
- **Recommendation:** Make checksum required or add a warning validation.

### Finding 5.4 -- No Terraform State Backend

- **Severity:** Medium
- **File:** All `provider.tf` files
- **Description:** State stored locally. No locking, no encryption, risk of loss.
- **Recommendation:** Configure a remote backend.

---

## Summary

| Severity | Count |
|----------|-------|
| High | 3 |
| Medium | 8 |
| Low | 4 |
| Info (Positive) | 4 |

**Top 3 Priorities:**
1. Fix command injection surface in pveum commands (3.1)
2. Add permissions block to CI workflow (4.1)
3. Delete deprecated playbooks with security issues (2.1, 1.2)
