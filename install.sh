#!/bin/bash
# Installation script for Git Vibe Brancher

set -e

echo "🌿 Installing Git Vibe Brancher..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Make scripts executable
chmod +x "$SCRIPT_DIR/vibe_brancher.py"
chmod +x "$SCRIPT_DIR/git-vibe"

# Check if user wants to install globally
read -p "Do you want to install globally? (add to PATH) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Add to PATH in shell profile
    SHELL_PROFILE=""
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_PROFILE="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        SHELL_PROFILE="$HOME/.bashrc"
    else
        SHELL_PROFILE="$HOME/.profile"
    fi
    
    echo "export PATH=\"\$PATH:$SCRIPT_DIR\"" >> "$SHELL_PROFILE"
    echo "✅ Added to PATH in $SHELL_PROFILE"
    echo "📝 Please run 'source $SHELL_PROFILE' or restart your terminal"
fi

# Create git alias
read -p "Do you want to create a git alias 'vibe'? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git config --global alias.vibe "!$SCRIPT_DIR/git-vibe"
    echo "✅ Created git alias 'vibe'"
    echo "📝 You can now use 'git vibe' from any repository"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  ./git-vibe                    # Analyze current changes"
echo "  ./git-vibe --verbose          # Show detailed analysis"
echo "  ./git-vibe --create           # Auto-create branch if recommended"
echo "  git vibe                      # If you created the alias"
echo ""
echo "Configuration: Edit config.json to customize thresholds and behavior"
