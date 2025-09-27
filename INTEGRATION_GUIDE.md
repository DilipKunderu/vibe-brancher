# Git Vibe Brancher - Integration Guide

This guide shows you how to integrate Git Vibe Brancher into your existing repository workflow.

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the integration setup script
./setup_integration.sh
```

### Option 2: Manual Setup
Follow the sections below to set up individual integrations.

## 🔧 Git Aliases (Already Set Up!)

The following git aliases are now available globally:

```bash
# Quick analysis
git vibe

# Detailed analysis with verbose output
git vibe-verbose
git should-branch

# Auto-create branch if recommended
git vibe-create
git create-branch
```

## ⚙️ Local Configuration

A local configuration file `.vibe-brancher-config.json` has been created with customized settings:

- **Lower thresholds** for more sensitive branching recommendations
- **Adjusted weights** to emphasize file count over line changes
- **Custom branch naming** with "feature/" prefix

### Using Custom Config
```bash
# Use local config
python3 vibe_brancher.py --config .vibe-brancher-config.json

# Or with git alias (if you modify the alias)
git vibe --config .vibe-brancher-config.json
```

## 🪝 Pre-commit Hook

A pre-commit hook has been installed that runs the vibe brancher analysis before each commit:

```bash
# The hook runs automatically, but you can test it:
git commit -m "Your commit message"
# You'll see the vibe brancher analysis output
```

## 🐚 Shell Integration

### Available Functions
Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Source the integration file
source /Users/dilipkunderu/git-vibe-brancher/shell_integration.sh

# Or copy the functions manually
vibe_check()    # Quick check for branch recommendations
vibe_analyze()  # Detailed analysis
vibe_branch()   # Create branch if recommended
```

### Shell Prompt Integration
Add to your prompt to see branch recommendations:

```bash
# For bash
PS1='$(vibe_check)'$PS1

# For zsh
PROMPT='$(vibe_check)'$PROMPT
```

## 💻 VS Code Integration

VS Code tasks have been created in `.vscode/tasks.json`:

1. **Ctrl+Shift+P** → **Tasks: Run Task**
2. Choose from:
   - **Vibe Brancher: Quick Analysis**
   - **Vibe Brancher: Detailed Analysis**
   - **Vibe Brancher: Create Branch**
   - **Vibe Brancher: With Custom Config**

## 📊 Usage Examples

### Daily Workflow
```bash
# Check if you should branch before starting work
git vibe

# Get detailed analysis
git vibe-verbose

# Create branch if recommended
git vibe-create
```

### Before Committing
```bash
# The pre-commit hook runs automatically, but you can also:
git vibe-verbose
# Review the analysis before committing
git commit -m "Your changes"
```

### Custom Analysis
```bash
# Use custom configuration
python3 vibe_brancher.py --config .vibe-brancher-config.json --verbose

# Create branch with custom name
python3 vibe_brancher.py --create --name "feature/my-awesome-feature"
```

## 🎯 Integration Tips

### 1. Team Workflow
- Share the `.vibe-brancher-config.json` with your team
- Set up the same git aliases across the team
- Use consistent branch naming conventions

### 2. CI/CD Integration
```bash
# Add to your CI pipeline
python3 vibe_brancher.py --verbose
# Use exit code to determine if branching is recommended
```

### 3. IDE Integration
- **VS Code**: Use the provided tasks
- **IntelliJ/PyCharm**: Create external tools pointing to the script
- **Vim/Neovim**: Add keybindings to run the tool

### 4. Shell Prompt
- Add `vibe_check` to your prompt for real-time feedback
- Use different colors for different recommendations
- Show branch score in your prompt

## 🔍 Troubleshooting

### Common Issues

1. **"Not in a git repository"**
   ```bash
   # Make sure you're in a git repository
   git status
   ```

2. **Permission denied**
   ```bash
   # Make sure the script is executable
   chmod +x vibe_brancher.py
   ```

3. **Python not found**
   ```bash
   # Use python3 explicitly
   python3 vibe_brancher.py
   ```

### Testing Integration
```bash
# Test all components
git vibe                    # Test git alias
vibe_analyze               # Test shell function
python3 vibe_brancher.py   # Test direct execution
```

## 📈 Customization

### Adjusting Thresholds
Edit `.vibe-brancher-config.json`:

```json
{
  "thresholds": {
    "files_changed": 3,    // Lower = more sensitive
    "lines_added": 30,     // Lower = more sensitive
    "time_minutes": 15,    // Lower = more sensitive
    "complexity_score": 5  // Lower = more sensitive
  }
}
```

### Custom Branch Naming
```json
{
  "branch_naming": {
    "prefix": "feature",           // Branch prefix
    "separator": "/",              // Separator character
    "include_timestamp": true      // Add timestamp to branch name
  }
}
```

### File Type Weights
```json
{
  "file_type_weights": {
    ".py": 1.0,    // Python files (high weight)
    ".js": 0.8,    // JavaScript files
    ".md": 0.1     // Documentation (low weight)
  }
}
```

## 🎉 You're All Set!

Your Git Vibe Brancher is now fully integrated into your workflow. The tool will help you make better branching decisions and maintain a clean git history.

### Next Steps
1. **Customize** the configuration to match your workflow
2. **Share** the setup with your team
3. **Integrate** with your CI/CD pipeline
4. **Monitor** your branching patterns and adjust thresholds

Happy vibe coding! 🌿
