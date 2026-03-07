@echo off
start "" ".\Celery_worker.bat"
daphne Campus_Connect.asgi:application
