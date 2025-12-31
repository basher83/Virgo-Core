---
name: block-uv-tool-install
enabled: true
event: bash
pattern: uv\s+tool\s+install
action: block
---

**Global tool installation blocked**

You attempted to run `uv tool install` which installs packages globally.

**Why this is blocked:**

- Global installations can conflict with project-level mise-managed tools
- Creates ambiguity about which version is used (PATH order dependent)
- Not documented in project config, so other contributors won't have it

**Alternatives:**

- Add to `.mise.toml` with `"pipx:package-name" = "version"` for project-level management
- Use `uv pip install` within the project's venv for local dependencies
- Ask user explicitly if global installation is truly intended

**To proceed:** Get explicit user approval for global installation, or use mise/venv instead.
