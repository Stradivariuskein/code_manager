# Usar una imagen base mínima
FROM alpine:latest

# Copiar el script que cambiará los permisos
COPY change_owner.sh /usr/local/bin/change_owner.sh

# Dar permisos de ejecución al script
RUN chmod +x /usr/local/bin/change_owner.sh

USER root

# Establecer el comando predeterminado
CMD ["/usr/local/bin/change_owner.sh"]



