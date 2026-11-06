import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "PROJECT AEGIS 2.0"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "aegis_dev_secret_key_change_in_production_8941279841289412")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "*"
    ]

    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "aegis")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "aegis_secure_password_2026")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "aegis_db")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    USE_SQLITE_FALLBACK: bool = os.getenv("USE_SQLITE_FALLBACK", "True").lower() in ("true", "1", "yes")
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "./data/aegis_local.db")

    # Redis & Celery
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Storage Paths
    DATA_ROOT: str = os.getenv("DATA_ROOT", "./data")
    RAW_DATA_PATH: str = os.getenv("RAW_DATA_PATH", "./data/raw")
    PROCESSED_DATA_PATH: str = os.getenv("PROCESSED_DATA_PATH", "./data/processed")
    REFERENCE_DATA_PATH: str = os.getenv("REFERENCE_DATA_PATH", "./data/reference")

    # Alerting & Webhooks
    SLACK_WEBHOOK_URL: str = os.getenv("SLACK_WEBHOOK_URL", "")
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")
    ALERT_THRESHOLD_SNP_DISTANCE: int = 15
    ALERT_THRESHOLD_OUTBREAK_CLUSTER_SIZE: int = 3
    ALERT_SPATIAL_CLUSTER_RADIUS_KM: float = 25.0

    # NCBI Integration
    NCBI_API_KEY: str = os.getenv("NCBI_API_KEY", "")
    NCBI_EMAIL: str = os.getenv("NCBI_EMAIL", "aegis-surveillance@example.org")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
