#!/bin/bash
# Git Vibe Brancher - Immersive Demo Launcher

echo "🌿 Git Vibe Brancher - Immersive Demo"
echo "====================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if the vibe brancher script exists
VIBE_BRANCHER_PATH="/Users/dilipkunderu/git-vibe-brancher/vibe_brancher.py"
if [ ! -f "$VIBE_BRANCHER_PATH" ]; then
    echo "❌ Vibe Brancher script not found at: $VIBE_BRANCHER_PATH"
    echo "Please ensure the script is in the correct location."
    exit 1
fi

# Check if the immersive demo script exists
IMMERSIVE_DEMO_PATH="/Users/dilipkunderu/git-vibe-brancher/immersive_demo.py"
if [ ! -f "$IMMERSIVE_DEMO_PATH" ]; then
    echo "❌ Immersive demo script not found at: $IMMERSIVE_DEMO_PATH"
    echo "Please ensure the script is in the correct location."
    exit 1
fi

echo "✅ All requirements met!"
echo ""
echo "This immersive demo will:"
echo "• Create a temporary demo repository"
echo "• Show 6 different coding scenarios"
echo "• Demonstrate all features of Git Vibe Brancher"
echo "• Take approximately 5-10 minutes to complete"
echo ""

read -p "🚀 Ready to start the immersive demo? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎬 Starting immersive demo..."
    echo ""
    python3 "$IMMERSIVE_DEMO_PATH"
else
    echo "Demo cancelled. Run this script again when you're ready!"
fi
