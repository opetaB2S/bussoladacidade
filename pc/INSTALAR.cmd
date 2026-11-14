@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
if exist "%LocalAppData%\Programs\Python\Python310\python.exe" (
  "%LocalAppData%\Programs\Python\Python310\python.exe" instalar.py
) else (
  py -3 instalar.py
)
echo.
pause
