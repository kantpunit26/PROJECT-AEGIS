import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings

router = APIRouter()
START_TIME = time.time()

@router.get("/health", summary="System Health & Diagnostic Status")
def health_check(db: Session = Depends(get_db)):
    """Verifies API server, database connectivity, and backend engine status."""
    db_status = "unhealthy"
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    uptime_seconds = round(time.time() - START_TIME, 1)

    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "uptime_seconds": uptime_seconds,
        "primary_organism": "Klebsiella pneumoniae"
    }

