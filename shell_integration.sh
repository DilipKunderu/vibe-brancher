# Git Vibe Brancher - Shell Integration
# Add this to your ~/.bashrc or ~/.zshrc

# Function to check if you should create a new branch
vibe_check() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        local result=$(python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py 2>/dev/null)
        if echo "$result" | grep -q "RECOMMENDATION: Create a new branch"; then
            echo "🌿 $(echo "$result" | grep "Branch Score" | sed "s/📊 //")"
        fi
    fi
}

# Function to get detailed vibe analysis
vibe_analyze() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py --verbose
    else
        echo "❌ Not in a git repository"
    fi
}

# Function to create branch if recommended
vibe_branch() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py --create
    else
        echo "❌ Not in a git repository"
    fi
}

# Add to your PS1 prompt (optional)
# For bash: PS1='$(vibe_check)'$PS1
# For zsh: PROMPT='$(vibe_check)'$PROMPT
