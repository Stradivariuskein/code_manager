# En la carpeta de la aplicación (por ejemplo, myapp/urls.py)
from django.urls import path #, re_path
from . import views
from apps.core.views import  dashboard, CreateExposePortView
#from proxy.views import proxy_view
urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("tmpports/", CreateExposePortView.as_view(), name="tmp_create_ports")
]
