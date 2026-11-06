from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel

class ASTRecordBase(BaseModel):
    antibiotic: str
    drug_class: Optional[str] = None
    mic_value: Optional[float] = None
    mic_operator: Optional[str] = "=="
    mic_unit: str = "mg/L"
    phenotype: str # S, I, R
    standard: str = "CLSI"
    standard_version: Optional[str] = "M100-ED34"
    testing_method: Optional[str] = "Broth microdilution"
    genotypic_prediction: Optional[str] = None
    concordance_status: Optional[str] = None

class ASTRecordCreate(ASTRecordBase):
    isolate_id: str

class ASTRecordOut(ASTRecordBase):
    id: str
    isolate_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ASTConcordanceMetrics(BaseModel):
    antibiotic: str
    total_tested: int
    true_positive_resistant: int
    true_negative_susceptible: int
    major_error_false_resistant: int # ME: Pheno S, Geno R
    very_major_error_false_susceptible: int # VME: Pheno R, Geno S
    sensitivity: float
    specificity: float
    precision_ppv: float
    concordance_rate: float
