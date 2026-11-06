from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SNPMatrixRequest(BaseModel):
    isolate_ids: Optional[List[str]] = None
    organism: str = "Klebsiella pneumoniae"
    reference_genome: Optional[str] = "HS11286"
    max_snp_distance_filter: Optional[int] = None

class SNPMatrixOut(BaseModel):
    id: str
    analysis_name: str
    reference_genome: str
    isolate_count: int
    accessions: List[str]
    distance_matrix: List[List[int]]
    total_core_positions: int
    filtered_snp_count: int
    created_at: datetime

class PhylogeneticTreeOut(BaseModel):
    id: str
    tree_name: str
    organism: str
    newick_string: str
    substitution_model: str
    log_likelihood: Optional[float] = None
    bootstrap_replicates: int
    metadata_tracks: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CircularGenomeCoordinate(BaseModel):
    position: int
    gc_content: float
    gc_skew: float
    features: List[Dict[str, Any]]
