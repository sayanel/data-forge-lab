@echo off
title API Gateway
cd ..
call venv\Scripts\activate
cd microservices\api_gateway
uvicorn main:app --reload --port 8000
