@echo off
title �������� �ý��� ����

echo start main server
start /b /d "./server" nodemon liveApp.js

echo start model server
start /b /d "./modelserver" uvicorn main:app