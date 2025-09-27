#!/bin/bash
# Git Vibe Brancher - Integration Setup Script
# This script helps you integrate the tool into your existing repository workflow

echo "🌿 Git Vibe Brancher - Integration Setup"
echo "========================================"
echo ""

# Get the absolute path to the vibe brancher script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIBE_BRANCHER_PATH="$SCRIPT_DIR/vibe_brancher.py"

# Check if the vibe brancher script exists
if [ ! -f "$VIBE_BRANCHER_PATH" ]; then
    echo "❌ Vibe Brancher script not found at: $VIBE_BRANCHER_PATH"
    echo "Please ensure you're running this script from the git-vibe-brancher directory."
    exit 1
fi

echo "✅ Found Vibe Brancher at: $VIBE_BRANCHER_PATH"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Please run this script from within your git repository."
    exit 1
fi

echo "✅ Detected git repository: $(git rev-parse --show-toplevel)"
echo ""

# Function to setup git aliases
setup_git_aliases() {
    echo "🔧 Setting up git aliases..."
    
    # Create git aliases
    git config --global alias.vibe "!python3 $VIBE_BRANCHER_PATH"
    git config --global alias.vibe-verbose "!python3 $VIBE_BRANCHER_PATH --verbose"
    git config --global alias.vibe-create "!python3 $VIBE_BRANCHER_PATH --create"
    git config --global alias.should-branch "!python3 $VIBE_BRANCHER_PATH --verbose"
    git config --global alias.create-branch "!python3 $VIBE_BRANCHER_PATH --create"
    
    echo "✅ Git aliases created:"
    echo "   • git vibe - Quick analysis"
    echo "   • git vibe-verbose - Detailed analysis"
    echo "   • git vibe-create - Auto-create branch if recommended"
    echo "   • git should-branch - Alias for detailed analysis"
    echo "   • git create-branch - Alias for auto-create"
    echo ""
}

# Function to create a local config file
create_local_config() {
    echo "⚙️ Creating local configuration file..."
    
    CONFIG_FILE=".vibe-brancher-config.json"
    
    if [ -f "$CONFIG_FILE" ]; then
        echo "⚠️  Configuration file already exists: $CONFIG_FILE"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping configuration file creation."
            return
        fi
    fi
    
    # Create a customized config for the current repository
    cat > "$CONFIG_FILE" << EOF
{
  "thresholds": {
    "files_changed": 5,
    "lines_added": 50,
    "lines_removed": 30,
    "time_minutes": 30,
    "complexity_score": 7
  },
  "weights": {
    "files_changed": 0.3,
    "lines_changed": 0.25,
    "time_factor": 0.2,
    "complexity": 0.15,
    "file_types": 0.1
  },
  "file_type_weights": {
    ".py": 1.0,
    ".js": 0.8,
    ".ts": 0.9,
    ".java": 1.0,
    ".cpp": 1.0,
    ".c": 1.0,
    ".go": 1.0,
    ".rs": 1.0,
    ".html": 0.3,
    ".css": 0.3,
    ".json": 0.2,
    ".md": 0.1,
    ".txt": 0.1,
    ".yml": 0.4,
    ".yaml": 0.4,
    ".xml": 0.3,
    ".sql": 0.7,
    ".sh": 0.6,
    ".bat": 0.6
  },
  "branch_naming": {
    "prefix": "feature",
    "separator": "/",
    "include_timestamp": false
  }
}
EOF
    
    echo "✅ Created local configuration: $CONFIG_FILE"
    echo "   You can customize this file to match your workflow preferences."
    echo ""
}

# Function to create a pre-commit hook
create_pre_commit_hook() {
    echo "🪝 Setting up pre-commit hook..."
    
    HOOK_DIR=".git/hooks"
    HOOK_FILE="$HOOK_DIR/pre-commit"
    
    if [ -f "$HOOK_FILE" ]; then
        echo "⚠️  Pre-commit hook already exists: $HOOK_FILE"
        read -p "Do you want to add vibe brancher to it? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Skipping pre-commit hook creation."
            return
        fi
        
        # Backup existing hook
        cp "$HOOK_FILE" "$HOOK_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        echo "✅ Backed up existing hook to: $HOOK_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Create or append to pre-commit hook
    cat >> "$HOOK_FILE" << EOF

# Git Vibe Brancher - Pre-commit Analysis
echo "🔍 Running Git Vibe Brancher analysis..."
python3 "$VIBE_BRANCHER_PATH" --verbose
if [ \$? -ne 0 ]; then
    echo "⚠️  Vibe Brancher analysis failed, but continuing with commit..."
fi
EOF
    
    chmod +x "$HOOK_FILE"
    echo "✅ Pre-commit hook created/updated: $HOOK_FILE"
    echo "   The tool will now run before each commit to suggest branching."
    echo ""
}

# Function to create shell prompt integration
create_shell_integration() {
    echo "🐚 Setting up shell prompt integration..."
    
    # Detect shell
    SHELL_NAME=$(basename "$SHELL")
    
    case "$SHELL_NAME" in
        "bash")
            RC_FILE="$HOME/.bashrc"
            ;;
        "zsh")
            RC_FILE="$HOME/.zshrc"
            ;;
        *)
            echo "⚠️  Unsupported shell: $SHELL_NAME"
            echo "   Please manually add the vibe brancher function to your shell configuration."
            return
            ;;
    esac
    
    # Create the vibe brancher function
    VIBE_FUNCTION='# Git Vibe Brancher - Shell Integration
vibe_check() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        local result=$(python3 "'$VIBE_BRANCHER_PATH'" 2>/dev/null)
        if echo "$result" | grep -q "RECOMMENDATION: Create a new branch"; then
            echo "🌿 $(echo "$result" | grep "Branch Score" | sed "s/📊 //")"
        fi
    fi
}'
    
    # Check if function already exists
    if grep -q "vibe_check()" "$RC_FILE" 2>/dev/null; then
        echo "⚠️  Vibe brancher function already exists in $RC_FILE"
    else
        echo "$VIBE_FUNCTION" >> "$RC_FILE"
        echo "✅ Added vibe brancher function to $RC_FILE"
        echo "   Run 'source $RC_FILE' or restart your shell to activate."
        echo "   Then use 'vibe_check' command to see branch recommendations."
    fi
    echo ""
}

# Function to create IDE integration examples
create_ide_integration() {
    echo "💻 Creating IDE integration examples..."
    
    IDE_DIR=".vscode"
    mkdir -p "$IDE_DIR"
    
    # VS Code tasks
    cat > "$IDE_DIR/tasks.json" << EOF
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Vibe Brancher: Quick Analysis",
            "type": "shell",
            "command": "python3",
            "args": ["$VIBE_BRANCHER_PATH"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "Vibe Brancher: Detailed Analysis",
            "type": "shell",
            "command": "python3",
            "args": ["$VIBE_BRANCHER_PATH", "--verbose"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "Vibe Brancher: Create Branch",
            "type": "shell",
            "command": "python3",
            "args": ["$VIBE_BRANCHER_PATH", "--create"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        }
    ]
}
EOF
    
    echo "✅ Created VS Code tasks in $IDE_DIR/tasks.json"
    echo "   You can now run 'Ctrl+Shift+P' > 'Tasks: Run Task' > 'Vibe Brancher'"
    echo ""
}

# Function to test the integration
test_integration() {
    echo "🧪 Testing integration..."
    
    # Test basic functionality
    echo "Testing basic analysis..."
    python3 "$VIBE_BRANCHER_PATH" --verbose
    
    echo ""
    echo "✅ Integration test completed!"
    echo ""
}

# Main setup process
echo "What would you like to set up?"
echo "1. Git aliases (recommended)"
echo "2. Local configuration file"
echo "3. Pre-commit hook"
echo "4. Shell prompt integration"
echo "5. IDE integration (VS Code)"
echo "6. Test current integration"
echo "7. Set up everything (recommended for first time)"
echo ""

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        setup_git_aliases
        ;;
    2)
        create_local_config
        ;;
    3)
        create_pre_commit_hook
        ;;
    4)
        create_shell_integration
        ;;
    5)
        create_ide_integration
        ;;
    6)
        test_integration
        ;;
    7)
        echo "🚀 Setting up everything..."
        setup_git_aliases
        create_local_config
        create_pre_commit_hook
        create_shell_integration
        create_ide_integration
        test_integration
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo "🎉 Integration setup complete!"
echo ""
echo "📚 Usage Examples:"
echo "   • git vibe                    # Quick analysis"
echo "   • git vibe-verbose           # Detailed analysis"
echo "   • git vibe-create            # Auto-create branch"
echo "   • python3 $VIBE_BRANCHER_PATH --config .vibe-brancher-config.json"
echo ""
echo "💡 Pro Tips:"
echo "   • Customize .vibe-brancher-config.json for your workflow"
echo "   • Use 'vibe_check' in your shell prompt (after restarting shell)"
echo "   • The pre-commit hook will remind you to branch before commits"
echo "   • VS Code users can use Ctrl+Shift+P > Tasks > Vibe Brancher"
echo ""
echo "Happy vibe coding! 🌿"
