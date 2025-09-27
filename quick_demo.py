#!/usr/bin/env python3
"""
Quick Git Vibe Brancher Demo
A fast demonstration of key features
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class QuickDemo:
    def __init__(self):
        self.demo_dir = "/tmp/git-vibe-quick-demo"
        self.vibe_brancher_path = "/Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py"
    
    def run_command(self, command: str, capture: bool = False):
        """Run a command and optionally capture output"""
        # Ensure the demo directory exists
        os.makedirs(self.demo_dir, exist_ok=True)
        
        if capture:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.demo_dir)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, cwd=self.demo_dir)
            return ""
    
    def run_vibe_brancher(self, args: str = "", capture: bool = False):
        """Run the vibe brancher tool"""
        command = f"python3 {self.vibe_brancher_path} {args}"
        return self.run_command(command, capture)
    
    def setup_demo(self):
        """Set up quick demo environment"""
        print("🌿 Git Vibe Brancher - Quick Demo")
        print("=" * 40)
        
        # Clean up and create demo directory
        self.run_command(f"rm -rf {self.demo_dir}")
        self.run_command(f"mkdir -p {self.demo_dir}")
        
        print("📁 Setting up demo repository...")
        self.run_command("git init")
        self.run_command('git config user.email "demo@example.com"')
        self.run_command('git config user.name "Demo User"')
        
        # Initial commit
        self.run_command('echo "# Demo Project" > README.md')
        self.run_command("git add README.md")
        self.run_command('git commit -m "Initial commit"')
        
        print("✅ Demo environment ready!\n")
    
    def demo_small_changes(self):
        """Demo small changes"""
        print("🔍 Scenario 1: Small Changes")
        print("-" * 30)
        
        self.run_command('echo "Small fix" >> README.md')
        
        print("Running analysis...")
        output = self.run_vibe_brancher("", capture=True)
        print(output)
        print()
    
    def demo_significant_changes(self):
        """Demo significant changes"""
        print("🔍 Scenario 2: Significant Changes")
        print("-" * 35)
        
        # Create multiple files
        code = '''def authenticate_user(username, password):
    # User authentication logic
    return True

def create_session(user_id):
    # Session creation logic
    return "session_token"

def validate_permissions(user_id, resource):
    # Permission validation logic
    return True
'''
        
        with open(f"{self.demo_dir}/auth.py", "w") as f:
            f.write(code)
        
        with open(f"{self.demo_dir}/middleware.py", "w") as f:
            f.write("from auth import authenticate_user\n\n# Middleware code here\n")
        
        with open(f"{self.demo_dir}/routes.py", "w") as f:
            f.write("from flask import Flask\nfrom middleware import *\n\n# Route definitions here\n")
        
        print("Running analysis...")
        output = self.run_vibe_brancher("--verbose", capture=True)
        print(output)
        print()
    
    def demo_auto_branch(self):
        """Demo automatic branch creation"""
        print("🔍 Scenario 3: Auto Branch Creation")
        print("-" * 35)
        
        print("Creating branch automatically...")
        output = self.run_vibe_brancher("--create", capture=True)
        print(output)
        
        print("\nCurrent branches:")
        branches = self.run_command("git branch", capture=True)
        print(branches)
        print()
    
    def cleanup(self):
        """Clean up demo environment"""
        print("🧹 Cleaning up...")
        self.run_command(f"rm -rf {self.demo_dir}")
        print("✅ Demo complete!")
    
    def run(self):
        """Run the quick demo"""
        try:
            self.setup_demo()
            self.demo_small_changes()
            self.demo_significant_changes()
            self.demo_auto_branch()
            self.cleanup()
        except KeyboardInterrupt:
            print("\n⚠️ Demo interrupted")
            self.cleanup()
        except Exception as e:
            print(f"\n❌ Demo error: {e}")
            self.cleanup()

if __name__ == "__main__":
    demo = QuickDemo()
    demo.run()
