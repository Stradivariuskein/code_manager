# Usa la imagen base de nginx
FROM nginx:latest

# Copia el archivo run.sh
COPY run.sh /bin/run.sh

# Hacer el script ejecutable
RUN chmod +x /bin/run.sh

CMD ["/bin/run.sh"]


# Definir el entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]



