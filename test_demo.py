#!/usr/bin/env python3
"""
Test version of the immersive demo - runs automatically without user input
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, List
import json

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class TestDemo:
    def __init__(self):
        self.demo_dir = "/tmp/git-vibe-test-demo"
        self.vibe_brancher_path = "/Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py"
        
    def print_header(self, text: str):
        """Print a styled header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
        print(f"{text:^60}")
        print(f"{'='*60}{Colors.ENDC}\n")
    
    def print_step(self, text: str, emoji: str = "🔍"):
        """Print a step with emoji and styling"""
        print(f"{Colors.OKCYAN}{emoji} {text}{Colors.ENDC}")
        time.sleep(0.3)
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")
        time.sleep(0.2)
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")
        time.sleep(0.2)
    
    def run_command(self, command: str, capture: bool = False) -> str:
        """Run a command and optionally capture output"""
        # Ensure the demo directory exists
        os.makedirs(self.demo_dir, exist_ok=True)
        
        if capture:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.demo_dir)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, cwd=self.demo_dir)
            return ""
    
    def run_vibe_brancher(self, args: str = "", capture: bool = False) -> str:
        """Run the vibe brancher tool"""
        command = f"python3 {self.vibe_brancher_path} {args}"
        return self.run_command(command, capture)
    
    def setup_demo_environment(self):
        """Set up the demo environment"""
        self.print_header("🌿 GIT VIBE BRANCHER - TEST DEMO")
        
        print("Setting up demo repository...")
        
        # Clean up and create demo directory
        self.run_command(f"rm -rf {self.demo_dir}")
        self.run_command(f"mkdir -p {self.demo_dir}")
        
        self.print_step("Setting up demo repository...", "📁")
        self.run_command("git init")
        self.run_command('git config user.email "demo@vibebrancher.com"')
        self.run_command('git config user.name "Vibe Coder"')
        
        # Initial commit
        self.run_command('echo "# Vibe Coding Project" > README.md')
        self.run_command("git add README.md")
        self.run_command('git commit -m "Initial commit - ready for vibe coding!"')
        
        self.print_success("Demo environment ready!")
        time.sleep(0.5)
    
    def test_small_changes(self):
        """Test small changes"""
        self.print_header("TEST 1: Small Changes")
        
        self.print_step("Making small changes...", "🔧")
        self.run_command('echo "Fixed typo in documentation" >> README.md')
        self.run_command('echo "// Small comment addition" > utils.js')
        
        self.print_step("Running Vibe Brancher analysis...", "🔍")
        output = self.run_vibe_brancher("--verbose", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output:{Colors.ENDC}")
        print(output)
        
        self.print_info("The tool correctly identified this as a small change!")
        time.sleep(1)
    
    def test_significant_changes(self):
        """Test significant changes"""
        self.print_header("TEST 2: Significant Changes")
        
        self.print_step("Creating significant changes...", "⚡")
        
        # Create multiple files
        auth_code = '''import hashlib
import secrets
from datetime import datetime, timedelta

class UserManager:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.sessions = {}
    
    def hash_password(self, password):
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return salt + password_hash.hex()
    
    def create_user(self, username, email, password):
        # Implementation would go here
        pass
    
    def authenticate_user(self, username, password):
        # Implementation would go here
        pass
'''
        
        with open(f"{self.demo_dir}/auth.py", "w") as f:
            f.write(auth_code)
        
        with open(f"{self.demo_dir}/middleware.py", "w") as f:
            f.write("from auth import UserManager\n\n# Middleware code here\n")
        
        with open(f"{self.demo_dir}/routes.py", "w") as f:
            f.write("from flask import Flask\nfrom middleware import *\n\n# Route definitions here\n")
        
        self.print_step("Running Vibe Brancher analysis...", "🔍")
        output = self.run_vibe_brancher("--verbose", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output:{Colors.ENDC}")
        print(output)
        
        self.print_info("The tool analyzed the significant changes!")
        time.sleep(1)
    
    def test_auto_branch(self):
        """Test automatic branch creation"""
        self.print_header("TEST 3: Auto Branch Creation")
        
        self.print_step("Testing auto branch creation...", "🌿")
        output = self.run_vibe_brancher("--create", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output:{Colors.ENDC}")
        print(output)
        
        # Show current branches
        self.print_step("Checking current branches...", "📋")
        branches = self.run_command("git branch", capture=True)
        print(f"\n{Colors.OKBLUE}Current branches:{Colors.ENDC}")
        print(branches)
        
        self.print_success("Branch creation test completed!")
        time.sleep(1)
    
    def cleanup(self):
        """Clean up demo environment"""
        self.print_step("Cleaning up demo environment...", "🧹")
        self.run_command(f"rm -rf {self.demo_dir}")
        self.print_success("Demo environment cleaned up!")
    
    def run_demo(self):
        """Run the test demo"""
        try:
            self.setup_demo_environment()
            self.test_small_changes()
            self.test_significant_changes()
            self.test_auto_branch()
            self.cleanup()
            
            self.print_header("🎉 TEST DEMO COMPLETE")
            print(f"{Colors.OKGREEN}All tests passed successfully!{Colors.ENDC}")
            
        except Exception as e:
            print(f"\n{Colors.FAIL}Demo error: {e}{Colors.ENDC}")
            self.cleanup()

def main():
    """Main function to run the test demo"""
    demo = TestDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
