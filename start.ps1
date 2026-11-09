# PROJECT AEGIS — PowerShell Quick Launcher

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Starting PROJECT AEGIS..." -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan

$root = $PSScriptRoot

Write-Host "[1/3] Starting Backend API Server (FastAPI on Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; .\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --port 8000 --reload"

Write-Host "[2/3] Starting Frontend Dev Server (Vite on Port 5173)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

Write-Host "[3/3] Waiting for servers to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 4
Start-Process "http://localhost:5173"

Write-Host "`n===================================================" -ForegroundColor Cyan
Write-Host "AEGIS is running!" -ForegroundColor Green
Write-Host " - Web Dashboard:   http://localhost:5173" -ForegroundColor White
Write-Host " - Interactive API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "===================================================`n" -ForegroundColor Cyan
