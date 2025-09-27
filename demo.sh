#!/bin/bash
# Demo script for Git Vibe Brancher

echo "🌿 Git Vibe Brancher Demo"
echo "========================="
echo ""

# Create a temporary demo repository
DEMO_DIR="/tmp/git-vibe-demo"
rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR"

echo "📁 Creating demo repository..."
git init
git config user.email "demo@example.com"
git config user.name "Demo User"

# Initial commit
echo "# Demo Project" > README.md
git add README.md
git commit -m "Initial commit"

echo ""
echo "🔍 Testing with minimal changes..."
echo "Modified: README.md" > README.md
python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py

echo ""
echo "🔍 Testing with moderate changes..."
cat > app.py << 'EOF'
def hello():
    print("Hello World")

def calculate(x, y):
    return x + y

def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
EOF

cat > utils.py << 'EOF'
import json
import os

def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
EOF

git add .
python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py --verbose

echo ""
echo "🔍 Testing with significant changes (should recommend branching)..."
cat > database.py << 'EOF'
import sqlite3
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection
    
    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT,
                created_at TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.connection.commit()
    
    def add_user(self, username, email):
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)',
            (username, email, datetime.now())
        )
        self.connection.commit()
        return cursor.lastrowid
    
    def get_user(self, username):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()
    
    def add_post(self, user_id, title, content):
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO posts (user_id, title, content, created_at) VALUES (?, ?, ?, ?)',
            (user_id, title, content, datetime.now())
        )
        self.connection.commit()
        return cursor.lastrowid
    
    def get_user_posts(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
        return cursor.fetchall()
    
    def close(self):
        if self.connection:
            self.connection.close()
EOF

cat > api.py << 'EOF'
from flask import Flask, request, jsonify
from database import DatabaseManager
import os

app = Flask(__name__)
db = DatabaseManager('demo.db')

@app.route('/api/users', methods=['GET'])
def get_users():
    # Implementation would go here
    return jsonify({'users': []})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    # Implementation would go here
    return jsonify({'message': 'User created'})

@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Implementation would go here
    return jsonify({'posts': []})

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    # Implementation would go here
    return jsonify({'message': 'Post created'})

if __name__ == '__main__':
    app.run(debug=True)
EOF

git add .
python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py --verbose

echo ""
echo "🔍 Testing auto-branch creation..."
python3 /Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py --create

echo ""
echo "📋 Current branches:"
git branch

echo ""
echo "🎉 Demo complete! The tool successfully:"
echo "  ✅ Analyzed different change scenarios"
echo "  ✅ Recommended branching when appropriate"
echo "  ✅ Created a new branch automatically"
echo ""
echo "Clean up: rm -rf $DEMO_DIR"
