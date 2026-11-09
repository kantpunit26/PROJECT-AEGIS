import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.init_db import init_db

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("aegis_backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing PROJECT AEGIS Backend & Database...")
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to auto-initialize database on startup: {e}")
    yield
    logger.info("Shutting down PROJECT AEGIS Backend...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Advanced Genomic Epidemiology & Intelligence System for AMR Pathogens",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", summary="Root Status")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "active",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }

