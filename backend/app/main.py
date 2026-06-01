from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.database import init_db
from app.middleware.auth_middleware import add_cors_middleware
from app.routes import admin_routes, auth_routes, company_routes, feature_routes, job_routes, report_routes

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Add CORS middleware
app = add_cors_middleware(app)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    logger.info("Database initialized")

# Include routes
app.include_router(auth_routes.router)
app.include_router(job_routes.router)
app.include_router(company_routes.router)
app.include_router(report_routes.router)
app.include_router(feature_routes.router)
app.include_router(admin_routes.router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "TrustHire AI API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
