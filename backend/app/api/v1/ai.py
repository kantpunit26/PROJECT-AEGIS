from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.services.ai_service import ai_service

router = APIRouter()

class MICPredictionRequest(BaseModel):
    organism: str = Field(default="Klebsiella pneumoniae", description="Target bacterial organism")
    isolate_accession: Optional[str] = Field(default=None, description="Optional isolate accession identifier")
    genes: Optional[List[str]] = Field(default=None, description="List of detected resistance genes / mutations")

class CopilotChatRequest(BaseModel):
    query: str = Field(..., description="Query or prompt for the epidemiological copilot")
    organism: str = Field(default="Klebsiella pneumoniae", description="Contextual target pathogen")

@router.post("/predict-mic", summary="Deep Learning Continuous MIC Prediction")
def predict_mic(req: MICPredictionRequest) -> Dict[str, Any]:
    """
    Computes continuous MIC regression values (ug/mL), 95% confidence intervals,
    and categorical resistance probabilities directly from genomic determinant profiles.
    """
    try:
        result = ai_service.predict_mic(
            isolate_accession=req.isolate_accession,
            organism=req.organism,
            genes=req.genes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/copilot-chat", summary="Epidemiological AI Copilot Consultation")
def copilot_chat(req: CopilotChatRequest) -> Dict[str, Any]:
    """
    Generates WHO GLASS / CDC MMWR-aligned outbreak hazard briefs, transmission hypotheses,
    and infection prevention and control (IPC) recommendations.
    """
    try:
        brief = ai_service.generate_copilot_brief(
            query=req.query,
            organism=req.organism
        )
        return brief
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
