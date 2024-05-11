from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from base.models import Cliente


class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ClienteWithOutPasswordSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        exclude = ['password']
