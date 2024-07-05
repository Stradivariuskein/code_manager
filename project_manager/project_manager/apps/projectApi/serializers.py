from rest_framework import serializers
from apps.core.models import Project, Container

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    container = ContainerSerializer()  # Incluir el serializador del contenedor

    class Meta:
        model = Project
        fields = '__all__'

class ProjectFactorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, required=False, allow_blank=True)
    port = serializers.IntegerField()
    enable_https = serializers.BooleanField(default=False, required=False)