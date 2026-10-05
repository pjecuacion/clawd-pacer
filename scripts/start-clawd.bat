@echo off
rem Start Clawd Pacer by hand (run scripts\install.bat once first).
cd /d "%~dp0.."
start "" ".venv\Scripts\pythonw.exe" -m clawd_pacer
