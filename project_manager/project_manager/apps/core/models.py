from django.db import IntegrityError, models, transaction
from project_manager.settings import PORTAINER_TOKEN, NETWORK_NAME
import requests
import json

# Create your models here.

# entidad contenedor (renduntante?)
class Container(models.Model):
    name = models.CharField(max_length=50, unique=True)
    dockerId = models.CharField(max_length=100, unique=True)
    imageId = models.CharField(max_length=50)
    ip = models.GenericIPAddressField(null=True)
    ports = models.CharField(max_length=400)
    status = models.CharField(max_length=50)
    
# maneja las peticiones acia la api
class PortainerApi(models.Model):
    apiToken = models.CharField(max_length=100)

    def send_request(self, path: str, method: str, headers: dict = {}, data: dict = None, params: dict = {}) -> dict:
        if path[0] == '/':
            path = path[1:]
        url = "https://192.168.2.115:9443/api/endpoints/2/docker/" + path
        headers["X-API-Key"] = self.apiToken

        try:
            if method.lower() == "get":
                
                response = requests.get(url, headers=headers, verify=False, params=params)
            elif method.lower() == "post":
                if data:
                    if "PortBindings" in data["HostConfig"]:
                        for port_binding in data['HostConfig']['PortBindings'].values():
                            for binding in port_binding:
                                binding['HostPort'] = str(binding['HostPort'])
                response = requests.post(url, headers=headers, json=data, params=params, verify=False)
            elif method.lower() == "delete":
                response = requests.delete(url, headers=headers, params=params, verify=False)
            else:
                raise ValueError(f"Error: método ({method}) no permitido")

            # Verificar el código de estado de la respuesta
            if response.status_code >= 400:
                raise Exception(f"Error en la solicitud: {response.status_code} {response.reason} {response.content}\ndata:\n{data}")

            # Verificar el tipo de contenido de la respuesta
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                return response

            data = response.content

            # Imprimir la respuesta para diagnóstico
            

            return json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            print(f"Contenido de la respuesta: {response.content}")
            raise
        except Exception as e:
            print(f"Error en la solicitud: {e}\ndata:\n {data}\n\n\n")
            raise

    def create_container(self, project_name: str, password: str, port: int, enable_https: bool=False) -> Container | None:
        if not project_name:
            raise Exception("Error: project_name param is requiered")
        if not password:
            password = "123q123q"
        if isinstance(port, int):
            if 10000 > port > 10100:
                raise Exception("Error: invalid port valis port: 10000 - 10099")
        if enable_https:
            print("##############################################\n")
            print("Warning: experimantal function, not working redy")
            print("##############################################\n")
        params = {"name": project_name}
        data = {
            
            "Image": "vscode:4.89.1-python3.10",
            "ExposedPorts": { "8080/tcp": {} },
            "HostConfig": {
                "NetworkMode": NETWORK_NAME,
                "PortBindings": { "8080/tcp": [{ "HostPort": port }] },
                "Binds": [
                    f"/home/mrkein/projects/{project_name}/workspace:/home/coder/workspace",
                    f"/home/mrkein/projects/{project_name}/config:/home/coder/.config",
                    f"/home/mrkein/projects/{project_name}/certs/cert.pem:/home/coder/.certs/cert.pem",
                ]
            },
            "Env": [
                f"PASSWORD={password}",
                "PATH=/home/coder/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                f"HTTPS_ENABLED={enable_https}",
                "APP_PORT=8080",
            ],
            "User": "1000:1000"
        }

        response = self.send_request("containers/create", "post", headers={}, data=data, params=params)
        print(f"\n\n+++++ response content +++++++++\n\n{response}\n\n")
        return response
   

    def run_container(self, container_id: str) -> bool:
        path = f"/containers/{container_id}/start"
        response = self.send_request(path, "post")
        if response.status_code == 204:
            return True
        return response.status_code
    
    def stop_container(self, container_id: str) -> bool:
        path = f"/containers/{container_id}/stop"
        response = self.send_request(path, "post")
        if response.status_code == 204:
            return True
        return response.status_code

    def restart_container(self, container_id: str) -> bool:
        path = f"/containers/{container_id}/restart"
        response = self.send_request(path, "post")
        if response.status_code == 204:
            return True
        return response.status_code

    def delete_container(self, container_id: str) -> bool:
        
        path =f"/containers/{container_id}"
        params = {"force": "true"}
        response = self.send_request(path,"delete",params=params)
        print(response)
        print(f"content: {response.content}")
        if response.status_code == 204:
            container = Container.objects.filter(dockerId=container_id).first()
            project = Project.objects.filter(container=container).first()
            container.delete()
            project.delete()
            return True
        return response.status_code


    # def update_container(self, container_id: str, settings: dict = None):
    #     pass

    def get_container(self, container_id: str) -> Container:
        path =f"containers/{container_id}/json"
        container = Container.objects.filter(dockerId=container_id).first()
        if not container:
            container = Container(dockerId=container_id)
        container_dic = self.send_request(path,"get")
        
        container.name = container_dic['Name']
        container.dockerId = container_dic['Id']
        container.imageId = container_dic['Image']
        if NETWORK_NAME in container_dic['NetworkSettings']['Networks']:
            container.ip = container_dic['NetworkSettings']['Networks'][NETWORK_NAME]['IPAddress']
        else:
            print(f"\n\n+++++ networks: {container_dic['NetworkSettings']['Networks']}")
            container.ip = None
        container.status = container_dic['State']['Status']
        container.ports = ''
        for _, ip_data in container_dic["NetworkSettings"]['Ports'].items():
            try:
                for current_ip in ip_data:
                    container.ports += f",{current_ip['HostPort']}"
            except KeyError:
                pass
        
        container.save()


        return container

    #obtiene todos los contenedores
    def get_all(self):
        #url = "https://192.168.2.115:9443/api/endpoints/2/docker/containers/json"
        path = "/containers/json"
        params = {"all":"true"}
        data = self.send_request(path, "get", params=params)

        containers = []

        for container in data:
            name = container['Names'][0]
            container_id = container['Id']
            imageId = container['ImageID']
            if NETWORK_NAME in  container['NetworkSettings']['Networks']:
                container_ip = container['NetworkSettings']['Networks'][NETWORK_NAME]['IPAddress']
            else:
                container_ip = None
            status = container['Status']
            ports = ''
            for ip_data in container['Ports']:
                try:
                    ports += f",{ip_data['PublicPort']}"
                except KeyError:
                    pass
            print(f"\n\n\n\tcontainer {name} id: {container_id}")
            existent_container = Container.objects.filter(name=name).first()
            
            if not existent_container:
                existent_container = Container.objects.filter(dockerId=container_id).first()
                if not existent_container:
                    print(f"\tno existe[{existent_container}]")
                    continue
                    new_container = Container(
                                            name=name,
                                            dockerId=container_id,
                                            imageId=imageId,
                                            ip=container_ip,
                                            ports=ports,
                                            status=status
                                        )
            if existent_container != None:
                print(f"\texistent container: {existent_container.name}\n\n\n")
                new_container = existent_container
                new_container.name = name
                new_container.dockerId = container_id
                new_container.imageId = imageId
                new_container.ip = container_ip
                new_container.ports = ports
                new_container.status = status

            try:
                new_container.save()
            except IntegrityError:
                new_container = Container.objects.filter(dockerId=container_id).first()
                if not new_container:
                    raise Exception(f"Error in database obtaining container {name}, id: {container_id}")
            except Exception as e:
                print(f"Error[{type(e).__name__}]: {e}")
            containers.append(new_container)
        return containers

class Project(models.Model):
    portApi = PortainerApi(apiToken=PORTAINER_TOKEN)
    name = models.CharField(max_length=50, unique=True)
    container = models.OneToOneField(Container, on_delete=models.CASCADE, null=True, blank=True)


    def run(self) -> bool:
        return self.portApi.run_container(self.container.dockerId)
        
    def stop(self) -> bool:
        return self.portApi.stop_container(self.container.dockerId)

    def delete_container(self) -> bool:
        return self.portApi.delete_contaier(self.container.dockerId)

    def deploy(self, id):
        pass # ajajaj


class ProjectFactory:

    @staticmethod
    def validate_port(port: int):
        if not (10000 <= port <= 10100):
            raise ValueError("Error: invalid port. Valid port range: 10000 - 10100")
        if Container.objects.filter(ports__contains=f",{port},").exists():
            container = Container.objects.filter(ports__contains=f",{port},").first()
            raise ValueError(f"Error: port {port} is already in use <br>{container.name}")

    def create_project(self, name: str, password: str, port: int, enable_https: bool = False) -> Project:
         with transaction.atomic():
            self.validate_port(port)

            portainer_api = PortainerApi(apiToken=PORTAINER_TOKEN)
            
            container_data = portainer_api.create_container(name, password, port, enable_https)
            # esto es para q cree las carpetas necesarioas primero hay q iniciarlo
            portainer_api.run_container(container_data['Id'])
            portainer_api.stop_container(container_data['Id'])
            print("\n\n++++++++ project create ++++++++\n\n")
            response = self.change_folders_owner()
            print(response)
            
            portainer_api.run_container(container_data['Id'])
            container = portainer_api.get_container(container_data['Id'])
            
            
            project = Project.objects.create(name=name, container=container)
            project.save()
            return project
    
    # create and add conteiner to database
    def save_container(self, name: str, container_data: json) -> Container:
        ports = ''
        initialized_container = True
        
        try:
            for _, ip_data in container_data["NetworkSettings"]['Ports'].items():
                for current_ip in ip_data:
                    ports += f",{current_ip['HostPort']}"
        except KeyError:
            initialized_container = False # todavia la maquia no se inicio se actualizara la informacion cuando se inicie

        container = Container.objects.create(
            name=name,
            dockerId=container_data['Id'],
            imageId=container_data['Image'],
            ip=container_data['NetworkSettings']['IPAddress'],
            ports=f",{ports},",
            status=container_data['State']['Status']
        )

        container.save()
        return container
    
    def change_folders_owner(self):
        # Datos de configuración para la creación del contenedor
        container_data = {
            "Image": "change_owner",
            "HostConfig": {
                "Binds": ["/home/mrkein/projects:/projects"],
                "AutoRemove": True  # Equivalente a --rm
            }
        }

        # Crear instancia de la API
        portainer_api = PortainerApi(apiToken=PORTAINER_TOKEN)

        # Crear contenedor
        try:
            create_response = portainer_api.send_request(
                path="containers/create",
                method="POST",
                data=container_data
            )
            container_id = create_response['Id']
            

            # Iniciar contenedor
            start_response = portainer_api.send_request(
                path=f"containers/{container_id}/start",
                method="POST"
            )
            

        except Exception as e:
            print(f"Error: {e}\n\n+++ response change owner: {start_response}\n\n")