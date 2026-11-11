from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.plasmid_service import plasmid_service
from app.models.plasmid import Plasmid
from app.models.isolate import Isolate

router = APIRouter()

@router.get("/summary", summary="Plasmid MOB-suite Replicon & Mobility Statistics")
def get_plasmid_summary(organism: Optional[str] = None, db: Session = Depends(get_db)):
    return plasmid_service.get_plasmid_summary(db, organism=organism)

@router.get("/matrix", summary="Chromosome vs Plasmid AMR Genetic Context")
def get_context_matrix(organism: Optional[str] = None, db: Session = Depends(get_db)):
    return plasmid_service.get_chromosome_vs_plasmid_matrix(db, organism=organism)

@router.get("/sankey", summary="ARG Mobilization Alluvial/Sankey Flows")
def get_mobilization_sankey(organism: Optional[str] = None):
    return plasmid_service.get_resistome_mobilization_sankey(organism=organism)

@router.get("/heatmaps", summary="Partitioned Resistome Dual Heatmaps (Chromosome vs. Plasmid)")
def get_partitioned_heatmaps(organism: Optional[str] = None):
    return plasmid_service.get_chromosome_vs_plasmid_heatmaps(organism=organism)

@router.get("/list", summary="List All Reconstructed Plasmids")
def list_plasmids(organism: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Plasmid)
    if organism:
        query = query.join(Isolate, Plasmid.isolate_id == Isolate.id).filter(Isolate.organism.ilike(f"%{organism}%"))
    plasmids = query.all()
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


