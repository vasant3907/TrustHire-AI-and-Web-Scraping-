# TrustHire Backend

FastAPI + SQLAlchemy + PostgreSQL. The backend reads `DATABASE_URL` from `backend/.env`.

## Setup

### 1. Virtual Environment

```bash
py -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` file:

```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/trusthire_db
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
```

Tables are created automatically at startup for local development.

### 5. Run Server

```bash
python -m uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`

## Project Structure

- `app/core/` - Configuration, database, security
- `app/models/` - SQLAlchemy models
- `app/schemas/` - Pydantic schemas
- `app/routes/` - API endpoints
- `app/services/` - Business logic
- `app/repositories/` - Database access layer
- `app/utils/` - Utilities and helpers
