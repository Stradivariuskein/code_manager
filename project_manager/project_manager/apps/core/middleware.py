from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        # Lista de rutas que no requieren autenticación
        exempt_urls = [reverse('login'),reverse('send_port'),]# reverse('signup'), reverse('logout')]

        # Añadir más rutas que no requieran autenticación si es necesario
        if hasattr(settings, 'EXEMPT_URLS'):
            exempt_urls += [reverse(url) for url in settings.EXEMPT_URLS]

        print(exempt_urls)

        # Obtener la ruta actual
        current_path = request.path_info

        # Evitar el bucle de redirección
        if any(current_path.startswith(url) for url in exempt_urls):
            return None  # No requiere autenticación

        # Si la ruta actual no está en la lista de exenciones y el usuario no está autenticado
        try:
            if not request.user.is_authenticated:
                return redirect(reverse('login'))  # Redirigir a la página de inicio de sesión
        except:
            return redirect(reverse('login'))
        return None