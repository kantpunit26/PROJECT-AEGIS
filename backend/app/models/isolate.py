import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, BigInteger, Float, Date, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Isolate(Base):
    __tablename__ = "isolates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    accession = Column(String(64), unique=True, nullable=False, index=True)
    sample_id = Column(String(128), index=True, nullable=True)
    organism = Column(String(128), nullable=False, default="Klebsiella pneumoniae", index=True)
    taxon_id = Column(Integer, nullable=True, default=573)
    strain = Column(String(128), nullable=True)
    
    # Temporal & Clinical Provenance
    collection_date = Column(Date, nullable=True)
    collection_year = Column(Integer, nullable=True, index=True)
    isolation_source = Column(String(128), nullable=True, index=True)
    host = Column(String(64), nullable=True, default="Homo sapiens")
    
    # Geospatial Metadata
    country = Column(String(64), nullable=True, index=True)
    state_province = Column(String(64), nullable=True, index=True)
    city = Column(String(64), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_spatial_aggregated = Column(Boolean, default=False)
    
    # Assembly & QC Metrics
    assembly_level = Column(String(32), nullable=True, default="Complete Genome")
    genome_size = Column(BigInteger, nullable=True)
    gc_percent = Column(Float, nullable=True)
    n50 = Column(Integer, nullable=True)
    contig_count = Column(Integer, nullable=True)
    qc_status = Column(String(16), nullable=False, default="PASS", index=True)  # PASS, WARNING, FAIL
    qc_notes = Column(Text, nullable=True)
    
    # Provenance & Audit
    checksum_sha256 = Column(String(64), nullable=True)
    provenance_source = Column(String(64), nullable=True, default="NCBI_DATASETS")
    raw_data_uri = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    amr_determinants = relationship("AMRDeterminant", back_populates="isolate", cascade="all, delete-orphan")
    molecular_types = relationship("MolecularType", back_populates="isolate", cascade="all, delete-orphan")
    ast_records = relationship("ASTRecord", back_populates="isolate", cascade="all, delete-orphan")
    plasmids = relationship("Plasmid", back_populates="isolate", cascade="all, delete-orphan")

