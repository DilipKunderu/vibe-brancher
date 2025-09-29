#!/usr/bin/env python3
"""
Git Vibe Brancher Daemon - Background monitoring and automatic git operations
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


class VibeDaemon:
    def __init__(self, repo_path: str = None, config_path: str = None, 
                 monitor_interval: int = 30, auto_commit_interval: int = 300):
        """
        Initialize the vibe daemon.
        
        Args:
            repo_path: Path to git repository (defaults to current directory)
            config_path: Path to configuration file
            monitor_interval: Seconds between file change checks
            auto_commit_interval: Seconds between automatic commits
        """
        self.repo_path = repo_path or os.getcwd()
        self.monitor_interval = monitor_interval
        self.auto_commit_interval = auto_commit_interval
        self.running = False
        self.last_commit_time = datetime.now()
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
        print(f"\n🛑 Received signal {signum}, shutting down daemon...")
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
    
    def _should_auto_commit(self) -> bool:
        """Determine if it's time for an automatic commit."""
        time_since_last = datetime.now() - self.last_commit_time
        return time_since_last.total_seconds() >= self.auto_commit_interval
    
    def _auto_save_if_needed(self):
        """Perform automatic save if conditions are met."""
        try:
            # Check if there are any changes
            files = self.brancher._get_git_status()
            total_files = len(files['modified']) + len(files['added']) + len(files['untracked'])
            
            if total_files == 0:
                return
            
            # Check if we should auto-save based on time
            if not self._should_auto_commit():
                return
            
            # Perform automatic save with branching (completely silent)
            success = self.brancher.save_progress(silent=True)
            if success:
                self.last_commit_time = datetime.now()
                # Only show minimal feedback, don't interrupt flow
                print(f"💾 Auto-saved at {datetime.now().strftime('%H:%M')}")
            
        except Exception as e:
            # Silent failure - don't interrupt the vibe
            pass
    
    def _check_branch_convergence(self):
        """Check if current branch is ready to merge."""
        try:
            # Only check convergence every 10 minutes to avoid overhead
            if not hasattr(self, 'last_convergence_check'):
                self.last_convergence_check = datetime.now()
            
            time_since_check = datetime.now() - self.last_convergence_check
            if time_since_check.total_seconds() < 600:  # 10 minutes
                return
            
            # Run convergence analysis
            convergence = self.brancher.analyze_branch_convergence()
            
            # If branch is ready to merge, show notification
            if convergence['should_merge'] and convergence['convergence_score'] >= 0.8:
                print(f"💡 Branch '{convergence['branch_info']['name']}' is ready to merge (score: {convergence['convergence_score']:.2f})")
                strategy = self.brancher.suggest_merge_strategy()
                print(f"   Suggested: {strategy}")
            
            self.last_convergence_check = datetime.now()
            
        except Exception:
            # Silent failure
            pass
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        print(f"🔍 Starting vibe daemon for: {self.brancher.repo_path}")
        print(f"📊 Monitor interval: {self.monitor_interval}s")
        print(f"⏰ Auto-commit interval: {self.auto_commit_interval}s")
        print("🛑 Press Ctrl+C to stop")
        
        while self.running:
            try:
                # Check for file changes
                if self._check_for_changes():
                    print(f"📝 Files changed at {datetime.now().strftime('%H:%M:%S')}")
                    
                    # Run analysis
                    analysis = self.brancher.analyze_branch_need()
                    if analysis['should_branch']:
                        print(f"🌿 Branch score: {analysis['branch_score']:.2f} - considering auto-branch")
                
                # Check for auto-save
                self._auto_save_if_needed()
                
                # Check branch convergence (every 10 minutes)
                self._check_branch_convergence()
                
                # Sleep until next check
                time.sleep(self.monitor_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️  Monitor error: {e}")
                time.sleep(self.monitor_interval)
        
        print("🛑 Vibe daemon stopped")
    
    def start(self):
        """Start the daemon."""
        self.running = True
        self._monitor_loop()
    
    def stop(self):
        """Stop the daemon."""
        self.running = False


def main():
    parser = argparse.ArgumentParser(description="Git Vibe Brancher Daemon - Automatic git operations")
    parser.add_argument('--repo', help='Path to git repository (default: current directory)')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--monitor-interval', type=int, default=30, 
                       help='Seconds between file change checks (default: 30)')
    parser.add_argument('--auto-commit-interval', type=int, default=300,
                       help='Seconds between automatic commits (default: 300)')
    parser.add_argument('--daemon', action='store_true', help='Run as background daemon')
    
    args = parser.parse_args()
    
    # Create and start daemon
    daemon = VibeDaemon(
        repo_path=args.repo,
        config_path=args.config,
        monitor_interval=args.monitor_interval,
        auto_commit_interval=args.auto_commit_interval
    )
    
    if args.daemon:
        # Run as background daemon
        import daemon
        with daemon.DaemonContext():
            daemon.start()
    else:
        # Run in foreground
        daemon.start()


if __name__ == "__main__":
    main()
