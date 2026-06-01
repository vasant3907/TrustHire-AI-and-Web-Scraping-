from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings

def add_cors_middleware(app):
    """Add CORS middleware to app"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
