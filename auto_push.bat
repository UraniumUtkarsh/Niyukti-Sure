@echo off
cd /d "%~dp0"

REM Set commit message with timestamp
set msg=Auto backup on %date% at %time%

git add .
git commit -m "%msg%"
git push origin desktop-sync-work
