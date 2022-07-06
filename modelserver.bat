@echo off
title ¸ðµ¨¼­¹ö

echo start model server
start /b /d "./modelserver" uvicorn main:app