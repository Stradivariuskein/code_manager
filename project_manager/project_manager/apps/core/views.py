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

import threading
from django.core.cache import cache
from .portainer_token import get_p_token
from datetime import timedelta
from django.utils.timezone import now

from .portainer_token import TIME_TO_DELETE

def delete_all():
    print("[+] Ejecutando delete_all")
    try:
        api = PortainerApi(apiToken=get_p_token())
        all_containers = api.get_all()
        for container in all_containers:
            api.delete_container(container.dockerId)

    except:
        pass
    cache.delete("deleteall_scheduled")  # Permitimos programar de nuevo después



def dashboard(request):

    # se verifica q la tarea no este programada para borrar todo
    if not cache.get("deleteall_scheduled"):
        print("[+] Programando delete_all dentro de 1 hora")
        delete_time = now() + timedelta(seconds=TIME_TO_DELETE)
        timer = threading.Timer(TIME_TO_DELETE, delete_all)  # 3600s = 1 hora
        timer.start()
        cache.set("deleteall_scheduled", True, timeout=TIME_TO_DELETE)
        cache.set("deleteall_time", delete_time.timestamp(), timeout=TIME_TO_DELETE)
    
    delete_time = cache.get("deleteall_time")

    context = {"delete_time": delete_time}
    print(f"view alowed host: {settings.ALLOWED_HOSTS}")
    return render(request,"dashboard.html", context)

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