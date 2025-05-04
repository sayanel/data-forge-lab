@echo off
title Kafka
echo ====================================
echo Starting Kafka Server inside WSL2...
echo ====================================

:: Set absolute paths
set KAFKA_HOME=/home/max/kafka/kafka_2.13-4.0.0
set LOG_DIR=%KAFKA_HOME%/logs
set DATA_DIR=%KAFKA_HOME%/data

:: Clean existing data and logs (delete directories completely)
echo Cleaning existing Kafka data...
wsl bash -c "rm -rf %KAFKA_HOME%/data %KAFKA_HOME%/logs"
wsl bash -c "mkdir -p %KAFKA_HOME%/data %KAFKA_HOME%/logs"

:: Check that directories are empty and no meta.properties exist
echo Checking for leftover meta.properties files...
wsl bash -c "if find %KAFKA_HOME% -name meta.properties | grep meta.properties; then echo ERROR: meta.properties still exists!; exit 1; else echo No meta.properties found. Proceeding.; fi"
if %errorlevel% neq 0 (
    echo ERROR: Please manually remove all meta.properties files before continuing.
    pause
    exit /b 1
)

:: Generate new UUID and format storage
echo Initializing Kafka storage...
wsl bash -c "cd %KAFKA_HOME% && UUID=\$(bin/kafka-storage.sh random-uuid | tr -d '\r\n') && echo Generated UUID: \$UUID && bin/kafka-storage.sh format -t \$UUID -c config/server.properties --standalone"

echo.
echo ====================================
echo Launching Kafka Server...
echo ====================================

:: Start Kafka server
wsl bash -c "cd %KAFKA_HOME% && bin/kafka-server-start.sh config/server.properties"

pause

:: bin/kafka-storage.sh format -t 0FiXdivsQHaZZ3K3-BxoXQ -c config/kraft/server.properties
