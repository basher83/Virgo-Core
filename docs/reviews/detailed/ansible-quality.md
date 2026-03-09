# Ansible Code Quality Review: Virgo-Core

**Review Date:** 2026-02-26
**Scope:** All 9 Ansible roles, playbooks, inventory, configuration

---

## Role Architecture Summary

All 9 roles follow a consistent pattern: `defaults/main.yml` for public API, `tasks/main.yml` as conditional entry point, `handlers/main.yml` for service operations, and `meta/main.yml` for metadata. The `proxmox_lxc` role is the gold standard with proper tagging, validation, and secrets integration.

---

## 1. system_user Role

### SU-1: Missing tags on all tasks (Medium)
Missing tags on all tasks. Makes selective execution impossible.

### SU-2: sudoers.j2 template variable mismatch (Medium)
The template references `user_item.name` and `user_item.sudo_nopasswd` which are set by the loop variable in `sudo_config.yml`. However, the template's conditional for `NOPASSWD:ALL` vs limited rules needs verification that it properly handles both cases. The template does handle both paths (lines 7-21).

### SU-3: .ssh directory only created when keys defined (Low)
If keys are later added through another mechanism, the directory may not exist. Consider always creating it.

---

## 2. proxmox_access Role

### PA-1: Roles cannot be updated, only created (Medium)
`tasks/roles.yml` only creates roles when name not found. If privileges need to change, there is no `pveum role modify` path. Not idempotent for updates.

**Recommendation:** Add update step using `pveum role modify`.

### PA-2: Token creation lacks robust idempotency (Medium)
Token existence check may not match properly. Token secret not captured for later storage.

### PA-3: Debug message exposes username (Low)
`tasks/secrets.yml:17` logs `"Proxmox API credentials retrieved for {{ proxmox_api_user }}"`.

### PA-4: Missing tags (Medium)
No tags on include_tasks in main.yml.

---

## 3. proxmox_network Role

### PN-1: Well-structured role (Positive)
Proper handlers, prerequisites, verification, dry-run, and backup. Model for other roles.

### PN-2: Massive single-line when condition (Medium)
`tasks/bridges.yml:87-91` has a giant inline condition for change detection.

**Recommendation:** Use list filter: `when: registered_results | select('changed') | list | length > 0`

### PN-3: Proper tagging (Positive)
Tags on every include_tasks in main.yml (`[proxmox_network, prerequisites]`, `[proxmox_network, bridges]`, etc.).

---

## 4. proxmox_repository Role

### PR-1: Variable naming inconsistency (Medium)
Mixed prefixes: some use `proxmox_` (e.g., `proxmox_version`) while others don't (`auto_update_packages`, `validate_certs`).

### PR-2: Generic `validate_certs` name collision risk (Medium)
Will collide with any other role using the same variable name.

**Recommendation:** Rename to `proxmox_repository_validate_certs`.

### PR-3: Subscription banner patch fragile across PVE versions (Low)
JavaScript replacement will break on Proxmox upgrades. Should document tested versions.

---

## 5. proxmox_cluster Role

### PC-1: Good block/rescue pattern (Positive)
`tasks/cluster_join.yml` properly uses block/rescue for join operations.

### PC-2: SSH key exchange lacks error handling (Medium)
If a node is unreachable during key exchange, cluster join fails later without clear error.

### PC-3: Missing tags (Medium)

---

## 6. proxmox_ceph Role

### CE-1: Stale file osd_create_OLD.yml (Low)
Should be removed. Not referenced anywhere.

### CE-2: Missing health check before OSD operations (Medium)
No verification that CEPH is healthy before adding OSDs.

**Recommendation:** Add `ceph health` assertion at start of `osd_create.yml`.

### CE-3: Complex OSD creation well-handled (Positive)
Multi-partition support, safety gates, existence checks are thorough.

### CE-4: Missing tags (Medium)

---

## 7. proxmox_template Role

### PT-1: Best-structured role (Positive)
Proper validation, Infisical integration, dry-run, verification, comprehensive docs.

### PT-2: Build command is a massive single line (Medium)
`tasks/build_template.yml:37` constructs a 500+ character command.

**Recommendation:** Build as list of arguments, then join.

### PT-3: Proper tagging (Positive)
Tags on every include_tasks in main.yml (`[proxmox_template, validate]`, `[proxmox_template, secrets]`, etc.).

---

## 8. proxmox_tuning Role

### TU-1: Excellent profile system (Positive)
Three profiles (minimal/balanced/aggressive) with `include_vars` is elegant.

### TU-2: Variable names lack role prefix (Medium)
Names like `net_core_rmem_max` are extremely generic and will collide.

### TU-3: Flush handlers before verify (Positive)
Good practice other roles should adopt.

---

## 9. proxmox_lxc Role

### LX-1: Best-in-class tagging (Positive)
One of three roles (with `proxmox_network` and `proxmox_template`) with proper tags on every include_tasks. Sets the standard for tag naming convention.

### LX-2: Comprehensive validation (Positive)
`validate.yml` checks all required variables with clear messages.

### LX-3: Repeated API credential parameters (Medium)
5 API parameters repeated 8 times across tasks.

**Recommendation:** Use `module_defaults` block.

---

## Playbook Findings

### PB-1: Duplicate template playbooks (Medium)
`create-template.yml` and `create-template-doggos.yml` should be consolidated.

### PB-2: Tailscale auth key exposed on command line (High)
`deploy-omni-provider.yml` line 93: auth key visible in process listings and logs.

**Recommendation:** Add `no_log: true`. Pass key via environment variable.

### PB-3: destroy-osds.yml hardcodes host and OSD IDs (Medium)
Should be parameterized with extra vars and require confirmation.

### PB-4: system-upgrade.yml noout flag race condition (Medium)
`run_once: true` with `serial: 1` may unset noout after first node instead of last.

### PB-5: initialize-matrix-cluster.yml well-structured (Positive)
Block/rescue, confirmation prompt, comprehensive post_tasks.

---

## Inventory Issues

### IN-1: Two conflicting inventory files (High)
`hosts.yml` and `proxmox.yml` have overlapping/conflicting group memberships. Same hosts appear in different clusters.

**Recommendation:** Consolidate into single inventory file.

### IN-2: doggos_cluster vs quantum_cluster confusion (Medium)
Same hosts (lloyd/mable/holly) in both groups.

### IN-3: Missing node_id for doggos_cluster (Low)
Matrix cluster has node_id, doggos does not. Network templates using `{{ node_id }}` will fail.

---

## Configuration

### CF-1: Global become=True in ansible.cfg (Medium)
Forces privilege escalation everywhere, conflicting with `delegate_to: localhost` tasks.

**Recommendation:** Remove global become, set per-play.

### CF-2: no-changed-when in ansible-lint skip_list (Medium)
May mask legitimate missing `changed_when` conditions.

---

## Missing Functionality

### MF-1: No Molecule tests (High)
None of the 9 roles have automated tests.

### MF-2: No preflight validation playbook (Medium)
No way to validate environment readiness before deployment.

### MF-3: SSH hardening variables declared but unused (Low)
`group_vars/all.yml` defines SSH variables but no role applies them.

### MF-4: NTP servers defined but no role configures them (Low)
`system_ntp_servers` is set but unused.

### MF-5: No proxmox_storage role (Medium)
Storage backend management not automated.

### MF-6: Duplicate sudoers template (Low)
`ansible/templates/sudoers.j2` (legacy) duplicates `roles/system_user/templates/sudoers.j2`.

---

## Cross-Cutting: Missing Tags

**6 of 9 roles have no tags in main.yml.** Three roles (`proxmox_lxc`, `proxmox_network`, `proxmox_template`) have proper tags. This is the single most impactful consistency improvement.

| Role | Tags? |
|------|-------|
| system_user | No |
| proxmox_access | No |
| proxmox_network | **Yes** |
| proxmox_repository | No |
| proxmox_cluster | No |
| proxmox_ceph | No |
| proxmox_template | **Yes** |
| proxmox_tuning | No |
| proxmox_lxc | **Yes** |

---

## Summary

| Priority | Count | Top Items |
|----------|-------|-----------|
| High | 3 | Conflicting inventory, Tailscale auth key exposure, no Molecule tests |
| Medium | 23 | Missing tags (x6), variable collisions, idempotency gaps, command construction |
| Low | 8 | Stale files, naming, missing documentation |
| Positive | 11 | proxmox_lxc design, proxmox_network structure and tagging, proxmox_template tagging, tuning profiles, cluster join error handling |
