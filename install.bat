@echo off
echo ===============================
echo Building all custom images...
echo ===============================

echo Building change_owner_image...
cd change_owner_image
call build.bat
cd..

echo Building code_server_image...
cd code_server_image
call build.bat
cd..

echo ===============================
echo Starting docker-compose stack...
echo ===============================
docker compose --project-name demo_code_manager up -d
