#!/bin/bash
# Enhanced Git Vibe Brancher Demo Launcher

echo "🌿 Enhanced Git Vibe Brancher - Auto-Commit Demo"
echo "================================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if the vibe brancher script exists
VIBE_BRANCHER_PATH="$SCRIPT_DIR/vibe_brancher.py"
if [ ! -f "$VIBE_BRANCHER_PATH" ]; then
    echo "❌ Vibe Brancher script not found at: $VIBE_BRANCHER_PATH"
    echo "Please ensure the script is in the correct location."
    exit 1
fi

# Check if the enhanced demo script exists
ENHANCED_DEMO_PATH="$SCRIPT_DIR/enhanced_demo.py"
if [ ! -f "$ENHANCED_DEMO_PATH" ]; then
    echo "❌ Enhanced demo script not found at: $ENHANCED_DEMO_PATH"
    echo "Please ensure the script is in the correct location."
    exit 1
fi

echo "✅ All requirements met!"
echo ""
echo "This enhanced demo will showcase:"
echo "• Intelligent auto-commit with smart message generation"
echo "• Interactive commit mode with file preview"
echo "• Vibe coding workflow combining analysis and auto-commit"
echo "• Real-world scenarios with your PoorlyWrittenService repository"
echo "• Branch suggestions integrated with auto-commit"
echo "• Git aliases for seamless integration"
echo ""

read -p "🚀 Ready to start the enhanced demo? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎬 Starting enhanced demo..."
    echo ""
    python3 "$ENHANCED_DEMO_PATH"
else
    echo "Demo cancelled. Run this script again when you're ready!"
fi
