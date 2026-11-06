import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON
from app.core.database import Base

class SNPAnalysis(Base):
    __tablename__ = "snp_analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_name = Column(String(128), nullable=False)
    organism = Column(String(128), nullable=False, default="Klebsiella pneumoniae")
    reference_genome = Column(String(128), nullable=False) # Accession or name (e.g. HS11286 / NC_016845.1)
    
    isolate_count = Column(Integer, nullable=False, default=0)
    isolate_accessions = Column(JSON, nullable=False) # List of accessions included
    total_core_positions = Column(Integer, nullable=False, default=0)
    filtered_snp_count = Column(Integer, nullable=False, default=0)
    
    # Distance Matrix: JSON object {"accessions": [...], "matrix": [[0, 5, 12], [5, 0, 8], ...]}
    distance_matrix_json = Column(JSON, nullable=False)
    
    tool_version = Column(String(32), nullable=True, default="Snippy v4.6.0 / Parsnp v1.7.4")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class PhylogeneticTree(Base):
    __tablename__ = "phylogenetic_trees"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tree_name = Column(String(128), nullable=False)
    organism = Column(String(128), nullable=False, default="Klebsiella pneumoniae")
    
    # Tree format
    newick_string = Column(Text, nullable=False)
    
    # Computational Metrics
    substitution_model = Column(String(64), nullable=False, default="GTR+F+R4")
    log_likelihood = Column(Float, nullable=True)
    bootstrap_replicates = Column(Integer, nullable=False, default=1000)
    tree_method = Column(String(64), nullable=False, default="Maximum Likelihood (IQ-TREE)")
    
    # Metadata tracks for visualization: {"ST": {...}, "AMR": {...}, "Country": {...}}
    metadata_tracks_json = Column(JSON, nullable=True)
    
    tool_version = Column(String(32), nullable=True, default="IQ-TREE v2.2.6")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
