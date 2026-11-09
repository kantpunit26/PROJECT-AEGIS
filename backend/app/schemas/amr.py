from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel

class AMRDeterminantBase(BaseModel):
    gene_symbol: str
    gene_family: Optional[str] = None
    drug_class: str
    subclass: Optional[str] = None
    element_type: str = "GENE"
    mutation_name: Optional[str] = None
    confidence: str = "EXACT"
    identity_percent: Optional[float] = None
    coverage_percent: Optional[float] = None
    contig_id: Optional[str] = None
    start_coord: Optional[int] = None
    end_coord: Optional[int] = None
    strand: Optional[str] = "+"
    predicted_context: str = "UNKNOWN"
    tool_version: Optional[str] = "AMRFinderPlus v3.12.8"
    db_version: Optional[str] = "2024-05-02.1"

class AMRDeterminantCreate(AMRDeterminantBase):
    isolate_id: str

class AMRDeterminantOut(AMRDeterminantBase):
    id: str
    isolate_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class AMRPrevalenceItem(BaseModel):
    gene_symbol: str
    gene_family: Optional[str]
    drug_class: str
    count: int
    prevalence_percent: float

class AMRPrevalenceResponse(BaseModel):
    total_isolates: int
    determinants: List[AMRPrevalenceItem]

