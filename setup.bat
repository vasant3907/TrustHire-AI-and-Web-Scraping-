@echo off
REM Quick start script for Windows

echo.
echo 🚀 TrustHire AI - Quick Start Setup
echo ====================================

REM Check Python version
echo Checking Python...
python --version

REM Check Node version
echo Checking Node...
node --version

REM Create backend virtual environment
echo.
echo Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.local .env 2>nul || echo Please copy .env file manually
echo ✓ Backend setup complete

REM Return to root
cd ..

REM Setup frontend
echo.
echo Setting up Frontend...
cd frontend
call npm install
echo ✓ Frontend setup complete

REM Return to root
cd ..

echo.
echo ✅ Setup Complete!
echo.
echo To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\Activate.ps1
echo   uvicorn app.main:app --reload
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:5173 in your browser
echo.
pause
