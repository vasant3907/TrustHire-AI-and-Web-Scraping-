# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}

Response: 200 OK
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user_id": 1
}
```

### Jobs

#### Create Job
```
POST /jobs
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Developer",
  "description": "Full job description...",
  "company_id": null
}

Response: 200 OK
{
  "id": 1,
  "title": "Senior Developer",
  "description": "Full job description...",
  "company_id": null,
  "risk_level": "unknown",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Get My Jobs
```
GET /jobs/my-jobs
Authorization: Bearer <token>

Response: 200 OK
[
  {
    "id": 1,
    "title": "Senior Developer",
    ...
  }
]
```

#### Get Job by ID
```
GET /jobs/{job_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "id": 1,
  ...
}
```

### Reports

#### Analyze Job
```
POST /reports/analyze/{job_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "message": "Analysis started"
}
```

#### Get Report
```
GET /reports/{report_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "id": 1,
  "job_id": 1,
  "ai_summary": "...",
  "trust_score": 75.0,
  "risk_level": "medium",
  "recommendation": "...",
  ...
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Job not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
