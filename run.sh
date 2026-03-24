#!/bin/bash

echo "🚀 Starting VitalSync Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for Firebase credentials
if [ ! -f "serviceAccountKey.json" ]; then
    echo "⚠️  Warning: serviceAccountKey.json not found!"
    echo "Please add your Firebase service account key before running."
    exit 1
fi

# Start server
echo ""
echo "✅ Starting server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
