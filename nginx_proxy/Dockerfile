# Usa la imagen base de nginx
FROM nginx:latest

# Copia el archivo entrypoint_ngrok.sh a /bin/entrypoint_ngrok.sh
COPY entrypoint_ngrok.sh /bin/entrypoint_ngrok.sh

# Instala ngrok
RUN apt-get update && \
    apt-get install -y curl gnupg2 && \
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && \
    apt-get install -y ngrok && \
    rm -rf /var/lib/apt/lists/*

RUN ngrok config add-authtoken 2gw0k2h1c7MU36CTDkTOproxVg2_3srKKmSGwhevP2bkrVtak

# Hacer el script ejecutable
RUN chmod +x /bin/entrypoint_ngrok.sh

CMD '/bin/entrypoint_ngrok.sh'


# Definir el entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
