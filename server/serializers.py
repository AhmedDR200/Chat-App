from rest_framework import serializers
from .models import Server, Category, Channel


class ServerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Server
        fields = '__all__'