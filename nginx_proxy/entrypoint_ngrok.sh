#!/bin/bash

# Archivo temporal para almacenar la salida de ngrok
echo ${IP_TO_HOST}
# Ejecuta ngrok en segundo plano y redirige la salida al archivo temporal
ngrok http ${IP_TO_HOST}:443 2>&1 1>/tmp/ngrok.log &


sleep 10
#obtiene el dominio dinamico
curl http://localhost:4040/api/tunnels > /usr/share/nginx/html/host.json

# Reemplaza variables de entorno en el archivo de configuración
envsubst '${WEB_SERVER_IP},${IP_TO_HOST}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf


nginx -g "daemon off;"

