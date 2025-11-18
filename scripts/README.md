# Utility Scripts

This directory contains utility scripts that extend the capabilities of the Virgo-Core infrastructure management system.

## Available Scripts

### firecrawl_sdk_research.py

A web research tool that searches, scrapes, and synthesizes technical documentation using the Firecrawl API.

**Use cases:**

- Find code examples on GitHub for specific technologies
- Gather research papers on technical topics
- Discover PDF documentation and whitepapers
- Build comprehensive research documents for infrastructure decisions

**Quick start:**

```bash
export FIRECRAWL_API_KEY="fc-YOUR-API-KEY"
./scripts/firecrawl_sdk_research.py "ansible proxmox ceph" --category github
```

**Documentation:** See [firecrawl_sdk_research.py.README.md](firecrawl_sdk_research.py.README.md) for complete usage guide.

## Prerequisites

### Required Tools

- **Python 3.11+**: All scripts require Python 3.11 or higher
- **uv**: Package manager for running scripts (installed via mise)

Check your Python version:

```bash
python --version
```

Install uv if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Environment Variables

Scripts may require environment variables for API access:

- **FIRECRAWL_API_KEY**: Required for firecrawl_sdk_research.py ([Get API key](https://firecrawl.dev/))

Set environment variables in your shell or add them to `.mise.local.toml`:

```bash
export FIRECRAWL_API_KEY="fc-your-api-key"
```

## Running Scripts

All Python scripts use inline dependency management via uv. No manual installation required.

### Direct Execution

Make scripts executable and run directly:

```bash
chmod +x scripts/firecrawl_sdk_research.py
./scripts/firecrawl_sdk_research.py "search query"
```

### Explicit uv Invocation

Run scripts explicitly with uv:

```bash
uv run scripts/firecrawl_sdk_research.py "search query"
```

Both methods work identically. The shebang `#!/usr/bin/env -S uv run --script` handles dependency installation automatically.

## Integration with Project Workflows

### Research Workflow

Use firecrawl_sdk_research.py to gather examples before implementing new features:

```bash
# Research Ansible Proxmox CEPH examples
./scripts/firecrawl_sdk_research.py "ansible proxmox ceph" \
  --category github \
  --limit 10 \
  --output ai_docs/ceph-research.md

# Research Terraform OpenTofu patterns
./scripts/firecrawl_sdk_research.py "terraform opentofu modules" \
  --category github \
  --output ai_docs/terraform-patterns.md
```

Generated markdown files in `ai_docs/` provide context for development decisions.

### Task Runner Integration

The project uses mise for task management. While scripts run independently, you can create custom mise tasks for frequent operations.

Example task in `.mise.local.toml`:

```toml
[tasks.research]
description = "Research Ansible best practices"
run = "./scripts/firecrawl_sdk_research.py 'ansible best practices' --category github --output ai_docs/ansible-research.md"
```

Run with:

```bash
mise run research
```

### Workspace Setup

The root-level `conductor-setup.sh` script initializes the development environment:

- Installs Python dependencies via uv
- Configures Ansible Galaxy collections
- Sets up git hooks (pre-commit, Infisical)
- Copies mise local configuration

Run after cloning the repository:

```bash
./conductor-setup.sh
```

See the root README.md for complete setup instructions.

## Common Patterns

### Researching Infrastructure Technologies

Search GitHub for infrastructure code examples:

```bash
# Proxmox + CEPH examples
./scripts/firecrawl_sdk_research.py "proxmox ceph osd deployment" --category github

# Ansible role patterns
./scripts/firecrawl_sdk_research.py "ansible role idempotency" --category github

# Terraform module design
./scripts/firecrawl_sdk_research.py "terraform module best practices" --category github
```

### Finding Documentation

Search for official documentation:

```bash
# Search research papers and documentation
./scripts/firecrawl_sdk_research.py "ceph distributed storage" --category research

# Search PDF whitepapers
./scripts/firecrawl_sdk_research.py "proxmox ve architecture" --category pdf
```

### Multiple Categories

Combine GitHub code examples with research papers:

```bash
./scripts/firecrawl_sdk_research.py "distributed consensus algorithms" \
  --categories github,research \
  --limit 15
```

## Output Organization

Scripts generate output in the `ai_docs/` directory by default. Organize research by topic:

```text
ai_docs/
├── ansible-research.md
├── ceph-research.md
├── terraform-patterns.md
└── networking-research.md
```

Commit research documents to share findings with the team or reference in pull requests.

## Troubleshooting

### Script Not Executable

Make scripts executable:

```bash
chmod +x scripts/firecrawl_sdk_research.py
```

### Missing Environment Variables

Set required environment variables:

```bash
export FIRECRAWL_API_KEY="fc-your-api-key"
```

Verify variables are set:

```bash
echo $FIRECRAWL_API_KEY
```

### Python Version Issues

Check Python version:

```bash
python --version
```

Update Python via mise:

```bash
mise install python@3.13
```

### uv Not Found

Install uv via mise:

```bash
mise install uv
```

Or install directly:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Adding New Scripts

Follow these conventions when adding utility scripts:

1. **Use uv shebang**: `#!/usr/bin/env -S uv run --script`
2. **Inline dependencies**: Define dependencies in script header
3. **Make executable**: `chmod +x scripts/new-script.py`
4. **Add documentation**: Create `new-script.py.README.md` for complex scripts
5. **Update this README**: Add script to the Available Scripts section

Example Python script header:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typer>=0.12.0",
# ]
# ///
```

## Related Documentation

- [Root README.md](../README.md) - Project overview and setup
- [docs/infrastructure.md](../docs/infrastructure.md) - Infrastructure specifications
- [.mise.toml](../.mise.toml) - Task runner configuration
- [Firecrawl Documentation](https://docs.firecrawl.dev/) - API reference for research tool

## Support

For script issues:

1. Check script-specific README files
2. Verify prerequisites (Python version, environment variables)
3. Review error messages for missing dependencies
4. Open an issue in the repository

For project setup issues, see the root README.md troubleshooting section.
