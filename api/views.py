from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from base.models import Cliente
from .serializers import ClienteSerializer, ClienteWithOutPasswordSerializer


@api_view(['GET'])
def get_all(request):
    clientes = Cliente.objects.all()
    serializer = ClienteWithOutPasswordSerializer(clientes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_one(request, email):
    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return Response({'error': 'No existe el usuario'})
    serializer = ClienteWithOutPasswordSerializer(cliente, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create(request):
    serializer = ClienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)


@api_view(['POST'])
def update(request, email):
    # Using .get() to avoid KeyError if 'cliente' is not present
    clienteRequest = request.data.get('cliente', {})
    emailRequest = request.data.get('email', '')
    passwordRequest = request.data.get('password', '')
    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return Response({'error': 'No existe el usuario'})
    if emailRequest != cliente.email or passwordRequest != cliente.password:
        return Response({'error': 'No tienes los permisos para cambiar a este usuario'})
    serializer = ClienteSerializer(
        instance=cliente, data=clienteRequest)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)
