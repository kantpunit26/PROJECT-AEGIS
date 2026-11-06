import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class MolecularType(Base):
    __tablename__ = "molecular_types"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isolate_id = Column(String(36), ForeignKey("isolates.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # MLST Typing
    scheme = Column(String(32), nullable=False, default="PASTEUR", index=True) # PASTEUR, OXFORD
    sequence_type = Column(String(32), nullable=False, default="ST11", index=True)
    allelic_profile = Column(JSON, nullable=True) # e.g. {"gapA": 3, "infB": 3, "mdh": 1, ...}
    
    # Kleborate Virulence & Capsule Typing
    kleborate_virulence_score = Column(Integer, nullable=True) # 0 to 5
    kleborate_resistance_score = Column(Integer, nullable=True) # 0 to 3
    k_locus = Column(String(32), nullable=True, index=True) # e.g. KL64, KL102, KL1
    wzi_allele = Column(String(32), nullable=True)          # e.g. wzi-64
    o_locus = Column(String(32), nullable=True, index=True) # e.g. O1v1, O2v2
    
    # Virulence Determinants
    yersiniabactin = Column(String(32), nullable=True) # ybt lineage
    colibactin = Column(String(32), nullable=True)     # clb
    aerobactin = Column(String(32), nullable=True)     # iuc
    salmochelin = Column(String(32), nullable=True)    # iro
    rmpA = Column(String(32), nullable=True)           # rmpA hypermucoviscosity
    
    tool_version = Column(String(32), nullable=True, default="Kleborate v2.4.1 / mlst v2.23.0")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    isolate = relationship("Isolate", back_populates="molecular_types")
