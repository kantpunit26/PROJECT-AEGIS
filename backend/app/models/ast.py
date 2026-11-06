import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class ASTRecord(Base):
    __tablename__ = "ast_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isolate_id = Column(String(36), ForeignKey("isolates.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Antimicrobial Identification
    antibiotic = Column(String(64), nullable=False, index=True) # Meropenem, Colistin, Amikacin, Ciprofloxacin, etc.
    drug_class = Column(String(64), nullable=True)             # Carbapenem, Polymyxin, Aminoglycoside, etc.
    
    # Experimental Measurement
    mic_value = Column(Float, nullable=True)                   # Numeric concentration
    mic_operator = Column(String(2), nullable=True, default="==") # <=, >=, ==, <, >
    mic_unit = Column(String(16), nullable=False, default="mg/L") # mg/L, ug/mL
    
    # Interpretation
    phenotype = Column(String(16), nullable=False, index=True) # S (Susceptible), I (Intermediate), R (Resistant)
    standard = Column(String(16), nullable=False, default="CLSI", index=True) # CLSI, EUCAST
    standard_version = Column(String(32), nullable=True, default="M100-ED34 (2024)")
    testing_method = Column(String(64), nullable=True, default="Broth microdilution")
    
    # Genotype-Phenotype Concordance Evaluation
    genotypic_prediction = Column(String(16), nullable=True) # S, R
    concordance_status = Column(String(32), nullable=True)  # CONCORDANT, MAJOR_ERROR (FP), VERY_MAJOR_ERROR (FN)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    isolate = relationship("Isolate", back_populates="ast_records")
