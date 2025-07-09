#!/bin/sh

# Directorio a verificar
DIR=/projects

# Verificar si hay archivos o carpetas con propietario root y cambiar permisos
if ls -lR $DIR | grep '^d' | grep 'root'; then
  echo "Changing ownership of directories from root to 1000:1000 in $DIR"
  chown -R 1000:1000 $DIR/*
else
  echo "No root-owned directories found in $DIR"
fi

# Salir del contenedor
exit 0
