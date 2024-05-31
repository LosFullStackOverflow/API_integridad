from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import Cliente, Estado


class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ClienteWithOutPasswordSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        exclude = ['password']


class EstadoSerializer(ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'
