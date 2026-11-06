# PROJECT AEGIS 2.0 — INSTALLATION & SETUP GUIDE

This guide details the step-by-step installation instructions for PROJECT AEGIS 2.0 across Windows (WSL2 / Docker Desktop), Linux (Ubuntu/Debian, RHEL), and macOS.

---

## 1. System Requirements

### Minimum Requirements (Development & Testing)
- **CPU**: 4 Cores (x86_64 or Apple Silicon)
- **RAM**: 8 GB
- **Disk**: 20 GB free SSD storage
- **OS**: Windows 10/11 with WSL2, Ubuntu 22.04 LTS+, or macOS 13+

### Recommended Requirements (Production & Heavy Comparative Genomics)
- **CPU**: 16+ Cores (for IQ-TREE bootstrap and core-genome SNP alignments)
- **RAM**: 32 GB to 64 GB
- **Disk**: 500 GB+ NVMe SSD
- **Docker**: Docker Engine 24+ & Docker Compose v2.20+

---

## 2. Docker Compose Deployment (Preferred Method)

Docker Compose provides a single-command setup that launches the PostgreSQL/PostGIS spatial database, Redis task queue, FastAPI backend, Celery workers, and the React scientific frontend.

### Step 1: Clone or Navigate to Project Directory
```bash
cd AEGIS-2.0
```

### Step 2: Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```
Inspect `.env` and configure custom database passwords, secret keys, or notification webhooks if required.

### Step 3: Launch Services
```bash
docker compose up --build -d
```

### Step 4: Verify Service Health
```bash
docker compose ps
curl http://localhost:8000/api/v1/health
```

The system will be accessible at:
- **Web UI**: `http://localhost:3000`
- **REST API & Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Step 5: (Optional) Launch Dedicated Bioinformatics Worker
For running resource-intensive Nextflow, IQ-TREE, and AMRFinderPlus pipelines inside containerized environments:
```bash
docker compose -f docker-compose.yml -f deploy/docker-compose.bioinfo.yml up --build -d
```

---

## 3. Native Local Development Setup

If developing without Docker containers:

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, 3.14, or 3.15
- Node.js 18+ & npm 9+
- (Optional) PostgreSQL 15+ with PostGIS 3.3+ extension installed

### Backend Setup
1. Open a terminal in `backend/`:
   ```bash
   cd backend
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Verify tests pass:
   ```bash
   pytest tests/ -v
   ```
5. Launch the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup
1. Open a terminal in `frontend/`:
   ```bash
   cd frontend
   npm install
   ```
2. Launch Vite development server:
   ```bash
   npm run dev
   ```
3. Open your browser at `http://localhost:5173`.

---

## 4. Operational Maintenance Commands

- **Stop all services**:
  ```bash
  docker compose down
  ```
- **Stop and wipe volume data** (Destructive):
  ```bash
  docker compose down -v
  ```
- **View container logs in real time**:
  ```bash
  docker compose logs -f backend
  ```
- **Perform Database Backup**:
  ```bash
  ./deploy/scripts/backup_db.sh ./data/backups
  ```
- **Restore Database**:
  ```bash
  ./deploy/scripts/restore_db.sh ./data/backups/aegis_db_backup_20261106_120000.dump
  ```
