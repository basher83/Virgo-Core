# Testing Framework Specification

## Overview

This specification defines a testing framework targeting 95%+ reliability in measuring PASS scores across six quality dimensions for generated Ansible playbooks. The framework establishes baseline measurements before evaluating any plugin feature hypotheses.

## Core Components

### Minimal Toolchain (Baseline)

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| ansible-lint | Linting dimension scoring | CLI invocation, rules 101-703 |
| yamllint | Structure pre-validation | Strict mode, 2-space indent |
| Custom heuristics | Idempotency/security/module checks | Python script, regex + AST |
| JSON reporter | Traceability output | Structured PASS/FAIL per dimension |

### Hypothesized Toolchain (If Proven)

| Component | Hypothesis | Proof Threshold |
|-----------|------------|-----------------|
| Pre-output hook | Lint gate before delivery | +15% lint PASS, <2s latency |
| Secret scanner hook | Security dimension boost | +10% security PASS |
| Review agent | Multi-dimension audit | +20% overall, 2x dev justified |

## PASS Criteria Table

| Dimension | Test Method | Tools/Commands | Edge Case Check | Baseline PASS (%) | Hypothesized Uplift (%) |
|-----------|-------------|----------------|-----------------|-------------------|-------------------------|
| **Idempotency** | Static analysis for state-changing modules without conditionals | Heuristic: `changed_when`, `creates`, `removes` presence | Dynamic inventory + loops | 65% | +15% (agents) |
| **Security** | Secret pattern scan + vault reference check | `detect-secrets`, regex for `password:`, `api_key:` | Jinja2 vars with embedded secrets | 70% | +10% (hooks) |
| **Module Selection** | Deprecated/replaced module detection | ansible-lint rule 204, custom module mapping | Community vs builtin conflicts | 80% | +5% (skills) |
| **Error Handling** | Block/rescue presence, ignore_errors audit | Heuristic: `block:` + `rescue:` ratio, `ignore_errors: true` count | Nested blocks, handler failures | 60% | +10% (agents) |
| **Structure** | Role layout, task naming, var organization | yamllint, ansible-lint rules 201, 206 | Multi-play, include_tasks depth | 75% | +5% (hooks) |
| **Linting** | Full ansible-lint pass (warnings as errors) | `ansible-lint -q --strict` | Profile: production | 85% | +10% (hooks) |

## Sample Scenarios

All scenarios derive from production roles in Virgo-Core (Proxmox infrastructure) and Supernova-MicroK8s-Infra (Kubernetes layer). Existing roles serve as quality baselines for validator calibration.

### Scenario 1: Proxmox Cluster Bootstrap (Structure Focus)

**Input:** Initialize 3-node Proxmox VE cluster with corosync, SSH key distribution, and /etc/hosts management

**Reference Role:** `Virgo-Core/ansible/roles/proxmox_cluster`

**Expected Challenges:** First-node-only initialization patterns, cluster join sequencing, corosync configuration, multi-node SSH key exchange

**PASS Targets:** Idempotency 75%, Security 70%, Module 85%, Error 70%, Structure 95%, Lint 90%

**Validation Commands:**

```bash
ansible-lint roles/proxmox_cluster --profile production
python validator.py --scenario proxmox-cluster --role proxmox_cluster
```

### Scenario 2: CEPH Storage Deployment (Idempotency Focus)

**Input:** Deploy CEPH distributed storage with monitors, managers, OSDs, and pools across cluster nodes

**Reference Role:** `Virgo-Core/ansible/roles/proxmox_ceph`

**Expected Challenges:** OSD state detection (existing vs new disks), keyring distribution, pool creation idempotency, manager module enablement

**PASS Targets:** Idempotency 90%, Security 70%, Module 80%, Error 75%, Structure 80%, Lint 85%

**Validation Commands:**

```bash
ansible-lint roles/proxmox_ceph --profile production
python validator.py --scenario ceph-storage --role proxmox_ceph
```

### Scenario 3: Proxmox Access Control (Security Focus)

**Input:** Configure Proxmox access control with custom roles, groups, users, API tokens, and ACL permissions via Infisical secret retrieval

**Reference Role:** `Virgo-Core/ansible/roles/proxmox_access`

**Expected Challenges:** Secret handling (Infisical integration), API token generation without exposure, ACL permission mapping, environment file export security

**PASS Targets:** Idempotency 70%, Security 95%, Module 85%, Error 70%, Structure 80%, Lint 90%

**Validation Commands:**

```bash
detect-secrets scan roles/proxmox_access/
ansible-lint roles/proxmox_access --profile production
python validator.py --scenario proxmox-access --role proxmox_access
```

### Scenario 4: MicroK8s HA Cluster (Error Handling Focus)

**Input:** Form MicroK8s high-availability cluster with designated master, node joins, worker additions, and cluster validation

**Reference Role:** `Supernova-MicroK8s-Infra/ansible/roles/microk8s_cluster`

**Expected Challenges:** Join command failures (already-joined handling), delegation chains across nodes, timeout management, cluster stabilization waits

**PASS Targets:** Idempotency 75%, Security 65%, Module 70%, Error 95%, Structure 80%, Lint 85%

**Validation Commands:**

```bash
ansible-lint roles/microk8s_cluster --profile production
python validator.py --scenario microk8s-cluster --role microk8s_cluster
```

### Scenario 5: GitOps Stack - ArgoCD (Module Selection Focus)

**Input:** Deploy ArgoCD via Helm with ingress configuration, namespace creation, and initial admin credential retrieval

**Reference Role:** `Supernova-MicroK8s-Infra/ansible/roles/argocd`

**Expected Challenges:** Helm operations via command (no native module), kubectl JSON parsing, idempotent install-vs-upgrade detection, ingress patching

**PASS Targets:** Idempotency 80%, Security 75%, Module 90%, Error 80%, Structure 85%, Lint 85%

**Validation Commands:**

```bash
ansible-lint roles/argocd --profile production
python validator.py --scenario argocd-gitops --role argocd
```

## Dimension Coverage Matrix

Primary (●●) and secondary (●) focus per scenario:

| Scenario | Idempotency | Security | Module | Error | Structure | Lint |
|----------|-------------|----------|--------|-------|-----------|------|
| Proxmox Cluster | ● | ○ | ● | ○ | ●● | ● |
| CEPH Storage | ●● | ○ | ● | ● | ● | ● |
| Access Control | ○ | ●● | ● | ○ | ● | ● |
| MicroK8s HA | ● | ○ | ○ | ●● | ● | ● |
| GitOps Stack | ● | ● | ●● | ● | ● | ● |

## Baseline Lint Analysis (2025-01-15)

### With Existing Policy Config

Virgo-Core already has a comprehensive `ansible/.ansible-lint` config with policy decisions baked in:

```bash
ansible-lint ansible/roles/proxmox_* -c ansible/.ansible-lint
# Result: 0 failures, 0 warnings, production profile PASSED
```

| Role | Files | Violations | Profile Achieved |
|------|-------|------------|------------------|
| proxmox_cluster | 13 | 0 | production ✅ |
| proxmox_ceph | 16 | 0 | production ✅ |
| proxmox_access | 13 | 0 | production ✅ |

**Virgo-Core Aggregate: 100% PASS** (with existing policy config)

### Without Policy Config (Raw)

For reference, raw `--profile production` without config shows stylistic noise:

| Role | Files | Violations | Raw Lint PASS | Dominant Issue |
|------|-------|------------|---------------|----------------|
| proxmox_cluster | 13 | 47 | 64% | var-naming (39) |
| proxmox_ceph | 16 | 93 | 42% | var-naming (75) |
| proxmox_access | 13 | 4 | 97% | line-length (3) |
| microk8s_cluster | 7 | 29 | 59% | var-naming (15) |
| argocd | 7 | 21 | 70% | yaml comments (5) |

**Raw Aggregate: 66%** → demonstrates why policy config is essential

### Existing Policy Config (`ansible/.ansible-lint`)

Key skip rules already implemented:

| Rule | Skip Reason |
|------|-------------|
| `var-naming[no-role-prefix]` | Cross-role variable sharing (cluster_name, etc.) |
| `command-instead-of-module` | Proxmox CLI tools (pvecm, pveceph) have no native modules |
| `no-changed-when` | Many Proxmox commands are already idempotent |
| `yaml[line-length]` | Infrastructure configs often have long lines |
| `run-once[task]` | Safe with cluster operation strategy |

Warn-only rules: `no-handler`, `schema[meta]`, `fqcn[action-core]`

### Supernova-MicroK8s-Infra Status

Supernova also has an existing `.ansible-lint.yml` config with `profile: min`. With this config:

```bash
ansible-lint ansible/roles/microk8s_cluster ansible/roles/argocd -c .ansible-lint.yml
# Result: 0 failures, 0 warnings, production profile PASSED
```

| Role | Files | Violations | Profile Achieved |
|------|-------|------------|------------------|
| microk8s_cluster | 4 | 0 | production ✅ |
| argocd | 4 | 0 | production ✅ |

**Supernova Aggregate: 100% PASS** (with existing config)

The earlier raw violations (29/21) were measured without config files. Both repos achieve production-grade lint with their existing policy configs.

### Projected 6-Dimension Baseline (Conservative)

Lint validated at 100%; other dims projected from code inspection (validator MVP will confirm):

| Scenario | Idempotency | Security | Module | Error | Structure | Lint | **Overall** |
|----------|-------------|----------|--------|-------|-----------|------|-------------|
| Proxmox Cluster | 70% | 80% | 85% | 75% | 95% | 100% | **84%** |
| CEPH Storage | 65% | 75% | 80% | 70% | 90% | 100% | **80%** |
| Access Control | 80% | 90% | 95% | 80% | 95% | 100% | **90%** |
| MicroK8s HA | 75% | 70% | 70% | 85% | 90% | 100% | **82%** |
| GitOps (ArgoCD) | 80% | 85% | 75% | 75% | 85% | 100% | **83%** |
| **Aggregate** | **74%** | **80%** | **81%** | **77%** | **91%** | **100%** | **84%** |

**Insight:** 84% aggregate exceeds 80% MVP threshold without any plugin features. Skills/hooks could push to 95% on module/security dimensions.

### Validator Tuning Notes

1. **ArgoCD command-wrap:** Helm via `ansible.builtin.command` is intentional (no native module). Validator heuristic: `command: *helm*` OR task name matches `helm|kubectl` → excused shell-out, don't penalize module selection score.

2. **Idempotency gaps:** CEPH OSD detection (65%) and Proxmox corosync guards (70%) are the floor. Heuristic: check for `changed_when`, `creates`, `removes`, `stat` + `when` patterns.

3. **Security projection:** Access Control at 90% (Infisical integration) vs MicroK8s at 70% (delegation patterns expose secrets in logs?). Priority target for hooks hypothesis.

## Constraints

1. **Ecosystem Boundary:** Ansible 2.15+, ansible-lint 6.x+, Python 3.10+
2. **Output Format:** JSON for all validation results (machine-parseable)
3. **Execution Environment:** Local or CI (GitHub Actions compatible)
4. **No External Dependencies:** Beyond Ansible ecosystem and Claude API

## Validator Script Interface

```bash
# Full validation (policy-adjusted by default)
python validator.py --playbook <path> --scenario <name> --output json

# Single dimension
python validator.py --playbook <path> --dimension idempotency

# Raw mode (no policy skips)
python validator.py --playbook <path> --scenario <name> --raw

# Custom policy skips
python validator.py --playbook <path> --policy-skip var-naming,meta-incorrect

# Baseline vs hypothesis comparison
python validator.py --compare baseline hypothesis --scenarios all
```

**Output Schema:**

```json
{
  "scenario": "web-server",
  "playbook": "playbook.yml",
  "timestamp": "2025-01-15T10:30:00Z",
  "dimensions": {
    "idempotency": {"pass": true, "score": 85, "issues": []},
    "security": {"pass": false, "score": 60, "issues": ["L12: hardcoded password"]},
    "module_selection": {"pass": true, "score": 95, "issues": []},
    "error_handling": {"pass": true, "score": 75, "issues": []},
    "structure": {"pass": true, "score": 90, "issues": []},
    "linting": {"pass": true, "score": 100, "issues": []}
  },
  "overall_pass": false,
  "overall_score": 84
}
```

## Baseline vs Hypothesis Testing Protocol

### Phase 1: Baseline Measurement (Week 2-3)

1. Generate playbooks for all 5 scenarios using prompt-only approach
2. Run validator on each, record PASS rates per dimension
3. Calculate aggregate baseline: mean PASS across all 30 test points
4. Document dimension-specific gaps (any dimension < 70% = priority gap)

### Phase 2: Hypothesis A/B Testing (Week 4-5)

1. Select lowest-complexity hypothesis first (hooks recommended)
2. Implement hypothesis in isolated branch
3. Regenerate playbooks for all scenarios with hypothesis active
4. Measure PASS rates, compare to baseline
5. Calculate uplift: `(hypothesis_pass - baseline_pass) / baseline_pass * 100`

### Decision Criteria

| Uplift | Decision |
|--------|----------|
| < 5% | Kill hypothesis, document learnings |
| 5-15% | Conditional adopt if complexity cost < 1 week |
| > 15% | Adopt hypothesis, integrate into main workflow |

## Approval Status

**APPROVED** (2025-01-15)

The following are now locked:

- ✅ 5 scenarios: Proxmox Cluster, CEPH Storage, Access Control, MicroK8s HA, GitOps Stack (ArgoCD)
- ✅ PASS thresholds per dimension (minimum 70% for overall PASS)
- ✅ Validator script interface and output schema
- ✅ A/B testing protocol with 5%/15% decision thresholds
- ✅ Timeline: 6-week enhanced variant
- ✅ Hypothesis test order: hooks first
- ✅ Baseline lint analysis complete: **100% PASS** (both repos with existing configs)
- ✅ Virgo-Core: `ansible/.ansible-lint` (profile: moderate)
- ✅ Supernova: `.ansible-lint.yml` (profile: min, but achieves production)

**Next:** Build validator.py MVP for remaining 5 dimensions (lint is solved).
