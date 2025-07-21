from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
#from django.http import HttpResponse, HttpResponseForbidden
#from proxy.views import proxy_view
import project_manager.settings as settings

from .models import Container, PortainerApi, Project, ExposePort, ProjectFactory
from apps.account.models import PortainerToken


def dashboard(request):
    # container = Container.objects.filter(name="/test_form").first()
    # if container:
    #     project_var = Project.objects.filter(container=container).first()
    #     container.delete()
    #     project_var.delete()

    print(f"view alowed host: {settings.ALLOWED_HOSTS}")
    return render(request,"dashboard.html")
from django.db.models import Max
class CreateExposePortView(View):
    def get(self, request):
        # ports = []
        # containers = Container.objects.all()
        # old_port = None
        # print("antes del for")
        # for container in containers:
        #     conteiner_ports = container.ports.rstrip(",").split(",") # obtiene el puerto
        #     print(conteiner_ports)
        #     if conteiner_ports == []:
        #         continue # si bo hay puerto no hay nada para hacer
        #     for port in conteiner_ports:
        #         if port != "":
        #             external_port = int(port)
        #             break
        #     else:
        #         continue # si bo hay puerto no hay nada para hacer

        #     print(f"container ports[{container.name}]: {container.ports}")
        #     print(f"external ports conteiner: {container.ports.rstrip(',').split(',')}")
        #     internal_port = 8080  # Puerto interno fijo

        #     # verfica q el puerto no este ya registrado
        #     print("se ejecuto o no la concha de tu madre")
        #     saved_ports = ExposePort.objects.filter(container=container)
        #     print(f"saved ports: {saved_ports}")
        #     exist_in_saved_ports = saved_ports.filter(external_port=external_port)
        #     print(f"saved port for[{external_port}]: {exist_in_saved_ports}")

        #     if exist_in_saved_ports:
        #         continue

        #     expose_port = ExposePort(
        #         external_port=external_port,
        #         internal_port=internal_port,
        #         container=container
        #     )

        #     try:
                
        #         expose_port.save()
        #         old_port = expose_port
        #         ports.append(expose_port)
                
        #     except Exception as e:
        #         print(old_port)
        #         print(expose_port)
        #         return JsonResponse({"error saving port": str(e)}, status=400)

        # return JsonResponse({"status": "success", "message": f"ExposePort entries created.<br>{ports}"})
        factory = ProjectFactory()
        response = factory.change_folders_owner()
        return JsonResponse({"status": "success", "message": f"{response.text}"})
    

