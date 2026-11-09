from typing import Optional, List, Any
from datetime import date, datetime
from pydantic import BaseModel, Field

class IsolateBase(BaseModel):
    accession: str
    sample_id: Optional[str] = None
    organism: str = "Klebsiella pneumoniae"
    taxon_id: Optional[int] = 573
    strain: Optional[str] = None
    collection_date: Optional[date] = None
    collection_year: Optional[int] = None
    isolation_source: Optional[str] = None
    host: Optional[str] = "Homo sapiens"
    country: Optional[str] = None
    state_province: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    assembly_level: Optional[str] = "Complete Genome"
    genome_size: Optional[int] = None
    gc_percent: Optional[float] = None
    n50: Optional[int] = None
    contig_count: Optional[int] = None
    qc_status: str = "PASS"
    qc_notes: Optional[str] = None
    provenance_source: Optional[str] = "NCBI_DATASETS"

class IsolateCreate(IsolateBase):
    checksum_sha256: Optional[str] = None

class IsolateUpdate(BaseModel):
    strain: Optional[str] = None
    isolation_source: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    qc_status: Optional[str] = None

class IsolateOut(IsolateBase):
    id: str
    checksum_sha256: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    amr_count: Optional[int] = 0
    sequence_type: Optional[str] = None

    class Config:
        from_attributes = True

class IsolateDetailOut(IsolateOut):
    amr_determinants: List[Any] = []
    molecular_types: List[Any] = []
    ast_records: List[Any] = []
    plasmids: List[Any] = []

    class Config:
        from_attributes = True

