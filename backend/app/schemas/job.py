from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class AnalysisJobCreate(BaseModel):
    job_type: str
    input_parameters: Optional[Dict[str, Any]] = None

class AnalysisJobOut(BaseModel):
    id: str
    job_type: str
    status: str
    input_parameters: Optional[Dict[str, Any]] = None
    results_summary: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class WorkflowExecutionLogOut(BaseModel):
    id: str
    job_id: str
    log_level: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True

