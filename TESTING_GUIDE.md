# TrustHire AI - Testing & Verification Guide

## Pre-Verification Checklist

Before testing, ensure:
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 15+ available (local or Docker)
- [ ] Git installed
- [ ] 4GB+ RAM available
- [ ] Port 8000, 5173, 5432 available

## Backend Verification

### Step 1: Environment Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Verify Python version
python --version  # Should be 3.11+

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected: All packages install without errors

### Step 3: Database Check

```bash
# Make sure PostgreSQL is running
# Windows
pg_isready -h localhost

# Linux/Mac
psql -U postgres -c "SELECT 1;"
```

Expected: Connection successful

### Step 4: Environment Configuration

```bash
# Copy .env file (already created)
# Verify it contains:
# - DATABASE_URL
# - SECRET_KEY
# - CORS_ORIGINS
```

### Step 5: Start Backend

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 6: Test Backend

#### API Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

#### API Docs
```bash
# Visit in browser:
http://localhost:8000/docs
# Should see Swagger UI with all endpoints
```

#### Test Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Expected: 200 OK with user data
```

#### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Expected: 200 OK with access_token
```

### Backend Test Results

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| Python version | 3.11+ | | ☐ |
| Dependencies | Install OK | | ☐ |
| Database | Connected | | ☐ |
| Health check | 200 OK | | ☐ |
| Swagger UI | Loads | | ☐ |
| Register | 200 OK | | ☐ |
| Login | Token received | | ☐ |

## Frontend Verification

### Step 1: Environment Setup

```bash
cd frontend

# Verify Node version
node --version  # Should be 18+
npm --version   # Should be 9+
```

### Step 2: Install Dependencies

```bash
npm install
```

Expected: All packages install without errors

### Step 3: Environment Configuration

```bash
# File .env.local should exist with:
cat .env.local
# Should show: REACT_APP_API_URL=http://localhost:8000/api
```

### Step 4: Start Development Server

```bash
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

### Step 5: Test Frontend in Browser

#### Check Page Loads
1. Open `http://localhost:5173`
2. Should see TrustHire AI login page
3. Check browser console (F12) for errors

#### Test Navigation
- [ ] Click "Register" - Should go to register page
- [ ] Click back to "Login" - Should return to login
- [ ] Form fields should be visible and interactive

#### Test Registration Flow
1. Click "Register"
2. Fill form:
   - Name: Test User
   - Email: test@user.com
   - Password: testpass123
   - Confirm: testpass123
3. Click "Register"
4. Expected: Success message and redirect to login

#### Test Login Flow
1. Should be on login page
2. Fill form:
   - Email: test@user.com
   - Password: testpass123
3. Click "Login"
4. Expected: Redirect to dashboard

#### Test Dashboard
1. Should see "Dashboard" page
2. Should display:
   - "No jobs analyzed yet" or job list
   - Button to "Analyze Your First Job"

#### Test Analyze Job
1. Click "Analyze Your First Job"
2. Should see form with:
   - Company Name field
   - Job Description textarea
   - Analyze Job button
3. Can enter test data and click analyze

#### Test Profile
1. Click "Profile" in navbar
2. Should display:
   - User name
   - User email
   - Logout button

### Frontend Test Results

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| Node version | 18+ | | ☐ |
| npm install | Success | | ☐ |
| Dev server starts | 5173 | | ☐ |
| Login page | Loads | | ☐ |
| Register page | Accessible | | ☐ |
| Registration | Success | | ☐ |
| Login | Redirect to dashboard | | ☐ |
| Dashboard | Loads | | ☐ |
| Navigation | Works | | ☐ |
| Profile | Shows user data | | ☐ |

## Integration Testing

### Test 1: Complete Registration to Dashboard Flow

```bash
# 1. Backend running on :8000
# 2. Frontend running on :5173

Steps:
1. Open http://localhost:5173
2. Click "Register"
3. Fill: Name="John", Email="john@test.com", Password="pass123"
4. Click Register
5. Should redirect to login
6. Fill: Email="john@test.com", Password="pass123"
7. Click Login
8. Should redirect to dashboard
9. Should show no jobs
10. Click "Analyze Your First Job"
11. Fill form and click analyze
12. Check console for API calls (no errors expected yet)
```

Expected: All steps complete without errors

### Test 2: JWT Token Validation

```bash
# After login, check localStorage
1. Open browser DevTools (F12)
2. Go to Application tab
3. Check localStorage
4. Should see: access_token, user

Steps to verify token works:
1. Open Network tab
2. Go to Dashboard
3. Check requests
4. Should see Authorization header with Bearer token
```

Expected: Token present and sent with requests

### Test 3: Protected Routes

```bash
# Test unauthenticated access
1. Open new private/incognito window
2. Try to access: http://localhost:5173/dashboard
3. Should redirect to login

# After logout
1. Click logout in profile
2. Try to access dashboard
3. Should redirect to login
```

Expected: Unauthorized access redirects to login

## Docker Verification

### Test Docker Setup

```bash
# Start all services
docker-compose up

# Expected output:
# postgres: ready on port 5432
# backend: running on port 8000
# frontend: running on port 5173
```

### Test Services

```bash
# Check containers are running
docker-compose ps

# Expected: 3 services running (postgres, backend, frontend)

# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:5173

# View logs
docker-compose logs -f backend
```

Expected: All services healthy and responsive

## Performance Testing

### Backend Response Times

```bash
# Time a login request
time curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Expected: < 500ms
```

### Frontend Load Times

```bash
# Using browser DevTools (F12) → Network tab
1. Open http://localhost:5173
2. Check load time
3. Expected: < 2 seconds for full page load
```

## Error Handling Tests

### Test 1: Invalid Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"wrong@email.com","password":"wrongpass"}'

Expected: 401 Unauthorized with error message
```

### Test 2: Invalid Token

```bash
curl -X GET http://localhost:8000/api/jobs/my-jobs \
  -H "Authorization: Bearer invalid-token"

Expected: 401 Unauthorized
```

### Test 3: CORS Error

```bash
# If frontend requests wrong backend URL, should error
# Check browser console for CORS errors
```

## Security Tests

### Test 1: Password Security

```bash
# Password should be hashed in database
# Check backend logs, password should never be printed
```

### Test 2: JWT Expiration

```bash
# JWT tokens expire after 30 minutes
# After expiration, requests should fail with 401
```

### Test 3: CORS Configuration

```bash
# Should only allow requests from http://localhost:5173
# Requests from other origins should fail (CORS error)
```

## Final Verification Checklist

### Backend
- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] PostgreSQL database accessible
- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] Swagger UI loads
- [ ] Registration works
- [ ] Login works and returns token
- [ ] Protected endpoints require token

### Frontend
- [ ] Node 18+ and npm installed
- [ ] Dependencies installed
- [ ] Dev server starts on 5173
- [ ] Login page loads
- [ ] Register page accessible
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Dashboard loads after login
- [ ] Navigation works
- [ ] Profile page shows user info
- [ ] Logout works
- [ ] No console errors

### Integration
- [ ] Backend and frontend communicate
- [ ] Tokens passed correctly
- [ ] Protected routes work
- [ ] CORS configured correctly
- [ ] Error handling works

### Docker
- [ ] docker-compose up starts all services
- [ ] All 3 containers running
- [ ] All services accessible
- [ ] No errors in logs

## Troubleshooting

If tests fail, check:

1. **Backend won't start**
   ```bash
   # Check if port 8000 in use
   netstat -ano | findstr :8000
   ```

2. **Database connection error**
   ```bash
   # Verify PostgreSQL running
   psql -U postgres -c "SELECT 1"
   ```

3. **Frontend won't start**
   ```bash
   # Clear node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **CORS error**
   ```bash
   # Check .env CORS_ORIGINS setting
   # Should include http://localhost:5173
   ```

5. **API requests failing**
   ```bash
   # Check Network tab in DevTools
   # Verify auth token present in requests
   ```

## Success Criteria

✅ Project is successfully set up when:
1. Backend API is running and responsive
2. Frontend loads without errors
3. User can register and login
4. Dashboard displays after login
5. Protected routes are protected
6. No console errors
7. All services work with Docker

Congratulations if you pass all tests! Your TrustHire AI project is ready for Phase 3 (AI Integration).
