@echo off
title Mongo DB SH
cd C:\Program Files\MongoDB\Server\8.0\bin
start cmd /k mongosh
cmd /k mongod --dbpath "..\data_forge_db\db"