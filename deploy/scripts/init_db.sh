#!/bin/bash
# ==============================================================================
# PROJECT AEGIS — DATABASE INITIALIZATION SCRIPT
# Ensures PostGIS extension and schema permissions are established
# ==============================================================================
set -e

echo "[AEGIS] Initializing PostgreSQL with PostGIS extensions..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS postgis;
    CREATE EXTENSION IF NOT EXISTS postgis_topology;
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
EOSQL

echo "[AEGIS] PostGIS & UUID extensions verified successfully."

