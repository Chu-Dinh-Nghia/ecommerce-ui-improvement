@echo off
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Chua tim thay Node.js. Hay cai Node.js 24 roi chay lai file nay.
  pause
  exit /b 1
)
start "" /b node server.js
timeout /t 2 >nul
start "" "http://localhost:8080"
echo Dang chay ung dung tai http://localhost:8080
echo Giu cua so nay mo trong khi su dung ung dung.
pause
