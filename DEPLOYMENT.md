# TrustHire AI Deployment Guide

## Prerequisites

- Docker & Docker Compose (recommended)
- Node.js 18+ (for local frontend)
- Python 3.11+ (for local backend)
- PostgreSQL 15+ (if not using Docker)

## Local Development Setup

### Option 1: Docker Compose (Recommended)

```bash
# Clone or navigate to project
cd Trust-hire-app

# Copy examples and add your real secrets
copy .env.example .env
copy backend\.env.example backend\.env

# Start all services
docker compose up --build

# Services will be available at:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8001
# - Database: localhost:5432

# To stop
docker compose down
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and configure
cp .env .env.local
# Update DATABASE_URL and other settings

# Run migrations (when setup)
# alembic upgrade head

# Start server
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local if needed
echo VITE_API_URL=http://127.0.0.1:8001/api > .env.local

# Start development server
npm run dev
```

## Database Setup

### Using Docker
Database automatically initializes with docker-compose.

### Manual PostgreSQL Setup

```bash
# Create database
createdb trusthire_db

# Connect and initialize (when migrations ready)
psql -d trusthire_db -f migrations/init.sql
```

## Environment Configuration

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/trusthire_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
ADMIN_EMAILS=admin@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=TrustHire AI
SMTP_USE_TLS=true
SMTP_USE_SSL=false
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```
VITE_API_URL=http://127.0.0.1:8001/api
```

## Docker Production-Like Deployment

This repository now includes:

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`
- `docker-compose.yml`

Run:

```bash
docker compose up --build -d
```

Open:

- Frontend: http://localhost:5173
- Backend health: http://localhost:8001/health
- API docs: http://localhost:8001/docs

Stop:

```bash
docker compose down
```

Reset database volume:

```bash
docker compose down -v
```

## Cloud Deployment

### Backend - Render.com

1. Create account on Render.com
2. Connect GitHub repository
3. Create new Web Service
4. Configure:
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from .env
6. Create PostgreSQL database on Render
7. Deploy

### Frontend - Vercel

1. Create account on Vercel
2. Import GitHub repository
3. Configure:
   - Framework Preset: Vite
   - Build command: `npm run build`
   - Output directory: `dist`
4. Add environment variables:
   - `VITE_API_URL=https://your-backend-url.onrender.com/api`
5. Deploy

### Using Docker Hub & Container Registry

```bash
# Build backend image
cd backend
docker build -t your-username/trusthire-backend:latest .
docker push your-username/trusthire-backend:latest

# Deploy using docker-compose or container service
```

## Testing

### Backend API Testing

```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Access Swagger UI
# http://localhost:8000/docs

# Access ReDoc
# http://localhost:8000/redoc
```

### Frontend Testing

```bash
npm run build
npm run preview
```

## Monitoring & Logs

### Docker Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Backend Logs
- Check `logs/` directory
- Enable DEBUG logging by setting `LOG_LEVEL=DEBUG` in .env

## Scaling Considerations

1. Database: Use managed PostgreSQL (RDS, Render, etc.)
2. Backend: Scale horizontally with load balancer
3. Frontend: Use CDN for static assets
4. Caching: Add Redis for session/cache layer
5. Job Queue: Use Celery for async tasks

## Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Test connection
psql -U postgres -d trusthire_db -c "SELECT 1"
```

### CORS Issues
- Update `CORS_ORIGINS` in backend .env
- Ensure frontend URL matches allowed origins

### Port Already in Use
```bash
# Find process using port
# Windows
netstat -ano | findstr :8000
# Linux/Mac
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Dependencies Issues
```bash
# Clear cache and reinstall
# Backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Frontend
rm -rf node_modules
npm install
```
