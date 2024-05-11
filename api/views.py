from rest_framework import status
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
    serializer = ClienteSerializer(cliente, many=False)
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
    # Using .get() to avoid KeyError if 'email', 'password', or 'newPassword' are not present
    email_request = request.data.get('email', '')
    password_request = request.data.get('password', '')
    new_password_request = request.data.get('newPassword', '')

    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)

    if email_request != cliente.email or password_request != cliente.password:
        return Response({'error': 'No tienes los permisos para cambiar a este usuario'}, status=status.HTTP_403_FORBIDDEN)

    if new_password_request != '':
        cliente.password = new_password_request
        cliente.save()
        serializer = ClienteSerializer(cliente, many=False)
        return Response(serializer.data)
    else:
        return Response({'error': 'No se ha enviado la nueva contraseña'}, status=status.HTTP_400_BAD_REQUEST)
