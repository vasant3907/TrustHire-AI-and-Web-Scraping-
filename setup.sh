#!/bin/bash
# Quick start script for Linux/Mac

echo "🚀 TrustHire AI - Quick Start Setup"
echo "===================================="

# Check Python version
echo "Checking Python..."
python3 --version

# Check Node version
echo "Checking Node..."
node --version

# Create backend virtual environment
echo ""
echo "Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.local .env 2>/dev/null || echo "Please copy .env file manually"
echo "✓ Backend setup complete"

# Return to root
cd ..

# Setup frontend
echo ""
echo "Setting up Frontend..."
cd frontend
npm install
echo "✓ Frontend setup complete"

# Return to root
cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
