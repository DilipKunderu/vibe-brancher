#!/bin/bash
# Shell integration for Git Vibe Brancher
# Add this to your shell profile for enhanced git workflow

# Function to run vibe analysis before git operations
vibe_git() {
    local cmd="$1"
    shift
    
    # Run vibe analysis for certain git commands
    case "$cmd" in
        "add"|"commit"|"status"|"diff")
            echo "🔍 Running vibe analysis..."
            python3 "$(git config --global --get vibe-brancher.path 2>/dev/null || echo "$HOME/git-vibe-brancher")/vibe_brancher.py"
            echo ""
            ;;
    esac
    
    # Execute the original git command
    git "$cmd" "$@"
}

# Function to check vibe before committing
vibe_commit() {
    echo "🔍 Running vibe analysis before commit..."
    python3 "$(git config --global --get vibe-brancher.path 2>/dev/null || echo "$HOME/git-vibe-brancher")/vibe_brancher.py" --verbose
    
    echo ""
    read -p "🤔 Continue with commit? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git commit "$@"
    else
        echo "❌ Commit cancelled."
    fi
}

# Function to create branch with vibe analysis
vibe_branch() {
    local branch_name="$1"
    
    if [ -z "$branch_name" ]; then
        echo "🔍 Analyzing current changes..."
        python3 "$(git config --global --get vibe-brancher.path 2>/dev/null || echo "$HOME/git-vibe-brancher")/vibe_brancher.py" --verbose
        
        echo ""
        read -p "🤔 Create branch based on analysis? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            python3 "$(git config --global --get vibe-brancher.path 2>/dev/null || echo "$HOME/git-vibe-brancher")/vibe_brancher.py" --create
        fi
    else
        git checkout -b "$branch_name"
        echo "🌿 Created and switched to branch: $branch_name"
    fi
}

# Function to show vibe status
vibe_status() {
    echo "🔍 Running vibe analysis..."
    python3 "$(git config --global --get vibe-brancher.path 2>/dev/null || echo "$HOME/git-vibe-brancher")/vibe_brancher.py"
    echo ""
    echo "📊 Git Status:"
    git status --short
}

# Function to show vibe diff
vibe_diff() {
    echo "🔍 Running vibe analysis..."
    python3 "$(git config --global --get vibe-brancher.path 2>/dev/null || echo "$HOME/git-vibe-brancher")/vibe_brancher.py"
    echo ""
    echo "📊 Git Diff Stats:"
    git diff --stat
}

# Export functions for use in shell
export -f vibe_git vibe_commit vibe_branch vibe_status vibe_diff

echo "✅ Git Vibe Brancher shell integration loaded!"
echo ""
echo "🚀 New commands available:"
echo "   vibe_commit [args]     - Commit with vibe analysis"
echo "   vibe_branch [name]     - Create branch with vibe analysis"
echo "   vibe_status            - Vibe analysis + git status"
echo "   vibe_diff              - Vibe analysis + git diff stats"
echo ""
echo "💡 Add this to your shell profile:"
echo "   source $(pwd)/shell-integration.sh"
