FROM python:3.10-slim

ARG USER
ARG UID
ARG GID

ENV CODE_SERVER_VERSION 4.89.1
ENV HTTPS_ENABLED false
ENV APP_BIND_HOST 0.0.0.0
ENV APP_PORT 8080
ENV USER ${USER}
ENV UID ${UID}
ENV GID ${GID}

ENV NVM_DIR=/root/.nvm

RUN chmod 1777 /tmp

RUN apt update \
 && apt install \
    ca-certificates sudo curl dumb-init \
    htop locales git procps ssh vim \
    lsb-release wget openssl xz-utils -y \
  #&& curl -fsSL https://code-server.dev/install.sh | sh \
  && wget https://github.com/cdr/code-server/releases/download/v${CODE_SERVER_VERSION}/code-server_${CODE_SERVER_VERSION}_amd64.deb \
  && dpkg -i code-server_${CODE_SERVER_VERSION}_amd64.deb && rm -f code-server_${CODE_SERVER_VERSION}_amd64.deb \
  && rm -rf /var/lib/apt/lists/* \
  && pip install django requests pillow djangorestframework

# Instalar node
RUN curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o /usr/local/bin/n && \
    chmod +x /usr/local/bin/n && \
    n 14.17.1 && \
    n 20.0.0 \
    sudo npm install -g pnpm

RUN sed -i "s/# en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8

RUN chsh -s /bin/bash
ENV SHELL /bin/bash

RUN adduser --gecos '' --disabled-password coder \
  && echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd

RUN ARCH="$(dpkg --print-architecture)" \
  && curl -fsSL "https://github.com/boxboat/fixuid/releases/download/v0.4.1/fixuid-0.4.1-linux-$ARCH.tar.gz" | tar -C /usr/local/bin -xzf - \
  && chown root:root /usr/local/bin/fixuid \
  && chmod 4755 /usr/local/bin/fixuid \
  && mkdir -p /etc/fixuid \
  && printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

COPY bin/entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh

# # Crear directorios y cambiar permisos antes de cambiar al usuario coder
# RUN mkdir -p /home/coder/workspace \
#     && chown -R ${UID}:${GID} /home/coder

# Creating work directory and setting permissions
RUN mkdir -p /home/coder/workspace && \
    mkdir -p /home/coder/.local/share/code-server/User && \
    chown ${UID}:${GID} /home/coder/workspace && \
    chown -R ${UID}:${GID} /home/coder && \
    chown ${UID}:${GID} /home/coder/.*


USER 1000
ENV USER=coder
WORKDIR /home/coder

ENV EXTENSIONS="ms-python.python,tushortz.python-extended-snippets,andyyaldoo.vscode-json,redhat.vscode-yaml,vscode-icons-team.vscode-icons,Tim-Koehler.helm-intellisense,Equinusocio.vsc-material-theme,rogalmic.bash-debug,./pylance.vsix"
ENV LAB_REPO="${LAB_REPO:-none}"



# Copying settings.json file
#RUN cat > /home/coder/.local/share/code-server/User/settings.json << EOF "{workbench.colorTheme: Visual Studio Dark}" EOF
RUN echo '{ "workbench.colorTheme": "Default Dark+" }' >> /home/coder/.local/share/code-server/User/settings.json
COPY ./pylance.vsix ./pylance.vsix
# Installing extensions if specified
RUN if [ "${EXTENSIONS}" != "none" ]; then \
        echo "Installing Extensions" && \
        for extension in $(echo ${EXTENSIONS} | tr "," "\n"); do \
            if [ "${extension}" != "" ]; then \
                dumb-init /usr/bin/code-server --install-extension "${extension}" /home/coder; \
            fi; \
        done; \
    fi

RUN rm ./pylance.vsix

# Cloning repository if specified
RUN if [ "${LAB_REPO}" != "none" ]; then \
        cd /home/coder/workspace && \
        git clone ${LAB_REPO}; \
    fi


ENTRYPOINT ["/usr/bin/entrypoint.sh"]

