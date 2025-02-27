@echo off
cd frontend
call npm run build-only
cd ..
docker compose up --build
