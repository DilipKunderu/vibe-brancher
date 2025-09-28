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

1. Clone or download this repository
2. Make the script executable: `chmod +x vibe_brancher.py`
3. Optionally, add to your PATH for global access

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

### Auto-Commit Changes (NEW!)
```bash
# Auto-commit with intelligent message generation
./vibe_brancher.py --commit

# Interactive auto-commit (shows files and asks for confirmation)
./vibe_brancher.py --commit --interactive

# Vibe coding commit (analyze + suggest branching + auto-commit)
./vibe_brancher.py --vibe-commit

# Custom commit message
./vibe_brancher.py --commit --message "Your custom message"
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

### Auto-Commit Settings (NEW!)
Control automatic commit behavior:
- `enabled`: Enable/disable auto-commit functionality
- `interactive_by_default`: Use interactive mode by default
- `commit_message_templates`: Customize commit message formats
- `include_statistics`: Include line count statistics in messages
- `max_files_display`: Maximum files to show in interactive mode

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

## 🎮 Unified Demo System

### Single Demo Script
Experience all Git Vibe Brancher features with our unified demo system:

```bash
# Interactive launcher with options
./run_demo

# Or run directly with different types
python3 demo.py                    # Full demo (comprehensive)
python3 demo.py --type quick       # Quick demo (basic features)
python3 demo.py --type visualizer  # Visualizer API demo only
python3 demo.py --help-demo        # Show demo help
```

### Demo Types
- **Full Demo**: Comprehensive demonstration with all features
  - Core vibe brancher analysis and branching suggestions
  - Auto-commit functionality with intelligent messages
  - Interactive commit mode with file preview
  - Vibe coding workflow combining analysis and auto-commit
  - Persistent branches that remain after the demo
  - Branch-out-of-branch scenarios
  - Live visualizer API monitoring
  - Web server on port 7171

- **Quick Demo**: Basic features for quick overview
  - Core vibe brancher analysis
  - Simple auto-commit demonstration
  - Visualizer API web server

- **Visualizer Demo**: API and web server functionality only
  - Web server on port 7171
  - RESTful API endpoints
  - Real-time git data
  - Web interface

## Git Aliases

Set up convenient git aliases for easy access:

```bash
# Analysis aliases
git config --global alias.vibe '!python3 /path/to/vibe_brancher.py'
git config --global alias.vibe-verbose '!python3 /path/to/vibe_brancher.py --verbose'
git config --global alias.vibe-create '!python3 /path/to/vibe_brancher.py --create'

# Auto-commit aliases (NEW!)
git config --global alias.auto-commit '!python3 /path/to/vibe_brancher.py --commit'
git config --global alias.vibe-commit '!python3 /path/to/vibe_brancher.py --vibe-commit'
git config --global alias.vibe-commit-interactive '!python3 /path/to/vibe_brancher.py --vibe-commit --interactive'
```

## Integration Ideas

- Add to your shell prompt to show branch recommendations
- Use in pre-commit hooks
- Integrate with your IDE or editor
- Use auto-commit for frequent commits during vibe coding
- Set up as a git alias: `git config --global alias.vibe '!./path/to/vibe_brancher.py'`

## Requirements

- Python 3.6+
- Git repository
- No additional Python packages required (uses only standard library)

## License

MIT License - feel free to modify and distribute!
