@echo off
title Create Kafka Topic
set /p TOPIC_NAME="Enter topic name: "
wsl bash -c "cd %KAFKA_HOME% && bin/kafka-topics.sh --create --topic %TOPIC_NAME% --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1"
pause
