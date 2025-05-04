@echo off
title Clean Kafka Data
echo WARNING: This will delete all Kafka data (logs, topics, etc)!
pause
wsl bash -c "rm -rf %KAFKA_HOME%/data"
echo Data cleaned.
pause
