# TrustHire AI - Complete Installation Guide

## Prerequisites

Before starting, ensure you have:
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- PostgreSQL 15 or higher
- Git

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Trust-hire-app
```

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Setup Environment Variables

```bash
# Copy example .env and update it
cp .env .env.local
```

Edit `.env.local` and configure:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/trusthire_db
SECRET_KEY=your-super-secret-key-generate-with-openssl-rand-hex-32
```

### 2.5 Initialize Database

Ensure PostgreSQL is running, then:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE trusthire_db;

# Exit psql
\q
```

### 2.6 Verify Backend Setup

```bash
# Run the backend server
uvicorn app.main:app --reload

# The API will be available at: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

Keep this terminal open.

## Step 3: Frontend Setup

### 3.1 Open New Terminal and Navigate to Frontend

```bash
cd frontend
```

### 3.2 Install Dependencies

```bash
npm install
# or
yarn install
```

### 3.3 Setup Environment Variables

```bash
# Create .env.local file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env.local
```

### 3.4 Start Development Server

```bash
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:5173`

## Step 4: Test the Application

### 4.1 Test Backend API

```bash
# Using curl
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy"}
```

### 4.2 Test Frontend

Open your browser and go to:
```
http://localhost:5173
```

You should see the TrustHire AI login page.

### 4.3 Register a Test User

1. Click "Register" on the login page
2. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: testpass123
   - Confirm Password: testpass123
3. Click Register

### 4.4 Login

1. Click Login (or navigate to login page)
2. Enter:
   - Email: test@example.com
   - Password: testpass123
3. Click Login

You should now see the Dashboard.

## Step 5: Docker Setup (Optional)

If you prefer using Docker:

```bash
# Make sure Docker and Docker Compose are installed

# Run all services
docker-compose up

# Services will be available at:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8000
# - PostgreSQL: localhost:5432
```

To stop:
```bash
docker-compose down
```

## Troubleshooting

### Backend Won't Start

```bash
# Check if port 8000 is in use
# Windows
netstat -ano | findstr :8000
# Linux/Mac
lsof -i :8000

# Kill the process if needed
# Windows
taskkill /PID <PID> /F
# Linux/Mac
kill -9 <PID>

# Try starting again
uvicorn app.main:app --reload
```

### Database Connection Error

```bash
# Verify PostgreSQL is running
# Windows
pg_isready -h localhost

# Check DATABASE_URL in .env.local
# Should be: postgresql://user:password@localhost:5432/trusthire_db
```

### Module Not Found Error

```bash
# Ensure virtual environment is activated
# Windows
venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Won't Load

```bash
# Ensure you're in frontend directory
cd frontend

# Clear node_modules and reinstall
rm -rf node_modules
npm install

# Start dev server
npm run dev
```

### CORS Error

```bash
# In backend/.env, update CORS_ORIGINS:
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Restart backend server
```

## Next Steps

1. Review the [README.md](README.md) for project overview
2. Check [API_DOCS.md](API_DOCS.md) for API documentation
3. Read [DEVELOPMENT.md](DEVELOPMENT.md) for development workflow
4. Explore [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment

## Project Structure

```
Trust-hire-app/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── docker-compose.yml
├── README.md
├── SETUP.md
├── INSTALLATION.md   # This file
├── DEVELOPMENT.md
├── DEPLOYMENT.md
└── API_DOCS.md
```

## Getting Help

- Check the individual README files in backend/ and frontend/
- Review API documentation in API_DOCS.md
- See troubleshooting section above

## Next Phase Development

Once the basic setup is working, proceed with:
- Phase 1 (Backend): ✓ Completed
- Phase 2 (Frontend): ✓ Completed  
- Phase 3 (AI Integration): Add Gemini/OpenAI integration
- Phase 4 (Company Intelligence): Add scraping and analysis
- Phase 5 (Advanced Features): Add OCR, charts, analytics
