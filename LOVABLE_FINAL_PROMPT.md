# Git Vibe Brancher Live Graph Visualizer - Complete Lovable.dev Prompt

## Project Overview
Create a beautiful, real-time graph visualizer for the Git Vibe Brancher tool that tracks and visualizes git branches as they're created during "vibe coding" sessions.

## 🎯 Core Features

### 1. Real-Time Branch Visualization
- **Interactive D3.js graph** with nodes representing git branches
- **Live updates** when new branches are created by the Git Vibe Brancher
- **Smooth animations** for new nodes appearing and connections forming
- **Color-coded branches** based on type (feature=green, bugfix=orange, main=blue, hotfix=red)

### 2. Branch Information Panel
- **Detailed branch view** showing:
  - Branch name and creation timestamp
  - Commit count and file changes
  - Lines added/removed statistics
  - Vibe Brancher analysis score (0.0-1.0)
  - Branch recommendation reasoning

### 3. Session Analytics Dashboard
- **Real-time statistics**:
  - Total branches created in session
  - Current active branch
  - Session duration
  - Total commits and file changes
  - Productivity metrics

## 🛠 Technical Stack
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Graph Visualization**: D3.js with React integration
- **Animations**: Framer Motion for smooth transitions
- **Backend**: Node.js/Express for API integration
- **Data Source**: Git Vibe Brancher API (Python script provided)

## 📊 Data Integration

### Git Vibe Brancher API
The visualizer connects to a Python API that provides real-time git data:

```bash
# Get current session data
python3 visualizer_api.py --json

# Watch for changes (real-time updates)
python3 visualizer_api.py --watch
```

### Sample API Response
```json
{
  "sessionId": "session_20240927_153927",
  "startTime": "2024-09-27T15:39:27.640487",
  "currentBranch": "feature/user-authentication",
  "totalBranches": 3,
  "totalCommits": 25,
  "totalFilesChanged": 31,
  "branches": [
    {
      "name": "feature/user-authentication",
      "type": "feature",
      "createdAt": "2024-09-27T15:34:43",
      "lastCommit": "2024-09-27T15:34:43",
      "commitCount": 19,
      "fileChanges": {
        "added": 4,
        "modified": 2,
        "deleted": 0,
        "linesAdded": 453,
        "linesRemoved": 12
      },
      "vibeScore": 0.96,
      "isActive": true
    }
  ],
  "repository": {
    "path": "/path/to/repo",
    "name": "PoorlyWrittenService"
  }
}
```

## 🎨 UI Design

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│ 🌿 Git Vibe Brancher - Live Visualizer                 │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────────────────────┐ │
│ │ Repository Info │ │ Interactive Branch Graph        │ │
│ │ PoorlyWritten   │ │ • Nodes = Branches              │ │
│ │ Service         │ │ • Colors = Branch Types         │ │
│ │                 │ │ • Size = Commit Count           │ │
│ │ Session Stats   │ │ • Glow = Active Branch          │ │
│ │ • 3 branches    │ │                                 │ │
│ │ • 25 commits    │ │                                 │ │
│ │ • 2.5 hours     │ │                                 │ │
│ │ • Current:      │ │                                 │ │
│ │   feature/auth  │ │                                 │ │
│ └─────────────────┘ └─────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Selected: feature/user-authentication                   │
│ Created: 2h ago | Commits: 19 | Files: 6 | Score: 0.96 │
│ Changes: +453 lines, -12 lines | Type: Feature Branch   │
└─────────────────────────────────────────────────────────┘
```

### Visual Design Elements
- **Color Palette**:
  - Main branch: Deep blue (#1e40af)
  - Feature branches: Emerald green (#10b981)
  - Bugfix branches: Amber orange (#f59e0b)
  - Hotfix branches: Red (#ef4444)
  - Background: Dark slate (#0f172a)
- **Typography**: Inter font family
- **Animations**: Subtle, professional transitions
- **Icons**: Lucide React icons

## 🔧 Key Components to Build

### 1. GraphVisualizer.tsx
```typescript
interface BranchNode {
  name: string;
  type: 'main' | 'feature' | 'bugfix' | 'hotfix';
  createdAt: Date;
  commitCount: number;
  fileChanges: {
    added: number;
    modified: number;
    deleted: number;
    linesAdded: number;
    linesRemoved: number;
  };
  vibeScore: number;
  isActive: boolean;
}

// D3.js graph component with:
// - Force-directed layout
// - Node interactions (click, hover)
// - Smooth animations for new nodes
// - Zoom and pan functionality
```

### 2. BranchInfoPanel.tsx
```typescript
// Side panel showing selected branch details
// - Branch metadata display
// - Commit history list
// - File changes breakdown
// - Vibe score visualization
```

### 3. SessionStats.tsx
```typescript
// Top panel with session statistics
// - Repository information
// - Session duration timer
// - Branch and commit counters
// - Current branch indicator
```

### 4. useGitData.ts
```typescript
// Custom hook for fetching git data
// - Poll API every 2 seconds
// - Handle WebSocket connection
// - Manage loading states
// - Update graph data
```

## 🎬 Animation Requirements

### Node Animations
- **New branch nodes**: Fade in with scale (0 → 1) over 500ms
- **Node hover**: Subtle glow effect with shadow
- **Active branch**: Gentle pulse animation (scale 1.0 → 1.1)
- **Node selection**: Highlight with border and background change

### Graph Animations
- **New connections**: Lines draw themselves from parent to child
- **Layout updates**: Smooth transitions when nodes reposition
- **Zoom/pan**: Smooth camera movements with easing

## 🔄 Real-Time Updates

### Update Flow
1. **Poll API** every 2 seconds for new data
2. **Compare** with previous state to detect changes
3. **Animate** new branches appearing
4. **Update** statistics and session info
5. **Highlight** current active branch

### Performance Optimization
- **Debounce** API calls to prevent excessive requests
- **Virtualize** large graphs with many branches
- **Memoize** expensive calculations
- **Lazy load** branch details on demand

## 🎯 Success Criteria

1. **Real-time updates** within 2 seconds of branch creation
2. **Smooth 60fps animations** for up to 20 branches
3. **Intuitive interactions** - click to select, hover for preview
4. **Responsive design** that works on desktop and tablet
5. **Professional appearance** suitable for presentations

## 🚀 Implementation Phases

### Phase 1: Core Visualization (MVP)
- Basic D3.js graph with nodes and edges
- Simple real-time data fetching
- Basic branch information display
- Click interactions

### Phase 2: Enhanced UX
- Smooth animations and transitions
- Hover effects and visual feedback
- Zoom and pan functionality
- Session statistics panel

### Phase 3: Advanced Features
- Branch relationship visualization
- Session recording and playback
- Export functionality (PNG/SVG)
- Advanced filtering and search

### Phase 4: Polish & Integration
- Performance optimizations
- Mobile responsiveness
- Accessibility features
- Advanced analytics

## 📱 Responsive Design

### Desktop (1200px+)
- Full layout with side panels
- Large interactive graph
- Detailed branch information

### Tablet (768px - 1199px)
- Collapsible side panels
- Medium-sized graph
- Touch-friendly interactions

### Mobile (320px - 767px)
- Stacked layout
- Compact graph view
- Swipe gestures for navigation

## 🔧 Development Setup

### Prerequisites
- Node.js 18+
- Git repository with Git Vibe Brancher
- Python 3.6+ for API

### Installation
```bash
# Clone and setup
git clone <repository>
cd git-vibe-brancher-visualizer
npm install

# Start development server
npm run dev

# In another terminal, start the API
python3 visualizer_api.py --watch
```

## 🎉 Expected Outcome

A beautiful, professional web application that transforms the Git Vibe Brancher from a command-line tool into an immersive, visual coding experience. The visualizer will make branch management intuitive and engaging, perfect for:

- **Team presentations** and code reviews
- **Developer onboarding** and training
- **Client demonstrations** of development workflow
- **Personal productivity** tracking and analysis

The application should feel like a modern development tool that developers would want to use daily, with smooth animations, intuitive interactions, and real-time insights into their coding patterns.

Build this as a production-ready application that showcases the power of visual git workflow management!
