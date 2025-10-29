#!/usr/bin/env bash
# ==============================================
# ChatAr Installer — cross-platform setup script
# Works on Linux, macOS, and Windows (via Git Bash or WSL)
# ==============================================

set -e  # Exit on error

echo ""
echo "=============================================="
echo "🧠  ChatAr — Arabic AI Chat Installer"
echo "=============================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)     platform="Linux";;
    Darwin*)    platform="macOS";;
    MINGW*|MSYS*|CYGWIN*) platform="Windows";;
    *)          platform="Unknown";;
esac

echo "Detected OS: $platform"
echo ""

# Step 1: Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 not found."
    if [ "$platform" = "Linux" ]; then
        echo "🟡 Installing Python3 using apt..."
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip
    elif [ "$platform" = "macOS" ]; then
        echo "🟡 Installing Python3 using Homebrew..."
        if ! command -v brew &>/dev/null; then
            echo "❌ Homebrew not found. Please install it manually: https://brew.sh"
            exit 1
        fi
        brew install python3
    else
        echo "⚠️  On Windows, please install Python 3.10+ from https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "✅ Python3 is installed."
fi

# Step 2: Create virtual environment
echo ""
echo "📁 Creating virtual environment..."
python3 -m venv .venv

# Step 3: Activate environment
echo ""
if [ "$platform" = "Windows" ]; then
    ACTIVATE_CMD=".venv/Scripts/activate"
else
    ACTIVATE_CMD="source .venv/bin/activate"
fi

echo "➡️  To activate the virtual environment, run:"
echo "   $ACTIVATE_CMD"
echo ""

# Step 4: Install dependencies
echo "📦 Installing dependencies..."
if [ "$platform" = "Windows" ]; then
    .venv/Scripts/pip install --upgrade pip
    .venv/Scripts/pip install -r requirements.txt
else
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Step 5: Setup .env file
echo ""
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp example_env/.env_example .env
    echo "✅ .env created. Please edit it and add your OpenAI API key."
else
    echo "✅ .env already exists."
fi

# Step 6: Done
echo ""
echo "✅ Installation completed successfully!"
echo "🚀 To start ChatAr, run:"
echo ""
if [ "$platform" = "Windows" ]; then
    echo "   .venv\\Scripts\\activate"
else
    echo "   source .venv/bin/activate"
fi
echo "   streamlit run app.py"
echo ""
echo "=============================================="
echo "🎉 ChatAr is ready!"
echo "=============================================="
