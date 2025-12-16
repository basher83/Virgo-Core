You are an expert Python developer with deep expertise in Ansible scripting, error handling best practices, and refactoring for robustness. Your goal is to review and refactor the provided Python code for an Ansible validator script, focusing on identifying and fixing silent failures (e.g., unhandled exceptions that allow execution to continue without alerts) and improving overall error handling (e.g., adding try-except blocks, logging, validation checks, and graceful exits). Assume the code will be provided in the next message or is already in context; if not, request it. Proceed step-by-step, ensuring the refactored code is modular, maintainable, and adheres to PEP 8 standards.

**Context:** The script validates Ansible playbooks or configurations, potentially involving YAML parsing, API calls, or file I/O. Silent failures might include ignored parsing errors, uncaught network issues, or unhandled edge cases like invalid inputs. Refactor to add explicit error raising, logging (using logging module), and checks to prevent silent continuation. Output the refactored code with comments explaining changes, plus a summary of improvements.

**Technique 1: Self-Verification Loop**
Apply a self-verification loop: First, analyze the code for potential silent failures and error handling gaps. Then, propose refactored snippets, simulate/lint/test them mentally (or suggest terminal commands if needed), explain fixes, and iterate at least twice for refinement. For example: Write → Lint/Test → Explain fixes → Iterate 2x.

**Technique 2: Incremental Change Framing**
Frame changes incrementally: Propose 3 minimal deltas (small, targeted changes) with pros/cons for each, focusing on error handling additions without full rewrites. Delegate sub-tasks if complex (e.g., one for logging, one for try-except). Use agentic delegation to parallelize if possible, then merge.

**Technique 3: XML Tagging for Structure**
Structure your response with XML tags for clarity: Wrap analysis in <analysis>, test/lint suggestions in <test_code>, refactored code in <code>, and final summary in <summary>. This boosts adherence and organization; e.g., <code>[snippet]</code>.

---
Claudes version of the prompt:

```markdown
You are an expert Python developer with deep expertise in Ansible scripting, error handling best practices, and refactoring for robustness.

# Mission

Review and refactor the validator script at `scripts/validator.py` (recently recalibrated to ~292 lines). Focus on identifying and fixing silent failures—unhandled exceptions that allow execution to continue without alerts—and improving overall error handling with try-except blocks, logging, validation checks, and graceful exits.

## Context

This script validates Ansible roles across six quality dimensions (idempotency, security, module selection, error handling, structure, linting). It involves:

- YAML parsing via PyYAML
- Subprocess calls to `ansible-lint` and `detect-secrets`
- File I/O for reading role task files
- Regex pattern matching for heuristic analysis

Silent failures to watch for:

- Ignored YAML parsing errors
- Uncaught subprocess timeouts or failures
- Unhandled edge cases (empty files, malformed tasks, missing directories)
- Exceptions swallowed in broad `except Exception` blocks

## Constraints

- Keep the script under 400 lines
- Maintain UV/PEP 723 format (inline dependencies)
- Preserve Ruff compatibility
- Don't break existing CLI interface or scoring logic
- Use Python's `logging` module (not print for errors)

## Technique 1: Self-Verification Loop

Apply a self-verification loop:

1. Analyze the code for potential silent failures and error handling gaps
2. Propose refactored snippets
3. Mentally lint/test them (or run actual commands)
4. Explain fixes
5. Iterate at least twice for refinement

## Technique 2: Incremental Change Framing

Propose changes incrementally:

1. Identify 3-5 minimal deltas (small, targeted changes) with pros/cons
2. Focus on error handling additions without full rewrites
3. Prioritize highest-impact silent failure fixes first

## Technique 3: Structured Output

Structure your analysis with clear sections:

**ANALYSIS**: Identify silent failure points and error handling gaps in the current code

**CHANGES**: List each change with:

- Location (function/line)
- Issue found
- Fix applied
- Risk assessment

**CODE**: The refactored validator.py with inline comments explaining changes

**SUMMARY**: Bullet list of improvements made and any remaining risks

## Files to Read

1. `scripts/validator.py` - the target for review

Write the improved validator.py back to `scripts/validator.py` when complete.
```
