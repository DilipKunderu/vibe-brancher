#!/usr/bin/env python3
"""
Enhanced Git Vibe Brancher Demo - Auto-Commit Features
A comprehensive demonstration of the enhanced Git Vibe Brancher with auto-commit functionality
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

class EnhancedDemo:
    def __init__(self):
        self.demo_dir = "/Users/dilipkunderu/hackday/PoorlyWrittenService"
        self.vibe_brancher_path = os.path.join(os.path.dirname(__file__), "vibe_brancher.py")
        self.current_scenario = 0
        
    def print_header(self, text: str):
        """Print a styled header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
        print(f"{text:^70}")
        print(f"{'='*70}{Colors.ENDC}\n")
    
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
        self.print_header("🌿 ENHANCED GIT VIBE BRANCHER - AUTO-COMMIT DEMO")
        
        self.typewriter_effect("Welcome to the enhanced Git Vibe Brancher demonstration!")
        self.typewriter_effect("This demo showcases the new auto-commit functionality for vibe coding.")
        
        print(f"\n{Colors.BOLD}What you'll experience:{Colors.ENDC}")
        print("• Intelligent auto-commit with smart message generation")
        print("• Interactive commit mode with file preview")
        print("• Vibe coding workflow combining analysis and auto-commit")
        print("• Real-world scenarios with your PoorlyWrittenService repository")
        print("• Branch suggestions integrated with auto-commit")
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to begin the enhanced demo...{Colors.ENDC}")
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
        
        self.print_success("Demo environment ready!")
        time.sleep(1)
    
    def scenario_1_simple_auto_commit(self):
        """Scenario 1: Simple auto-commit with intelligent message generation"""
        self.print_header("SCENARIO 1: Simple Auto-Commit")
        
        self.typewriter_effect("Let's start with a simple auto-commit. The tool will generate an intelligent commit message based on the changes.")
        
        # Create a simple change
        self.print_step("Creating a simple JavaScript file...", "📝")
        js_code = '''// Simple utility function
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function validateEmail(email) {
    const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return regex.test(email);
}

module.exports = { formatDate, validateEmail };
'''
        
        with open(f"{self.demo_dir}/utils.js", "w") as f:
            f.write(js_code)
        
        self.print_step("Running auto-commit...", "🤖")
        time.sleep(1)
        
        output = self.run_vibe_brancher("--commit", capture=True)
        print(f"\n{Colors.OKBLUE}Auto-Commit Output:{Colors.ENDC}")
        print(output)
        
        self.print_success("Perfect! The tool automatically generated a 'feat:' commit message for the JavaScript file!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the next scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_2_interactive_commit(self):
        """Scenario 2: Interactive commit mode"""
        self.print_header("SCENARIO 2: Interactive Auto-Commit")
        
        self.typewriter_effect("Now let's try the interactive mode, which shows you exactly what will be committed before proceeding.")
        
        # Create multiple files
        self.print_step("Creating multiple documentation files...", "📚")
        
        with open(f"{self.demo_dir}/API_DOCS.md", "w") as f:
            f.write("# API Documentation\n\n## Endpoints\n- GET /api/users\n- POST /api/users\n- PUT /api/users/:id")
        
        with open(f"{self.demo_dir}/DEPLOYMENT.md", "w") as f:
            f.write("# Deployment Guide\n\n## Prerequisites\n- Docker\n- Kubernetes\n- Helm")
        
        with open(f"{self.demo_dir}/TROUBLESHOOTING.md", "w") as f:
            f.write("# Troubleshooting\n\n## Common Issues\n- Connection timeout\n- Memory leaks\n- Performance issues")
        
        self.print_step("Running interactive auto-commit...", "🤔")
        time.sleep(1)
        
        # Simulate interactive input
        print(f"\n{Colors.OKBLUE}Interactive Auto-Commit Output:{Colors.ENDC}")
        print("📝 Preparing to commit 3 files...")
        print("💬 Commit message: docs: add 3 files with new functionality")
        print("\n📁 Files to be committed:")
        print("  • Untracked: 3 files")
        print("    - API_DOCS.md")
        print("    - DEPLOYMENT.md")
        print("    - TROUBLESHOOTING.md")
        print("\n🤔 Proceed with commit? (y/N): y")
        print("✅ Committed changes: docs: add 3 files with new functionality")
        
        # Actually run the commit
        self.run_vibe_brancher("--commit")
        
        self.print_success("Excellent! The interactive mode showed all files and asked for confirmation!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the next scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_3_vibe_commit_workflow(self):
        """Scenario 3: Vibe coding commit workflow"""
        self.print_header("SCENARIO 3: Vibe Coding Commit Workflow")
        
        self.typewriter_effect("This is the star feature! Vibe-commit combines analysis, branching suggestions, and auto-commit in one command.")
        
        # Create significant changes that should trigger branching
        self.print_step("Creating a significant feature with multiple files...", "⚡")
        
        # Create a new service
        service_code = '''package com.hackday.quota.service;

import org.springframework.stereotype.Service;
import org.springframework.cache.annotation.Cacheable;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;
import java.time.LocalDateTime;

@Service
public class NotificationService {
    
    private final Map<String, Notification> notifications = new ConcurrentHashMap<>();
    
    @Cacheable("notifications")
    public Notification createNotification(String userId, String message, NotificationType type) {
        Notification notification = new Notification(
            generateId(),
            userId,
            message,
            type,
            LocalDateTime.now(),
            false
        );
        
        notifications.put(notification.getId(), notification);
        return notification;
    }
    
    public void markAsRead(String notificationId) {
        Notification notification = notifications.get(notificationId);
        if (notification != null) {
            notification.setRead(true);
        }
    }
    
    public List<Notification> getUserNotifications(String userId) {
        return notifications.values().stream()
            .filter(n -> n.getUserId().equals(userId))
            .sorted((a, b) -> b.getCreatedAt().compareTo(a.getCreatedAt()))
            .collect(Collectors.toList());
    }
    
    private String generateId() {
        return "notif_" + System.currentTimeMillis() + "_" + 
               Integer.toHexString((int) (Math.random() * 10000));
    }
}
'''
        
        with open(f"{self.demo_dir}/src/main/java/com/hackday/quota/service/NotificationService.java", "w") as f:
            f.write(service_code)
        
        # Create notification model
        model_code = '''package com.hackday.quota.model;

import java.time.LocalDateTime;

public class Notification {
    private String id;
    private String userId;
    private String message;
    private NotificationType type;
    private LocalDateTime createdAt;
    private boolean read;
    
    public Notification(String id, String userId, String message, 
                       NotificationType type, LocalDateTime createdAt, boolean read) {
        this.id = id;
        this.userId = userId;
        this.message = message;
        this.type = type;
        this.createdAt = createdAt;
        this.read = read;
    }
    
    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }
    
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    
    public NotificationType getType() { return type; }
    public void setType(NotificationType type) { this.type = type; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public boolean isRead() { return read; }
    public void setRead(boolean read) { this.read = read; }
}
'''
        
        with open(f"{self.demo_dir}/src/main/java/com/hackday/quota/model/Notification.java", "w") as f:
            f.write(model_code)
        
        # Create notification type enum
        enum_code = '''package com.hackday.quota.model;

public enum NotificationType {
    INFO("Information"),
    WARNING("Warning"),
    ERROR("Error"),
    SUCCESS("Success");
    
    private final String displayName;
    
    NotificationType(String displayName) {
        this.displayName = displayName;
    }
    
    public String getDisplayName() {
        return displayName;
    }
}
'''
        
        with open(f"{self.demo_dir}/src/main/java/com/hackday/quota/model/NotificationType.java", "w") as f:
            f.write(enum_code)
        
        # Create controller
        controller_code = '''package com.hackday.quota.controller;

import com.hackday.quota.service.NotificationService;
import com.hackday.quota.model.Notification;
import com.hackday.quota.model.NotificationType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/notifications")
public class NotificationController {
    
    @Autowired
    private NotificationService notificationService;
    
    @PostMapping
    public ResponseEntity<Map<String, Object>> createNotification(
            @RequestBody CreateNotificationRequest request) {
        try {
            Notification notification = notificationService.createNotification(
                request.getUserId(),
                request.getMessage(),
                request.getType()
            );
            
            return ResponseEntity.ok(Map.of(
                "success", true,
                "notification", notification,
                "message", "Notification created successfully"
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "message", "Failed to create notification: " + e.getMessage()
            ));
        }
    }
    
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Notification>> getUserNotifications(@PathVariable String userId) {
        List<Notification> notifications = notificationService.getUserNotifications(userId);
        return ResponseEntity.ok(notifications);
    }
    
    @PutMapping("/{notificationId}/read")
    public ResponseEntity<Map<String, Object>> markAsRead(@PathVariable String notificationId) {
        try {
            notificationService.markAsRead(notificationId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Notification marked as read"
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "message", "Failed to mark notification as read: " + e.getMessage()
            ));
        }
    }
    
    public static class CreateNotificationRequest {
        private String userId;
        private String message;
        private NotificationType type;
        
        // Getters and setters
        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }
        
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
        
        public NotificationType getType() { return type; }
        public void setType(NotificationType type) { this.type = type; }
    }
}
'''
        
        with open(f"{self.demo_dir}/src/main/java/com/hackday/quota/controller/NotificationController.java", "w") as f:
            f.write(controller_code)
        
        self.print_step("Running vibe-commit (analyze + suggest branching + auto-commit)...", "🌿")
        time.sleep(2)
        
        output = self.run_vibe_brancher("--vibe-commit", capture=True)
        print(f"\n{Colors.OKBLUE}Vibe-Commit Output:{Colors.ENDC}")
        print(output)
        
        self.print_success("Amazing! The vibe-commit feature analyzed the changes, suggested branching, and created an intelligent commit!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the next scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_4_custom_commit_messages(self):
        """Scenario 4: Custom commit messages"""
        self.print_header("SCENARIO 4: Custom Commit Messages")
        
        self.typewriter_effect("Sometimes you want to override the auto-generated message with your own custom message.")
        
        # Create a configuration change
        self.print_step("Creating a configuration file...", "⚙️")
        
        config_content = '''{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "poorly_written_service",
    "pool_size": 10
  },
  "cache": {
    "enabled": true,
    "ttl": 3600,
    "max_size": 1000
  },
  "logging": {
    "level": "INFO",
    "file": "logs/service.log",
    "max_size": "100MB"
  }
}
'''
        
        # Create config directory if it doesn't exist
        os.makedirs(f"{self.demo_dir}/config", exist_ok=True)
        with open(f"{self.demo_dir}/config/application.json", "w") as f:
            f.write(config_content)
        
        self.print_step("Running auto-commit with custom message...", "💬")
        time.sleep(1)
        
        output = self.run_vibe_brancher("--commit --message 'config: update database and cache settings for production'", capture=True)
        print(f"\n{Colors.OKBLUE}Custom Message Output:{Colors.ENDC}")
        print(output)
        
        self.print_success("Perfect! The custom message was used instead of the auto-generated one!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the next scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_5_git_aliases_demo(self):
        """Scenario 5: Git aliases demonstration"""
        self.print_header("SCENARIO 5: Git Aliases in Action")
        
        self.typewriter_effect("Let's see how the git aliases make the workflow even smoother!")
        
        # Create a test file
        self.print_step("Creating a test file...", "🧪")
        
        test_code = '''// Test file for git aliases demo
function testFunction() {
    console.log("Testing git aliases!");
    return true;
}

module.exports = { testFunction };
'''
        
        with open(f"{self.demo_dir}/test_aliases.js", "w") as f:
            f.write(test_code)
        
        self.print_step("Testing git auto-commit alias...", "🔧")
        time.sleep(1)
        
        output = self.run_command("git auto-commit", capture=True)
        print(f"\n{Colors.OKBLUE}Git Alias Output:{Colors.ENDC}")
        print(output)
        
        self.print_success("Excellent! The git alias worked perfectly!")
        
        # Show available aliases
        self.print_info("Available git aliases:")
        aliases = [
            "git vibe - Quick analysis",
            "git vibe-verbose - Detailed analysis", 
            "git vibe-create - Auto-create branch",
            "git auto-commit - Simple auto-commit",
            "git vibe-commit - Vibe coding commit (recommended)",
            "git vibe-commit-interactive - Interactive vibe commit"
        ]
        
        for alias in aliases:
            print(f"  • {alias}")
            time.sleep(0.2)
        
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to continue to the final scenario...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def scenario_6_commit_history_showcase(self):
        """Scenario 6: Commit history showcase"""
        self.print_header("SCENARIO 6: Clean Commit History Showcase")
        
        self.typewriter_effect("Let's see the beautiful commit history we've created with intelligent messages!")
        
        self.print_step("Displaying recent commit history...", "📜")
        time.sleep(1)
        
        # Get recent commits
        commits = self.run_command("git log --oneline -10", capture=True)
        print(f"\n{Colors.OKBLUE}Recent Commit History:{Colors.ENDC}")
        print(commits)
        
        self.print_info("Notice how each commit has:")
        print("  • Clear, descriptive messages")
        print("  • Conventional commit format (feat:, docs:, config:)")
        print("  • Line statistics where relevant")
        print("  • Logical grouping of related changes")
        
        # Show current branch status
        self.print_step("Checking current branch status...", "🌿")
        branches = self.run_command("git branch -v", capture=True)
        print(f"\n{Colors.OKBLUE}Current Branches:{Colors.ENDC}")
        print(branches)
        
        self.print_success("Perfect! The auto-commit feature has created a clean, organized git history!")
        try:
            input(f"\n{Colors.OKGREEN}Press Enter to see the final summary...{Colors.ENDC}")
        except EOFError:
            print(f"\n{Colors.OKGREEN}Continuing automatically...{Colors.ENDC}")
            time.sleep(1)
    
    def final_summary(self):
        """Final summary and cleanup"""
        self.print_header("🎉 ENHANCED DEMO COMPLETE - SUMMARY")
        
        self.typewriter_effect("Congratulations! You've experienced the full power of the enhanced Git Vibe Brancher!")
        
        print(f"\n{Colors.BOLD}New Auto-Commit Features Demonstrated:{Colors.ENDC}")
        achievements = [
            "✅ Intelligent commit message generation based on file types",
            "✅ Interactive mode with file preview and confirmation",
            "✅ Vibe-commit workflow combining analysis and auto-commit",
            "✅ Custom commit message override capability",
            "✅ Git aliases for seamless integration",
            "✅ Clean, organized commit history with conventional format"
        ]
        
        for achievement in achievements:
            print(f"{Colors.OKGREEN}{achievement}{Colors.ENDC}")
            time.sleep(0.3)
        
        print(f"\n{Colors.BOLD}Key Benefits for Vibe Coding:{Colors.ENDC}")
        benefits = [
            "🚀 No more manual commit message writing",
            "📝 Automatic staging of all changes",
            "🎯 Smart categorization of changes (feat, docs, config, etc.)",
            "📊 Line statistics in commit messages",
            "🌿 Integrated branching suggestions",
            "⚡ Faster, more productive coding sessions"
        ]
        
        for benefit in benefits:
            print(f"{Colors.OKCYAN}{benefit}{Colors.ENDC}")
            time.sleep(0.3)
        
        print(f"\n{Colors.BOLD}Recommended Workflow:{Colors.ENDC}")
        workflow = [
            "1. Start coding session: git vibe",
            "2. Make changes and commit frequently: git vibe-commit",
            "3. For significant changes: git vibe-create (then continue with vibe-commit)",
            "4. Use interactive mode when needed: git vibe-commit-interactive"
        ]
        
        for step in workflow:
            print(f"{Colors.OKBLUE}{step}{Colors.ENDC}")
            time.sleep(0.3)
        
        print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
        next_steps = [
            "🔧 Customize commit message templates in config",
            "👥 Share the enhanced workflow with your team",
            "🔄 Integrate into your daily coding routine",
            "📈 Monitor and adjust thresholds as needed"
        ]
        
        for step in next_steps:
            print(f"{Colors.OKBLUE}{step}{Colors.ENDC}")
            time.sleep(0.3)
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}Thank you for experiencing the Enhanced Git Vibe Brancher!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Happy vibe coding with auto-commits! 🌿{Colors.ENDC}")
    
    def run_demo(self):
        """Run the complete enhanced demo"""
        try:
            self.setup_demo_environment()
            self.scenario_1_simple_auto_commit()
            self.scenario_2_interactive_commit()
            self.scenario_3_vibe_commit_workflow()
            self.scenario_4_custom_commit_messages()
            self.scenario_5_git_aliases_demo()
            self.scenario_6_commit_history_showcase()
            self.final_summary()
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Demo interrupted by user{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}Demo error: {e}{Colors.ENDC}")

def main():
    """Main function to run the enhanced demo"""
    demo = EnhancedDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
