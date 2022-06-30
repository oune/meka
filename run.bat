@echo off
title 고장진단 시스템 서버

echo start main server
start /b /d "./server" nodemon liveApp.js

echo start model server
start /b /d "./modelserver" uvicorn main:app