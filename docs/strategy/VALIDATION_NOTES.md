# Validation Notes

## Confidence Ratings by Phase

| Phase | Confidence | Rationale | Weight on Outcome Proof |
|-------|------------|-----------|-------------------------|
| **Design (Week 1)** | 95% | Scenarios locked, lint validated at 100%, projections exceed MVP threshold | 70% |
| **Build (Weeks 2-3)** | 85% | Lint integration proven; 5 remaining dims need heuristics but patterns clear from code inspection | 70% |
| **Test & Refine (Weeks 4-5)** | 75% | Hooks for security scan is highest-value hypothesis; skills conditional on module gaps | 70% |
| **Deploy & Scale (Week 6)** | 85% | Plugin packaging is templated; 84% projected baseline reduces risk | 70% |

**Overall Confidence:** 85% weighted average (upgraded from 75%), anchored on:
- ✅ Lint at 100% (validated)
- 📊 84% projected aggregate (exceeds 80% MVP threshold)
- 🎯 Hooks hypothesis reprioritized to security (highest uncertainty dim)

## Key Assumptions with Proof Status

| Assumption | Status | Proof Method | Risk if False |
|------------|--------|--------------|---------------|
| Claude's Ansible knowledge covers top 50 modules | Unproven | Baseline testing | Module selection PASS < 70% |
| ansible-lint 6.x rules detect deprecated modules | **Proven** | Both repos pass production profile | N/A |
| Six dimensions are programmatically validatable | **Lint Proven** | 100% PASS both repos; 5 dims need heuristics | Manual review for edge cases |
| Hooks add < 2s latency | Unproven | Hook prototype timing (Week 4) | User experience degradation |
| Single-pass generation sufficient for 75%+ PASS | **Projected 84%** | Code inspection + lint validation | Agents required if <80% |
| Existing policy configs achieve production lint | **Proven** | `ansible-lint -c <config>` = 0 violations | N/A |

## What-If Triggers

### Trigger 1: Baseline PASS < 70%

**Condition:** Aggregate PASS rate across 5 scenarios falls below 70% after Build phase.

**Response:**

1. Identify worst-performing dimension(s)
2. Prioritize prompt engineering fixes for that dimension
3. If still < 70% after 1 week iteration, escalate to hooks hypothesis immediately
4. Extend timeline by 1 week; notify stakeholders

### Trigger 2: No Uplift from Hooks

**Condition:** Hooks hypothesis shows < 5% combined uplift on lint and security dimensions.

**Response:**

1. Document hook implementation details and failure modes
2. Kill hooks hypothesis; do not integrate
3. Evaluate: Is 75-80% PASS acceptable? If yes, ship baseline
4. If 90%+ required, proceed to skills hypothesis with skepticism

### Trigger 3: Agent Orchestration Failures > 5%

**Condition:** Review/refine agent pipeline fails (timeouts, SubagentStop bugs, malformed outputs) more than 5% of runs.

**Response:**

1. Abort agent hypothesis immediately
2. Document failure modes for future reference
3. Revert to best-performing simpler approach (baseline or hooks)
4. Flag orchestration as architectural risk for future features

## De-Scoping Rationale

### Commands: Deferred to Post-MVP

**Rationale:** Commands improve developer experience but have no direct PASS impact. Core goal is PASS scores, not iteration speed. Once 90%+ PASS is achieved, commands become a polish feature.

**Re-Scope Trigger:** User feedback indicates significant friction in manual workflow.

### Agents: Conditional, Not Default

**Rationale:** Observed SubagentStop hook bugs in codebase suggest orchestration instability. Agents are highest-complexity, highest-risk hypothesis. Only justified if simpler approaches (prompt tuning, hooks, skills) cannot achieve 80%+ PASS.

**Re-Scope Trigger:** Baseline + hooks + skills combined < 80% PASS.

### Skills: Conditional on Module Selection Gap

**Rationale:** If baseline module selection PASS is 85%+, skill overhead (maintenance, load time) exceeds marginal benefit. Skills justify only if module selection is a documented gap.

**Re-Scope Trigger:** Module selection PASS < 75% after baseline.

## Variant Recommendation

**Recommended Path: Lean Baseline with Conditional Hooks**

| Decision Point | Condition | Action |
|----------------|-----------|--------|
| End Week 3 | Baseline PASS >= 85% | Ship baseline, defer all hypotheses |
| End Week 3 | Baseline PASS 75-84% | Test hooks hypothesis |
| End Week 3 | Baseline PASS < 75% | Test hooks + skills in parallel |
| End Week 4 | Hooks uplift >= 10% | Integrate hooks, ship |
| End Week 4 | Hooks uplift < 10%, baseline >= 80% | Ship baseline without hooks |
| End Week 5 | All approaches < 80% | Evaluate agents as last resort |

## De-Risking Tweaks

### Tweak 1: Parallel Validator Development

Start validator script development in Week 1 alongside scenario definition. This front-loads the Build phase and provides early signal on dimension measurement feasibility.

**Impact:** Reduces Week 2-3 risk; surfaces heuristic challenges early.

### Tweak 2: Scenario Prioritization

Order scenarios by expected difficulty:

1. **Proxmox Access Control** (moderate) - Straightforward task flow, clear security dimension
2. **Proxmox Cluster Bootstrap** (moderate) - Multi-node but well-understood patterns
3. **CEPH Storage Deployment** (hard) - Complex idempotency with disk state detection
4. **MicroK8s HA Cluster** (hard) - Delegation chains, error handling complexity
5. **GitOps Stack - ArgoCD** (hard) - Module selection challenges, Helm wrapping

Early wins on Proxmox roles build confidence; harder MicroK8s scenarios stress-test at end when validator is mature.

**Impact:** Smoother progress curve; avoids early demoralization from hard scenario failures.

## Open Questions for Stakeholder Review

1. ~~Is 80% PASS acceptable as MVP threshold, or is 90%+ mandatory for launch?~~ → Deferred to baseline measurement
2. ~~Which scenarios are highest priority if timeline compresses to 4 weeks?~~ → N/A, 6-week timeline selected
3. ~~Are there existing Ansible playbooks in the organization that can serve as baseline quality references?~~ → **YES**: 5 production roles identified across Virgo-Core and Supernova-MicroK8s-Infra
4. What is acceptable latency for playbook generation (with/without hooks)? → **Still open**, to be determined during hook hypothesis testing

## Sign-Off Checklist

- [x] Scenarios approved by stakeholder (2025-01-15)
- [x] PASS thresholds confirmed (70% minimum per dimension, 80% overall)
- [x] Hypothesis test order agreed (hooks first)
- [x] Kill thresholds accepted (5%/15% uplift bands)
- [x] Timeline variant selected: **6-week enhanced**
