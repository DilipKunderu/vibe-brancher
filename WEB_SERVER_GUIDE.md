# Git Vibe Brancher - Web Server Guide

## 🌐 **Web Server on Port 7171**

The Git Vibe Brancher Visualizer API can now run as a web server on port 7171, providing RESTful endpoints for real-time git repository data.

## 🚀 **Quick Start**

### **Start the Web Server**
```bash
# Default: localhost:7171
python3 visualizer_api.py --server

# Custom port
python3 visualizer_api.py --server --port 8080

# Custom host and port
python3 visualizer_api.py --server --host 0.0.0.0 --port 7171

# Monitor different repository
python3 visualizer_api.py --server --repo /path/to/your/repo
```

### **Access the Web Interface**
Open your browser and go to: **http://localhost:7171**

## 🔗 **API Endpoints**

### **1. Health Check**
```bash
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "repository": "/path/to/repo",
  "currentBranch": "main",
  "timestamp": "2024-09-27T16:25:29.474496"
}
```

### **2. Complete Git Data**
```bash
GET /api/git-data
```
**Response:**
```json
{
  "sessionId": "session_20240927_162529",
  "startTime": "2024-09-27T16:25:29.123456",
  "currentBranch": "main",
  "totalBranches": 2,
  "totalCommits": 18,
  "totalFilesChanged": 0,
  "branches": [
    {
      "name": "main",
      "type": "main",
      "createdAt": "2024-09-27T15:44:43",
      "lastCommit": "2024-09-27T15:44:43",
      "commitCount": 18,
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

### **3. Branches List**
```bash
GET /api/branches
```
**Response:**
```json
{
  "branches": [...],
  "currentBranch": "main",
  "totalBranches": 2
}
```

### **4. Current Branch Info**
```bash
GET /api/current-branch
```
**Response:**
```json
{
  "currentBranch": "main",
  "branchData": {
    "name": "main",
    "type": "main",
    "commitCount": 18,
    "vibeScore": 0.22,
    "isActive": true
  }
}
```

### **5. Repository Statistics**
```bash
GET /api/stats
```
**Response:**
```json
{
  "totalBranches": 2,
  "totalCommits": 18,
  "totalFilesChanged": 0,
  "sessionId": "session_20240927_162529",
  "startTime": "2024-09-27T16:25:29.123456"
}
```

## 💻 **Usage Examples**

### **JavaScript/Fetch**
```javascript
// Get complete git data
fetch('http://localhost:7171/api/git-data')
  .then(response => response.json())
  .then(data => {
    console.log('Current branch:', data.currentBranch);
    console.log('Total branches:', data.totalBranches);
    console.log('Branches:', data.branches);
  });

// Get health status
fetch('http://localhost:7171/api/health')
  .then(response => response.json())
  .then(health => {
    if (health.status === 'healthy') {
      console.log('API is running on:', health.repository);
    }
  });
```

### **Python/Requests**
```python
import requests

# Get git data
response = requests.get('http://localhost:7171/api/git-data')
data = response.json()

print(f"Current branch: {data['currentBranch']}")
print(f"Total branches: {data['totalBranches']}")

# Get branches
response = requests.get('http://localhost:7171/api/branches')
branches_data = response.json()

for branch in branches_data['branches']:
    print(f"Branch: {branch['name']} ({branch['type']})")
```

### **cURL**
```bash
# Health check
curl http://localhost:7171/api/health

# Get git data
curl http://localhost:7171/api/git-data

# Get branches
curl http://localhost:7171/api/branches

# Get current branch
curl http://localhost:7171/api/current-branch

# Get stats
curl http://localhost:7171/api/stats
```

### **Node.js/Express Integration**
```javascript
const express = require('express');
const fetch = require('node-fetch');

const app = express();

// Proxy git data to your frontend
app.get('/api/git-data', async (req, res) => {
  try {
    const response = await fetch('http://localhost:7171/api/git-data');
    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch git data' });
  }
});

app.listen(3000, () => {
  console.log('Your app is running on port 3000');
});
```

## 🌐 **Web Interface**

The web server includes a beautiful HTML interface at **http://localhost:7171** that shows:

- ✅ **Server Status** - Repository and current branch info
- 📋 **API Documentation** - All available endpoints
- 💻 **Usage Examples** - Code samples for JavaScript, Python, cURL
- 🔗 **Direct Links** - Click to test endpoints

## 🔧 **Configuration Options**

### **Command Line Arguments**
```bash
python3 visualizer_api.py --server [OPTIONS]

Options:
  --repo REPO     Path to git repository (default: current directory)
  --port PORT     Port for web server (default: 7171)
  --host HOST     Host for web server (default: localhost)
```

### **Environment Variables**
```bash
# Set default repository
export GIT_VIBE_REPO="/path/to/your/repo"

# Set default port
export GIT_VIBE_PORT="8080"

# Set default host
export GIT_VIBE_HOST="0.0.0.0"
```

## 🚀 **Integration with Lovable.dev**

Perfect for the Lovable.dev visualizer! The web server provides:

### **Real-time Data**
```javascript
// Poll for updates every 2 seconds
setInterval(async () => {
  const response = await fetch('http://localhost:7171/api/git-data');
  const data = await response.json();
  
  // Update your visualizer
  updateBranchGraph(data.branches);
  updateStats(data);
}, 2000);
```

### **WebSocket-like Updates**
```javascript
// Simple polling for real-time updates
async function watchRepository() {
  while (true) {
    try {
      const response = await fetch('http://localhost:7171/api/git-data');
      const data = await response.json();
      
      // Check if data changed
      if (data.sessionId !== lastSessionId) {
        updateVisualizer(data);
        lastSessionId = data.sessionId;
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
}
```

## 🛠️ **Development Setup**

### **Install Dependencies**
```bash
pip3 install flask requests
```

### **Test the Server**
```bash
# Run the test script
python3 test_web_server.py

# Or test manually
python3 visualizer_api.py --server --port 7171
curl http://localhost:7171/api/health
```

### **Production Deployment**
```bash
# Use gunicorn for production
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:7171 visualizer_api:app

# Or use Docker
docker run -p 7171:7171 -v /path/to/repo:/repo git-vibe-brancher
```

## 🎯 **Use Cases**

### **1. Live Branch Visualizer**
- Real-time branch monitoring
- Interactive git workflow visualization
- Team collaboration dashboards

### **2. Development Tools**
- IDE integrations
- Git workflow automation
- Code review assistance

### **3. CI/CD Integration**
- Build pipeline monitoring
- Deployment status tracking
- Branch health metrics

### **4. Educational/Training**
- Git workflow demonstrations
- Branching strategy visualization
- Code collaboration patterns

## 🔒 **Security Considerations**

### **Local Development**
```bash
# Safe for local development
python3 visualizer_api.py --server --host localhost --port 7171
```

### **Network Access**
```bash
# Accessible from network (use with caution)
python3 visualizer_api.py --server --host 0.0.0.0 --port 7171
```

### **Production Security**
- Use reverse proxy (nginx, Apache)
- Implement authentication
- Use HTTPS
- Restrict network access

## 🎉 **Perfect for Lovable.dev!**

The web server on port 7171 is ideal for the Lovable.dev visualizer because:

- ✅ **RESTful API** - Easy to integrate
- ✅ **Real-time Data** - Live updates
- ✅ **JSON Format** - Standard data exchange
- ✅ **Health Checks** - Reliable monitoring
- ✅ **Web Interface** - Built-in documentation
- ✅ **Cross-Origin** - Works with web apps

Start the server and build your beautiful git branch visualizer! 🌿
