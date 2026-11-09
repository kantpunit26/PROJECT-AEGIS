from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.plasmid_service import plasmid_service
from app.models.plasmid import Plasmid

router = APIRouter()

@router.get("/summary", summary="Plasmid MOB-suite Replicon & Mobility Statistics")
def get_plasmid_summary(db: Session = Depends(get_db)):
    return plasmid_service.get_plasmid_summary(db)

@router.get("/matrix", summary="Chromosome vs Plasmid AMR Genetic Context")
def get_context_matrix(db: Session = Depends(get_db)):
    return plasmid_service.get_chromosome_vs_plasmid_matrix(db)

@router.get("/list", summary="List All Reconstructed Plasmids")
def list_plasmids(db: Session = Depends(get_db)):
    plasmids = db.query(Plasmid).all()
    return [
        {
            "id": p.id,
            "isolate_id": p.isolate_id,
            "plasmid_id": p.plasmid_id,
            "cluster_id": p.cluster_id,
            "replicon_types": p.replicon_types,
            "mobility": p.mobility,
            "predicted_length": p.predicted_length,
            "associated_amr_genes": p.associated_amr_genes
        }
        for p in plasmids
    ]

