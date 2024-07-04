#!/bin/bash

# Archivo temporal para almacenar la salida de ngrok

# Ejecuta ngrok en segundo plano y redirige la salida al archivo temporal
ngrok http 172.22.0.2:443 2>&1 1>/tmp/ngrok.log &


sleep 10

curl http://localhost:4040/api/tunnels > /usr/share/nginx/html/host.json


nginx -g "daemon off;"

