import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON, Boolean
from app.core.database import Base

class SurveillanceAlert(Base):
    __tablename__ = "surveillance_alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    alert_type = Column(String(64), nullable=False, index=True) # OUTBREAK_CLUSTER, NOVEL_AMR, VME_DETECTED, HIGH_RISK_CLONE
    severity = Column(String(16), nullable=False, default="HIGH", index=True) # INFO, WARNING, HIGH, CRITICAL
    
    title = Column(String(256), nullable=False)
    message = Column(Text, nullable=False)
    
    organism = Column(String(128), nullable=False, default="Klebsiella pneumoniae")
    region = Column(String(128), nullable=True)
    cluster_size = Column(Integer, nullable=True)
    isolate_accessions = Column(JSON, nullable=True)
    
    acknowledged = Column(Boolean, default=False, nullable=False)
    dispatched_slack = Column(Boolean, default=False)
    dispatched_discord = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EpidemiologicalScenario(Base):
    __tablename__ = "epidemiological_scenarios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_name = Column(String(128), nullable=False)
    model_type = Column(String(32), nullable=False, default="SEIR_EXTENDED")
    
    # Parameters stored as JSON
    parameters_json = Column(JSON, nullable=False)
    
    # Trajectory results: {"time": [...], "S": [...], "C": [...], "I": [...], "R": [...]}
    trajectory_json = Column(JSON, nullable=False)
    
    # Calculated Epidemiological Constants
    r0 = Column(Float, nullable=False)
    effective_re = Column(Float, nullable=True)
    peak_infected_count = Column(Float, nullable=True)
    peak_day = Column(Integer, nullable=True)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

