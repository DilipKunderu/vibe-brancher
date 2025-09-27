# Git Vibe Brancher Live Graph Visualizer - Lovable.dev Prompt

## Project: Real-Time Git Branch Visualization

Create a beautiful, live-updating graph visualizer for the Git Vibe Brancher tool that shows git branches as they're created during coding sessions.

## Core Features to Build

### 1. Main Graph Visualization
- **Interactive D3.js graph** showing git branches as nodes
- **Real-time updates** when new branches are created
- **Smooth animations** for new nodes appearing
- **Color-coded branches** (feature=green, bugfix=orange, main=blue)
- **Hover effects** showing branch details

### 2. Branch Information Display
- **Side panel** showing selected branch details:
  - Branch name and creation time
  - Number of commits
  - Files changed (added/modified/deleted)
  - Lines added/removed
  - Vibe Brancher score (0.0-1.0)

### 3. Real-Time Monitoring
- **File system watcher** to detect git repository changes
- **Auto-refresh** every 2 seconds to catch new branches
- **Session tracking** from start to finish

## Technical Stack
- **React 18** with TypeScript
- **D3.js** for graph visualization
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Node.js** backend for file monitoring

## UI Layout
```
┌─────────────────────────────────────────────────────────┐
│ Git Vibe Brancher - Live Visualizer                    │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────────────────────┐ │
│ │ Repository Path │ │ Interactive Branch Graph        │ │
│ │ /path/to/repo   │ │ • Nodes = Branches              │ │
│ │                 │ │ • Lines = Relationships         │ │
│ │ Session Stats   │ │ • Colors = Branch Types         │ │
│ │ • 5 branches    │ │ • Animations = New Branches     │ │
│ │ • 12 commits    │ │                                 │ │
│ │ • 2.5 hours     │ │                                 │ │
│ └─────────────────┘ └─────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Selected Branch: feature/user-auth                      │
│ Created: 2 hours ago | Commits: 3 | Files: 4 | Score: 0.96 │
└─────────────────────────────────────────────────────────┘
```

## Sample Data Structure
```typescript
interface Branch {
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
```

## Key Components to Build

### 1. GraphVisualizer.tsx
```typescript
// Main D3.js graph component
// - Render branch nodes as circles
// - Draw connections between branches
// - Handle zoom/pan interactions
// - Animate new nodes appearing
```

### 2. BranchInfoPanel.tsx
```typescript
// Side panel showing branch details
// - Display selected branch information
// - Show commit history
// - Display file change statistics
```

### 3. SessionStats.tsx
```typescript
// Top panel with session statistics
// - Total branches created
// - Session duration
// - Current branch
// - Repository path
```

### 4. useGitMonitor.ts
```typescript
// Custom hook for monitoring git repository
// - Watch for branch changes
// - Parse git log output
// - Update state with new branches
```

## Animation Requirements
- **New branch nodes**: Fade in with scale animation
- **Branch connections**: Draw themselves smoothly
- **Hover effects**: Subtle glow and shadow
- **Active branch**: Gentle pulse animation

## Color Scheme
- **Main branch**: Deep blue (#1e40af)
- **Feature branches**: Emerald green (#10b981)
- **Bugfix branches**: Amber orange (#f59e0b)
- **Hotfix branches**: Red (#ef4444)
- **Background**: Dark slate (#0f172a)

## Git Commands to Monitor
```bash
# Get all branches
git branch -a

# Get branch details
git log --oneline --graph --all

# Get file changes
git diff --stat HEAD~1
```

## Success Criteria
1. **Real-time updates** within 2 seconds of branch creation
2. **Smooth 60fps animations** for up to 20 branches
3. **Intuitive interactions** - click to select, hover for details
4. **Responsive design** that works on desktop and tablet

## Sample Implementation Flow
1. User selects git repository path
2. App monitors repository for changes
3. When new branch detected, parse git data
4. Add new node to graph with animation
5. Update statistics and session info
6. Allow user to click nodes for details

Build this as a modern, professional web application that makes git branch visualization engaging and informative!
