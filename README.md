# Git Vibe Brancher 🌿

A smart tool that analyzes your coding session and suggests when to create a new git branch during "vibe coding" (informal, exploratory development).

## Features

- **Intelligent Analysis**: Considers multiple factors to determine when to branch:
  - Number of files changed
  - Lines of code added/removed
  - Time since last commit
  - Complexity of changes
  - File types being modified

- **Configurable Thresholds**: Customize the tool's sensitivity through a JSON config file
- **Smart Branch Naming**: Suggests meaningful branch names based on your changes
- **Git Integration**: Seamlessly works with your existing git workflow

## Installation

### Quick Install
```bash
# Clone the repository
git clone https://github.com/yourusername/git-vibe-brancher.git
cd git-vibe-brancher

# Run the installer
./install.sh
```

The installer will:
- Set up git aliases (`git vibe`, `git vibe-verbose`, etc.)
- Create git hooks for automatic analysis
- Optionally add to your PATH
- Configure git templates for new repositories

### Manual Install
1. Clone or download this repository
2. Make scripts executable: `chmod +x vibe_brancher.py git-vibe`
3. Add to PATH or use full path to scripts

## Usage

### Basic Analysis
```bash
./vibe_brancher.py
```

### Detailed Analysis
```bash
./vibe_brancher.py --verbose
```

### Auto-create Branch
```bash
./vibe_brancher.py --create
```

### Custom Branch Name
```bash
./vibe_brancher.py --create --name "feature/my-awesome-feature"
```

### Custom Configuration
```bash
./vibe_brancher.py --config /path/to/your/config.json
```

## Configuration

The tool uses `config.json` to customize its behavior. Key settings:

### Thresholds
- `files_changed`: Number of files that trigger branching consideration (default: 5)
- `lines_added`: Lines added threshold (default: 50)
- `lines_removed`: Lines removed threshold (default: 30)
- `time_minutes`: Minutes since last commit (default: 30)
- `complexity_score`: Complexity score threshold (default: 7)

### Weights
Control how much each factor influences the branching decision:
- `files_changed`: Weight for file count factor (default: 0.3)
- `lines_changed`: Weight for line changes (default: 0.25)
- `time_factor`: Weight for time since last commit (default: 0.2)
- `complexity`: Weight for complexity score (default: 0.15)
- `file_types`: Weight for file type complexity (default: 0.1)

### File Type Weights
Different file types have different complexity weights:
- Source code files (.py, .js, .java, etc.): Higher weights (0.8-1.0)
- Configuration files (.json, .yml): Medium weights (0.2-0.4)
- Documentation (.md, .txt): Lower weights (0.1)

## How It Works

The tool calculates a "branch score" (0.0 to 1.0) based on:

1. **File Count Factor**: More files = higher score
2. **Line Change Factor**: More additions/deletions = higher score
3. **Time Factor**: Longer since last commit = higher score
4. **Complexity Factor**: Based on file types and change patterns
5. **File Type Factor**: Different file types have different weights

If the final score is ≥ 0.6, the tool recommends creating a new branch.

## Examples

### Scenario 1: Small Changes
```
🔍 Git Vibe Brancher Analysis
========================================
⏳ RECOMMENDATION: Continue on current branch
📊 Branch Score: 0.25/1.0
```

### Scenario 2: Significant Changes
```
🔍 Git Vibe Brancher Analysis
========================================
🌿 RECOMMENDATION: Create a new branch!
📊 Branch Score: 0.78/1.0

💡 Suggested branch name: feature/user-authentication
```

## Git Integration

### Git Aliases (Auto-configured by installer)
```bash
git vibe                    # Quick analysis
git vibe-verbose           # Detailed analysis  
git vibe-create            # Auto-create branch if recommended
git vibe-check             # Same as vibe-verbose
git vibe-status            # Analysis + git status
git vibe-diff              # Analysis + git diff stats
```

### Git Hooks
The installer sets up git hooks for automatic analysis:

**Pre-commit Hook**: Runs vibe analysis before each commit
```bash
# Enable for current repository
./setup-git-hooks

# Or manually copy the hook
cp ~/.git-templates/hooks/pre-commit-vibe .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Post-checkout Hook**: Runs analysis when switching branches

### Shell Integration
For enhanced workflow, add to your shell profile:
```bash
# Add to ~/.bashrc, ~/.zshrc, etc.
source /path/to/git-vibe-brancher/shell-integration.sh
```

This provides additional commands:
```bash
vibe_commit [args]         # Commit with vibe analysis
vibe_branch [name]         # Create branch with vibe analysis  
vibe_status                # Vibe analysis + git status
vibe_diff                  # Vibe analysis + git diff stats
```

## Requirements

- Python 3.6+
- Git repository
- No additional Python packages required (uses only standard library)

## License

MIT License - feel free to modify and distribute!