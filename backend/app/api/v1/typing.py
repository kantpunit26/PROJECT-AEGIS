from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.typing_service import typing_service

router = APIRouter()

@router.get("/mlst-distribution", summary="MLST Sequence Type Distribution")
def get_mlst_distribution(organism: Optional[str] = None, db: Session = Depends(get_db)):
    return typing_service.get_mlst_distribution(db, organism=organism)

@router.get("/kleborate-summary", summary="Kleborate Virulence vs Resistance Matrix")
def get_kleborate_summary(db: Session = Depends(get_db)):
    return typing_service.get_kleborate_summary(db)

