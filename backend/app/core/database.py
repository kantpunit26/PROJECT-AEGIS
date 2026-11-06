import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from app.core.config import settings

# Determine Database Connection URL
if settings.USE_SQLITE_FALLBACK and (not settings.POSTGRES_SERVER or settings.POSTGRES_SERVER in ("localhost", "127.0.0.1")):
    # Ensure SQLite directory exists
    os.makedirs(os.path.dirname(os.path.abspath(settings.SQLITE_DB_PATH)), exist_ok=True)
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.abspath(settings.SQLITE_DB_PATH)}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

def get_db():
    """FastAPI dependency for yielding database session with automatic commit/rollback and closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
