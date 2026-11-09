import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import AnalysisJob, WorkflowExecutionLog
from app.schemas.job import AnalysisJobCreate, AnalysisJobOut, WorkflowExecutionLogOut

router = APIRouter()

@router.get("", response_model=List[AnalysisJobOut], summary="List Background Bioinformatics Jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(AnalysisJob).order_by(AnalysisJob.created_at.desc()).limit(100).all()

@router.post("", response_model=AnalysisJobOut, status_code=status.HTTP_201_CREATED, summary="Submit Analysis Job")
def create_job(job_in: AnalysisJobCreate, db: Session = Depends(get_db)):
    job = AnalysisJob(
        job_type=job_in.job_type,
        status="RUNNING",
        input_parameters=job_in.input_parameters,
        started_at=datetime.datetime.utcnow(),
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Add initial workflow log
    log = WorkflowExecutionLog(
        job_id=job.id,
        log_level="INFO",
        message=f"Dispatched Nextflow pipeline for {job.job_type}."
    )
    db.add(log)
    db.commit()
    return job

@router.get("/{id}/logs", response_model=List[WorkflowExecutionLogOut], summary="Fetch Job Execution Logs")
def get_job_logs(id: str, db: Session = Depends(get_db)):
    return db.query(WorkflowExecutionLog).filter(WorkflowExecutionLog.job_id == id).order_by(WorkflowExecutionLog.timestamp.asc()).all()

