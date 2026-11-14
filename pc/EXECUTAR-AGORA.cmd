@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
if not exist ".venv\Scripts\python.exe" (
  echo Execute INSTALAR.cmd primeiro.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" rodar.py
type estado.json
pause
