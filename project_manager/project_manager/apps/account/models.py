from django.db import models
from django.contrib.auth.models import User

class PortainerToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='portainer_token',
        help_text="Usuario al que pertenece el token de Portainer"
    )
    token = models.CharField(
        max_length=255,
        help_text="Token de acceso generado por Portainer"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token de {self.user.username}"
