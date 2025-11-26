#!/bin/bash
set -euo pipefail

echo "🚀 Setting up Virgo-Core workspace..."

# Check for required tools
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed. Please install mise and uv first."
    exit 1
fi

if ! command -v mise &> /dev/null; then
    echo "❌ Error: mise is not installed. Please install mise first."
    exit 1
fi

# Copy mise local config files if they exist in the root repo
MISE_LOCAL_COPIED=false

if [ -f "$CONDUCTOR_ROOT_PATH/.mise.local.toml" ]; then
    echo "📋 Copying .mise.local.toml from root repository..."
    cp "$CONDUCTOR_ROOT_PATH/.mise.local.toml" ./.mise.local.toml
    echo "✅ .mise.local.toml copied"
    MISE_LOCAL_COPIED=true
fi

if [ -f "$CONDUCTOR_ROOT_PATH/mise.local.toml" ]; then
    echo "📋 Copying mise.local.toml from root repository..."
    cp "$CONDUCTOR_ROOT_PATH/mise.local.toml" ./mise.local.toml
    echo "✅ mise.local.toml copied"
    MISE_LOCAL_COPIED=true
fi

if [ "$MISE_LOCAL_COPIED" = false ]; then
    echo "⚠️  Warning: No mise local config found in root repository at $CONDUCTOR_ROOT_PATH"
    echo "   You may need to create .mise.local.toml or mise.local.toml with your environment variables"
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
uv sync
echo "✅ Python dependencies installed"

# Install Ansible Galaxy collections
echo "📦 Installing Ansible Galaxy collections..."
cd ansible
uv run ansible-galaxy collection install -r requirements.yml
cd ..
echo "✅ Ansible collections installed"

# Install pre-commit and Infisical hooks
echo "🪝 Installing git hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "✅ Pre-commit hooks installed"
else
    echo "⚠️  Warning: pre-commit not found, skipping pre-commit hook installation"
fi

if command -v infisical &> /dev/null; then
    infisical scan install --pre-commit-hook
    echo "✅ Infisical hooks installed"
else
    echo "⚠️  Warning: infisical not found, skipping Infisical hook installation"
fi

echo ""
echo "✨ Workspace setup complete!"
echo ""
echo "You can now:"
echo "  - Run Ansible playbooks: cd ansible && uv run ansible-playbook playbooks/<playbook>.yml"
echo "  - Use mise tasks: mise run <task-name>"
echo "  - Work with OpenTofu: cd terraform && tofu <command>"
