#!/usr/bin/env python3
"""
Quick Enhanced Demo - Test the auto-commit features
"""

import os
import sys
import subprocess
import time

class QuickEnhancedDemo:
    def __init__(self):
        self.demo_dir = "/Users/dilipkunderu/hackday/PoorlyWrittenService"
        self.vibe_brancher_path = os.path.join(os.path.dirname(__file__), "vibe_brancher.py")
    
    def run_command(self, command: str, capture: bool = False):
        """Run a command and optionally capture output"""
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
    
    def test_simple_auto_commit(self):
        """Test simple auto-commit"""
        print("🧪 Testing Simple Auto-Commit")
        print("-" * 40)
        
        # Create a simple file
        with open(f"{self.demo_dir}/test_simple.js", "w") as f:
            f.write("// Simple test file\nfunction test() { return true; }")
        
        print("Running auto-commit...")
        output = self.run_vibe_brancher("--commit", capture=True)
        print(output)
        print()
    
    def test_interactive_commit(self):
        """Test interactive commit"""
        print("🧪 Testing Interactive Commit")
        print("-" * 40)
        
        # Create multiple files
        with open(f"{self.demo_dir}/test_doc1.md", "w") as f:
            f.write("# Test Doc 1")
        
        with open(f"{self.demo_dir}/test_doc2.md", "w") as f:
            f.write("# Test Doc 2")
        
        print("Running interactive auto-commit...")
        output = self.run_vibe_brancher("--commit", capture=True)
        print(output)
        print()
    
    def test_vibe_commit(self):
        """Test vibe-commit"""
        print("🧪 Testing Vibe-Commit")
        print("-" * 40)
        
        # Create a Java file
        os.makedirs(f"{self.demo_dir}/src/test/java/com/demo", exist_ok=True)
        with open(f"{self.demo_dir}/src/test/java/com/demo/TestService.java", "w") as f:
            f.write("package com.demo;\n\npublic class TestService {\n    public void test() {}\n}")
        
        print("Running vibe-commit...")
        output = self.run_vibe_brancher("--vibe-commit", capture=True)
        print(output)
        print()
    
    def test_custom_message(self):
        """Test custom commit message"""
        print("🧪 Testing Custom Message")
        print("-" * 40)
        
        # Create config file
        os.makedirs(f"{self.demo_dir}/config", exist_ok=True)
        with open(f"{self.demo_dir}/config/test.json", "w") as f:
            f.write('{"test": true}')
        
        print("Running auto-commit with custom message...")
        output = self.run_vibe_brancher("--commit --message 'config: add test configuration'", capture=True)
        print(output)
        print()
    
    def show_commit_history(self):
        """Show commit history"""
        print("📜 Recent Commit History")
        print("-" * 40)
        
        commits = self.run_command("git log --oneline -8", capture=True)
        print(commits)
        print()
    
    def run_demo(self):
        """Run the quick demo"""
        print("🌿 Quick Enhanced Demo - Auto-Commit Features")
        print("=" * 50)
        print()
        
        try:
            self.test_simple_auto_commit()
            self.test_interactive_commit()
            self.test_vibe_commit()
            self.test_custom_message()
            self.show_commit_history()
            
            print("✅ All tests completed successfully!")
            
        except Exception as e:
            print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    demo = QuickEnhancedDemo()
    demo.run_demo()
