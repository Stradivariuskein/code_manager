from rest_framework import generics
from apps.core.models import Project, Container, ProjectFactory, PortainerApi
from .serializers import ProjectSerializer, ContainerSerializer, ProjectFactorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.portainer_token import get_p_token



class ProjectCreateView(APIView):

    def post(self, request):
        
        serializer = ProjectFactorySerializer(data=request.data)
        print("################################")
        print(request.data)
        print("################################")
        print(serializer.is_valid())
        if serializer.is_valid():
            # try:
            name = serializer.validated_data['name']

            password = serializer.validated_data.get('password', '123q123q')
            port = serializer.validated_data['port']
            enable_https = False #enable_https = serializer.validated_data['enable_https']
            print(f"""                      name: {name}
                    pass: {password}
                    port: {port}
                    https: {enable_https}""")
            factory = ProjectFactory()
            print("create factory")
            project = factory.create_project(name, password, port, enable_https)
            print("normal response")
            return Response({'status': 'Project created', 'project_id': project.id}, status=status.HTTP_201_CREATED)
        #     except Exception as e:
        #         print(f"Error creating project\n{e}")
        #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # print(serializer.errors)  # Imprimir errores del serializador
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectStartView(APIView):
    def post(self, request, id):
        # Lógica para iniciar el proyecto
        try:
            api = PortainerApi(apiToken=get_p_token())
            response = api.run_container(id)
            if response == True:
                return Response({'status': 'Project started'}, status=status.HTTP_200_OK)
            return Response({'error': str(response)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProjectStopView(APIView):
    def post(self, request, id):
        # Lógica para detener el proyecto
        try:
            api = PortainerApi(apiToken=get_p_token())
            response = api.stop_container(id)
            if response == True:
                return Response({'status': 'Project started'}, status=status.HTTP_200_OK)
            return Response({'error': str(response)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProjectRestartView(APIView):
    def post(self, request, id):
        # Lógica para reiniciar el proyecto
        try:
            api = PortainerApi(apiToken=get_p_token())
            response = api.restart_container(id)
            if response == True:
                return Response({'status': 'Project started'}, status=status.HTTP_200_OK)
            return Response({'error': str(response)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProjectDeleteView(APIView):
    def delete(self, request, id):
        
        # Lógica para eliminar el proyecto
        try:
            api = PortainerApi(apiToken=get_p_token())
            response = api.delete_container(id)
            print(response)
            if response == True:
                return Response({'status': 'Project deleted'}, status=status.HTTP_200_OK)
            return Response({'error': str(response)}, status=response)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        api = PortainerApi(apiToken=get_p_token())
        api.get_all() #  sincroniza el estado de los contenedores Docker con tu base de datos local
        
        # Luego llamamos al método 'list' que maneja la lógica de listado
        response = super().get(request, *args, **kwargs)
        return response



class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ContainerListCreate(generics.ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

class ContainerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
