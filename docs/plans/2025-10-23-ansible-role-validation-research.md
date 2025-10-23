# Ansible Role Validation Research Design

**Date:** 2025-10-23
**Status:** Approved for Implementation

## Executive Summary

This research validates Phase 1-3 Ansible roles (`system_user`, `proxmox_access`, `proxmox_network`) against production patterns from geerlingguy roles. We extract comprehensive patterns from exemplar roles (`security`, `users`), validate across 3-5 additional roles, then generate prioritized action items for role improvements.

## Goals

1. **Validate current work** - Compare Phase 1-3 roles against rock-solid production examples
2. **Build knowledge base** - Extract patterns proactively for Phase 4+ work
3. **Update skill** - Enhance `ansible-best-practices` skill with production patterns
4. **Generate action items** - Create prioritized improvement list for the three roles

## Research Approach: Tiered Sampling

### Phase 1: Deep Exemplar Analysis

**Primary Exemplars:**
- `geerlingguy.security` - System hardening, directly relevant to security concerns
- `geerlingguy.users` - User/SSH management, maps to `system_user` role

**Secondary Exemplars (Later):**
- `geerlingguy.kubernetes` - Complex orchestration patterns
- `geerlingguy.mysql` - Service management and coordination

**Why These Roles:**
- Security and users directly relate to current Phase 1-3 work
- Both have extensive testing infrastructure
- Heavily downloaded, battle-tested in production
- kubernetes and mysql provide complex patterns for future phases

### Phase 2: Breadth Validation

**Validation Targets (3-5 roles):**
- `geerlingguy.docker` - Already referenced, service management
- `geerlingguy.postgresql` - Complex configuration, data management
- `geerlingguy.nginx` - Template-heavy, web server patterns
- `geerlingguy.pip` or `geerlingguy.git` - Simple utility roles for baseline

**Validation Questions:**
- Does this role follow the same molecule testing structure?
- How does task organization compare?
- Variable naming conventions consistent?
- README structure similar?
- Handler usage patterns match?

**Confidence Levels:**
- **Universal** - 6-7 roles all use same pattern
- **Contextual** - Variations with documented rationale
- **Evolving** - Newer roles differ, note improved pattern

## Pattern Extraction Categories

### 1. Testing Patterns
- Molecule configuration structure (`molecule.yml`)
- Test scenarios (default, convergence, idempotence, side-effect)
- Test matrix (multiple OS/versions)
- CI/CD integration (GitHub Actions)
- Assertion and verification strategies

### 2. Role Structure
- Directory organization (`tasks/`, `defaults/`, `handlers/`, `templates/`, `vars/`, `meta/`, `files/`)
- Task file organization (`main.yml` vs split files, when to split)
- Naming conventions (files, variables, tasks)
- File placement decisions

### 3. Documentation
- README structure and sections
- Variable documentation format
- Example usage patterns
- Requirements and dependencies listing
- Troubleshooting sections

### 4. Variable Management
- `defaults/` vs `vars/` usage
- Variable naming conventions
- Boolean vs string patterns
- Complex structures (lists, dicts)
- Precedence documentation

### 5. Handler Patterns
- When handlers vs tasks
- Handler naming conventions
- Notification patterns
- Handler dependencies

### 6. Meta/Dependencies
- `galaxy_info` structure
- Platform/version specifications
- Role dependencies declaration
- Tags and categories

## Deliverables

### 1. Enhanced ansible-best-practices Skill

**New Pattern Documents:**
- `.claude/skills/ansible-best-practices/patterns/testing-comprehensive.md`
- `.claude/skills/ansible-best-practices/patterns/role-structure-standards.md`
- `.claude/skills/ansible-best-practices/patterns/documentation-templates.md`
- `.claude/skills/ansible-best-practices/patterns/variable-management-patterns.md`
- `.claude/skills/ansible-best-practices/patterns/handler-best-practices.md`
- `.claude/skills/ansible-best-practices/patterns/meta-dependencies.md`

**Pattern Document Structure:**
- Pattern description
- Example code from geerlingguy roles
- When to use (guidance)
- Anti-patterns (what to avoid)
- Comparison to Virgo-Core roles

### 2. Action Items Document

**Location:** `docs/action-items/2025-10-23-role-improvements.md`

**Format:**
```markdown
## system_user Role Improvements

### Critical
- [ ] Add molecule testing infrastructure (default scenario)
- [ ] Create meta/main.yml with galaxy_info

### Important
- [ ] Enhance README with examples section
- [ ] Reorganize variables in defaults/ (naming conventions)

### Nice-to-have
- [ ] Add CI/CD integration (GitHub Actions)
```

**Organization:**
- Organized by role (system_user, proxmox_access, proxmox_network)
- Prioritized (Critical, Important, Nice-to-have)
- Each item links to pattern document
- Estimated effort (quick, moderate, significant)

### 3. Reference Index

**Location:** `.claude/skills/ansible-best-practices/reference/production-repos.md`

**Contents:**
- Studied repositories list
- Pattern extraction date
- Key learnings summary
- Links to roles analyzed

## Execution Workflow

### Using ansible-research Agent

1. **Launch parallel agents** for security and users analysis
2. **Extract comprehensive patterns** from both exemplar roles
3. **Launch validation agents** for 3-5 additional roles
4. **Synthesize findings** into pattern documents
5. **Compare against Virgo-Core roles** for gap analysis
6. **Generate prioritized action items** for improvements

### Expected Timeline

- Session 1: Deep exemplar analysis (security + users), initial pattern documentation
- Session 2: Breadth validation, pattern refinement, action items generation
- Future: kubernetes + mysql analysis for complex orchestration patterns

## Success Criteria

- Six new pattern documents in ansible-best-practices skill
- Each pattern has 2+ real-world examples from geerlingguy roles
- Prioritized action items for all three Phase 1-3 roles
- Clear comparison showing what matches vs gaps
- Confidence levels documented (universal, contextual, evolving)

## Benefits

**Immediate:**
- Validate Phase 1-3 work against production standards
- Identify gaps and improvements

**Short-term:**
- Enhanced ansible-best-practices skill for Phase 4+ work
- Testing infrastructure knowledge ready to apply

**Long-term:**
- Comprehensive pattern library from A-tier projects
- Faster implementation (patterns ready vs discovered during work)
- Higher quality (learn from millions of downloads worth of feedback)
