@echo off
rem Clawd Pacer launcher. Safe to copy into shell:startup (uses full paths).
cd /d "E:\Git\clawd-pacer"
start "" "E:\Git\clawd-pacer\.venv\Scripts\pythonw.exe" -m clawd_pacer
