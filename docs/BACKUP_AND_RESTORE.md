# PROJECT AEGIS 2.0 — BACKUP AND DISASTER RECOVERY

## 1. Overview
The platform maintains strict persistence for:
1. PostgreSQL / PostGIS relational database records.
2. Raw genomic files and processed bioinformatics artifacts (`data/raw`, `data/processed`).
3. Configuration and environment parameters.

---

## 2. Backup Procedures

### Automated Database Backup
Execute the provided script:
```bash
./deploy/scripts/backup_db.sh /path/to/backup/destination
```
This runs `pg_dump` with `-F c` (custom compressed format with complete PostGIS spatial indexes and sequence states).

### Volume Snapshotting
Docker volumes can be backed up directly:
```bash
docker run --rm -v aegis_pgdata:/volume -v $(pwd)/data/backups:/backup \
    alpine tar -czf /backup/pgdata_backup.tar.gz -C /volume ./
```

---

## 3. Restoration Procedures

To restore an existing dump:
```bash
./deploy/scripts/restore_db.sh /path/to/backup/aegis_db_backup_TIMESTAMP.dump
```
Verify restore:
```bash
docker exec -it aegis_db psql -U aegis -d aegis_db -c "SELECT COUNT(*) FROM isolates;"
```
