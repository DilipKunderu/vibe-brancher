# Git Vibe Brancher - Auto-Commit Guide

## 🚀 New Feature: Auto-Commit for Vibe Coding

The Git Vibe Brancher now includes powerful auto-commit functionality that creates intelligent commits for each change during your "vibe coding" sessions.

## ✨ Features

### **Intelligent Commit Messages**
- Automatically generates commit messages based on file types and changes
- Uses conventional commit format (feat:, docs:, config:, etc.)
- Includes line statistics (+X lines, -Y lines)
- Customizable message templates

### **Smart Change Analysis**
- Analyzes file types to determine commit category
- Counts lines added/removed for statistics
- Groups related changes intelligently

### **Interactive Mode**
- Shows files to be committed before proceeding
- Asks for confirmation in interactive mode
- Displays detailed change information

### **Branch Integration**
- Suggests creating branches for significant changes
- Combines branching analysis with auto-commit
- Maintains clean git workflow

## 🎯 Usage Options

### **1. Simple Auto-Commit**
```bash
# Auto-commit with intelligent message generation
python3 vibe_brancher.py --commit

# Or use the git alias
git auto-commit
```

### **2. Interactive Auto-Commit**
```bash
# Interactive mode - shows files and asks for confirmation
python3 vibe_brancher.py --commit --interactive

# Or use the git alias
git auto-commit --interactive
```

### **3. Vibe Coding Commit (Recommended)**
```bash
# Combines analysis + branching suggestion + auto-commit
python3 vibe_brancher.py --vibe-commit

# Interactive vibe commit
python3 vibe_brancher.py --vibe-commit --interactive

# Or use the git alias
git vibe-commit
git vibe-commit-interactive
```

### **4. Custom Commit Message**
```bash
# Override auto-generated message
python3 vibe_brancher.py --commit --message "Your custom message"

# Or
python3 vibe_brancher.py --commit -m "Your custom message"
```

## 📊 Commit Message Examples

### **Feature Development**
```
feat: add user_authentication functionality (+453 lines)
feat: add 3 files with new functionality (+120 lines)
```

### **Documentation**
```
docs: update README documentation (+25 lines)
docs: update 2 documentation files (+45 lines)
```

### **Configuration**
```
config: update database configuration (+12 lines)
config: update 3 configuration files (+30 lines)
```

### **Scripts**
```
script: update deploy script (+15 lines)
script: add 2 new utility scripts (+50 lines)
```

### **General Updates**
```
update: update main_controller (+8 lines)
update: update 5 files (+25 lines, -10 lines)
```

## ⚙️ Configuration

### **Auto-Commit Settings**
Add to your `.vibe-brancher-config.json`:

```json
{
  "auto_commit": {
    "enabled": true,
    "interactive_by_default": false,
    "commit_message_templates": {
      "feat": "feat: {description}",
      "fix": "fix: {description}",
      "docs": "docs: {description}",
      "config": "config: {description}",
      "script": "script: {description}",
      "update": "update: {description}"
    },
    "include_statistics": true,
    "max_files_display": 5
  }
}
```

### **Configuration Options**

- **`enabled`**: Enable/disable auto-commit functionality
- **`interactive_by_default`**: Use interactive mode by default
- **`commit_message_templates`**: Customize message templates
- **`include_statistics`**: Include line count statistics
- **`max_files_display`**: Max files to show in interactive mode

## 🔧 Git Aliases

The following git aliases are now available:

```bash
# Auto-commit aliases
git auto-commit                    # Simple auto-commit
git vibe-commit                    # Vibe coding commit (recommended)
git vibe-commit-interactive        # Interactive vibe commit

# Original aliases
git vibe                          # Quick analysis
git vibe-verbose                  # Detailed analysis
git vibe-create                   # Auto-create branch
```

## 🎮 Vibe Coding Workflow

### **Recommended Daily Workflow**

1. **Start coding session**
   ```bash
   git vibe  # Check if you should branch
   ```

2. **Make changes and commit frequently**
   ```bash
   git vibe-commit  # Analyze, suggest branching, and commit
   ```

3. **For significant changes**
   ```bash
   git vibe-create  # Create branch if recommended
   git vibe-commit  # Continue committing on the branch
   ```

### **Interactive Workflow**
```bash
# For more control over commits
git vibe-commit-interactive
```

This will:
- Show analysis results
- Suggest branching if needed
- Display files to be committed
- Ask for confirmation before committing

## 📈 Benefits

### **Clean Git History**
- Atomic commits for each logical change
- Consistent commit message format
- Clear separation of concerns

### **Improved Productivity**
- No need to manually write commit messages
- Automatic staging of changes
- Intelligent change categorization

### **Better Collaboration**
- Consistent commit format across team
- Clear commit history for code reviews
- Easy to track changes and features

### **Vibe Coding Support**
- Perfect for exploratory development
- Frequent commits without overhead
- Maintains clean git workflow

## 🧪 Testing the Feature

### **Test Scenarios**

1. **Single File Change**
   ```bash
   echo "// Test change" > test.js
   git vibe-commit
   # Result: "feat: add test functionality (+1 lines)"
   ```

2. **Multiple Files**
   ```bash
   echo "# Docs" > README.md
   echo "// Code" > app.js
   git vibe-commit
   # Result: "feat: add 2 files with new functionality (+2 lines)"
   ```

3. **Documentation Update**
   ```bash
   echo "# Updated docs" >> README.md
   git vibe-commit
   # Result: "docs: update README documentation (+1 lines)"
   ```

4. **Interactive Mode**
   ```bash
   echo "// Interactive test" > interactive.js
   git vibe-commit-interactive
   # Shows files and asks for confirmation
   ```

## 🎉 Success!

The auto-commit feature is now fully integrated and working perfectly. It will help you maintain a clean, organized git history during your vibe coding sessions while providing intelligent commit messages and branching suggestions.

**Happy vibe coding with auto-commits! 🌿**
