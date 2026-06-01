from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {"connect_timeout": 5}
)

# Create engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Dependency for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database tables
    """
    from app.models import company_model, feature_model, job_model, report_model, uploaded_file_model, user_model  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _apply_lightweight_migrations()


def _apply_lightweight_migrations():
    inspector = inspect(engine)
    table_columns = {
        table: {column["name"] for column in inspector.get_columns(table)}
        for table in inspector.get_table_names()
    }
    migrations = {
        "jobs": {
            "source_type": "VARCHAR(50) DEFAULT 'text'",
            "extracted_text": "TEXT",
        },
        "analysis_reports": {
            "scam_probability": "FLOAT DEFAULT 0",
            "company_intelligence": "TEXT",
            "review_summary": "TEXT",
        },
    }

    with engine.begin() as connection:
        for table, columns in migrations.items():
            existing = table_columns.get(table, set())
            for column_name, column_type in columns.items():
                if column_name not in existing:
                    connection.execute(text(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}"))
