from django.contrib import admin
from .models import Container, Project, ExposePort

# Register your models here.
admin.site.register(Container)
admin.site.register(ExposePort)
#admin.site.register(ExposePort)