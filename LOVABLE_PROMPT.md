# Git Vibe Brancher - Live Graph Visualizer

## Project Overview

Create a beautiful, real-time graph visualizer for the Git Vibe Brancher tool that tracks and visualizes git branches as they're created during "vibe coding" sessions. The application should provide an immersive, live-updating visualization of the branching workflow.

## Core Features

### 1. Real-Time Branch Tracking
- **Live Updates**: Automatically detect when new branches are created by the Git Vibe Brancher
- **Branch Monitoring**: Track branch creation, commits, and merges in real-time
- **Session Tracking**: Monitor entire coding sessions from start to finish
- **File System Watching**: Watch for changes in git repository to detect new branches

### 2. Interactive Graph Visualization
- **Node-Based Graph**: Each branch represented as a node with:
  - Branch name as the main label
  - Commit count as a secondary metric
  - File change statistics (lines added/removed)
  - Creation timestamp
  - Current status (active, merged, deleted)
- **Connection Lines**: Show relationships between branches (parent-child, merge relationships)
- **Dynamic Layout**: Auto-arrange nodes for optimal viewing
- **Zoom & Pan**: Smooth navigation through large branch graphs

### 3. Visual Design & Animations
- **Modern UI**: Clean, professional interface with dark/light theme support
- **Smooth Animations**: 
  - New branch nodes appear with a gentle fade-in and scale animation
  - Branch connections draw themselves smoothly
  - Hover effects with subtle shadows and color changes
  - Pulse animations for active branches
- **Color Coding**:
  - Different colors for different branch types (feature, bugfix, hotfix, etc.)
  - Gradient effects based on commit activity
  - Status-based coloring (active, merged, stale)

### 4. Branch Information Panel
- **Detailed View**: Click on any branch to see:
  - Full branch name and creation time
  - Commit history with messages
  - File changes summary
  - Vibe Brancher analysis score
  - Branch recommendation reason
- **Statistics Dashboard**: 
  - Total branches created in session
  - Average commits per branch
  - Most active file types
  - Session duration and productivity metrics

### 5. Integration with Git Vibe Brancher
- **Real-Time Sync**: Connect to the Git Vibe Brancher tool via:
  - File system monitoring of git repository
  - WebSocket connection (if tool is extended)
  - REST API polling
- **Branch Analysis Display**: Show the vibe brancher's analysis:
  - Branch score (0.0-1.0)
  - Recommendation reasoning
  - File change complexity
  - Time-based factors

## Technical Requirements

### Frontend Framework
- **React 18+** with TypeScript
- **D3.js** or **vis.js** for graph visualization
- **Tailwind CSS** for styling
- **Framer Motion** for smooth animations
- **React Query** for state management and caching

### Graph Visualization Library
- **D3.js** for custom, highly interactive graphs
- **vis.js Network** as alternative for easier implementation
- **React Flow** for modern, React-native graph components

### Real-Time Updates
- **WebSocket** connection for live updates
- **File System API** for monitoring git repository changes
- **Polling mechanism** as fallback for git status updates

### Data Structure
```typescript
interface BranchNode {
  id: string;
  name: string;
  type: 'feature' | 'bugfix' | 'hotfix' | 'main' | 'other';
  createdAt: Date;
  lastCommit: Date;
  commitCount: number;
  fileChanges: {
    added: number;
    modified: number;
    deleted: number;
    linesAdded: number;
    linesRemoved: number;
  };
  vibeScore: number;
  status: 'active' | 'merged' | 'stale' | 'deleted';
  parentBranch?: string;
  children: string[];
}

interface SessionData {
  sessionId: string;
  startTime: Date;
  endTime?: Date;
  totalBranches: number;
  totalCommits: number;
  branches: BranchNode[];
  currentBranch: string;
}
```

## UI/UX Design

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│ Header: Git Vibe Brancher - Live Visualizer            │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────────────────────┐ │
│ │ Control Panel   │ │ Main Graph Visualization        │ │
│ │ - Start/Stop    │ │ - Interactive branch graph      │ │
│ │ - Settings      │ │ - Real-time updates             │ │
│ │ - Export        │ │ - Zoom/Pan controls             │ │
│ │ - Statistics    │ │ - Node interactions             │ │
│ └─────────────────┘ └─────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Branch Details Panel (collapsible)                     │
│ - Selected branch info                                 │
│ - Commit history                                       │
│ - File changes                                         │
└─────────────────────────────────────────────────────────┘
```

### Visual Design Elements
- **Color Palette**: 
  - Primary: Deep blue (#1e40af) for main branches
  - Secondary: Emerald green (#10b981) for feature branches
  - Accent: Amber (#f59e0b) for bugfix branches
  - Background: Dark slate (#0f172a) with subtle gradients
- **Typography**: Modern sans-serif (Inter or Poppins)
- **Icons**: Lucide React icons for consistency
- **Animations**: Subtle, professional transitions

### Interactive Features
- **Hover Effects**: Branch nodes highlight with glow effect
- **Click Actions**: Select branch for detailed view
- **Drag & Drop**: Reposition nodes for better layout
- **Search/Filter**: Find specific branches quickly
- **Timeline Slider**: Navigate through session history

## Advanced Features

### 1. Session Analytics
- **Productivity Metrics**: 
  - Branches per hour
  - Average commits per branch
  - Code velocity trends
- **Pattern Recognition**: 
  - Identify common branching patterns
  - Suggest optimal branching strategies
  - Detect potential merge conflicts

### 2. Export & Sharing
- **Export Options**:
  - PNG/SVG image export
  - JSON data export
  - Shareable session URLs
- **Session Recording**: Save and replay coding sessions

### 3. Integration Features
- **IDE Integration**: Show current branch status
- **Notification System**: Alert for branch recommendations
- **Keyboard Shortcuts**: Quick navigation and actions

## Implementation Phases

### Phase 1: Core Visualization
- Basic graph rendering with D3.js
- Node and edge creation
- Simple real-time updates
- Basic branch information display

### Phase 2: Enhanced Interactivity
- Smooth animations and transitions
- Interactive node selection
- Zoom and pan functionality
- Branch details panel

### Phase 3: Advanced Features
- Session analytics and metrics
- Export functionality
- Advanced filtering and search
- Performance optimizations

### Phase 4: Integration & Polish
- Git Vibe Brancher integration
- Real-time synchronization
- Advanced animations
- Mobile responsiveness

## Sample Data for Testing

```json
{
  "sessionId": "session_2024_01_15_14_30",
  "startTime": "2024-01-15T14:30:00Z",
  "currentBranch": "feature/user-authentication",
  "branches": [
    {
      "id": "main",
      "name": "main",
      "type": "main",
      "createdAt": "2024-01-15T14:30:00Z",
      "lastCommit": "2024-01-15T14:25:00Z",
      "commitCount": 5,
      "fileChanges": {
        "added": 2,
        "modified": 3,
        "deleted": 0,
        "linesAdded": 45,
        "linesRemoved": 12
      },
      "vibeScore": 0.0,
      "status": "active",
      "children": ["feature/user-authentication"]
    },
    {
      "id": "feature/user-authentication",
      "name": "feature/user-authentication",
      "type": "feature",
      "createdAt": "2024-01-15T14:35:00Z",
      "lastCommit": "2024-01-15T14:40:00Z",
      "commitCount": 3,
      "fileChanges": {
        "added": 4,
        "modified": 1,
        "deleted": 0,
        "linesAdded": 453,
        "linesRemoved": 0
      },
      "vibeScore": 0.96,
      "status": "active",
      "parentBranch": "main",
      "children": []
    }
  ]
}
```

## Success Criteria

1. **Real-Time Updates**: Graph updates within 2 seconds of branch creation
2. **Smooth Performance**: 60fps animations with up to 50 branch nodes
3. **Intuitive UX**: Users can understand the visualization without training
4. **Responsive Design**: Works on desktop, tablet, and mobile devices
5. **Accessibility**: Keyboard navigation and screen reader support

## Additional Considerations

- **Performance**: Optimize for large repositories with many branches
- **Scalability**: Handle repositories with 100+ branches efficiently
- **Error Handling**: Graceful handling of git command failures
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Offline Support**: Cache data for offline viewing

This visualizer will transform the Git Vibe Brancher from a command-line tool into an immersive, visual coding experience that makes branch management intuitive and engaging!
