#!/usr/bin/env python3
"""
Immersive Git Vibe Brancher Demo
A comprehensive, interactive demonstration of the Git Vibe Brancher tool
"""

import os
import sys
import subprocess
import time
import random
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

class ImmersiveDemo:
    def __init__(self):
        self.demo_dir = "/tmp/git-vibe-immersive-demo"
        self.vibe_brancher_path = "/Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py"
        self.current_scenario = 0
        self.scenarios = []
        
    def print_header(self, text: str):
        """Print a styled header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
        print(f"{text:^60}")
        print(f"{'='*60}{Colors.ENDC}\n")
    
    def print_step(self, text: str, emoji: str = "🔍"):
        """Print a step with emoji and styling"""
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
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")
        time.sleep(0.3)
    
    def typewriter_effect(self, text: str, delay: float = 0.03):
        """Simulate typewriter effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
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
        self.print_header("🌿 GIT VIBE BRANCHER - IMMERSIVE DEMO")
        
        self.typewriter_effect("Welcome to the most comprehensive demonstration of Git Vibe Brancher!")
        self.typewriter_effect("This tool helps you decide when to create new git branches during 'vibe coding'.")
        
        print(f"\n{Colors.BOLD}What you'll experience:{Colors.ENDC}")
        print("• Real coding scenarios with different complexity levels")
        print("• Intelligent branch recommendations based on multiple factors")
        print("• Automatic branch creation with smart naming")
        print("• Detailed analysis of your coding patterns")
        print("• Interactive decision-making process")
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to begin the immersive experience...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Starting demo automatically...{Colors.ENDC}")
            time.sleep(1)
        
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
        time.sleep(1)
    
    def scenario_1_small_changes(self):
        """Scenario 1: Small changes - should NOT recommend branching"""
        self.print_header("SCENARIO 1: Small Bug Fix")
        
        self.typewriter_effect("You're working on a small bug fix. Let's see what the Vibe Brancher thinks...")
        
        # Create small changes
        self.print_step("Making small changes...", "🔧")
        self.run_command('echo "Fixed typo in documentation" >> README.md')
        self.run_command('echo "// Small comment addition" > utils.js')
        
        self.print_step("Running Vibe Brancher analysis...", "🔍")
        time.sleep(1)
        
        # Run vibe brancher
        output = self.run_vibe_brancher("--verbose", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output:{Colors.ENDC}")
        print(output)
        
        self.print_info("The tool correctly identified this as a small change that doesn't need branching!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the next scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_2_moderate_changes(self):
        """Scenario 2: Moderate changes - borderline case"""
        self.print_header("SCENARIO 2: Feature Enhancement")
        
        self.typewriter_effect("Now you're adding a new feature. This is where it gets interesting...")
        
        # Create moderate changes
        self.print_step("Adding new feature files...", "⚡")
        
        # Create a new feature file
        feature_code = '''def calculate_discount(price, discount_percent):
    """Calculate discounted price"""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount

def apply_tax(price, tax_rate=0.08):
    """Apply tax to price"""
    return price * (1 + tax_rate)

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:.2f}"
'''
        
        with open(f"{self.demo_dir}/pricing.py", "w") as f:
            f.write(feature_code)
        
        # Update existing file
        self.run_command('echo "Added pricing utilities" >> README.md')
        
        self.print_step("Running Vibe Brancher analysis...", "🔍")
        time.sleep(1)
        
        output = self.run_vibe_brancher("--verbose", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output:{Colors.ENDC}")
        print(output)
        
        self.print_info("This is a borderline case - the tool considers multiple factors!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the next scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_3_significant_changes(self):
        """Scenario 3: Significant changes - should recommend branching"""
        self.print_header("SCENARIO 3: Major Feature Implementation")
        
        self.typewriter_effect("Now you're implementing a major feature with multiple files and complex logic...")
        
        # Create significant changes
        self.print_step("Implementing user authentication system...", "🔐")
        
        # Create multiple files for a complete feature
        auth_code = '''import hashlib
import secrets
from datetime import datetime, timedelta
import json

class UserManager:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.sessions = {}
    
    def hash_password(self, password):
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return salt + password_hash.hex()
    
    def verify_password(self, stored_password, provided_password):
        """Verify password against stored hash"""
        salt = stored_password[:32]
        stored_hash = stored_password[32:]
        password_hash = hashlib.pbkdf2_hmac('sha256',
                                          provided_password.encode('utf-8'),
                                          salt.encode('utf-8'),
                                          100000)
        return password_hash.hex() == stored_hash
    
    def create_user(self, username, email, password):
        """Create new user"""
        # Implementation would go here
        pass
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        # Implementation would go here
        pass
    
    def create_session(self, user_id):
        """Create user session"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        self.sessions[session_token] = {
            'user_id': user_id,
            'expires_at': expires_at
        }
        return session_token
    
    def validate_session(self, session_token):
        """Validate session token"""
        if session_token not in self.sessions:
            return False
        
        session = self.sessions[session_token]
        if datetime.now() > session['expires_at']:
            del self.sessions[session_token]
            return False
        
        return True
'''
        
        with open(f"{self.demo_dir}/auth.py", "w") as f:
            f.write(auth_code)
        
        # Create additional related files
        middleware_code = '''from flask import request, jsonify, g
from auth import UserManager

user_manager = UserManager()

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not user_manager.validate_session(token):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current authenticated user"""
    token = request.headers.get('Authorization')
    if token and user_manager.validate_session(token):
        return user_manager.get_user_by_token(token)
    return None
'''
        
        with open(f"{self.demo_dir}/middleware.py", "w") as f:
            f.write(middleware_code)
        
        # Create routes file
        routes_code = '''from flask import Flask, request, jsonify
from auth import UserManager
from middleware import require_auth, get_current_user

app = Flask(__name__)
user_manager = UserManager()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_id = user_manager.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        return jsonify({'user_id': user_id, 'message': 'User created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_manager.authenticate_user(data['username'], data['password'])
    if user:
        session_token = user_manager.create_session(user['id'])
        return jsonify({'token': session_token, 'user': user})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/profile', methods=['GET'])
@require_auth
def get_profile():
    user = get_current_user()
    return jsonify({'user': user})

@app.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    token = request.headers.get('Authorization')
    user_manager.invalidate_session(token)
    return jsonify({'message': 'Logged out successfully'})
'''
        
        with open(f"{self.demo_dir}/routes.py", "w") as f:
            f.write(routes_code)
        
        # Create tests
        test_code = '''import unittest
from auth import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager(":memory:")
    
    def test_password_hashing(self):
        password = "testpassword123"
        hashed = self.user_manager.hash_password(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(self.user_manager.verify_password(hashed, password))
    
    def test_invalid_password(self):
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = self.user_manager.hash_password(password)
        self.assertFalse(self.user_manager.verify_password(hashed, wrong_password))
    
    def test_session_creation(self):
        user_id = 1
        token = self.user_manager.create_session(user_id)
        self.assertIsNotNone(token)
        self.assertTrue(self.user_manager.validate_session(token))
    
    def test_session_validation(self):
        user_id = 1
        token = self.user_manager.create_session(user_id)
        self.assertTrue(self.user_manager.validate_session(token))
        self.assertFalse(self.user_manager.validate_session("invalid_token"))

if __name__ == '__main__':
    unittest.main()
'''
        
        with open(f"{self.demo_dir}/test_auth.py", "w") as f:
            f.write(test_code)
        
        # Update README
        self.run_command('echo "Added complete user authentication system" >> README.md')
        
        self.print_step("Running Vibe Brancher analysis...", "🔍")
        time.sleep(2)
        
        output = self.run_vibe_brancher("--verbose", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output:{Colors.ENDC}")
        print(output)
        
        self.print_success("Perfect! The tool correctly identified this as a major change requiring a new branch!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to see automatic branch creation...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_4_auto_branch_creation(self):
        """Scenario 4: Automatic branch creation"""
        self.print_header("SCENARIO 4: Automatic Branch Creation")
        
        self.typewriter_effect("Now let's see the magic happen - automatic branch creation with smart naming!")
        
        self.print_step("Creating branch automatically...", "🌿")
        time.sleep(1)
        
        output = self.run_vibe_brancher("--create", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output:{Colors.ENDC}")
        print(output)
        
        # Show current branches
        self.print_step("Checking current branches...", "📋")
        branches = self.run_command("git branch", capture=True)
        print(f"\n{Colors.OKBLUE}Current branches:{Colors.ENDC}")
        print(branches)
        
        self.print_success("Branch created successfully with intelligent naming!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the next scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_5_custom_configuration(self):
        """Scenario 5: Custom configuration demonstration"""
        self.print_header("SCENARIO 5: Custom Configuration")
        
        self.typewriter_effect("Let's explore how you can customize the tool's behavior with configuration!")
        
        # Create custom config
        custom_config = {
            "thresholds": {
                "files_changed": 3,  # Lower threshold
                "lines_added": 30,
                "lines_removed": 20,
                "time_minutes": 15,  # Shorter time
                "complexity_score": 5
            },
            "weights": {
                "files_changed": 0.4,  # Higher weight for file count
                "lines_changed": 0.2,
                "time_factor": 0.3,
                "complexity": 0.1,
                "file_types": 0.0
            },
            "branch_naming": {
                "prefix": "dev",
                "separator": "-",
                "include_timestamp": True
            }
        }
        
        config_path = f"{self.demo_dir}/custom_config.json"
        with open(config_path, "w") as f:
            json.dump(custom_config, f, indent=2)
        
        self.print_info("Created custom configuration with:")
        print("• Lower thresholds (more sensitive)")
        print("• Different branch naming convention")
        print("• Adjusted weights for different factors")
        
        # Make some changes
        self.print_step("Making changes to test custom config...", "🔧")
        self.run_command('echo "Added new utility function" > utils.py')
        self.run_command('echo "Updated configuration" >> README.md')
        
        self.print_step("Running with custom configuration...", "🔍")
        output = self.run_vibe_brancher(f"--config {config_path} --verbose", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe Brancher Output (Custom Config):{Colors.ENDC}")
        print(output)
        
        self.print_info("Notice how the custom configuration affects the analysis!")
        input(f"\n{Colors.OKGREEN}Press Enter to continue to the final scenario...{Colors.ENDC}")
    
    def scenario_6_integration_ideas(self):
        """Scenario 6: Integration ideas and advanced usage"""
        self.print_header("SCENARIO 6: Integration Ideas & Advanced Usage")
        
        self.typewriter_effect("Let's explore how you can integrate this tool into your workflow!")
        
        print(f"\n{Colors.BOLD}Integration Ideas:{Colors.ENDC}")
        
        ideas = [
            ("Shell Prompt Integration", "Add to your PS1 to show branch recommendations"),
            ("Pre-commit Hooks", "Run before commits to suggest branching"),
            ("IDE Integration", "Add as a custom command in your editor"),
            ("Git Aliases", "Create shortcuts like 'git vibe' or 'git should-branch'"),
            ("CI/CD Integration", "Use in automated workflows"),
            ("Team Workflows", "Share configs across team members")
        ]
        
        for i, (title, description) in enumerate(ideas, 1):
            print(f"{Colors.OKCYAN}{i}. {title}{Colors.ENDC}")
            print(f"   {description}")
            time.sleep(0.5)
        
        self.print_step("Demonstrating git alias setup...", "⚙️")
        
        alias_commands = [
            'git config --global alias.vibe "!python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py"',
            'git config --global alias.should-branch "!python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py --verbose"',
            'git config --global alias.create-branch "!python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py --create"'
        ]
        
        for cmd in alias_commands:
            print(f"{Colors.OKBLUE}$ {cmd}{Colors.ENDC}")
            time.sleep(0.3)
        
        self.print_info("After setting these aliases, you can use:")
        print("• git vibe - Quick analysis")
        print("• git should-branch - Detailed analysis")
        print("• git create-branch - Auto-create if recommended")
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to see the final summary...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def final_summary(self):
        """Final summary and cleanup"""
        self.print_header("🎉 DEMO COMPLETE - SUMMARY")
        
        self.typewriter_effect("Congratulations! You've experienced the full power of Git Vibe Brancher!")
        
        print(f"\n{Colors.BOLD}What you've learned:{Colors.ENDC}")
        achievements = [
            "✅ How the tool analyzes multiple factors for branching decisions",
            "✅ Different scenarios and their branching recommendations",
            "✅ Automatic branch creation with intelligent naming",
            "✅ Custom configuration options",
            "✅ Integration possibilities for your workflow",
            "✅ Real-world usage patterns and best practices"
        ]
        
        for achievement in achievements:
            print(f"{Colors.OKGREEN}{achievement}{Colors.ENDC}")
            time.sleep(0.3)
        
        print(f"\n{Colors.BOLD}Key Features Demonstrated:{Colors.ENDC}")
        features = [
            "🔍 Intelligent analysis of file changes, line counts, and complexity",
            "⏰ Time-based factors for branching decisions",
            "🎯 Configurable thresholds and weights",
            "🌿 Smart branch naming suggestions",
            "⚡ Automatic branch creation",
            "🔧 Custom configuration support"
        ]
        
        for feature in features:
            print(f"{Colors.OKCYAN}{feature}{Colors.ENDC}")
            time.sleep(0.3)
        
        print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
        print(f"{Colors.OKBLUE}1. Install the tool in your development environment{Colors.ENDC}")
        print(f"{Colors.OKBLUE}2. Customize the configuration for your workflow{Colors.ENDC}")
        print(f"{Colors.OKBLUE}3. Set up git aliases for easy access{Colors.ENDC}")
        print(f"{Colors.OKBLUE}4. Integrate with your IDE or shell prompt{Colors.ENDC}")
        print(f"{Colors.OKBLUE}5. Share with your team for consistent branching practices{Colors.ENDC}")
        
        self.print_step("Cleaning up demo environment...", "🧹")
        self.run_command(f"rm -rf {self.demo_dir}")
        self.print_success("Demo environment cleaned up!")
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}Thank you for experiencing Git Vibe Brancher!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Happy vibe coding! 🌿{Colors.ENDC}")
    
    def run_demo(self):
        """Run the complete immersive demo"""
        try:
            self.setup_demo_environment()
            self.scenario_1_small_changes()
            self.scenario_2_moderate_changes()
            self.scenario_3_significant_changes()
            self.scenario_4_auto_branch_creation()
            self.scenario_5_custom_configuration()
            self.scenario_6_integration_ideas()
            self.final_summary()
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Demo interrupted by user{Colors.ENDC}")
            self.run_command(f"rm -rf {self.demo_dir}")
        except Exception as e:
            print(f"\n{Colors.FAIL}Demo error: {e}{Colors.ENDC}")
            self.run_command(f"rm -rf {self.demo_dir}")

def main():
    """Main function to run the immersive demo"""
    demo = ImmersiveDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
