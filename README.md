# 🧠 code_manager

**Entorno de desarrollo remoto multiplataforma** basado en Docker, que permite ejecutar proyectos en Python/Django directamente desde el navegador usando `code-server` (VSCode en el browser).

---

## 🚀 Descripción

`code_manager` es una herramienta que replica un entorno de desarrollo como GitHub Codespaces pero en local o en servidores propios. Está pensada para facilitar la edición y ejecución de proyectos desde cualquier dispositivo, sin necesidad de configurar el entorno manualmente.

Ideal para pruebas rápidas, desarrollo remoto, demostraciones o entornos de enseñanza.

---

## 📸 Captura de pantalla

### Dashboar
![Vista del entorno](ilustrations/code_manager_dashboard_ilustration.png)


### Editor
![Vista del entorno](ilustrations/code_server_ilustration.png)


---

## 🛠️ Tecnologías utilizadas

- 🐍 Python
- 🌐 Django
- 🐳 Docker
- 🧩 code-server (VSCode en navegador)
- ⚙️ Nginx
- 🐘 SQLite 

---

## ✅ Requisitos

- Docker
- Docker Compose
- Navegador web moderno

---


## ⚙️ Instalación y uso

```bash
# 1. Clonar el repositorio
git clone https://github.com/Stradivariuskein/code_manager
cd code_manager

# 2. Construir y correr los contenedores 
# Windows:
install.bat

# Linux:
install.sh

# 3. Acceder al entorno de desarrollo
# Por defecto: http://localhost:10443
```

---

## 🧩 Versiones disponibles

El proyecto cuenta con **dos versiones**:

- `master`: versión normal.
- `demo`: versión demostración.

### 🔧 Instalación de la versión demo

#### ✅ Si ya tenés la versión normal instalada:

Instalá la rama `demo` de forma normal, siguiendo los pasos anteriores.

#### ⚠️ Si instalás **solo** la demo (sin tener la versión normal):

1. **Cloná la rama demo** en un entorno separado:

```bash
git clone -b demo https://github.com/Stradivariuskein/code_manager code_manager_demo
cd code_manager_demo
```

2. **Modificá el archivo `docker-compose.yml`**:

- **Descomentá** el bloque del servicio `portainer`:

```yaml
  portainer:
    image: portainer/portainer-ce
    container_name: portainer
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    ports:  
      - "9443:9443"
    networks:
      manager:
        ipv4_address: 172.32.0.4  # <-- recordá esta IP
```

- **Actualizá la IP de `PORTAINER_IP`** en la sección `demo_web`:

```yaml
  demo_web:
    build:
      context: ./project_manager
    restart: always
    volumes:
      - ./project_manager:/app
    depends_on:
      - demo_nginx_proxy
      #- portainer
    networks:
      manager:
        ipv4_address: 172.32.0.3
      code_manager_manager:
        ipv4_address: 172.22.0.10
    environment:
      - PROXY_IP=172.32.0.2
      - PORTAINER_IP=172.22.0.4  # <-- cambiá esta IP
```

3. **Ejecutá el script de instalación** normalmente:

```bash
# Windows:
install.bat

# Linux:
install.sh
```
