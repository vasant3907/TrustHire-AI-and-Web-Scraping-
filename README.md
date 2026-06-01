# TrustHire AI - Complete Project Structure

Industry-style, beginner-manageable, and scalable project setup.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Tailwind CSS |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT |
| AI | Gemini/OpenAI |
| OCR | Tesseract/EasyOCR |
| Scraping | BeautifulSoup + Playwright |
| Deployment | Vercel + Render |

## Project Architecture

```
React Frontend
      ↓
FastAPI Backend
      ↓
Service Layer
      ↓
AI + Scraping + OCR
      ↓
PostgreSQL Database
```

## Folder Structure

```
Trust-hire-app/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── middleware/
│   │   ├── dependencies/
│   │   └── utils/
│   ├── requirements.txt
│   ├── .env
│   ├── Dockerfile
│   └── README.md
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   ├── components/
    │   ├── context/
    │   ├── services/
    │   ├── routes/
    │   ├── api/
    │   ├── layouts/
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── README.md
```

## Phase-Wise Development

### Phase 1: Backend Foundation ✓
- FastAPI setup
- PostgreSQL connection
- JWT authentication
- User system
- Basic models and schemas

### Phase 2: Frontend Setup (Next)
- React app with Vite
- Login/Signup UI
- Dashboard layout
- Upload form

### Phase 3: AI Integration
- JD analysis using Gemini/OpenAI
- Trust score calculation
- Scam detection

### Phase 4: Company Intelligence
- Company scraping
- Review analysis
- Domain verification

### Phase 5: Advanced Features
- OCR for screenshots
- Email verification
- Analytics and charts

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Database Tables

### users
- id, name, email, password, created_at

### companies
- id, company_name, website, linkedin_url, trust_score, created_at

### jobs
- id, title, description, company_id, uploaded_by, risk_level, created_at

### analysis_reports
- id, job_id, ai_summary, trust_score, risk_level, recommendation, created_at

## API Endpoints

### Auth
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user

### Jobs
- `POST /api/jobs` - Create job
- `GET /api/jobs/{job_id}` - Get job
- `GET /api/jobs/my-jobs` - Get user's jobs

### Companies
- `GET /api/companies/{company_id}` - Get company
- `GET /api/companies/search/{name}` - Search company

### Reports
- `GET /api/reports/{report_id}` - Get report
- `POST /api/reports/analyze/{job_id}` - Analyze job

## Next Steps

1. Start PostgreSQL and create the database configured in `backend/.env`.
2. Start the backend server.
3. Install frontend dependencies and start the dev server.
