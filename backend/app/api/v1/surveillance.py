from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.spatial_service import spatial_service
from app.schemas.surveillance import NaturalLanguageQueryRequest, NaturalLanguageQueryResponse, SurveillanceAlertOut
from app.models.surveillance import SurveillanceAlert

router = APIRouter()

@router.get("/spatial-clusters", summary="Isolates Geospatial Cluster Coordinates")
def get_spatial_clusters(
    organism: Optional[str] = None,
    country: Optional[str] = None,
    year: Optional[int] = None,
    gene: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return spatial_service.get_spatial_clusters(
        db,
        organism=organism,
        country=country,
        year=year,
        gene=gene
    )

@router.post("/nl-query", response_model=NaturalLanguageQueryResponse, summary="Natural Language Outbreak Spatial Query")
def execute_natural_language_query(req: NaturalLanguageQueryRequest, db: Session = Depends(get_db)):
    """
    Safely translates questions (e.g. 'Show all K. pneumoniae isolates with blaNDM within 50 km of Vadodara')
    into parameterized spatial filter queries with zero raw SQL execution.
    """
    return spatial_service.parse_and_execute_nl_query(db, req.query)

@router.get("/alerts", summary="Surveillance Outbreak Alerts")
def get_alerts(organism: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(SurveillanceAlert)
    if organism:
        query = query.filter(SurveillanceAlert.organism.ilike(f"%{organism}%"))
    alerts = query.order_by(SurveillanceAlert.created_at.desc()).all()
    return alerts


