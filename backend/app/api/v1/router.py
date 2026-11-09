from fastapi import APIRouter
from app.api.v1 import (
    health,
    auth,
    isolates,
    amr,
    typing,
    ast,
    comparative,
    plasmids,
    surveillance,
    modelling,
    reports,
    jobs
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health & Diagnostics"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(isolates.router, prefix="/isolates", tags=["Isolate Registry"])
api_router.include_router(amr.router, prefix="/amr", tags=["AMR Determinants"])
api_router.include_router(typing.router, prefix="/typing", tags=["Molecular Typing"])
api_router.include_router(ast.router, prefix="/ast", tags=["AST Concordance"])
api_router.include_router(comparative.router, prefix="/comparative", tags=["Comparative Genomics"])
api_router.include_router(plasmids.router, prefix="/plasmids", tags=["Plasmid Profiling"])
api_router.include_router(surveillance.router, prefix="/surveillance", tags=["Geospatial Surveillance"])
api_router.include_router(modelling.router, prefix="/modelling", tags=["Epidemiological Modelling"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reporting & Export"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Workflow Execution"])

