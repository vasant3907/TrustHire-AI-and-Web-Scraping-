# TrustHire AI - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser (Client)                     │
│                  (React + Tailwind CSS)                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                    HTTP/REST API (JSON)
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   FastAPI Web Server                        │
│                    (Uvicorn ASGI)                           │
├─────────────────────────────────────────────────────────────┤
│  Routes Layer (API Endpoints)                               │
│  - Authentication Routes                                    │
│  - Job Routes                                               │
│  - Company Routes                                           │
│  - Report Routes                                            │
├─────────────────────────────────────────────────────────────┤
│  Middleware & Dependencies                                  │
│  - JWT Authentication                                       │
│  - CORS                                                     │
│  - Request Validation                                       │
├─────────────────────────────────────────────────────────────┤
│  Service Layer (Business Logic)                             │
│  - AIService (Gemini/OpenAI integration)                    │
│  - TrustScoreService                                        │
│  - ScrapingService (BeautifulSoup/Playwright)              │
│  - OCRService (Tesseract/EasyOCR)                          │
├─────────────────────────────────────────────────────────────┤
│  Repository Layer (Data Access)                             │
│  - UserRepository                                           │
│  - JobRepository                                            │
│  - ReportRepository                                         │
├─────────────────────────────────────────────────────────────┤
│  ORM & Database                                             │
│  - SQLAlchemy ORM                                           │
│  - Connection Pooling                                       │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              PostgreSQL Database                            │
│  Tables:                                                    │
│  - users, companies, jobs, analysis_reports                │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow - Job Analysis

```
User Uploads Job
      │
      ▼
Validate & Store Job
      │
      ▼
Extract Text (OCR if needed)
      │
      ▼
Company Lookup/Scraping
      ▼
      ├─► Search Company in Database
      ├─► If not found: Scrape LinkedIn/Web
      └─► Store Company Data
      │
      ▼
AI Analysis
      ├─► Check Suspicious Keywords
      ├─► Validate Salary
      ├─► Verify Email Domain
      ├─► Analyze Description
      └─► Generate Report
      │
      ▼
Calculate Trust Score
      ├─► Company Presence Score
      ├─► Email Validity
      ├─► Salary Validity
      └─► Keyword Risk Score
      │
      ▼
Store Analysis Report
      │
      ▼
Return to User
```

## Authentication Flow

```
User Login
      │
      ▼
Verify Credentials
      │
      ▼
Generate JWT Token
      │
      ▼
Return Token to Frontend
      │
      ▼
Store in localStorage
      │
      ▼
Include in API Requests
      │
      ▼
Backend Validates Token
      │
      ▼
Return Protected Resource
```

## Component Interaction

### Frontend Components

```
App
├── AuthContext (Global State)
│
├── Login/Register Pages
│   └── Connect to Auth API
│
├── Dashboard
│   ├── Shows Recent Jobs
│   ├── Displays Trust Scores
│   └── Links to Detailed Reports
│
├── AnalyzeJob Page
│   ├── Text Input
│   ├── File Upload
│   └── URL Input
│
└── Protected Routes
    └── Wraps Dashboard, Analyze, Reports, Profile
```

### Backend Modules

```
Main App
├── Database Connection
├── CORS Middleware
│
├── Auth Routes → Auth Service → User Repository
├── Job Routes → Job Service → Job Repository
├── Company Routes → Company Service → Company Repository
├── Report Routes → Report Service → AI/Scraping Services
│
└── Services
    ├── AI Service (Language Model Integration)
    ├── Scraping Service (Web Data Collection)
    ├── OCR Service (Image Text Extraction)
    └── Trust Score Service (Risk Calculation)
```

## Database Schema

```
users
├── id (PK)
├── name
├── email (UK)
├── password (hashed)
├── is_active
├── created_at
└── updated_at

companies
├── id (PK)
├── company_name
├── website
├── linkedin_url
├── trust_score
├── created_at
└── updated_at

jobs
├── id (PK)
├── title
├── description
├── company_id (FK)
├── uploaded_by (FK → users.id)
├── risk_level
├── created_at
└── updated_at

analysis_reports
├── id (PK)
├── job_id (FK)
├── ai_summary
├── trust_score
├── risk_level
├── recommendation
├── suspicious_keywords
├── company_presence_score
├── salary_validity
├── email_validity
├── created_at
└── updated_at
```

## Security Architecture

```
Frontend
├── Token Storage (localStorage)
├── Auth Guard (Protected Routes)
└── HTTPS in Production

API Layer
├── CORS Validation
├── Request Validation
├── Rate Limiting (optional)
└── Request Logging

Database Layer
├── SQL Injection Prevention (Parameterized Queries)
├── Access Control (User Isolation)
├── Connection Encryption (SSL)
└── Backup & Recovery

Secret Management
├── Environment Variables
├── No Secrets in Code
└── Secrets Manager (AWS/Azure in Production)
```

## Scalability Considerations

### Horizontal Scaling

```
Load Balancer (Nginx/HAProxy)
├── Backend Instance 1
├── Backend Instance 2
└── Backend Instance N

All pointing to:
├── Shared PostgreSQL (Managed Service)
└── Shared Cache (Redis)
```

### Performance Optimization

```
1. Database
   ├── Indexes on frequently queried columns
   ├── Connection pooling
   └── Query optimization

2. Caching
   ├── Redis for session data
   ├── Browser cache for static assets
   └── API response caching

3. Frontend
   ├── Code splitting
   ├── Lazy loading
   └── CDN for static files

4. Backend
   ├── Async operations
   ├── Background job processing (Celery)
   └── API rate limiting
```

## Deployment Architecture

### Local Development
```
Laptop
├── Backend (Uvicorn on :8000)
├── Frontend (Vite dev server on :5173)
└── PostgreSQL (Docker or Local)
```

### Production (Cloud)
```
Internet
    │
    ▼
CDN (Vercel Edge)
    │
    ├─► Frontend (Vercel)
    │
    └─► API Gateway (Render/Railway)
        │
        ▼
    Backend (Container)
        │
        ▼
    Managed Database (Render/AWS RDS)
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Client | React 18 | UI Framework |
| Styling | Tailwind CSS | Utility-first CSS |
| Bundler | Vite | Fast build tool |
| Server | FastAPI | Web Framework |
| ASGI | Uvicorn | Server |
| ORM | SQLAlchemy | Database abstraction |
| Database | PostgreSQL | Data persistence |
| Auth | JWT + bcrypt | Authentication |
| AI | Gemini/OpenAI | Text analysis |
| Scraping | BeautifulSoup/Playwright | Web scraping |
| OCR | Tesseract/EasyOCR | Image text extraction |
| Deployment | Vercel/Render | Hosting |
| Containerization | Docker | Container runtime |

## Development Pipeline

```
1. Plan
   ├── Define Requirements
   ├── Design Database
   └── Design API

2. Develop
   ├── Backend Implementation
   ├── Frontend Implementation
   └── Integration

3. Test
   ├── Unit Tests
   ├── Integration Tests
   └── E2E Tests

4. Deploy
   ├── Staging
   ├── Production
   └── Monitoring

5. Maintain
   ├── Bug Fixes
   ├── Feature Enhancements
   └── Performance Optimization
```
