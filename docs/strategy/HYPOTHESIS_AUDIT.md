# Hypothesis Audit

## Overview

This document audits four Claude Code plugin features as hypotheses for improving PASS rates on Ansible playbook generation. Each hypothesis is evaluated against a null baseline (no feature) with explicit proof requirements and kill switches.

## Hypothesis Details

### Hypothesis 1: Skills

**Feature Description:** Inject domain-specific context (Ansible best practices, module documentation, security patterns) via a dedicated skill that loads before generation.

**Null Hypothesis:** Prompt template alone provides sufficient context for module selection and pattern adherence.

**Alternative Hypothesis:** Skill-based context injection improves module selection accuracy by surfacing correct module names, parameters, and deprecation warnings.

| Attribute | Value |
|-----------|-------|
| Target Dimension | Module Selection |
| Expected Uplift | +10% PASS |
| Complexity Cost | 1 week dev, ongoing maintenance |
| Proof Method | A/B: 5 scenarios, module selection PASS rate |
| Kill Threshold | < 5% uplift OR > 500ms latency added |

**Proof Plan:**

1. Build skill with curated Ansible module reference (top 50 modules)
2. Generate playbooks with/without skill loaded
3. Measure module selection PASS: correct module, no deprecated modules, proper parameters
4. Compare latency impact (skill load time + generation time)

**Risk Assessment:** Skill content becomes stale as Ansible evolves. Maintenance burden may exceed benefit. If module selection baseline is already 80%+, uplift ceiling is limited.

### Hypothesis 2: Commands

**Feature Description:** Slash commands for common workflows (`/ansible-gen`, `/ansible-lint`, `/ansible-validate`) to streamline iteration cycles.

**Null Hypothesis:** Manual CLI invocation is sufficient; command abstraction adds no meaningful efficiency.

**Alternative Hypothesis:** Slash commands reduce iteration time by 30%+ through standardized invocation patterns.

| Attribute | Value |
|-----------|-------|
| Target Dimension | Developer Experience (indirect PASS impact) |
| Expected Uplift | 30% faster iterations (not direct PASS) |
| Complexity Cost | 0.5 week dev |
| Proof Method | Time-to-iterate measurement across 10 generation cycles |
| Kill Threshold | < 15% time reduction |

**Proof Plan:**

1. Implement three commands: generate, lint, validate
2. Measure time from prompt to validated playbook (manual vs command)
3. Survey: perceived friction reduction

**Risk Assessment:** Commands are convenience, not quality. If baseline workflow is already fast (< 2 min iteration), commands add marginal value. May justify only after core PASS targets met.

### Hypothesis 3: Hooks

**Feature Description:** Pre-output hooks for ansible-lint gating and secret scanning before playbook delivery.

**Null Hypothesis:** Post-hoc validation is sufficient; inline gating adds latency without quality improvement.

**Alternative Hypothesis:** Hooks catch issues before delivery, forcing regeneration and improving delivered PASS rates by 15%+.

| Attribute | Value |
|-----------|-------|
| Target Dimension | Linting, Security |
| Expected Uplift | +15% lint PASS, +10% security PASS |
| Complexity Cost | 0.5 week dev |
| Proof Method | Compare delivered playbook PASS rates with/without hooks |
| Kill Threshold | < 5% combined uplift OR > 2s latency |

**Proof Plan:**

1. Implement pre-output hook: `ansible-lint --strict` gate
2. Implement pre-output hook: `detect-secrets scan` gate
3. Hook failure triggers regeneration (max 2 retries)
4. Measure: PASS rate of delivered playbooks, total latency

**Risk Assessment:** Hooks may mask underlying prompt issues. If generation consistently fails lint, hooks create infinite retry loops. Need circuit breaker (2 retries max). Lowest complexity hypothesis; test first.

### Hypothesis 4: Agents

**Feature Description:** Multi-agent workflow with review agent (audits generated playbook) and refine agent (fixes flagged issues).

**Null Hypothesis:** Single-pass generation with validation is sufficient; multi-agent adds complexity without proportional quality gain.

**Alternative Hypothesis:** Review/refine loop improves overall PASS by 20%+ through iterative correction.

| Attribute | Value |
|-----------|-------|
| Target Dimension | All (Idempotency, Error Handling primary) |
| Expected Uplift | +20% overall PASS |
| Complexity Cost | 2 weeks dev, ongoing orchestration maintenance |
| Proof Method | A/B across all scenarios, all dimensions |
| Kill Threshold | < 15% uplift OR > 3x latency OR orchestration failures > 5% |

**Proof Plan:**

1. Build review agent with dimension-specific audit prompts
2. Build refine agent with targeted fix capabilities
3. Orchestrate: generate → review → refine (max 2 iterations)
4. Measure: PASS rates, latency, orchestration reliability

**Risk Assessment:** Highest complexity. Agent orchestration introduces failure modes (SubagentStop bugs observed in codebase). If baseline achieves 80%+ PASS, agent overhead may not justify 15-20% uplift. Test only if baseline < 75% and hooks insufficient.

## Variants Comparison Table

| Attribute | Lean Baseline | Hypothesized Enhanced |
|-----------|---------------|----------------------|
| **Timeline** | 4 weeks | 6 weeks |
| **Features** | Prompt template + validator script | + Hooks (proven) + Skills (conditional) |
| **Complexity** | Low (single-thread workflow) | Medium (hook integration, skill loading) |
| **PASS Target** | 80% average | 90% average |
| **Dev Effort** | 2 person-weeks | 4 person-weeks |
| **Maintenance** | Minimal (prompt updates only) | Moderate (hook/skill updates) |
| **Pros** | Fast delivery, low risk, clear baseline | Higher ceiling, automated gating |
| **Cons** | May plateau at 75-80% | Unproven uplift, added complexity |
| **PASS Impact** | Known: 70-80% achievable | Hypothesized: +10-20% if proven |
| **Complexity Cost** | 1x | 2x |

## Proof Plans Summary

| Hypothesis | Priority | Test Order | Go/No-Go Date |
|------------|----------|------------|---------------|
| Hooks | High | 1st | End Week 4 |
| Skills | Medium | 2nd (if hooks insufficient) | End Week 5 |
| Commands | Low | Defer | Post-MVP |
| Agents | Low | Conditional (baseline < 75%) | End Week 5 |

## Kill Switch Protocol

Each hypothesis includes a pre-defined kill switch to prevent sunk cost fallacy:

1. **Pre-Test Kill:** If baseline achieves 85%+ PASS, skip all hypotheses except commands (convenience)
2. **Mid-Test Kill:** If hypothesis shows < 5% uplift at 50% test completion, abort and document
3. **Post-Test Kill:** If proven hypothesis adds > 2x latency or > 5% reliability issues, revert
4. **Maintenance Kill:** If hypothesis requires > 4 hours/month maintenance after 3 months, deprecate

## Recommendation

**Test hooks first.** Lowest complexity, highest signal-to-noise ratio. If hooks achieve +10% combined uplift on lint and security dimensions, defer all other hypotheses. If hooks are insufficient and baseline < 80%, proceed to skills hypothesis. Agents are last resort only if overall PASS remains < 75% after hooks and skills.

## Approved Configuration (2025-01-15)

- **Timeline:** 6-week enhanced variant
- **Hypothesis Order:** Hooks → Skills (conditional) → Agents (last resort)
- **Scenario Corpus:** 5 domain-specific scenarios from Virgo-Core + Supernova-MicroK8s-Infra
- **Reference Roles:** `proxmox_cluster`, `proxmox_ceph`, `proxmox_access`, `microk8s_cluster`, `argocd`

## Baseline Findings Impact (2025-01-15)

### Lint Dimension: SOLVED

Both repos achieve **100% lint PASS** with existing configs:

- Virgo-Core: `ansible/.ansible-lint` (profile: moderate)
- Supernova: `.ansible-lint.yml` (profile: min, achieves production)

This eliminates hooks hypothesis for lint gating (no uplift possible from 100%).

### Hypothesis Priority Shift

| Hypothesis | Original | Updated | Rationale | Test Order |
|------------|----------|---------|-----------|------------|
| Hooks (lint gate) | High | **Defer** | 100% baseline = 0% uplift room; kill if latency >1s | Post-MVP |
| Hooks (security scan) | Medium | **High** | Unvalidated dim; detect-secrets could +10% on Infisical patterns | 1st (Week 4) |
| Skills | Medium | Medium | Module selection at 81%; curate top-50 Proxmox/K8s refs for helm-wrap excuses | 2nd (if security <75%) |
| Commands | Low | Low | DX polish only—defer till 90% PASS achieved | Post-MVP |
| Agents | Low | Low | Last resort; SubagentStop bugs risk for MicroK8s error chains | Conditional (Week 5, if <80%) |

### Stylistic Hypothesis: KILLED

The var-naming prefix question is resolved by existing policy. No A/B test needed.

- **Outcome:** Flat vars (`ceph_version`) accepted via `skip_list`
- **Rationale:** Cross-role compatibility and readability
- **Generator implication:** Default to flat vars for Proxmox/K8s infrastructure patterns

### Remaining Validation Needed

| Dimension | Baseline Status | Validation Method |
|-----------|-----------------|-------------------|
| Linting | ✅ 100% (both repos) | `ansible-lint -c <config>` |
| Idempotency | ❓ Unvalidated | Heuristic: `changed_when`, `creates`, `removes` |
| Security | ❓ Unvalidated | `detect-secrets` + vault reference check |
| Module Selection | ❓ Unvalidated | Deprecated module detection |
| Error Handling | ❓ Unvalidated | Block/rescue ratio, `ignore_errors` audit |
| Structure | ❓ Unvalidated | yamllint + task naming heuristics |
