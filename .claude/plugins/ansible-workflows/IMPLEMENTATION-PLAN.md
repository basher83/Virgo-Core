# Ansible Workflows Plugin - Implementation Plan

## Status: Phase 5c In Progress

**Last Updated:** Session ended during agent implementation

## What's Done ✅

### Phase 1-4: Complete

- Plugin structure created at `.claude/plugins/ansible-workflows/`
- `plugin.json` manifest created
- README.md created
- Directory structure established

### Phase 5a: Skills (8 total) ✅

All 8 skills created and validated:

| Skill | Path | Words | Status |
|-------|------|-------|--------|
| ansible-fundamentals | skills/ansible-fundamentals/SKILL.md | 999 | ✅ |
| ansible-playbook-design | skills/ansible-playbook-design/SKILL.md | 1022 | ✅ |
| ansible-role-design | skills/ansible-role-design/SKILL.md | 1099 | ✅ |
| ansible-idempotency | skills/ansible-idempotency/SKILL.md | 1073 | ✅ |
| ansible-secrets | skills/ansible-secrets/SKILL.md | 841 | ✅ |
| ansible-error-handling | skills/ansible-error-handling/SKILL.md | 1030 | ✅ |
| ansible-testing | skills/ansible-testing/SKILL.md | 900 | ✅ |
| ansible-proxmox | skills/ansible-proxmox/SKILL.md | 1058 | ✅ |

**Validation:** All descriptions use third-person format with specific trigger phrases.

### Phase 5b: Commands (4 total) ✅

All 4 commands created with proper format:

| Command | Path | Status |
|---------|------|--------|
| /ansible:create-role | commands/create-role.md | ✅ Fixed |
| /ansible:create-playbook | commands/create-playbook.md | ✅ Fixed |
| /ansible:lint | commands/lint.md | ✅ Fixed |
| /ansible:analyze | commands/analyze.md | ✅ Fixed |

**Format fixes applied:**
- Removed `name:` field (not standard)
- Added `$ARGUMENTS` and `$1`, `$2` for dynamic arguments
- Made instructions concise and FOR Claude (not user)

## What's Remaining ❌

### Phase 5c: Agents (4 total) - IN PROGRESS

**CRITICAL:** Must use `agent-creator` agent from plugin-dev to generate agents properly.

Agents exist but were NOT created with agent-creator. Need to:

1. Load `plugin-dev:agent-development` skill
2. Use `agent-creator` agent to regenerate each agent
3. Validate with proper triggering examples

| Agent | Current Status | Action Needed |
|-------|----------------|---------------|
| ansible-generator | Exists, needs regen | Use agent-creator |
| ansible-validator | Exists, needs regen | Use agent-creator |
| ansible-reviewer | Exists, needs regen | Use agent-creator |
| ansible-debugger | Exists, needs regen | Use agent-creator |

**Agent Specifications (from design):**

```yaml
ansible-generator:
  trigger: From commands or explicit request to create Ansible code
  skills: fundamentals, idempotency, proxmox, secrets, playbook-design, role-design
  model: sonnet
  output: Code + path, hands off to validator

ansible-validator:
  trigger: After generation
  skills: testing, fundamentals
  model: haiku
  output: PASS → reviewer, FAIL → debugger

ansible-reviewer:
  trigger: After validation passes
  skills: ALL skills
  model: opus
  output: Structured report (see format below)

ansible-debugger:
  trigger: Validation/execution failures
  skills: fundamentals, idempotency, error-handling
  model: sonnet
  output: Root cause + fix, loops back to generator
```

### Phase 5d: Hook - NOT STARTED PROPERLY

Hook exists but wasn't created following `hook-development` skill.

**Current hook:** `hooks/hooks.json` with PreToolUse prompt-based hook

**Action:** Load `plugin-dev:hook-development` skill and validate/fix hook.

### Phase 6: Validation - NOT DONE

Use `plugin-validator` agent to validate entire plugin.

### Phase 7: Testing - NOT DONE

1. Enable plugin: `/plugin enable ansible-workflows`
2. Test commands
3. Test skill loading
4. Test agent triggering

### Phase 8: Cleanup - NOT DONE

1. Remove old skill: `rm -rf .claude/skills/ansible-best-practices/`
2. Update CLAUDE.md to reference new plugin

## Key Design Decisions

### Orchestration Flow

```
/ansible:create-* ──► ansible-generator ──► ansible-validator ──► ansible-reviewer
                                                    │
                                                  FAIL?
                                                    │
                                                    ▼
                                            ansible-debugger ──► Loop back
```

### Reviewer Structured Output Format

```yaml
# Ansible Review Report

## Summary
overall_rating: 4.2/5
recommendation: APPROVED | APPROVED_WITH_CHANGES | NEEDS_REWORK

## Findings by Category
### IDEMPOTENCY
### SECURITY
### STRUCTURE
### PERFORMANCE
### MAINTAINABILITY
### PROXMOX

## Metrics
idempotency_score: 0.85
security_score: 0.70
# etc.

## Narrative Assessment
### What's Working Well
### Recommended Improvements
### Why [recommendation]
```

## Resume Instructions

To continue implementation:

1. **Load create-plugin command context:**
   ```
   Read /Users/basher8383/.claude/plugins/marketplaces/claude-code-plugins/plugins/plugin-dev/commands/create-plugin.md
   ```

2. **Resume at Phase 5c:**
   - Load `plugin-dev:agent-development` skill
   - Use `agent-creator` agent for each of the 4 agents
   - Agent specs are in this plan above

3. **Then complete:**
   - Phase 5d: Load `plugin-dev:hook-development`, validate hook
   - Phase 6: Run `plugin-validator` agent
   - Phase 7: Test plugin
   - Phase 8: Cleanup old skill, update CLAUDE.md

## Files Reference

```
.claude/plugins/ansible-workflows/
├── .claude-plugin/plugin.json     ✅
├── .gitignore                     ✅
├── README.md                      ✅
├── IMPLEMENTATION-PLAN.md         ✅ (this file)
├── agents/
│   ├── ansible-debugger.md        ⚠️ Needs agent-creator regen
│   ├── ansible-generator.md       ⚠️ Needs agent-creator regen
│   ├── ansible-reviewer.md        ⚠️ Needs agent-creator regen
│   └── ansible-validator.md       ⚠️ Needs agent-creator regen
├── commands/
│   ├── analyze.md                 ✅
│   ├── create-playbook.md         ✅
│   ├── create-role.md             ✅
│   └── lint.md                    ✅
├── hooks/
│   └── hooks.json                 ⚠️ Needs validation
├── skills/
│   ├── ansible-error-handling/    ✅
│   ├── ansible-fundamentals/      ✅
│   ├── ansible-idempotency/       ✅
│   ├── ansible-playbook-design/   ✅
│   ├── ansible-proxmox/           ✅
│   ├── ansible-role-design/       ✅
│   ├── ansible-secrets/           ✅
│   └── ansible-testing/           ✅
└── templates/                     (empty, unused)
```
