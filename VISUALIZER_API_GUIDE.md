# Git Vibe Brancher - Visualizer API Usage Guide

## 🎯 Overview

The `visualizer_api.py` script provides real-time git repository data for the live graph visualizer. It monitors git repositories and outputs structured JSON data that can be consumed by web applications to create beautiful branch visualizations.

## 🚀 Basic Usage

### **1. Get Repository Summary**
```bash
python3 visualizer_api.py
```
**Output**: Human-readable summary of current repository
```
Repository: git-vibe-brancher
Current Branch: master
Total Branches: 1
Total Commits: 6
Total Files Changed: 0

Branches:
  • master (main) - 6 commits
```

### **2. Get JSON Data for Visualizer**
```bash
python3 visualizer_api.py --json
```
**Output**: Structured JSON data for web applications
```json
{
  "sessionId": "session_20240927_154624",
  "startTime": "2024-09-27T15:46:24.123456",
  "currentBranch": "master",
  "totalBranches": 1,
  "totalCommits": 6,
  "totalFilesChanged": 0,
  "branches": [
    {
      "name": "master",
      "type": "main",
      "createdAt": "2024-09-27T15:44:43",
      "lastCommit": "2024-09-27T15:44:43",
      "commitCount": 6,
      "fileChanges": {
        "added": 0,
        "modified": 0,
        "deleted": 0,
        "linesAdded": 0,
        "linesRemoved": 0
      },
      "vibeScore": 0.22,
      "isActive": true
    }
  ],
  "repository": {
    "path": "/path/to/repo",
    "name": "git-vibe-brancher"
  }
}
```

### **3. Monitor Different Repository**
```bash
python3 visualizer_api.py --repo /path/to/your/repository --json
```
**Use case**: Monitor a specific repository instead of current directory

### **4. Real-Time Monitoring (Watch Mode)**
```bash
python3 visualizer_api.py --watch
```
**Output**: Continuously outputs JSON data whenever repository changes
**Use case**: Live updates for real-time visualizer

## 📊 Data Structure

### **Session Data**
```typescript
interface SessionData {
  sessionId: string;           // Unique session identifier
  startTime: string;          // ISO timestamp of session start
  currentBranch: string;      // Currently active branch
  totalBranches: number;      // Total number of branches
  totalCommits: number;       // Total commits across all branches
  totalFilesChanged: number;  // Total files modified
  branches: BranchNode[];     // Array of branch information
  repository: RepositoryInfo; // Repository metadata
}
```

### **Branch Node**
```typescript
interface BranchNode {
  name: string;               // Branch name
  type: 'main' | 'feature' | 'bugfix' | 'hotfix' | 'other';
  createdAt: string;          // ISO timestamp of creation
  lastCommit: string;         // ISO timestamp of last commit
  commitCount: number;        // Number of commits on branch
  fileChanges: {
    added: number;            // Files added
    modified: number;         // Files modified
    deleted: number;          // Files deleted
    linesAdded: number;       // Lines added
    linesRemoved: number;     // Lines removed
  };
  vibeScore: number;          // Git Vibe Brancher score (0.0-1.0)
  isActive: boolean;          // Whether this is the current branch
}
```

### **Repository Info**
```typescript
interface RepositoryInfo {
  path: string;               // Full path to repository
  name: string;               // Repository name (basename)
}
```

## 🔧 Integration Examples

### **1. Web Application Integration**
```javascript
// Fetch data from API
async function fetchGitData() {
  const response = await fetch('/api/git-data');
  const data = await response.json();
  
  // Update visualizer with new data
  updateGraph(data.branches);
  updateStats(data);
}

// Poll for updates every 2 seconds
setInterval(fetchGitData, 2000);
```

### **2. Node.js Backend Integration**
```javascript
const { spawn } = require('child_process');

// Start the visualizer API in watch mode
const apiProcess = spawn('python3', ['visualizer_api.py', '--watch']);

apiProcess.stdout.on('data', (data) => {
  const sessionData = JSON.parse(data.toString());
  
  // Broadcast to connected clients
  io.emit('git-update', sessionData);
});
```

### **3. Python Integration**
```python
import subprocess
import json

def get_git_data(repo_path=None):
    cmd = ['python3', 'visualizer_api.py', '--json']
    if repo_path:
        cmd.extend(['--repo', repo_path])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

# Get current repository data
data = get_git_data()
print(f"Current branch: {data['currentBranch']}")
```

## 🎨 Visualizer Integration

### **Real-Time Updates**
The visualizer should poll the API every 2 seconds or use the watch mode for real-time updates:

```bash
# Terminal 1: Start the API in watch mode
python3 visualizer_api.py --watch

# Terminal 2: Start your visualizer application
npm start
```

### **WebSocket Integration**
For real-time updates, you can create a WebSocket server that uses the API:

```python
import asyncio
import websockets
import subprocess
import json

async def git_data_handler(websocket, path):
    # Start the visualizer API
    process = subprocess.Popen(
        ['python3', 'visualizer_api.py', '--watch'],
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Stream data to connected clients
    for line in process.stdout:
        if line.strip():
            await websocket.send(line.strip())

# Start WebSocket server
start_server = websockets.serve(git_data_handler, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
```

## 🚀 Advanced Usage

### **Custom Repository Monitoring**
```bash
# Monitor specific repository with custom polling
python3 visualizer_api.py --repo /path/to/project --json
```

### **Integration with Git Hooks**
Add to your `.git/hooks/post-commit`:
```bash
#!/bin/bash
# Trigger visualizer update after commit
python3 /path/to/visualizer_api.py --json > /tmp/git-data.json
```

### **CI/CD Integration**
```yaml
# GitHub Actions example
- name: Update Visualizer
  run: |
    python3 visualizer_api.py --json > visualizer-data.json
    # Upload to your visualizer service
```

## 🎯 Use Cases

### **1. Development Team Dashboard**
- Real-time branch activity monitoring
- Team productivity metrics
- Branch creation patterns analysis

### **2. Code Review Visualization**
- Visual representation of feature branches
- Merge conflict prediction
- Code review workflow optimization

### **3. Project Management**
- Sprint progress tracking
- Feature completion visualization
- Developer workload distribution

### **4. Educational/Training**
- Git workflow demonstration
- Branching strategy visualization
- Code collaboration patterns

## 🔧 Troubleshooting

### **Common Issues**

1. **"Not in a git repository"**
   ```bash
   # Solution: Specify repository path
   python3 visualizer_api.py --repo /path/to/git/repo
   ```

2. **Permission denied**
   ```bash
   # Solution: Make script executable
   chmod +x visualizer_api.py
   ```

3. **Python not found**
   ```bash
   # Solution: Use python3 explicitly
   python3 visualizer_api.py --json
   ```

### **Performance Tips**

- Use `--json` flag for programmatic consumption
- Implement caching for large repositories
- Use watch mode sparingly to avoid excessive git operations
- Consider rate limiting for web applications

## 📚 Examples

### **Complete Demo**
Run the demonstration script to see all features:
```bash
python3 demo_visualizer_api.py
```

### **Quick Test**
```bash
# Test with current repository
python3 visualizer_api.py --json | jq '.branches[].name'

# Test with different repository
python3 visualizer_api.py --repo /path/to/repo --json | jq '.totalBranches'
```

The visualizer API is designed to be simple, reliable, and easy to integrate with any web application or visualization tool! 🌿
