from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
#from django.http import HttpResponse, HttpResponseForbidden
#from proxy.views import proxy_view
import project_manager.settings as settings

from .models import Container, PortainerApi, Project


def dashboard(request):
    # container = Container.objects.filter(name="/test_form").first()
    # if container:
    #     project_var = Project.objects.filter(container=container).first()
    #     container.delete()
    #     project_var.delete()
    print(f"view alowed host: {settings.ALLOWED_HOSTS}")
    return render(request,"dashboard.html")

