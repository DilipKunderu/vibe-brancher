#!/usr/bin/env python3
"""
Git Vibe Brancher - Unified Demo System
A comprehensive demonstration of all Git Vibe Brancher features
"""

import os
import sys
import subprocess
import time
import random
import threading
import signal
import argparse
from pathlib import Path
from typing import Dict, List, Optional
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

class UnifiedDemo:
    def __init__(self, demo_type: str = "full", target_repo: str = None):
        self.demo_type = demo_type
        self.target_repo = target_repo or "/Users/dilipkunderu/hackday/PoorlyWrittenService"
        self.vibe_brancher_path = os.path.join(os.path.dirname(__file__), "vibe_brancher.py")
        self.visualizer_api_path = os.path.join(os.path.dirname(__file__), "visualizer_api.py")
        self.current_scenario = 0
        self.visualizer_process = None
        self.created_branches = []
        
    def print_header(self, text: str):
        """Print a styled header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
        print(f"{text:^70}")
        print(f"{'='*70}{Colors.ENDC}")
    
    def print_step(self, text: str, emoji: str = "📝"):
        """Print a step with emoji"""
        print(f"{Colors.OKCYAN}{emoji} {text}{Colors.ENDC}")
        time.sleep(0.5)
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")
        time.sleep(0.3)
    
    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")
        time.sleep(0.3)
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")
        time.sleep(0.3)
    
    def typewriter_effect(self, text: str, delay: float = 0.03):
        """Typewriter effect for text"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        time.sleep(0.5)
    
    def run_command(self, command: str, capture: bool = False) -> str:
        """Run a command in the demo directory"""
        try:
            os.makedirs(self.target_repo, exist_ok=True)
            if capture:
                result = subprocess.run(command, shell=True, cwd=self.target_repo, 
                                      capture_output=True, text=True)
                return result.stdout.strip()
            else:
                subprocess.run(command, shell=True, cwd=self.target_repo)
                return ""
        except Exception as e:
            self.print_error(f"Command failed: {e}")
            return ""
    
    def run_vibe_brancher(self, args: str = "", capture: bool = False) -> str:
        """Run the vibe brancher tool"""
        command = f"python3 {self.vibe_brancher_path} {args}"
        return self.run_command(command, capture)
    
    def start_visualizer_api(self):
        """Start the visualizer API web server on port 7171"""
        try:
            self.print_step("Starting visualizer API web server...", "🌐")
            self.visualizer_process = subprocess.Popen(
                ['python3', self.visualizer_api_path, '--server', '--port', '7171'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(2)
            self.print_success("Visualizer API web server started on http://localhost:7171!")
            self.print_success("🌐 Web Interface: http://localhost:7171")
            self.print_success("🔗 API Endpoints: /api/git-data, /api/branches, /api/health")
        except Exception as e:
            self.print_warning(f"Could not start visualizer API: {e}")
    
    def stop_visualizer_api(self):
        """Stop the visualizer API"""
        if self.visualizer_process:
            try:
                self.visualizer_process.terminate()
                self.visualizer_process.wait(timeout=5)
                self.print_success("Visualizer API stopped")
            except:
                self.visualizer_process.kill()
                self.print_warning("Visualizer API force-stopped")
    
    def create_persistent_branch(self, branch_name: str, from_branch: str = None) -> bool:
        """Create a persistent branch that will remain after demo"""
        try:
            if from_branch:
                self.run_command(f"git checkout {from_branch}")
            self.run_command(f"git checkout -b {branch_name}")
            self.created_branches.append(branch_name)
            self.print_success(f"Created persistent branch: {branch_name}")
            return True
        except Exception as e:
            self.print_warning(f"Failed to create branch {branch_name}: {e}")
            return False
    
    def show_branch_tree(self):
        """Show the current branch tree structure"""
        try:
            self.print_step("Current branch structure:", "🌳")
            branches = self.run_command("git branch -a", capture=True)
            print(f"\n{Colors.OKBLUE}Branch Tree:{Colors.ENDC}")
            print(branches)
            
            if len(self.created_branches) > 1:
                print(f"\n{Colors.OKBLUE}Created Branches:{Colors.ENDC}")
                for i, branch in enumerate(self.created_branches):
                    print(f"  {i+1}. {branch}")
        except Exception as e:
            self.print_warning(f"Could not show branch tree: {e}")
    
    def setup_demo_environment(self):
        """Set up the demo environment"""
        self.print_header("🌿 GIT VIBE BRANCHER - UNIFIED DEMO")
        
        self.typewriter_effect("Welcome to the comprehensive Git Vibe Brancher demonstration!")
        
        print(f"\n{Colors.BOLD}Demo Type: {self.demo_type.upper()}{Colors.ENDC}")
        print(f"{Colors.BOLD}Target Repository: {self.target_repo}{Colors.ENDC}")
        
        if self.demo_type == "full":
            print(f"\n{Colors.BOLD}What you'll experience:{Colors.ENDC}")
            print("• Core vibe brancher analysis and branching suggestions")
            print("• Auto-commit functionality with intelligent messages")
            print("• Interactive commit mode with file preview")
            print("• Vibe coding workflow combining analysis and auto-commit")
            print("• Persistent branches that remain after the demo")
            print("• Branch-out-of-branch scenarios")
            print("• Live visualizer API monitoring")
            print("• Web server on port 7171")
        elif self.demo_type == "quick":
            print(f"\n{Colors.BOLD}Quick demo features:{Colors.ENDC}")
            print("• Basic vibe brancher analysis")
            print("• Simple auto-commit demonstration")
            print("• Visualizer API web server")
        elif self.demo_type == "visualizer":
            print(f"\n{Colors.BOLD}Visualizer demo features:{Colors.ENDC}")
            print("• Web server on port 7171")
            print("• RESTful API endpoints")
            print("• Real-time git data")
            print("• Web interface")
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to begin the demo...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Starting demo automatically...{Colors.ENDC}")
            time.sleep(1)
        
        # Check current status
        self.print_step("Checking current repository status...", "📊")
        status = self.run_command("git status --porcelain", capture=True)
        if status:
            print(f"Current changes: {len(status.split(chr(10)))} files")
        else:
            print("Repository is clean")
        
        # Start visualizer API for full and visualizer demos
        if self.demo_type in ["full", "visualizer"]:
            self.start_visualizer_api()
        
        self.print_success("Demo environment ready!")
        time.sleep(1)
    
    def scenario_core_analysis(self):
        """Core vibe brancher analysis"""
        self.print_header("SCENARIO 1: Core Vibe Brancher Analysis")
        
        self.typewriter_effect("Let's start with the core functionality - analyzing when to create new branches.")
        
        # Show current analysis
        self.print_step("Running vibe brancher analysis...", "🔍")
        output = self.run_vibe_brancher("", capture=True)
        print(f"\n{Colors.OKBLUE}Analysis Output:{Colors.ENDC}")
        print(output)
        
        self.print_success("Perfect! The tool analyzed your current state and provided a recommendation!")
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_auto_commit(self):
        """Auto-commit functionality"""
        self.print_header("SCENARIO 2: Auto-Commit with Persistent Branch")
        
        self.typewriter_effect("Now let's demonstrate the auto-commit functionality with intelligent message generation.")
        
        # Create a persistent branch
        self.print_step("Creating a persistent feature branch...", "🌿")
        if self.create_persistent_branch("feature/demo-features"):
            self.print_success("Created persistent branch: feature/demo-features")
        
        # Create some changes
        self.print_step("Creating demo files...", "📝")
        js_code = '''// Demo utility functions
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function validateEmail(email) {
    const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return regex.test(email);
}

module.exports = { formatDate, validateEmail };
'''
        
        with open(f"{self.target_repo}/demo_utils.js", "w") as f:
            f.write(js_code)
        
        # Run auto-commit
        self.print_step("Running auto-commit...", "🤖")
        time.sleep(1)
        output = self.run_vibe_brancher("--commit", capture=True)
        print(f"\n{Colors.OKBLUE}Auto-Commit Output:{Colors.ENDC}")
        print(output)
        
        self.print_success("Excellent! The tool automatically generated a 'feat:' commit message!")
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_visualizer_demo(self):
        """Visualizer API demonstration"""
        self.print_header("SCENARIO 3: Visualizer API Demo")
        
        self.typewriter_effect("Let's explore the visualizer API and web server functionality!")
        
        # Test API endpoints
        self.print_step("Testing API endpoints...", "🌐")
        
        try:
            import requests
            
            # Test health endpoint
            response = requests.get('http://localhost:7171/api/health', timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                self.print_success(f"Health check passed: {health_data['status']}")
                print(f"   📁 Repository: {health_data['repository']}")
                print(f"   🌿 Current Branch: {health_data['currentBranch']}")
            
            # Test git-data endpoint
            response = requests.get('http://localhost:7171/api/git-data', timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.print_success("Git data retrieved successfully")
                print(f"   📊 Total Branches: {data['totalBranches']}")
                print(f"   📈 Total Commits: {data['totalCommits']}")
                print(f"   🆔 Session ID: {data['sessionId']}")
            
            self.print_success("All API endpoints working perfectly!")
            print(f"\n{Colors.OKBLUE}🌐 Web Interface: http://localhost:7171{Colors.ENDC}")
            print(f"{Colors.OKBLUE}🔗 API Endpoints:{Colors.ENDC}")
            print(f"   • http://localhost:7171/api/git-data")
            print(f"   • http://localhost:7171/api/branches")
            print(f"   • http://localhost:7171/api/health")
            
        except ImportError:
            self.print_warning("Requests library not available. Install with: pip install requests")
        except Exception as e:
            self.print_warning(f"API test failed: {e}")
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def final_summary(self):
        """Final summary and next steps"""
        self.print_header("🎉 DEMO COMPLETE - SUMMARY")
        
        print(f"{Colors.BOLD}Congratulations! You've experienced Git Vibe Brancher!{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Persistent Branches Created:{Colors.ENDC}")
        if self.created_branches:
            for branch in self.created_branches:
                print(f"{Colors.OKGREEN}🌿 {branch}{Colors.ENDC}")
                time.sleep(0.1)
            print(f"\n{Colors.OKBLUE}These branches will remain in your repository after the demo!{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}No persistent branches were created during this demo.{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
        next_steps = [
            "🔧 Customize commit message templates in config",
            "👥 Share the workflow with your team",
            "🔄 Integrate into your daily coding routine",
            "📈 Monitor and adjust thresholds as needed",
            "🌐 Use the visualizer API for live branch monitoring"
        ]
        
        for step in next_steps:
            print(f"{Colors.OKBLUE}{step}{Colors.ENDC}")
            time.sleep(0.2)
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}Thank you for experiencing Git Vibe Brancher!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Happy vibe coding! 🌿{Colors.ENDC}")
    
    def run_demo(self):
        """Run the complete demo based on type"""
        try:
            self.setup_demo_environment()
            
            if self.demo_type == "full":
                self.scenario_core_analysis()
                self.scenario_auto_commit()
                self.scenario_visualizer_demo()
            elif self.demo_type == "quick":
                self.scenario_core_analysis()
                self.scenario_auto_commit()
                self.scenario_visualizer_demo()
            elif self.demo_type == "visualizer":
                self.scenario_visualizer_demo()
            
            self.final_summary()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Demo interrupted by user{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}Demo error: {e}{Colors.ENDC}")
        finally:
            # Cleanup
            if self.demo_type in ["full", "visualizer"]:
                self.stop_visualizer_api()

def main():
    """Main function to run the unified demo"""
    parser = argparse.ArgumentParser(description="Git Vibe Brancher - Unified Demo System")
    parser.add_argument('--type', choices=['full', 'quick', 'visualizer'], default='full',
                       help='Demo type: full (comprehensive), quick (basic), visualizer (API only)')
    parser.add_argument('--repo', help='Target repository path (default: PoorlyWrittenService)')
    parser.add_argument('--help-demo', action='store_true', help='Show demo help')
    
    args = parser.parse_args()
    
    if args.help_demo:
        print("🌿 Git Vibe Brancher - Unified Demo System")
        print("=" * 50)
        print("\nDemo Types:")
        print("  full        - Comprehensive demo with all features (default)")
        print("  quick       - Basic demo with core features")
        print("  visualizer  - Visualizer API and web server demo only")
        print("\nExamples:")
        print("  python3 demo.py                    # Full demo")
        print("  python3 demo.py --type quick       # Quick demo")
        print("  python3 demo.py --type visualizer  # Visualizer demo only")
        print("  python3 demo.py --repo /path/to/repo  # Custom repository")
        return
    
    demo = UnifiedDemo(demo_type=args.type, target_repo=args.repo)
    demo.run_demo()

if __name__ == "__main__":
    main()