from django.urls import path
from .views import send_token, send_port

urlpatterns = [
    path('', send_token, name="whatsapp_api"),
    path('send_port/', send_port, name="send_port")
]