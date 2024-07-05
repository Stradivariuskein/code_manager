# En la carpeta de la aplicación (por ejemplo, myapp/urls.py)
from django.urls import path #, re_path
from . import views
from apps.core.views import  dashboard
#from proxy.views import proxy_view
urlpatterns = [
    path("", dashboard, name="dashboard")
]
