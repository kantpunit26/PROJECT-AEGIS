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
        reference_genome=req.reference_genome or "HS11286",
        organism=req.organism
    )

@router.get("/tree", summary="Phylogenetic Tree (IQ-TREE Newick & Tracks)")
def get_phylogenetic_tree(organism: str = "Klebsiella pneumoniae", db: Session = Depends(get_db)):
    tree = phylo_service.get_default_tree(db, organism=organism)
    return tree

@router.get("/circular-genome", summary="Circular Genome GC Profile Coordinates")
def get_circular_genome(genome_size: int = 5333942, bins: int = 100):
    return comparative_service.get_circular_genome_coordinates(genome_size=genome_size, bins=bins)

@router.get("/circular-atlas", summary="Multi-Track Circular Genome Atlas (Circos/BRIG)")
def get_circular_genome_atlas(
    genome_size: int = 5333942,
    bins: int = 120,
    organism: str = "Klebsiella pneumoniae"
):
    return comparative_service.get_circular_genome_atlas(genome_size=genome_size, bins=bins, organism=organism)

@router.get("/minimum-spanning-tree", summary="Minimum Spanning Tree (MST / GrapeTree Outbreak Network)")
def get_minimum_spanning_tree(organism: str = "Klebsiella pneumoniae"):
    return comparative_service.get_minimum_spanning_tree()

@router.get("/time-scaled-tree", summary="Time-Scaled Phylodynamic Tree (BEAST / Molecular Clock)")
def get_time_scaled_tree(organism: str = "Klebsiella pneumoniae"):
    return comparative_service.get_time_scaled_phylogeny()

@router.get("/bayesian-skyline", summary="Bayesian Skyline Plot (BSP / Effective Population Size)")
def get_bayesian_skyline(organism: str = "Klebsiella pneumoniae"):
    return comparative_service.get_bayesian_skyline_data()

@router.get("/pan-genome-matrix", summary="Phylogeny Aligned Multi-Panel Matrix (iTOL style)")
def get_pan_genome_matrix(organism: str = "Klebsiella pneumoniae"):
    return comparative_service.get_pan_genome_matrix()

@router.get("/linear-synteny", summary="Linear Genetic Synteny & Resistance Island Maps (Easyfig style)")
def get_linear_synteny(organism: str = "Klebsiella pneumoniae"):
    return comparative_service.get_linear_synteny_data()



