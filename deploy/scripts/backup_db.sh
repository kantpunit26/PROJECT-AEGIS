#!/bin/bash
# ==============================================================================
# PROJECT AEGIS — DATABASE BACKUP UTILITY
# Creates versioned timestamped dumps of PostgreSQL / PostGIS data
# ==============================================================================
set -e

BACKUP_DIR="${1:-./data/backups}"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/aegis_db_backup_${TIMESTAMP}.dump"

echo "[AEGIS] Starting database backup to ${BACKUP_FILE}..."

if command -v docker &> /dev/null && docker ps | grep -q aegis_db; then
    docker exec -t aegis_db pg_dump -U aegis -F c aegis_db > "$BACKUP_FILE"
else
    pg_dump -U "${POSTGRES_USER:-aegis}" -h "${POSTGRES_SERVER:-localhost}" -p "${POSTGRES_PORT:-5432}" -F c -b -v -f "$BACKUP_FILE" "${POSTGRES_DB:-aegis_db}"
fi

echo "[AEGIS] Database backup completed: ${BACKUP_FILE} ($(du -h "$BACKUP_FILE" | cut -f1))"

