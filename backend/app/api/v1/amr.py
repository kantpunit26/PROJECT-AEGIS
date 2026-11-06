from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.amr_service import amr_service
from app.models.amr import AMRDeterminant

router = APIRouter()

@router.get("/prevalence", summary="AMR Gene Population Prevalence")
def get_amr_prevalence(organism: Optional[str] = None, db: Session = Depends(get_db)):
    return amr_service.get_amr_prevalence(db, organism=organism)

@router.get("/co-occurrence", summary="Pairwise AMR Co-occurrence Matrix")
def get_co_occurrence(top_n: int = Query(10, ge=3, le=30), db: Session = Depends(get_db)):
    return amr_service.get_amr_co_occurrence(db, top_n=top_n)

@router.get("/determinants", summary="Query All AMR Determinants")
def get_determinants(
    db: Session = Depends(get_db),
    gene: Optional[str] = None,
    drug_class: Optional[str] = None,
    subclass: Optional[str] = None
):
    query = db.query(AMRDeterminant)
    if gene:
        query = query.filter(AMRDeterminant.gene_symbol.ilike(f"%{gene}%"))
    if drug_class:
        query = query.filter(AMRDeterminant.drug_class.ilike(f"%{drug_class}%"))
    if subclass:
        query = query.filter(AMRDeterminant.subclass.ilike(f"%{subclass}%"))
    
    dets = query.limit(200).all()
    return [
        {
            "id": d.id,
            "isolate_id": d.isolate_id,
            "gene_symbol": d.gene_symbol,
            "gene_family": d.gene_family,
            "drug_class": d.drug_class,
            "subclass": d.subclass,
            "element_type": d.element_type,
            "predicted_context": d.predicted_context,
            "contig_id": d.contig_id
        }
        for d in dets
    ]
