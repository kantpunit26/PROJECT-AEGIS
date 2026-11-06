#!/bin/bash
# ==============================================================================
# PROJECT AEGIS 2.0 — DATABASE RESTORATION UTILITY
# Restores a PostgreSQL/PostGIS dump file into the AEGIS database
# ==============================================================================
set -e

BACKUP_FILE="$1"
if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <path_to_backup_file.dump>"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file $BACKUP_FILE does not exist."
    exit 1
fi

echo "[AEGIS 2.0] Restoring database from ${BACKUP_FILE}..."

if command -v docker &> /dev/null && docker ps | grep -q aegis_db; then
    cat "$BACKUP_FILE" | docker exec -i aegis_db pg_restore -U aegis -d aegis_db --clean --if-exists
else
    pg_restore -U "${POSTGRES_USER:-aegis}" -h "${POSTGRES_SERVER:-localhost}" -p "${POSTGRES_PORT:-5432}" -d "${POSTGRES_DB:-aegis_db}" --clean --if-exists "$BACKUP_FILE"
fi

echo "[AEGIS 2.0] Database restored successfully."
