#!/bin/sh
set -eu

export PS1='\w $ '

EXTENSIONS="${EXTENSIONS:-none}"
LAB_REPO="${LAB_REPO:-none}"

eval "$(fixuid -q)"



if [ "${DOCKER_USER-}" ]; then
  echo "$DOCKER_USER ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/nopasswd > /dev/null
  sudo usermod --login "$DOCKER_USER" coder
  sudo groupmod -n "$DOCKER_USER" coder
  USER="$DOCKER_USER"
  sudo sed -i "/coder/d" /etc/sudoers.d/nopasswd
fi



if [ ${HTTPS_ENABLED} = "true" ]
  then
    dumb-init /usr/bin/code-server \
      --bind-addr "${APP_BIND_HOST}":"${APP_PORT}" \
      --cert /home/coder/.certs/cert.pem \
      --cert-key /home/coder/.certs/key.pem \
      /home/coder/workspace
else
    dumb-init /usr/bin/code-server \
      --bind-addr "${APP_BIND_HOST}":"${APP_PORT}" \
      /home/coder/workspace
fi
