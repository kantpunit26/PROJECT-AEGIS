from typing import Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.export_service import export_service

router = APIRouter()

@router.get("/export/csv", summary="Export Isolates Registry to CSV")
def export_csv(organism: Optional[str] = None, db: Session = Depends(get_db)):
    csv_content = export_service.export_csv(db, organism=organism)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=aegis_isolates_export.csv"}
    )

@router.get("/export/geojson", summary="Export Geospatial Isolates to GeoJSON")
def export_geojson(organism: Optional[str] = None, db: Session = Depends(get_db)):
    return export_service.export_geojson(db, organism=organism)

@router.get("/export/who-glass", summary="Export WHO GLASS Standardized Surveillance Data")
def export_who_glass(db: Session = Depends(get_db)):
    return export_service.export_who_glass_format(db)

@router.get("/export/newick", summary="Export Phylogenetic Tree to Newick")
def export_newick(tree_id: Optional[str] = None, db: Session = Depends(get_db)):
    newick_content = export_service.export_newick(db, tree_id=tree_id)
    return Response(
        content=newick_content,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=aegis_phylogeny.nwk"}
    )
