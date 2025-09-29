#!/usr/bin/env python3
"""
Git Vibe Brancher - A tool that decides when to create git branches during vibe coding.

Analyzes your changes and suggests when to create a new branch based on:
- Number of files changed
- Lines of code added/removed  
- Time since last commit
- Complexity of changes
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse


class GitVibeBrancher:
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.repo_path = self._find_git_repo()
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults."""
        default_config = {
            "thresholds": {
                "files_changed": 5,
                "lines_added": 50,
                "lines_removed": 30,
                "time_minutes": 30,
                "complexity_score": 7
            },
            "weights": {
                "files_changed": 0.3,
                "lines_changed": 0.25,
                "time_factor": 0.2,
                "complexity": 0.15,
                "file_types": 0.1
            },
            "file_type_weights": {
                ".py": 1.0, ".js": 0.8, ".ts": 0.9, ".java": 1.0,
                ".cpp": 1.0, ".c": 1.0, ".go": 1.0, ".rs": 1.0,
                ".html": 0.3, ".css": 0.3, ".json": 0.2,
                ".md": 0.1, ".txt": 0.1
            },
            "branch_naming": {
                "prefix": "feature",
                "separator": "/",
                "include_timestamp": False
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config from {config_path}: {e}")
                
        return default_config
    
    def _find_git_repo(self) -> str:
        """Find the git repository root."""
        current_dir = os.getcwd()
        while current_dir != '/':
            if os.path.exists(os.path.join(current_dir, '.git')):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        raise RuntimeError("Not in a git repository")
    
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
    
    def _get_git_status(self) -> Dict:
        """Get current git status information."""
        status_output = self._run_git_command(['status', '--porcelain'])
        
        files = {
            'modified': [],
            'added': [],
            'deleted': [],
            'renamed': [],
            'untracked': []
        }
        
        for line in status_output.split('\n'):
            if not line:
                continue
                
            status = line[:2]
            filename = line[3:]
            
            if status[0] in 'MADRC':
                if status[0] == 'M':
                    files['modified'].append(filename)
                elif status[0] == 'A':
                    files['added'].append(filename)
                elif status[0] == 'D':
                    files['deleted'].append(filename)
                elif status[0] == 'R':
                    files['renamed'].append(filename)
                elif status[0] == 'C':
                    files['modified'].append(filename)
            elif status[1] in 'MADRC':
                if status[1] == 'M':
                    files['modified'].append(filename)
                elif status[1] == 'A':
                    files['added'].append(filename)
                elif status[1] == 'D':
                    files['deleted'].append(filename)
            elif status == '??':
                files['untracked'].append(filename)
        
        return files
    
    def _get_diff_stats(self) -> Dict:
        """Get diff statistics for staged and unstaged changes."""
        stats = {
            'staged': {'files': 0, 'insertions': 0, 'deletions': 0},
            'unstaged': {'files': 0, 'insertions': 0, 'deletions': 0}
        }
        
        # Get staged changes
        try:
            staged_output = self._run_git_command(['diff', '--cached', '--numstat'])
            if staged_output:
                for line in staged_output.split('\n'):
                    if line:
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            stats['staged']['files'] += 1
                            if parts[0] != '-':
                                stats['staged']['insertions'] += int(parts[0])
                            if parts[1] != '-':
                                stats['staged']['deletions'] += int(parts[1])
        except RuntimeError:
            pass
        
        # Get unstaged changes
        try:
            unstaged_output = self._run_git_command(['diff', '--numstat'])
            if unstaged_output:
                for line in unstaged_output.split('\n'):
                    if line:
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            stats['unstaged']['files'] += 1
                            if parts[0] != '-':
                                stats['unstaged']['insertions'] += int(parts[0])
                            if parts[1] != '-':
                                stats['unstaged']['deletions'] += int(parts[1])
        except RuntimeError:
            pass
        
        return stats
    
    def _get_last_commit_time(self) -> Optional[datetime]:
        """Get the timestamp of the last commit."""
        try:
            timestamp_str = self._run_git_command(['log', '-1', '--format=%ct'])
            if timestamp_str:
                return datetime.fromtimestamp(int(timestamp_str))
        except RuntimeError:
            pass
        return None
    
    def _calculate_file_type_complexity(self, files: Dict) -> float:
        """Calculate complexity based on file types being modified."""
        all_files = files['modified'] + files['added'] + files['untracked']
        if not all_files:
            return 0.0
        
        total_weight = 0.0
        for filename in all_files:
            file_ext = Path(filename).suffix.lower()
            weight = self.config['file_type_weights'].get(file_ext, 0.5)
            total_weight += weight
        
        return total_weight / len(all_files)
    
    def _calculate_complexity_score(self, files: Dict, diff_stats: Dict) -> float:
        """Calculate overall complexity score based on various factors."""
        total_files = len(files['modified']) + len(files['added']) + len(files['untracked'])
        total_insertions = diff_stats['staged']['insertions'] + diff_stats['unstaged']['insertions']
        total_deletions = diff_stats['staged']['deletions'] + diff_stats['unstaged']['deletions']
        
        # Base complexity from file count
        file_complexity = min(total_files / 10.0, 1.0)  # Normalize to 0-1
        
        # Line change complexity
        line_complexity = min((total_insertions + total_deletions) / 100.0, 1.0)
        
        # File type complexity
        type_complexity = self._calculate_file_type_complexity(files)
        
        # Combine factors
        complexity = (
            file_complexity * 0.4 +
            line_complexity * 0.4 +
            type_complexity * 0.2
        )
        
        return complexity * 10  # Scale to 0-10
    
    def _calculate_time_factor(self) -> float:
        """Calculate time-based factor for branching decision."""
        last_commit = self._get_last_commit_time()
        if not last_commit:
            return 1.0  # No previous commits, high factor
        
        time_diff = datetime.now() - last_commit
        minutes = time_diff.total_seconds() / 60
        
        # Linear increase with time, max at 1.0 after threshold
        threshold = self.config['thresholds']['time_minutes']
        return min(minutes / threshold, 1.0)
    
    def analyze_branch_need(self) -> Dict:
        """Analyze whether a new branch should be created."""
        files = self._get_git_status()
        diff_stats = self._get_diff_stats()
        
        # Calculate individual factors
        total_files = len(files['modified']) + len(files['added']) + len(files['untracked'])
        total_insertions = diff_stats['staged']['insertions'] + diff_stats['unstaged']['insertions']
        total_deletions = diff_stats['staged']['deletions'] + diff_stats['unstaged']['deletions']
        
        file_factor = min(total_files / self.config['thresholds']['files_changed'], 1.0)
        line_factor = min((total_insertions + total_deletions) / 
                         (self.config['thresholds']['lines_added'] + self.config['thresholds']['lines_removed']), 1.0)
        time_factor = self._calculate_time_factor()
        complexity = self._calculate_complexity_score(files, diff_stats)
        complexity_factor = min(complexity / self.config['thresholds']['complexity_score'], 1.0)
        
        # Calculate weighted score
        weights = self.config['weights']
        branch_score = (
            file_factor * weights['files_changed'] +
            line_factor * weights['lines_changed'] +
            time_factor * weights['time_factor'] +
            complexity_factor * weights['complexity'] +
            self._calculate_file_type_complexity(files) * weights['file_types']
        )
        
        should_branch = branch_score >= 0.6  # Threshold for branching
        
        return {
            'should_branch': should_branch,
            'branch_score': branch_score,
            'factors': {
                'files_changed': total_files,
                'file_factor': file_factor,
                'lines_added': total_insertions,
                'lines_removed': total_deletions,
                'line_factor': line_factor,
                'time_factor': time_factor,
                'complexity_score': complexity,
                'complexity_factor': complexity_factor
            },
            'files': files,
            'diff_stats': diff_stats
        }
    
    def suggest_branch_name(self, analysis: Dict) -> str:
        """Suggest a branch name based on the analysis."""
        config = self.config['branch_naming']
        prefix = config['prefix']
        separator = config['separator']
        
        # Try to infer feature name from modified files
        files = analysis['files']
        all_files = files['modified'] + files['added'] + files['untracked']
        
        if all_files:
            # Use the most significant file as basis for name
            main_file = all_files[0]
            feature_name = Path(main_file).stem.lower().replace('_', '-').replace(' ', '-')
        else:
            feature_name = "changes"
        
        branch_name = f"{prefix}{separator}{feature_name}"
        
        if config['include_timestamp']:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M")
            branch_name += f"-{timestamp}"
        
        return branch_name
    
    def create_branch(self, branch_name: str, silent: bool = False) -> bool:
        """Create a new git branch."""
        try:
            # Check if branch already exists
            existing_branches = self._run_git_command(['branch', '--list', branch_name])
            if existing_branches:
                if not silent:
                    print(f"Branch '{branch_name}' already exists!")
                return False
            
            # Create and checkout new branch
            self._run_git_command(['checkout', '-b', branch_name])
            if not silent:
                print(f"✅ Created and switched to branch: {branch_name}")
            return True
        except RuntimeError as e:
            if not silent:
                print(f"❌ Failed to create branch: {e}")
            return False
    
    def auto_branch_if_needed(self, silent: bool = False) -> bool:
        """Automatically create a branch if analysis suggests it."""
        analysis = self.analyze_branch_need()
        
        if analysis['should_branch']:
            branch_name = self.suggest_branch_name(analysis)
            return self.create_branch(branch_name, silent=silent)
        
        return False
    
    def save_progress(self, description: str = None, silent: bool = False) -> bool:
        """Save current progress with intelligent branching."""
        try:
            # First check if we should branch
            if self.auto_branch_if_needed(silent=silent):
                if not silent:
                    print("🌿 Auto-created branch for significant changes")
            
            # Get current status
            files = self._get_git_status()
            diff_stats = self._get_diff_stats()
            
            # Check if there are any changes to save
            total_files = len(files['modified']) + len(files['added']) + len(files['untracked'])
            if total_files == 0:
                if not silent:
                    print("💾 No changes to save.")
                return True
            
            # Generate save message if not provided
            if not description:
                description = self._generate_simple_commit_message(files, diff_stats)
            
            # Stage all changes
            self._run_git_command(['add', '.'])
            
            # Save progress
            self._run_git_command(['commit', '-m', description])
            if not silent:
                print(f"💾 Progress saved: {description}")
            return True
            
        except RuntimeError as e:
            if not silent:
                print(f"❌ Failed to save progress: {e}")
            return False
    
    def checkpoint(self, description: str = None, silent: bool = False) -> bool:
        """Create a checkpoint of current work."""
        return self.save_progress(description, silent)
    
    def _generate_simple_commit_message(self, files: Dict, diff_stats: Dict) -> str:
        """Generate a simple commit message based on changes."""
        total_files = len(files['modified']) + len(files['added']) + len(files['untracked'])
        total_insertions = diff_stats['staged']['insertions'] + diff_stats['unstaged']['insertions']
        total_deletions = diff_stats['staged']['deletions'] + diff_stats['unstaged']['deletions']
        
        # Simple message based on file count
        if total_files == 1:
            main_file = (files['modified'] + files['added'] + files['untracked'])[0]
            return f"update {Path(main_file).stem}"
        else:
            return f"update {total_files} files"
    
    def _get_branch_info(self, branch_name: str = None) -> Dict:
        """Get information about a branch."""
        if not branch_name:
            branch_name = self._run_git_command(['branch', '--show-current'])
        
        try:
            # Get branch creation time (first commit on branch)
            first_commit = self._run_git_command(['log', '--oneline', '--reverse', branch_name])
            if first_commit:
                first_commit_hash = first_commit.split()[0]
                timestamp_str = self._run_git_command(['log', '-1', '--format=%ct', first_commit_hash])
                if timestamp_str:
                    creation_time = datetime.fromtimestamp(int(timestamp_str))
                else:
                    creation_time = None
            else:
                creation_time = None
            
            # Get number of commits on branch
            commit_count = len(self._run_git_command(['log', '--oneline', branch_name]).split('\n'))
            
            # Get last commit time
            last_commit_time = self._get_last_commit_time()
            
            # Check if branch is up to date with main
            try:
                self._run_git_command(['merge-base', '--is-ancestor', 'main', branch_name])
                is_behind_main = False
            except RuntimeError:
                is_behind_main = True
            
            return {
                'name': branch_name,
                'creation_time': creation_time,
                'last_commit_time': last_commit_time,
                'commit_count': commit_count,
                'is_behind_main': is_behind_main
            }
        except RuntimeError:
            return {
                'name': branch_name,
                'creation_time': None,
                'last_commit_time': None,
                'commit_count': 0,
                'is_behind_main': True
            }
    
    def analyze_branch_convergence(self, branch_name: str = None) -> Dict:
        """Analyze if a branch is ready to be merged back to main."""
        branch_info = self._get_branch_info(branch_name)
        
        if not branch_info['name'] or branch_info['name'] == 'main':
            return {'should_merge': False, 'reason': 'Not on a feature branch'}
        
        convergence_score = 0.0
        reasons = []
        
        # Time-based factors
        if branch_info['creation_time']:
            age_hours = (datetime.now() - branch_info['creation_time']).total_seconds() / 3600
            
            # Older branches are more likely to be ready
            if age_hours > 24:  # More than 1 day
                convergence_score += 0.3
                reasons.append(f"Branch is {age_hours:.1f} hours old")
            elif age_hours > 168:  # More than 1 week
                convergence_score += 0.5
                reasons.append(f"Branch is {age_hours/24:.1f} days old - consider merging")
        
        # Commit count factors
        commit_count = branch_info['commit_count']
        if commit_count >= 5:
            convergence_score += 0.2
            reasons.append(f"Has {commit_count} commits - substantial work")
        elif commit_count >= 10:
            convergence_score += 0.3
            reasons.append(f"Has {commit_count} commits - significant feature")
        
        # Stability factors (no recent commits)
        if branch_info['last_commit_time']:
            time_since_last = datetime.now() - branch_info['last_commit_time']
            hours_since_last = time_since_last.total_seconds() / 3600
            
            if hours_since_last > 2:  # No commits for 2+ hours
                convergence_score += 0.2
                reasons.append(f"No commits for {hours_since_last:.1f} hours - appears stable")
            elif hours_since_last > 24:  # No commits for 1+ day
                convergence_score += 0.4
                reasons.append(f"No commits for {hours_since_last/24:.1f} days - likely complete")
        
        # Check if branch is behind main (needs updating)
        if branch_info['is_behind_main']:
            convergence_score -= 0.2
            reasons.append("Branch is behind main - needs updating before merge")
        
        # Check current changes (if any)
        current_files = self._get_git_status()
        total_current_files = len(current_files['modified']) + len(current_files['added']) + len(current_files['untracked'])
        
        if total_current_files == 0:
            convergence_score += 0.3
            reasons.append("No uncommitted changes - clean state")
        else:
            convergence_score -= 0.1
            reasons.append(f"Has {total_current_files} uncommitted changes")
        
        should_merge = convergence_score >= 0.6
        
        return {
            'should_merge': should_merge,
            'convergence_score': convergence_score,
            'reasons': reasons,
            'branch_info': branch_info
        }
    
    def suggest_merge_strategy(self, branch_name: str = None) -> str:
        """Suggest merge strategy for a branch."""
        convergence = self.analyze_branch_convergence(branch_name)
        
        if not convergence['should_merge']:
            return "Branch not ready for merge"
        
        branch_info = convergence['branch_info']
        
        # Suggest merge strategy based on branch characteristics
        if branch_info['commit_count'] <= 3:
            return "squash merge (few commits, clean history)"
        elif branch_info['is_behind_main']:
            return "rebase then merge (update branch first)"
        else:
            return "merge commit (preserve branch history)"
    
    
    def show_analysis(self, analysis: Dict, verbose: bool = False):
        """Display the analysis results."""
        print("🔍 Git Vibe Brancher Analysis")
        print("=" * 40)
        
        if analysis['should_branch']:
            print("🌿 RECOMMENDATION: Create a new branch!")
            print(f"📊 Branch Score: {analysis['branch_score']:.2f}/1.0")
        else:
            print("⏳ RECOMMENDATION: Continue on current branch")
            print(f"📊 Branch Score: {analysis['branch_score']:.2f}/1.0")
        
        if verbose:
            print("\n📈 Detailed Analysis:")
            factors = analysis['factors']
            print(f"  • Files changed: {factors['files_changed']} (factor: {factors['file_factor']:.2f})")
            print(f"  • Lines added: {factors['lines_added']} (factor: {factors['line_factor']:.2f})")
            print(f"  • Lines removed: {factors['lines_removed']}")
            print(f"  • Time factor: {factors['time_factor']:.2f}")
            print(f"  • Complexity score: {factors['complexity_score']:.1f}/10 (factor: {factors['complexity_factor']:.2f})")
            
            print("\n📁 File Changes:")
            files = analysis['files']
            if files['modified']:
                print(f"  • Modified: {len(files['modified'])} files")
            if files['added']:
                print(f"  • Added: {len(files['added'])} files")
            if files['untracked']:
                print(f"  • Untracked: {len(files['untracked'])} files")
            if files['deleted']:
                print(f"  • Deleted: {len(files['deleted'])} files")
        
        if analysis['should_branch']:
            suggested_name = self.suggest_branch_name(analysis)
            print(f"\n💡 Suggested branch name: {suggested_name}")
    
    def show_convergence_analysis(self, branch_name: str = None, verbose: bool = False):
        """Display branch convergence analysis."""
        convergence = self.analyze_branch_convergence(branch_name)
        
        print("🔄 Branch Convergence Analysis")
        print("=" * 40)
        
        if convergence['should_merge']:
            print("✅ RECOMMENDATION: Branch is ready to merge!")
            print(f"📊 Convergence Score: {convergence['convergence_score']:.2f}/1.0")
        else:
            print("⏳ RECOMMENDATION: Continue working on branch")
            print(f"📊 Convergence Score: {convergence['convergence_score']:.2f}/1.0")
        
        if verbose:
            print("\n📈 Detailed Analysis:")
            branch_info = convergence['branch_info']
            print(f"  • Branch: {branch_info['name']}")
            print(f"  • Commits: {branch_info['commit_count']}")
            
            if branch_info['creation_time']:
                age_hours = (datetime.now() - branch_info['creation_time']).total_seconds() / 3600
                print(f"  • Age: {age_hours:.1f} hours")
            
            if branch_info['last_commit_time']:
                time_since_last = datetime.now() - branch_info['last_commit_time']
                hours_since_last = time_since_last.total_seconds() / 3600
                print(f"  • Last commit: {hours_since_last:.1f} hours ago")
            
            print(f"  • Behind main: {'Yes' if branch_info['is_behind_main'] else 'No'}")
            
            print("\n📋 Reasons:")
            for reason in convergence['reasons']:
                print(f"  • {reason}")
        
        if convergence['should_merge']:
            strategy = self.suggest_merge_strategy(branch_name)
            print(f"\n💡 Suggested merge strategy: {strategy}")


def main():
    parser = argparse.ArgumentParser(description="Git Vibe Brancher - Automatic git operations for vibe coding")
    parser.add_argument('--create', action='store_true', help='Automatically create branch if recommended')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed analysis')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--name', help='Custom branch name (overrides suggestion)')
    
    # New automatic operation options
    parser.add_argument('--auto-branch', action='store_true', help='Automatically create branch if needed (silent)')
    parser.add_argument('--save', action='store_true', help='Save current progress with intelligent branching')
    parser.add_argument('--checkpoint', action='store_true', help='Create a checkpoint of current work')
    parser.add_argument('--auto-commit', action='store_true', help='Legacy: use --save instead')
    parser.add_argument('--message', '-m', help='Description for saving progress')
    parser.add_argument('--silent', action='store_true', help='Run silently (minimal output)')
    
    # Branch convergence options
    parser.add_argument('--convergence', action='store_true', help='Analyze branch convergence (merge readiness)')
    parser.add_argument('--branch', help='Specific branch to analyze (default: current branch)')
    
    args = parser.parse_args()
    
    try:
        brancher = GitVibeBrancher(args.config)
        
        # Handle automatic operations
        if args.save or args.checkpoint or args.auto_commit:
            success = brancher.save_progress(args.message, silent=args.silent)
            if not success:
                sys.exit(1)
        elif args.auto_branch:
            success = brancher.auto_branch_if_needed(silent=args.silent)
            if not success and not args.silent:
                print("No branching needed")
        elif args.convergence:
            # Branch convergence analysis
            brancher.show_convergence_analysis(args.branch, args.verbose)
        else:
            # Original analysis mode
            analysis = brancher.analyze_branch_need()
            brancher.show_analysis(analysis, args.verbose)
            
            if args.create and analysis['should_branch']:
                branch_name = args.name or brancher.suggest_branch_name(analysis)
                brancher.create_branch(branch_name)
            elif args.create and not analysis['should_branch']:
                print("\n⚠️  Branch creation not recommended based on current analysis.")
            
    except RuntimeError as e:
        if not args.silent:
            print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
