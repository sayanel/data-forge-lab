@echo off
title Data Forge Lab - Mongo DB SH
cd C:\Program Files\MongoDB\Server\8.0\bin
start cmd /k mongod --dbpath "C:\Users\maximilien\Dev\data_forge_db\db"
start cmd /k mongosh