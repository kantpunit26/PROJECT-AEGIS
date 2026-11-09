@echo off
echo ===================================================
echo Starting PROJECT AEGIS...
echo ===================================================

echo [1/3] Starting Backend API Server (FastAPI on Port 8000)...
start "AEGIS Backend (FastAPI)" cmd /k "cd /d %~dp0 && .venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --port 8000 --reload"

echo [2/3] Starting Frontend Dev Server (Vite on Port 5173)...
start "AEGIS Frontend (Vite/React)" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo [3/3] Waiting for servers to initialize...
timeout /t 4 /nobreak >nul
start http://localhost:5173

echo.
echo ===================================================
echo AEGIS is running!
echo - Web Dashboard:   http://localhost:5173
echo - Interactive API: http://localhost:8000/docs
echo ===================================================
echo.
