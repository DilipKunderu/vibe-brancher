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

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is required but not installed."
    exit 1
fi

# Make scripts executable
chmod +x "$SCRIPT_DIR/vibe_brancher.py"
chmod +x "$SCRIPT_DIR/git-vibe"

echo "✅ Made scripts executable"

# Create comprehensive git aliases
echo "🔧 Setting up git integration..."

# Core aliases (manual)
git config --global alias.vibe "!$SCRIPT_DIR/git-vibe"
git config --global alias.vibe-verbose "!$SCRIPT_DIR/git-vibe --verbose"
git config --global alias.vibe-create "!$SCRIPT_DIR/git-vibe --create"
git config --global alias.vibe-check "!$SCRIPT_DIR/git-vibe --verbose"

# Workflow aliases (manual)
git config --global alias.vibe-status "!$SCRIPT_DIR/git-vibe && echo '' && git status --short"
git config --global alias.vibe-diff "!$SCRIPT_DIR/git-vibe && echo '' && git diff --stat"

# Automatic aliases (seamless integration)
git config --global alias.save "!$SCRIPT_DIR/vibe_brancher.py --save"
git config --global alias.checkpoint "!$SCRIPT_DIR/vibe_brancher.py --checkpoint"
git config --global alias.vibe-auto-branch "!$SCRIPT_DIR/vibe_brancher.py --auto-branch"
git config --global alias.vibe-daemon "!$SCRIPT_DIR/vibe_daemon.py"
git config --global alias.vibe-stop "!pkill -f vibe_daemon.py"

# Invisible auto-save (like IDE auto-save)
git config --global alias.vibe-autosave "!$SCRIPT_DIR/vibe_autosave.py"
git config --global alias.vibe-autosave-stop "!pkill -f vibe_autosave.py"

# Legacy aliases (for backward compatibility)
git config --global alias.vibe-auto-commit "!$SCRIPT_DIR/vibe_brancher.py --save"

# Branch convergence aliases
git config --global alias.vibe-convergence "!$SCRIPT_DIR/vibe_brancher.py --convergence"
git config --global alias.vibe-merge-check "!$SCRIPT_DIR/vibe_brancher.py --convergence --verbose"

echo "✅ Created git aliases:"
echo "   Manual Commands:"
echo "     git vibe          - Quick analysis"
echo "     git vibe-verbose  - Detailed analysis"
echo "     git vibe-create   - Auto-create branch if recommended"
echo "     git vibe-check    - Same as vibe-verbose"
echo "     git vibe-status   - Analysis + git status"
echo "     git vibe-diff     - Analysis + git diff stats"
echo "   Vibe Coder Commands:"
echo "     git save          - Save current progress with intelligent branching"
echo "     git checkpoint    - Create a checkpoint of current work"
echo "     git vibe-auto-branch - Automatic branch creation"
echo "     git vibe-daemon   - Start background daemon"
echo "     git vibe-stop     - Stop background daemon"
echo "   Invisible Auto-Save:"
echo "     git vibe-autosave - Start invisible auto-save (like IDE auto-save)"
echo "     git vibe-autosave-stop - Stop invisible auto-save"
echo "   Branch Convergence:"
echo "     git vibe-convergence - Check if branch is ready to merge"
echo "     git vibe-merge-check - Detailed merge readiness analysis"

# Create git hooks directory if it doesn't exist
GIT_HOOKS_DIR="$HOME/.git-templates/hooks"
mkdir -p "$GIT_HOOKS_DIR"

# Create pre-commit hook template
cat > "$GIT_HOOKS_DIR/pre-commit-vibe" << 'EOF'
#!/bin/bash
# Git Vibe Brancher pre-commit hook
# This hook runs vibe analysis before commits

# Get the directory where vibe_brancher is installed
VIBE_DIR="$(git config --global --get vibe-brancher.path 2>/dev/null)"
if [ -z "$VIBE_DIR" ]; then
    # Try to find it in common locations
    for dir in "$HOME/git-vibe-brancher" "$HOME/.local/bin" "/usr/local/bin"; do
        if [ -f "$dir/vibe_brancher.py" ]; then
            VIBE_DIR="$dir"
            break
        fi
    done
fi

if [ -n "$VIBE_DIR" ] && [ -f "$VIBE_DIR/vibe_brancher.py" ]; then
    echo "🔍 Running vibe analysis..."
    python3 "$VIBE_DIR/vibe_brancher.py" --verbose
    
    # Ask if user wants to continue with commit
    echo ""
    read -p "🤔 Continue with commit? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Commit cancelled."
        exit 1
    fi
fi
EOF

chmod +x "$GIT_HOOKS_DIR/pre-commit-vibe"

# Store the vibe-brancher path in git config
git config --global vibe-brancher.path "$SCRIPT_DIR"

echo "✅ Created git hook template: pre-commit-vibe"
echo "   To enable: git config --global init.templatedir '$HOME/.git-templates'"

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

# Offer to set up git templates for new repositories
read -p "Do you want to enable vibe hooks for new repositories? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git config --global init.templatedir "$HOME/.git-templates"
    echo "✅ Enabled vibe hooks for new repositories"
    echo "   New repos will have vibe analysis on commits"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "🚀 Git Integration Ready:"
echo "  Manual Commands:"
echo "    git vibe                    # Quick analysis"
echo "    git vibe-verbose           # Detailed analysis"
echo "    git vibe-create            # Auto-create branch if recommended"
echo "    git vibe-status            # Analysis + git status"
echo "    git vibe-diff              # Analysis + git diff stats"
echo ""
echo "  Vibe Coder Commands:"
echo "    git save                   # Save current progress with intelligent branching"
echo "    git checkpoint             # Create a checkpoint of current work"
echo "    git vibe-auto-branch       # Automatic branch creation"
echo "    git vibe-daemon            # Start background daemon"
echo "    git vibe-stop              # Stop background daemon"
echo ""
echo "  Invisible Auto-Save (Recommended):"
echo "    git vibe-autosave          # Start invisible auto-save (like IDE auto-save)"
echo "    git vibe-autosave-stop     # Stop invisible auto-save"
echo ""
echo "  Branch Convergence:"
echo "    git vibe-convergence       # Check if branch is ready to merge"
echo "    git vibe-merge-check       # Detailed merge readiness analysis"
echo ""
echo "🔧 For seamless integration on existing repositories:"
echo "  $SCRIPT_DIR/setup-seamless-integration"
echo ""
echo "📝 Configuration: Edit config.json to customize thresholds and behavior"
