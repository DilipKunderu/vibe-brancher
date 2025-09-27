#!/usr/bin/env python3
"""
Test script for the visualizer API web server
"""

import subprocess
import time
import requests
import json
import sys

def test_web_server():
    """Test the visualizer API web server"""
    print("🧪 Testing Git Vibe Brancher Visualizer API Web Server")
    print("=" * 60)
    
    # Start the web server
    print("🚀 Starting web server on port 7171...")
    try:
        server_process = subprocess.Popen([
            'python3', 'visualizer_api.py', '--server', '--port', '7171'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        base_url = "http://localhost:7171"
        
        print(f"\n🔗 Testing API endpoints...")
        
        # Test health endpoint
        print("1. Testing /api/health...")
        try:
            response = requests.get(f"{base_url}/api/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"   ✅ Health check passed: {health_data['status']}")
                print(f"   📁 Repository: {health_data['repository']}")
                print(f"   🌿 Current Branch: {health_data['currentBranch']}")
            else:
                print(f"   ❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
        
        # Test git-data endpoint
        print("\n2. Testing /api/git-data...")
        try:
            response = requests.get(f"{base_url}/api/git-data", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Git data retrieved successfully")
                print(f"   📊 Total Branches: {data['totalBranches']}")
                print(f"   📈 Total Commits: {data['totalCommits']}")
                print(f"   📝 Total Files Changed: {data['totalFilesChanged']}")
                print(f"   🆔 Session ID: {data['sessionId']}")
            else:
                print(f"   ❌ Git data failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Git data error: {e}")
        
        # Test branches endpoint
        print("\n3. Testing /api/branches...")
        try:
            response = requests.get(f"{base_url}/api/branches", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Branches data retrieved successfully")
                print(f"   🌿 Current Branch: {data['currentBranch']}")
                print(f"   📊 Total Branches: {data['totalBranches']}")
                print(f"   📋 Branch List:")
                for branch in data['branches']:
                    status = "🟢 ACTIVE" if branch['isActive'] else "⚪"
                    print(f"      {status} {branch['name']} ({branch['type']}) - {branch['commitCount']} commits")
            else:
                print(f"   ❌ Branches data failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Branches data error: {e}")
        
        # Test stats endpoint
        print("\n4. Testing /api/stats...")
        try:
            response = requests.get(f"{base_url}/api/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Stats data retrieved successfully")
                print(f"   📊 Total Branches: {data['totalBranches']}")
                print(f"   📈 Total Commits: {data['totalCommits']}")
                print(f"   📝 Total Files Changed: {data['totalFilesChanged']}")
                print(f"   🆔 Session ID: {data['sessionId']}")
            else:
                print(f"   ❌ Stats data failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Stats data error: {e}")
        
        # Test web interface
        print("\n5. Testing web interface...")
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ Web interface accessible")
                print(f"   🌐 Open http://localhost:7171 in your browser to see the interface")
            else:
                print(f"   ❌ Web interface failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Web interface error: {e}")
        
        print(f"\n🎉 Web server test completed!")
        print(f"🌐 Web Interface: http://localhost:7171")
        print(f"🔗 API Endpoints:")
        print(f"   • http://localhost:7171/api/git-data")
        print(f"   • http://localhost:7171/api/branches")
        print(f"   • http://localhost:7171/api/current-branch")
        print(f"   • http://localhost:7171/api/stats")
        print(f"   • http://localhost:7171/api/health")
        
        # Stop the server
        print(f"\n🛑 Stopping web server...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print(f"✅ Web server stopped")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        if 'server_process' in locals():
            server_process.terminate()

if __name__ == "__main__":
    test_web_server()
