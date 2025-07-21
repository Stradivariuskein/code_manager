from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views import View

from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.cache import cache
import os
import threading
import json

from .models import PortainerToken
from apps.core.portainer_token import TIME_TO_DELETE
class LoginOrRegisterView(LoginView):
    template_name = 'registration/login.html'
    next_page = 'dashboard'

    def get(self, request, *args, **kwargs):
        if not User.objects.exists():
            return render(request, 'registration/register.html')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not User.objects.exists():
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            token = request.POST.get('token') 

            # Validaciones básicas
            if not username or not password1 or not password2 or not token:
                messages.error(request, "Todos los campos son obligatorios.")
            elif password1 != password2:
                messages.error(request, "Las contraseñas no coinciden.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "El usuario ya existe.")
            else:
                # Crear usuario
                user = User.objects.create_user(username=username, password=password1)
                
                # Guardar el token de Portainer asociado
                PortainerToken.objects.create(user=user, token=token)
                # Lo actualizás en caché
                cache.set("portainer_token", token, timeout=TIME_TO_DELETE)

                # Autenticar
                login(request, user)
                return redirect(self.next_page)

            return render(request, 'registration/register.html')

        return super().post(request, *args, **kwargs)




def check_auth(request):
    if request.user.is_authenticated:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)
    
def firstinit(request):
    User = get_user_model()

    if User.objects.exists():
        return HttpResponseForbidden()
    else:
        return HttpResponse(status=200)
    



class ChangePortainerToken(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            token = data.get("token")
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        token_obj = PortainerToken.objects.first()
        if not token_obj:
            return JsonResponse({"error": "No existe un objeto PortainerToken"}, status=404)

        token_obj.token = token
        token_obj.save()

        cache.set("portainer_token", token, timeout=3600)

        return JsonResponse({"message": "Token actualizado correctamente"}, status=200)