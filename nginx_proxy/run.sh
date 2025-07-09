
# Reemplaza variables de entorno en el archivo de configuración
envsubst '${WEB_SERVER_IP},${IP_TO_HOST}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

nginx -g "daemon off;"
