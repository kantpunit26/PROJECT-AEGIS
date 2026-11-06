import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON
from app.core.database import Base

class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_type = Column(String(64), nullable=False, index=True) # NCBI_INGEST, QC_PIPELINE, AMRFINDER, MLST, SNP_CALLING, IQTREE, MOB_SUITE
    status = Column(String(32), nullable=False, default="PENDING", index=True) # PENDING, RUNNING, COMPLETED, FAILED
    
    input_parameters = Column(JSON, nullable=True)
    results_summary = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class WorkflowExecutionLog(Base):
    __tablename__ = "workflow_execution_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), nullable=False, index=True)
    log_level = Column(String(16), nullable=False, default="INFO")
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
