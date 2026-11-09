from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.comparative import SNPMatrixRequest, SNPMatrixOut, PhylogeneticTreeOut
from app.services.comparative_service import comparative_service
from app.services.phylo_service import phylo_service

router = APIRouter()

@router.post("/snp-matrix", summary="Compute or Retrieve Core-Genome SNP Matrix")
def get_snp_matrix(req: SNPMatrixRequest, db: Session = Depends(get_db)):
    return comparative_service.get_or_create_snp_matrix(
        db,
        isolate_ids=req.isolate_ids,
        reference_genome=req.reference_genome or "HS11286"
    )

@router.get("/tree", summary="Phylogenetic Tree (IQ-TREE Newick & Tracks)")
def get_phylogenetic_tree(organism: str = "Klebsiella pneumoniae", db: Session = Depends(get_db)):
    tree = phylo_service.get_default_tree(db, organism=organism)
    return tree

@router.get("/circular-genome", summary="Circular Genome GC Profile Coordinates")
def get_circular_genome(genome_size: int = 5333942, bins: int = 100):
    return comparative_service.get_circular_genome_coordinates(genome_size=genome_size, bins=bins)

