# PROJECT AEGIS — TROUBLESHOOTING & SYSTEM DIAGNOSTICS

## 1. Common Diagnostics

### 1.1 Backend Health Check Fails
Check if the service is running and inspect container logs:
```bash
docker compose logs backend
```
Common causes:
- Database container still initializing: Wait 10 seconds for PostGIS healthcheck to turn green.
- Port 8000 or 5432 already occupied: Change `POSTGRES_PORT` or backend port in `.env`.

### 1.2 PostGIS Extension Not Found
If running against an external PostgreSQL instance without PostGIS:
```sql
CREATE EXTENSION postgis;
CREATE EXTENSION "uuid-ossp";
```
In local standalone development mode, enable `USE_SQLITE_FALLBACK=True` in `.env` to execute tests without a local PostgreSQL daemon.

### 1.3 Celery Worker Not Connecting to Redis
Ensure Redis is healthy:
```bash
docker compose exec redis redis-cli ping
# Expected: PONG
```

### 1.4 NCBI Ingestion Network Timeouts
When downloading large SRA or assembly files, ensure `NCBI_API_KEY` is specified in `.env` to prevent rate-limiting (NCBI allows 10 requests/sec with key vs. 3 requests/sec without).

