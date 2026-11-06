from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SpatialClusterItem(BaseModel):
    id: str
    latitude: float
    longitude: float
    accession: str
    organism: str
    sequence_type: Optional[str] = None
    carbapenemases: List[str] = []
    colistin_genes: List[str] = []
    country: Optional[str] = None
    city: Optional[str] = None
    collection_year: Optional[int] = None
    distance_km: Optional[float] = None

class NaturalLanguageQueryRequest(BaseModel):
    query: str

class NaturalLanguageQueryResponse(BaseModel):
    interpreted_query: Dict[str, Any]
    total_matched: int
    matched_isolates: List[SpatialClusterItem]
    execution_time_ms: float

class SurveillanceAlertOut(BaseModel):
    id: str
    alert_type: str
    severity: str
    title: str
    message: str
    organism: str
    region: Optional[str]
    cluster_size: Optional[int]
    isolate_accessions: Optional[List[str]]
    acknowledged: bool
    created_at: datetime

    class Config:
        from_attributes = True
