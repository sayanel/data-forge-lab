@echo off
title Stop Kafka Server
echo Stopping Kafka Server...
wsl bash -c "pkill -f kafka.Kafka"
echo Kafka server stopped.
pause
