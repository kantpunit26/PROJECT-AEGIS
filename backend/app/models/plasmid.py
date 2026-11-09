import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Plasmid(Base):
    __tablename__ = "plasmids"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isolate_id = Column(String(36), ForeignKey("isolates.id", ondelete="CASCADE"), nullable=False, index=True)
    
    plasmid_id = Column(String(64), nullable=False, index=True) # e.g. pKPN-101, plasmid_1
    cluster_id = Column(String(64), nullable=True, index=True)  # MOB-suite cluster e.g. AA042
    
    # Typing & Characteristics
    replicon_types = Column(JSON, nullable=True) # e.g. ["IncFII", "IncFIB"]
    relaxase_type = Column(String(32), nullable=True) # e.g. MOBF, MOBP
    mpf_type = Column(String(32), nullable=True)      # e.g. MPF_F, MPF_T
    mobility = Column(String(32), nullable=False, default="CONJUGATIVE") # CONJUGATIVE, MOBILIZABLE, NON_MOBILIZABLE
    
    predicted_length = Column(Integer, nullable=True) # base pairs
    gc_percent = Column(Float, nullable=True)
    contig_count = Column(Integer, nullable=True, default=1)
    
    # Associated AMR Cargo
    associated_amr_genes = Column(JSON, nullable=True) # e.g. ["blaKPC-2", "aac(6')-Ib-cr"]
    
    tool_version = Column(String(32), nullable=True, default="MOB-suite v3.1.8")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    isolate = relationship("Isolate", back_populates="plasmids")

