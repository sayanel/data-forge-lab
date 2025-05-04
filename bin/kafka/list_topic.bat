@echo off
title List Kafka Topics
echo Listing all topics...
wsl bash -c "cd %KAFKA_HOME% && bin/kafka-topics.sh --list --bootstrap-server localhost:9092"
pause
