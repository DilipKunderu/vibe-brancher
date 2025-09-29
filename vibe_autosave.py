#!/usr/bin/env python3
"""
Git Vibe Brancher Auto-Save - Completely invisible progress saving
Works like IDE auto-save - you never think about it
"""

import os
import sys
import time
import signal
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional
import argparse

# Add the current directory to path to import vibe_brancher
sys.path.append(str(Path(__file__).parent))
from vibe_brancher import GitVibeBrancher


class VibeAutoSave:
    def __init__(self, repo_path: str = None, config_path: str = None, 
                 save_interval: int = 60, branch_threshold: float = 0.7):
        """
        Initialize the vibe auto-save.
        
        Args:
            repo_path: Path to git repository (defaults to current directory)
            config_path: Path to configuration file
            save_interval: Seconds between automatic saves
            branch_threshold: Score threshold for automatic branching
        """
        self.repo_path = repo_path or os.getcwd()
        self.save_interval = save_interval
        self.branch_threshold = branch_threshold
        self.running = False
        self.last_save_time = datetime.now()
        self.last_file_check = {}
        
        # Initialize the brancher
        try:
            self.brancher = GitVibeBrancher(config_path)
            if repo_path:
                self.brancher.repo_path = repo_path
        except Exception as e:
            print(f"❌ Failed to initialize GitVibeBrancher: {e}")
            sys.exit(1)
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.running = False
    
    def _get_file_modification_times(self) -> Dict[str, float]:
        """Get modification times for all tracked files."""
        try:
            # Get list of tracked files
            result = self.brancher._run_git_command(['ls-files'])
            files = {}
            
            for file_path in result.split('\n'):
                if file_path.strip():
                    full_path = os.path.join(self.brancher.repo_path, file_path)
                    if os.path.exists(full_path):
                        files[file_path] = os.path.getmtime(full_path)
            
            return files
        except Exception:
            return {}
    
    def _check_for_changes(self) -> bool:
        """Check if any files have been modified since last check."""
        current_files = self._get_file_modification_times()
        
        if not self.last_file_check:
            self.last_file_check = current_files
            return False
        
        # Check if any files have been modified
        for file_path, mtime in current_files.items():
            if file_path not in self.last_file_check or self.last_file_check[file_path] != mtime:
                self.last_file_check = current_files
                return True
        
        return False
    
    def _should_auto_save(self) -> bool:
        """Determine if it's time for an automatic save."""
        time_since_last = datetime.now() - self.last_save_time
        return time_since_last.total_seconds() >= self.save_interval
    
    def _invisible_save(self):
        """Perform completely invisible save."""
        try:
            # Check if there are any changes
            files = self.brancher._get_git_status()
            total_files = len(files['modified']) + len(files['added']) + len(files['untracked'])
            
            if total_files == 0:
                return
            
            # Check if we should auto-save based on time
            if not self._should_auto_save():
                return
            
            # Run vibe analysis to see if we should branch
            analysis = self.brancher.analyze_branch_need()
            
            # If branch score is high, auto-branch silently
            if analysis['branch_score'] >= self.branch_threshold:
                self.brancher.auto_branch_if_needed(silent=True)
            
            # Perform automatic save (completely silent)
            success = self.brancher.save_progress(silent=True)
            if success:
                self.last_save_time = datetime.now()
                # No output - completely invisible
            
        except Exception:
            # Silent failure - never interrupt the vibe
            pass
    
    def _check_branch_convergence(self):
        """Check if current branch is ready to merge (invisible)."""
        try:
            # Only check convergence every 5 minutes to avoid overhead
            if not hasattr(self, 'last_convergence_check'):
                self.last_convergence_check = datetime.now()
            
            time_since_check = datetime.now() - self.last_convergence_check
            if time_since_check.total_seconds() < 300:  # 5 minutes
                return
            
            # Run convergence analysis
            convergence = self.brancher.analyze_branch_convergence()
            
            # If branch is ready to merge, show subtle notification
            if convergence['should_merge'] and convergence['convergence_score'] >= 0.8:
                print(f"💡 Branch '{convergence['branch_info']['name']}' is ready to merge (score: {convergence['convergence_score']:.2f})")
                strategy = self.brancher.suggest_merge_strategy()
                print(f"   Suggested: {strategy}")
            
            self.last_convergence_check = datetime.now()
            
        except Exception:
            # Silent failure
            pass
    
    def _monitor_loop(self):
        """Main monitoring loop - completely silent."""
        while self.running:
            try:
                # Check for file changes
                if self._check_for_changes():
                    # Files changed, check if we should save
                    self._invisible_save()
                
                # Check branch convergence (every 5 minutes)
                self._check_branch_convergence()
                
                # Sleep until next check
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                break
            except Exception:
                # Silent failure
                time.sleep(10)
        
        # Silent shutdown
        pass
    
    def start(self):
        """Start the invisible auto-save."""
        self.running = True
        self._monitor_loop()
    
    def stop(self):
        """Stop the auto-save."""
        self.running = False


def main():
    parser = argparse.ArgumentParser(description="Git Vibe Brancher Auto-Save - Invisible progress saving")
    parser.add_argument('--repo', help='Path to git repository (default: current directory)')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--save-interval', type=int, default=60, 
                       help='Seconds between automatic saves (default: 60)')
    parser.add_argument('--branch-threshold', type=float, default=0.7,
                       help='Score threshold for automatic branching (default: 0.7)')
    parser.add_argument('--daemon', action='store_true', help='Run as background daemon')
    
    args = parser.parse_args()
    
    # Create and start auto-save
    autosave = VibeAutoSave(
        repo_path=args.repo,
        config_path=args.config,
        save_interval=args.save_interval,
        branch_threshold=args.branch_threshold
    )
    
    if args.daemon:
        # Run as background daemon
        import daemon
        with daemon.DaemonContext():
            autosave.start()
    else:
        # Run in foreground
        autosave.start()


if __name__ == "__main__":
    main()
