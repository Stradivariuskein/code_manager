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
git clone https://github.com/tu-usuario/code_manager.git
cd code_manager

# 2. Construir y correr los contenedores
docker-compose up --build

# 3. Acceder al entorno de desarrollo
# Por defecto: http://localhost:8080
