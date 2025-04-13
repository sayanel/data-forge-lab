@echo off
title Data Forge Lab - App
cd C:\Users\maximilien\Dev\data-forge-lab
call venv\Scripts\activate
cd data_forge_lab
start cmd /k python app.py
