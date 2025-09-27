#!/usr/bin/env python3
"""
Demo script showing how to use the visualizer API
"""

import subprocess
import json
import time
import sys

def demo_basic_usage():
    """Demonstrate basic API usage"""
    print("🔍 Basic Usage - Get Repository Summary")
    print("=" * 50)
    
    result = subprocess.run([
        'python3', 'visualizer_api.py'
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)

def demo_json_output():
    """Demonstrate JSON output"""
    print("📊 JSON Output - For Visualizer Integration")
    print("=" * 50)
    
    result = subprocess.run([
        'python3', 'visualizer_api.py', '--json'
    ], capture_output=True, text=True)
    
    if result.stdout:
        data = json.loads(result.stdout)
        print(f"Repository: {data['repository']['name']}")
        print(f"Current Branch: {data['currentBranch']}")
        print(f"Total Branches: {data['totalBranches']}")
        print(f"Total Commits: {data['totalCommits']}")
        print(f"Session ID: {data['sessionId']}")
        print("\nBranches:")
        for branch in data['branches']:
            print(f"  • {branch['name']} ({branch['type']}) - {branch['commitCount']} commits - Score: {branch['vibeScore']:.2f}")

def demo_different_repo():
    """Demonstrate monitoring different repository"""
    print("📁 Different Repository - PoorlyWrittenService")
    print("=" * 50)
    
    result = subprocess.run([
        'python3', 'visualizer_api.py', 
        '--repo', '/Users/dilipkunderu/hackday/PoorlyWrittenService',
        '--json'
    ], capture_output=True, text=True)
    
    if result.stdout:
        data = json.loads(result.stdout)
        print(f"Repository: {data['repository']['name']}")
        print(f"Current Branch: {data['currentBranch']}")
        print(f"Total Branches: {data['totalBranches']}")
        print(f"Total Commits: {data['totalCommits']}")
        print("\nBranches:")
        for branch in data['branches']:
            status = "🟢 ACTIVE" if branch['isActive'] else "⚪"
            print(f"  {status} {branch['name']} ({branch['type']}) - {branch['commitCount']} commits - Score: {branch['vibeScore']:.2f}")

def demo_watch_mode():
    """Demonstrate watch mode (simulated)"""
    print("👀 Watch Mode - Real-Time Monitoring")
    print("=" * 50)
    print("The watch mode continuously monitors the repository for changes.")
    print("It outputs JSON data whenever new branches are created or commits are made.")
    print("\nExample usage:")
    print("  python3 visualizer_api.py --watch")
    print("  python3 visualizer_api.py --repo /path/to/repo --watch")
    print("\nThis would continuously output JSON data like:")
    
    # Show sample output
    sample_data = {
        "sessionId": "session_20240927_154600",
        "startTime": "2024-09-27T15:46:00.855222",
        "currentBranch": "feature/new-feature",
        "totalBranches": 4,
        "totalCommits": 30,
        "totalFilesChanged": 45,
        "branches": [
            {
                "name": "feature/new-feature",
                "type": "feature",
                "createdAt": "2024-09-27T15:50:00",
                "lastCommit": "2024-09-27T15:50:00",
                "commitCount": 5,
                "fileChanges": {
                    "added": 3,
                    "modified": 2,
                    "deleted": 0,
                    "linesAdded": 150,
                    "linesRemoved": 10
                },
                "vibeScore": 0.85,
                "isActive": True
            }
        ],
        "repository": {
            "path": "/path/to/repo",
            "name": "MyProject"
        }
    }
    
    print(json.dumps(sample_data, indent=2))

def main():
    """Run all demonstrations"""
    print("🌿 Git Vibe Brancher - Visualizer API Demo")
    print("=" * 60)
    print()
    
    try:
        demo_basic_usage()
        print()
        
        demo_json_output()
        print()
        
        demo_different_repo()
        print()
        
        demo_watch_mode()
        print()
        
        print("✅ All demonstrations completed!")
        print("\n📚 Usage Summary:")
        print("  • python3 visualizer_api.py                    # Basic summary")
        print("  • python3 visualizer_api.py --json             # JSON output")
        print("  • python3 visualizer_api.py --repo /path       # Different repo")
        print("  • python3 visualizer_api.py --watch            # Real-time monitoring")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
