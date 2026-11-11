from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.services.one_health_service import one_health_service

router = APIRouter()

class AlertSimulationRequest(BaseModel):
    site_id: str = Field(default="WWTP-METRO-01", description="Wastewater monitoring site ID")
    pathogen: str = Field(default="Klebsiella pneumoniae", description="Target pathogen")
    resistance_gene: str = Field(default="blaNDM-5", description="Emergent resistance gene")
    log10_load: float = Field(default=7.2, description="Genomic load in log10 copies/L")

@router.get("/sites", summary="List Wastewater & One Health Monitoring Sites")
def list_wastewater_sites() -> List[Dict[str, Any]]:
    """
    Returns spatial coordinates, catchment populations, current genomic load (log10),
    and alert tiers for wastewater treatment plants and environmental catchment sites.
    """
    return one_health_service.get_wastewater_sites()

@router.get("/lead-time", summary="Wastewater-to-Clinical Early Warning Lead Time")
def get_lead_time_timeseries(days: int = Query(default=45, ge=14, le=90)) -> Dict[str, Any]:
    """
    Returns synchronised paired timeseries of wastewater metagenomic AMR signals
    versus clinical inpatient admissions, calculating lead-time prediction windows.
    """
    return one_health_service.get_wbe_lead_time_timeseries(days=days)

@router.get("/nexus", summary="One Health Cross-Compartment Matrix")
def get_one_health_nexus() -> Dict[str, Any]:
    """
    Returns mobile genetic element (MGE) diffusion and transmission events across
    Clinical, Agricultural/Veterinary, and Wastewater/Environmental reservoirs.
    """
    return one_health_service.get_one_health_matrix()

@router.post("/simulate-alert", summary="Simulate Outbreak Alert Dispatch")
def simulate_alert(req: AlertSimulationRequest) -> Dict[str, Any]:
    """
    Simulates real-time multi-channel early warning alert dispatching to public health authorities.
    """
    lead_time = 12 if req.log10_load >= 6.5 else 8
    severity = "CRITICAL" if req.log10_load >= 7.0 else "WARNING"

    return {
        "dispatch_id": f"DISPATCH-WBE-{int(datetime.now().timestamp())}",
        "status": "DISPATCHED",
        "channels": [
            {"channel": "WHO-GLASS-Webhook", "status": "DELIVERED", "latency_ms": 142},
            {"channel": "CDC-NHSN-Gateway", "status": "DELIVERED", "latency_ms": 198},
            {"channel": "Hospital-IPC-Pager-Broadcast", "status": "DELIVERED", "latency_ms": 64},
            {"channel": "SMS-Epi-Command", "status": "DELIVERED", "latency_ms": 210}
        ],
        "alert": {
            "site_id": req.site_id,
            "pathogen": req.pathogen,
            "resistance_marker": req.resistance_gene,
            "detected_load_log10": req.log10_load,
            "severity": severity,
            "forecasted_lead_time_days": lead_time,
            "recommended_action": f"Activate early hospital ICU bed isolation protocols. Anticipated clinical surge within {lead_time} days.",
            "dispatched_at": datetime.now().isoformat()
        }
    }
