from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.modelling import SEIRParameters, SEIRSimulationResult
from app.services.modelling_service import modelling_service
from app.models.surveillance import EpidemiologicalScenario

router = APIRouter()

@router.post("/seir/simulate", response_model=SEIRSimulationResult, summary="Execute Deterministic SEIR Simulation")
def simulate_seir(params: SEIRParameters, save_scenario: bool = False, db: Session = Depends(get_db)):
    """Runs RK4 numerical integration of extended colonization-infection transmission equations."""
    result = modelling_service.simulate_seir_extended(params)

    if save_scenario:
        scenario = EpidemiologicalScenario(
            scenario_name=f"Hospital SCIR Simulation (R0={result.r0})",
            model_type="SEIR_EXTENDED",
            parameters_json=params.model_dump(),
            trajectory_json=result.model_dump(),
            r0=result.r0,
            effective_re=result.effective_re[-1] if result.effective_re else None,
            peak_infected_count=result.peak_infected_count,
            peak_day=result.peak_day
        )
        db.add(scenario)
        db.commit()

    return result
