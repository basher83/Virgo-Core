# PR #21 After-Action Review

## Step 1: `/verify-pr` Command

**Performance:** Excellent ✅

**Improvements:** None required

**Optional Enhancements:**
- Suggest code review automatically after verification
- Verify bug existence when claims mention "fixes bug"

---

## Step 2: `superpowers:requesting-code-review` Skill

**Performance:** Good structure, flawed execution ⚠️

### 2a. Update `requesting-code-review` Skill

**File:** `.claude/skills/requesting-code-review/SKILL.md`

**Add Pre-Review Checklist:**

Before dispatching code-reviewer:

1. ☐ Verify clean working directory
   ```bash
   git status
   # If dirty, stash or acknowledge uncommitted changes
   ```

2. ☐ Verify correct commit
   ```bash
   git log --oneline -3
   # Confirm HEAD matches review target
   ```

3. ☐ Extract SHAs from git
   ```bash
   BASE_SHA=$(git rev-parse main)
   HEAD_SHA=$(git rev-parse HEAD)
   ```

**Add Critical Rule:**

When providing code examples to code-reviewer:

- Quote actual code using: `git show COMMIT:path | sed -n 'X,Yp'`
- Include actual line numbers
- Never quote from memory
- Never show invented examples

**Why:** Code-reviewer cannot verify hallucinated code.

### 2b. Update `code-reviewer` Subagent

**File:** `.claude/skills/requesting-code-review/code-reviewer.md`

**Add Code Verification Protocol:**

Before claiming code exists or has issues:

1. Read actual code:
   ```bash
   git show {HEAD_SHA}:path/to/file | sed -n 'X,Yp'
   ```

2. Verify all code snippets from git

3. Require evidence for external claims:
   - "API returns dict" → docs URL or SDK source
   - "Library does X" → import statement and usage
   - Cannot verify → mark "Needs Verification", not "Issue"

**Add Evidence Section:**

```markdown
### Evidence
- Code snippets: `git show {SHA}:file:lines`
- API claims: [docs link or SDK source]
- File:line references verified: ✓/✗
```

**Add Review Depth Scaling:**

```markdown
## Review Depth Based on PR Size

**Micro (1-2 files, <200 lines):**
- Focus: Critical only
- Time: 2-3 minutes
- Output: 3-5 issues maximum

**Small (2-5 files, 200-800 lines):**
- Focus: Critical + Important
- Time: 5-7 minutes
- Output: 5-8 issues

**Medium (5-15 files, 800-2000 lines):**
- Focus: All categories
- Time: 10-15 minutes
- Output: 8-12 issues

**Large (15+ files, 2000+ lines):**
- Focus: Architecture + Critical
- Time: 15-20 minutes
- Output: High-level + critical details
- Suggest splitting into smaller PRs
```

---

## Step 3: Compare with CodeRabbit

**Performance:** Good ✅

**Optional Enhancement:** Formalize as `compare-review-sources` skill

**Create:** `.claude/skills/compare-review-sources/SKILL.md`

```yaml
---
name: compare-review-sources
description: Compare findings from multiple code review sources
---
```

**When to Use:**

After manual code review, compare with:
- CodeRabbit comments
- GitHub Actions checks
- SonarQube reports
- Other automated tools

**Process:**

1. Fetch automated review comments
2. Create comparison matrix:
   | Issue | Manual Review | Automation | Severity Match? |
3. Identify:
   - Manual-only findings
   - Automation-only findings
   - Disagreements (investigate)
4. Learn from differences

**Output:**
- Confirmed issues (found by both)
- Unique findings (found by one)
- Disagreements to investigate

---

## Step 4: Investigation

**Performance:** Required cleanup

**Improvement:** Apply Step 2 improvements to eliminate this step

---

## Step 5: Fix Bugs

**Performance:** Good execution ✅

**Enhancement:** Add to `requesting-code-review` skill:

### After Fixes Section

**1. Offer Tests**

When no tests exist for fixed code, ask:
"Would you like me to add a test to prevent regression?"

**2. Re-verify Critical Fixes**

For Critical or Important fixes:

```bash
git diff --stat {BEFORE_SHA}..{AFTER_SHA}
```

Dispatch code-reviewer again with narrow scope:
- Review only fixes for issues X, Y, Z
- Verify fixes resolve the issues

**3. Document in PR**

Update PR with:
- What you fixed
- Why it matters
- How to verify

---

## Step 6: Push and Update

**Performance:** Excellent ✅

**Improvements:** None required

---

## Summary: File Updates Required

| Improvement | File |
|-------------|------|
| Pre-review checklist | `.claude/skills/requesting-code-review/SKILL.md` |
| Code verification protocol | `.claude/skills/requesting-code-review/code-reviewer.md` |
| Review depth scaling | `.claude/skills/requesting-code-review/code-reviewer.md` |
| API claim verification | `.claude/skills/requesting-code-review/code-reviewer.md` |
| Test offering after fixes | `.claude/skills/requesting-code-review/SKILL.md` |
| Re-verify critical fixes | `.claude/skills/requesting-code-review/SKILL.md` |
| Multi-source comparison | `.claude/skills/compare-review-sources/SKILL.md` (new) |

## Implementation Priority

**Immediate (high value):**
- Add Pre-Review Checklist to `requesting-code-review` skill
- Add Code Verification Protocol to `code-reviewer` agent

**Medium priority:**
- Add review depth scaling to `code-reviewer`
- Add After Fixes section to `requesting-code-review`

**Optional:**
- Create `compare-review-sources` skill
- Add API verification requirements
