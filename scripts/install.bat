@echo off
rem Clawd Pacer installer: sets up Python env, adds start-with-Windows, starts Clawd.
rem Usage: install.bat            (install + start)
rem        install.bat --uninstall (remove from startup)
cd /d "%~dp0.."
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY (
  echo Python was not found. Install it from https://www.python.org/downloads/ and run this again.
  pause
  exit /b 1
)
%PY% -m clawd_pacer.install %*
pause
