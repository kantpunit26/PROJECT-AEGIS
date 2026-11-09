from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class MolecularTypeBase(BaseModel):
    scheme: str = "PASTEUR"
    sequence_type: str = "ST11"
    allelic_profile: Optional[Dict[str, Any]] = None
    kleborate_virulence_score: Optional[int] = None
    kleborate_resistance_score: Optional[int] = None
    k_locus: Optional[str] = None
    wzi_allele: Optional[str] = None
    o_locus: Optional[str] = None
    yersiniabactin: Optional[str] = None
    colibactin: Optional[str] = None
    aerobactin: Optional[str] = None
    salmochelin: Optional[str] = None
    rmpA: Optional[str] = None
    tool_version: Optional[str] = "Kleborate v2.4.1"

class MolecularTypeCreate(MolecularTypeBase):
    isolate_id: str

class MolecularTypeOut(MolecularTypeBase):
    id: str
    isolate_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class MLSTDistributionItem(BaseModel):
    sequence_type: str
    count: int
    percentage: float
    predominant_carbapenemase: Optional[str] = None

