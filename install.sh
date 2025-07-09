#!/bin/bash
set -e

echo "==============================="
echo "Building all custom images..."
echo "==============================="

echo "Building change_owner_image..."
cd change_owner_image
chmod +x build.sh
./build.sh
cd ..

echo "Building code_server_image..."
cd code_server_image
chmod +x build.sh
./build.sh
cd ..

echo "==============================="
echo "Starting docker-compose stack..."
echo "==============================="
docker compose up -d
