# Git Vibe Brancher 🌿

Invisible git management for vibe coders. Automatically saves progress, creates branches, and suggests merges without interrupting your flow.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/git-vibe-brancher.git
cd git-vibe-brancher
```

### 2. Run the installer
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- Set up git aliases (`git vibe`, `git save`, `git vibe-autosave`, etc.)
- Create git hooks for automatic analysis
- Add the tool to your PATH
- Configure git templates for new repositories

### 3. Verify installation
```bash
git vibe --help
```

## Quick Start

```bash
# Start invisible auto-save
git vibe-autosave

# Just code - everything happens automatically
# Progress saved every 60 seconds
# Branches created for significant changes
# Merge suggestions when ready

# Stop when done
git vibe-autosave-stop
```

## Manual Commands

```bash
git vibe                    # Analyze current changes
git vibe-verbose           # Detailed analysis
git save                   # Save progress with auto-branching
git checkpoint             # Alias for save
git vibe-convergence       # Check if branch ready to merge
```

## How It Works

- **Auto-save**: Saves progress every 60 seconds
- **Auto-branch**: Creates branches for significant changes (5+ files, 50+ lines)
- **Convergence**: Analyzes when branches are ready to merge
- **Invisible**: Runs in background, zero interruption

## Configuration

Edit `config.json` to customize thresholds:
- `files_changed`: Files needed to trigger branching (default: 5)
- `lines_added`: Lines added threshold (default: 50)
- `time_minutes`: Minutes since last commit (default: 30)

## Requirements

- Python 3.6+
- Git repository

## License

MIT