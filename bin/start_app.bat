@echo off
title Flask App
cd ..
call venv\Scripts\activate
cd data_forge_lab
cmd /k python app.py
