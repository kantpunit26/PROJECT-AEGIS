import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class AMRDeterminant(Base):
    __tablename__ = "amr_determinants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isolate_id = Column(String(36), ForeignKey("isolates.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Classification
    gene_symbol = Column(String(64), nullable=False, index=True) # e.g. blaNDM-1, blaKPC-2, mcr-1.1
    gene_family = Column(String(64), nullable=True, index=True)  # Carbapenemase, ESBL, Colistin resistance
    drug_class = Column(String(64), nullable=False, index=True)   # Beta-lactam, Polymyxin, Aminoglycoside
    subclass = Column(String(64), nullable=True, index=True)     # Carbapenem, Cephalosporin, Fluoroquinolone
    element_type = Column(String(32), nullable=False, default="GENE") # GENE, POINT_MUTATION
    
    # Mutation specifics (if element_type == POINT_MUTATION)
    mutation_name = Column(String(64), nullable=True) # e.g. GyrA_S83I, ParC_S80I, mgrB_truncation
    
    # Assembly Mapping & Coordinates
    confidence = Column(String(16), nullable=False, default="EXACT") # EXACT, BLAST_MATCH, PARTIAL
    identity_percent = Column(Float, nullable=True)
    coverage_percent = Column(Float, nullable=True)
    contig_id = Column(String(128), nullable=True)
    start_coord = Column(Integer, nullable=True)
    end_coord = Column(Integer, nullable=True)
    strand = Column(String(1), nullable=True, default="+")
    
    # Genetic Context
    predicted_context = Column(String(32), nullable=False, default="UNKNOWN") # CHROMOSOME, PLASMID, UNKNOWN
    
    # Tool and Database Tracking
    tool_version = Column(String(32), nullable=True, default="AMRFinderPlus v3.12.8")
    db_version = Column(String(32), nullable=True, default="2024-05-02.1")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    isolate = relationship("Isolate", back_populates="amr_determinants")

