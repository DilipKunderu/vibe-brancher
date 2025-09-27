#!/usr/bin/env python3
"""
Git Vibe Brancher - Visualizer API
Provides JSON data for the live graph visualizer
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class VisualizerAPI:
    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = repo_path or os.getcwd()
        self.vibe_brancher_path = os.path.join(os.path.dirname(__file__), 'vibe_brancher.py')
    
    def _run_git_command(self, command: List[str]) -> str:
        """Run a git command and return the output."""
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {' '.join(command)}\nError: {e.stderr}")
    
    def get_all_branches(self) -> List[Dict]:
        """Get all branches with their information."""
        try:
            # Get all branches
            branches_output = self._run_git_command(['branch', '-a', '--format=%(refname:short)|%(committerdate:iso)|%(authorname)'])
            
            branches = []
            for line in branches_output.split('\n'):
                if not line or 'HEAD' in line:
                    continue
                
                parts = line.split('|')
                if len(parts) >= 3:
                    branch_name = parts[0].replace('origin/', '').replace('remotes/', '')
                    commit_date = parts[1]
                    author = parts[2]
                    
                    # Skip if it's a remote tracking branch
                    if branch_name.startswith('origin/'):
                        continue
                    
                    branch_info = self._get_branch_details(branch_name)
                    if branch_info:
                        branches.append(branch_info)
            
            return branches
        except RuntimeError:
            return []
    
    def _get_branch_details(self, branch_name: str) -> Optional[Dict]:
        """Get detailed information about a specific branch."""
        try:
            # Get commit count
            commit_count = self._run_git_command(['rev-list', '--count', branch_name])
            
            # Get last commit date
            last_commit = self._run_git_command(['log', '-1', '--format=%ct', branch_name])
            last_commit_date = datetime.fromtimestamp(int(last_commit)) if last_commit else None
            
            # Get file changes (compared to main/master)
            try:
                main_branch = 'main' if 'main' in self._run_git_command(['branch', '--list', 'main']) else 'master'
                diff_stats = self._run_git_command(['diff', '--stat', f'{main_branch}...{branch_name}'])
            except:
                diff_stats = ""
            
            # Parse diff stats
            file_changes = self._parse_diff_stats(diff_stats)
            
            # Determine branch type
            branch_type = self._determine_branch_type(branch_name)
            
            # Get vibe brancher score if possible
            vibe_score = self._get_vibe_score(branch_name)
            
            return {
                'name': branch_name,
                'type': branch_type,
                'createdAt': last_commit_date.isoformat() if last_commit_date else None,
                'lastCommit': last_commit_date.isoformat() if last_commit_date else None,
                'commitCount': int(commit_count) if commit_count else 0,
                'fileChanges': file_changes,
                'vibeScore': vibe_score,
                'isActive': branch_name == self._get_current_branch()
            }
        except RuntimeError:
            return None
    
    def _parse_diff_stats(self, diff_stats: str) -> Dict:
        """Parse git diff --stat output to get file change statistics."""
        if not diff_stats:
            return {
                'added': 0,
                'modified': 0,
                'deleted': 0,
                'linesAdded': 0,
                'linesRemoved': 0
            }
        
        lines = diff_stats.split('\n')
        added_files = 0
        modified_files = 0
        deleted_files = 0
        lines_added = 0
        lines_removed = 0
        
        for line in lines:
            if '|' in line and ('+' in line or '-' in line):
                # Parse file change line like "file.py | 5 +++++"
                parts = line.split('|')
                if len(parts) >= 2:
                    file_part = parts[0].strip()
                    change_part = parts[1].strip()
                    
                    if 'new file' in change_part:
                        added_files += 1
                    elif 'deleted' in change_part:
                        deleted_files += 1
                    else:
                        modified_files += 1
                    
                    # Extract line changes
                    if '+' in change_part:
                        try:
                            lines_added += int(change_part.split('+')[1].split()[0])
                        except:
                            pass
                    if '-' in change_part:
                        try:
                            lines_removed += int(change_part.split('-')[1].split()[0])
                        except:
                            pass
        
        return {
            'added': added_files,
            'modified': modified_files,
            'deleted': deleted_files,
            'linesAdded': lines_added,
            'linesRemoved': lines_removed
        }
    
    def _determine_branch_type(self, branch_name: str) -> str:
        """Determine the type of branch based on its name."""
        if branch_name in ['main', 'master']:
            return 'main'
        elif branch_name.startswith('feature/'):
            return 'feature'
        elif branch_name.startswith('bugfix/') or branch_name.startswith('fix/'):
            return 'bugfix'
        elif branch_name.startswith('hotfix/'):
            return 'hotfix'
        else:
            return 'other'
    
    def _get_vibe_score(self, branch_name: str) -> float:
        """Get the vibe brancher score for a branch."""
        try:
            # Checkout the branch temporarily to get vibe score
            current_branch = self._get_current_branch()
            self._run_git_command(['checkout', branch_name])
            
            # Run vibe brancher
            result = subprocess.run(
                ['python3', self.vibe_brancher_path],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            # Parse the output for branch score
            output = result.stdout
            if 'Branch Score:' in output:
                score_line = [line for line in output.split('\n') if 'Branch Score:' in line][0]
                score = float(score_line.split(':')[1].split('/')[0].strip())
            else:
                score = 0.0
            
            # Return to original branch
            self._run_git_command(['checkout', current_branch])
            
            return score
        except:
            return 0.0
    
    def _get_current_branch(self) -> str:
        """Get the current branch name."""
        try:
            return self._run_git_command(['branch', '--show-current'])
        except:
            return 'main'
    
    def get_session_data(self) -> Dict:
        """Get complete session data for the visualizer."""
        branches = self.get_all_branches()
        current_branch = self._get_current_branch()
        
        # Calculate session statistics
        total_commits = sum(branch['commitCount'] for branch in branches)
        total_files_changed = sum(
            branch['fileChanges']['added'] + 
            branch['fileChanges']['modified'] + 
            branch['fileChanges']['deleted'] 
            for branch in branches
        )
        
        return {
            'sessionId': f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'startTime': datetime.now().isoformat(),
            'currentBranch': current_branch,
            'totalBranches': len(branches),
            'totalCommits': total_commits,
            'totalFilesChanged': total_files_changed,
            'branches': branches,
            'repository': {
                'path': self.repo_path,
                'name': os.path.basename(self.repo_path)
            }
        }
    
    def watch_repository(self, callback=None):
        """Watch repository for changes and call callback with updated data."""
        last_branches = set()
        
        while True:
            try:
                current_branches = set(branch['name'] for branch in self.get_all_branches())
                
                if current_branches != last_branches:
                    session_data = self.get_session_data()
                    if callback:
                        callback(session_data)
                    last_branches = current_branches
                
                time.sleep(2)  # Check every 2 seconds
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error watching repository: {e}")
                time.sleep(5)

def main():
    parser = argparse.ArgumentParser(description="Git Vibe Brancher Visualizer API")
    parser.add_argument('--repo', help='Path to git repository')
    parser.add_argument('--watch', action='store_true', help='Watch repository for changes')
    parser.add_argument('--json', action='store_true', help='Output JSON data')
    
    args = parser.parse_args()
    
    api = VisualizerAPI(args.repo)
    
    if args.watch:
        def print_update(data):
            print(json.dumps(data, indent=2))
        
        print("Watching repository for changes...")
        api.watch_repository(print_update)
    elif args.json:
        data = api.get_session_data()
        print(json.dumps(data, indent=2))
    else:
        # Default: show summary
        data = api.get_session_data()
        print(f"Repository: {data['repository']['name']}")
        print(f"Current Branch: {data['currentBranch']}")
        print(f"Total Branches: {data['totalBranches']}")
        print(f"Total Commits: {data['totalCommits']}")
        print(f"Total Files Changed: {data['totalFilesChanged']}")
        print("\nBranches:")
        for branch in data['branches']:
            print(f"  • {branch['name']} ({branch['type']}) - {branch['commitCount']} commits")

if __name__ == "__main__":
    main()
