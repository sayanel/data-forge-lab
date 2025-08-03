@echo off
echo Starting Redis in WSL...

REM Launch Redis server inside WSL
wsl -d Ubuntu -- bash -c "redis-server"

pause
