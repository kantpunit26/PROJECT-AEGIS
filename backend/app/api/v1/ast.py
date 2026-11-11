from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ast_service import ast_service
from app.models.ast import ASTRecord
from app.models.isolate import Isolate

router = APIRouter()

@router.get("/concordance", summary="AST Genotype-Phenotype Diagnostic Metrics")
def get_ast_concordance(
    antibiotic: Optional[str] = None,
    organism: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return ast_service.calculate_concordance_metrics(db, antibiotic=antibiotic, organism=organism)

@router.get("/records", summary="List Experimental AST Records")
def get_ast_records(
    db: Session = Depends(get_db),
    antibiotic: Optional[str] = None,
    organism: Optional[str] = None
):
    query = db.query(ASTRecord)
    if organism:
        query = query.join(Isolate, ASTRecord.isolate_id == Isolate.id).filter(Isolate.organism.ilike(f"%{organism}%"))
    if antibiotic:
        query = query.filter(ASTRecord.antibiotic.ilike(f"%{antibiotic}%"))
    records = query.limit(200).all()
    return [
        {
            "id": r.id,
            "isolate_id": r.isolate_id,
            "antibiotic": r.antibiotic,
            "mic_value": r.mic_value,
            "mic_unit": r.mic_unit,
            "phenotype": r.phenotype,
            "standard": r.standard,
            "genotypic_prediction": r.genotypic_prediction,
            "concordance_status": r.concordance_status
        }
        for r in records
    ]


