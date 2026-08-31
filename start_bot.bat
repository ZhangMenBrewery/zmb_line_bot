@echo off
cd /d "%~dp0"

docker info >nul 2>&1
if not errorlevel 1 goto startall

echo Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

:waitdocker
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if errorlevel 1 goto waitdocker

:startall
echo Starting Docker containers (db + web)...
docker compose up -d

echo Starting ngrok tunnel (hidden)...
wscript.exe "C:\Users\zmb26\ngrok\ngrok-hidden.vbs"

echo.
echo ================================================
echo  Django :  http://localhost:8010
echo  Webhook:  https://uninjured-cesarean-cofounder.ngrok-free.dev/callback/
echo  ngrok  :  http://localhost:4040
echo ================================================
echo  Done. You can close this window.
pause
