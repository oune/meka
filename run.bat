@echo off
title �������� �ý��� ����

echo start main server
start /b /d "./web" node app.js

echo start model server
start /b /d "./modelserver" uvicorn main:app