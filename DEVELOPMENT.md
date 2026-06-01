# Development Workflow

## Directory Structure Overview

```
Trust-hire-app/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── core/           # Configuration, DB, Security
│   │   ├── models/         # SQLAlchemy Models
│   │   ├── schemas/        # Pydantic Schemas
│   │   ├── routes/         # API Endpoints
│   │   ├── services/       # Business Logic
│   │   ├── repositories/   # Data Access Layer
│   │   ├── middleware/     # CORS, Auth Middleware
│   │   ├── dependencies/   # Dependency Injection
│   │   └── utils/          # Helpers, Validators
│   ├── requirements.txt
│   ├── .env
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── pages/          # Page Components
│   │   ├── components/     # Reusable Components
│   │   ├── context/        # React Context (Auth)
│   │   ├── services/       # API Services
│   │   ├── routes/         # Routing Config
│   │   ├── api/            # Axios Configuration
│   │   ├── layouts/        # Layout Components
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
│
├── docker-compose.yml       # Docker Orchestration
├── .gitignore
├── README.md               # Main Documentation
├── SETUP.md                # Setup Instructions
├── DEPLOYMENT.md           # Deployment Guide
├── API_DOCS.md            # API Documentation
└── DEVELOPMENT.md         # This file
```

## Backend Development

### Adding a New Feature

1. **Create Model** (if needed)
```python
# app/models/new_model.py
from sqlalchemy import Column, String, etc.
from app.core.database import Base

class NewModel(Base):
    __tablename__ = "new_models"
    # Define columns
```

2. **Create Schema**
```python
# app/schemas/new_schema.py
from pydantic import BaseModel

class NewModelCreate(BaseModel):
    # Define fields

class NewModelResponse(BaseModel):
    # Define response fields
```

3. **Create Repository** (Data Access)
```python
# app/repositories/new_repository.py
class NewModelRepository:
    def create(self, db, data):
        # Implementation
```

4. **Create Service** (Business Logic)
```python
# app/services/new_service.py
class NewService:
    def process(self, data):
        # Business logic
```

5. **Create Routes** (API Endpoints)
```python
# app/routes/new_routes.py
@router.post("/")
def create_new(data: NewModelCreate):
    # Implementation
```

6. **Include Router** in `app/main.py`
```python
from app.routes import new_routes
app.include_router(new_routes.router)
```

### Testing Backend Endpoints

```bash
# Using curl
curl -X GET http://localhost:8000/api/endpoint \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"

# Using HTTPie
http GET localhost:8000/api/endpoint Authorization:"Bearer <token>"

# Using Swagger UI
# Visit: http://localhost:8000/docs
```

## Frontend Development

### Adding a New Page

1. **Create Page Component**
```jsx
// src/pages/NewPage.jsx
import React from 'react';
import { Navbar } from '../components/Navbar';

export const NewPage = () => {
  return (
    <div>
      <Navbar />
      <div className="container mx-auto p-6">
        {/* Page content */}
      </div>
    </div>
  );
};
```

2. **Add Route**
```jsx
// src/routes/AppRoutes.jsx
<Route path="/new-page" element={<NewPage />} />
```

3. **Add Navigation**
```jsx
// src/components/Navbar.jsx
<a href="/new-page" className="hover:text-blue-200">New Page</a>
```

### Adding a New Component

```jsx
// src/components/NewComponent.jsx
import React from 'react';

export const NewComponent = ({ prop1, prop2 }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      {/* Component content */}
    </div>
  );
};

export default NewComponent;
```

### API Integration

```javascript
// src/services/apiService.js - Add new endpoint
newEndpoint: (data) =>
  axiosInstance.post('/new-endpoint', data),

// In component
const handleClick = async () => {
  try {
    const response = await apiService.newEndpoint(data);
    setResult(response.data);
  } catch (err) {
    console.error('Error:', err);
  }
};
```

## Styling with Tailwind CSS

### Common Patterns

```jsx
// Responsive Grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

// Buttons
<button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
  Click me
</button>

// Cards
<div className="bg-white p-6 rounded-lg shadow-md">

// Forms
<input className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-600" />

// Alerts
<div className="bg-green-100 border border-green-400 text-green-700 p-3 rounded">
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature

# Create Pull Request
```

## Code Standards

### Backend
- Use type hints
- Follow PEP 8
- Write docstrings
- Keep functions small and focused

### Frontend
- Use React hooks
- Keep components reusable
- Use meaningful variable names
- Add prop validation

## Performance Optimization

### Backend
- Use database indexes
- Implement caching (Redis)
- Use async/await for I/O operations
- Profile with Python profiler

### Frontend
- Code splitting with React.lazy()
- Optimize images
- Use memoization (React.memo, useMemo)
- Monitor bundle size

## Security Checklist

- [ ] Environment variables not in code
- [ ] JWT tokens validated
- [ ] Database queries parameterized
- [ ] CORS properly configured
- [ ] Input validation on both ends
- [ ] HTTPS in production
- [ ] Secrets management (AWS Secrets Manager, etc.)

## Common Commands

### Backend
```bash
# Run server
uvicorn app.main:app --reload

# Run tests (when added)
pytest

# Generate API docs
# Auto-generated at http://localhost:8000/docs
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

## Debugging

### Backend
```python
# Add debugging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")

# Use breakpoint
breakpoint()  # Python 3.7+
```

### Frontend
```javascript
// Console logging
console.log('Debug:', variable);

// Browser DevTools
// F12 or Ctrl+Shift+I
```

## Next Steps

1. Set up PostgreSQL locally
2. Run backend and test endpoints
3. Run frontend and test UI
4. Implement Phase 2 features
5. Add more comprehensive tests
6. Set up CI/CD pipeline
