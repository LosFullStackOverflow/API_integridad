import base64
import random
import string
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from base.models import Cliente, Estado
from .serializers import ClienteSerializer, EstadoSerializer

apiUrlMachine = "127.0.0.1:5000"


def getKey(email: str):
    api_url = f'http://{apiUrlMachine}/users/{email}/key/'
    response = requests.get(api_url)

    if response.ok:
        try:
            response_data = response.json()
            key = response_data.get('key')
            if not key:
                raise ValueError("Key not found in response")
            print(f"Key retrieved: {key}")
        except (ValueError, KeyError):
            print("Error parsing JSON response")
            key = None
        return key
    return None


@api_view(['GET'])
def get_all(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)


def generar_clave(longitud, clave):
    random.seed(clave)
    return [random.randint(0, 255) for _ in range(longitud)]


def cifrar_numero(numero, clave):
    if clave % 3 == 0:
        clave = -clave/100
    return ((numero + round((clave*clave)/23, 2))/clave)

# Función para descifrar números


def descifrar_numero(numero_cifrado: float, clave: int):
    if clave % 3 == 0:
        clave = -clave*100
    return round(numero_cifrado * clave - round((clave*clave)/23, 2))


def cifrarCadena(texto, clave):
    clave_cifrado = generar_clave(len(texto), clave)
    texto_cifrado = []
    for i, char in enumerate(texto):
        valor_cifrado = (ord(char) + clave_cifrado[i]) % 256
        texto_cifrado.append(chr(valor_cifrado))
    texto_cifrado = ''.join(texto_cifrado)
    # Codificamos el texto cifrado en base64 para asegurar compatibilidad con bases de datos
    texto_cifrado_base64 = base64.b64encode(
        texto_cifrado.encode('utf-8')).decode('utf-8')
    return texto_cifrado_base64


def descifrarCadena(texto_cifrado_base64, clave):
    # Decodificamos el texto cifrado en base64
    texto_cifrado = base64.b64decode(
        texto_cifrado_base64.encode('utf-8')).decode('utf-8')
    clave_descifrado = generar_clave(len(texto_cifrado), clave)
    texto_descifrado = []
    for i, char in enumerate(texto_cifrado):
        valor_descifrado = (ord(char) - clave_descifrado[i]) % 256
        texto_descifrado.append(chr(valor_descifrado))
    return ''.join(texto_descifrado)


def desCifrarCliente(cliente, key):
    cliente.nombre = descifrarCadena(cliente.nombre, key)
    cliente.apellido = descifrarCadena(cliente.apellido, key)
    cliente.pais = descifrarCadena(cliente.pais, key)
    cliente.ciudad = descifrarCadena(cliente.ciudad, key)
    cliente.celular = descifrarCadena(cliente.celular, key)
    cliente.email = descifrarCadena(cliente.email, key)
    cliente.password = descifrarCadena(cliente.password, key)
    cliente.actividadEconomica = descifrarCadena(
        cliente.actividadEconomica, key)
    cliente.empresa = descifrarCadena(cliente.empresa, key)
    cliente.ingresos = descifrar_numero(float(cliente.ingresos), key)
    cliente.pasivos = descifrar_numero(float(cliente.pasivos), key)
    return cliente


def desCifrarEstado(estado, key):
    estado.email = descifrarCadena(estado.email, key)
    estado.estado = descifrarCadena(estado.estado, key)
    return estado


@api_view(['GET'])
def get_one(request, email):
    try:
        key = getKey(email)
        if not key:
            return Response({'error': 'No existe el usuario'})
        email = cifrarCadena(email, key)
        cliente = Cliente.objects.get(email=email)
        cliente = desCifrarCliente(cliente, key)

    except Cliente.DoesNotExist:
        return Response({'error': 'No existe el usuario'})
    serializer = ClienteSerializer(cliente, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def get_estadoPOST(request, email):
    try:
        key = getKey(email)
        if not key:
            return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)

        email_cifrado = cifrarCadena(email, key)
        try:
            estado = Estado.objects.get(email=email_cifrado)
        except Estado.DoesNotExist:
            estado = Estado(email=email_cifrado, estado='vacio')

        # Utiliza request.data para obtener los datos del cuerpo de la solicitud
        estadoReq = request.data.get('estado')
        estado.estado = cifrarCadena(estadoReq, key)

        estado.save()  # Guarda el objeto Estado en la base de datos

        # Crea el serializer con el objeto Estado
        serializer = EstadoSerializer(estado)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_estado(request, email):
    try:
        key = getKey(email)
        if not key:
            return Response({'error': 'No existe el usuario'})
        email = cifrarCadena(email, key)
        estado = Estado.objects.get(email=email)
        estado = desCifrarEstado(estado, key)

    except Estado.DoesNotExist:
        return Response({'error': 'No existe el usuario'})
    serializer = EstadoSerializer(estado, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create(request):
    if 'email' not in request.data:
        return Response({"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()  # Create a copy of the request data
    email = data.get('email')

    api_url = f'http://{apiUrlMachine}/users/{email}/key/'
    response = requests.get(api_url)

    if response.ok:
        try:
            response_data = response.json()
            key = response_data.get('key')
            if not key:
                raise ValueError("Key not found in response")
            print(f"Key retrieved: {key}")
        except (ValueError, KeyError):
            print("Error parsing JSON response")
            key = None
    else:
        url = f'http://{apiUrlMachine}/users/add/'
        key = random.randrange(1000, 10000)
        payload = {'email': email, 'key': key}
        add_response = requests.post(url, json=payload)
        if not add_response.ok:
            return Response({"error": "Failed to add user and retrieve key"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data['nombre'] = cifrarCadena(data['nombre'], key)
        data['apellido'] = cifrarCadena(data['apellido'], key)
        data['pais'] = cifrarCadena(data['pais'], key)
        data['ciudad'] = cifrarCadena(data['ciudad'], key)
        data['celular'] = cifrarCadena(str(data['celular']), key)
        data['email'] = cifrarCadena(data['email'], key)
        data['password'] = cifrarCadena(data['password'], key)
        data['actividadEconomica'] = cifrarCadena(
            data['actividadEconomica'], key)
        data['empresa'] = cifrarCadena(data['empresa'], key)
        data['ingresos'] = cifrar_numero(data['ingresos'], key)
        data['pasivos'] = cifrar_numero(data['pasivos'], key)
    except KeyError as e:
        return Response({"error": f"Missing field: {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ClienteSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response("usuario ya existe", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update(request, email):
    # Using .get() to avoid KeyError if 'email', 'password', or 'newPassword' are not present
    email_request = request.data.get('email', '')
    password_request = request.data.get('password', '')
    new_password_request = request.data.get('newPassword', '')

    key = getKey(email_request)

    if not (key):
        print('no hay key')
        return Response({'error': 'No tienes los permisos para cambiar a este usuario'}, status=status.HTTP_403_FORBIDDEN)
    email = cifrarCadena(email, key)
    passwordCifrada = cifrarCadena(password_request, key)
    new_passwordCifrada = cifrarCadena(new_password_request, key)
    try:
        cliente = Cliente.objects.get(email=email)
    except Cliente.DoesNotExist:
        return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)

    if email != cliente.email or passwordCifrada != cliente.password:
        return Response({'error': 'No tienes los permisos para cambiar a este usuario'}, status=status.HTTP_403_FORBIDDEN)

    if new_passwordCifrada != '':
        cliente.password = new_passwordCifrada
        cliente.save()
        serializer = ClienteSerializer(cliente, many=False)
        return Response(serializer.data)
    else:
        return Response({'error': 'No se ha enviado la nueva contraseña'}, status=status.HTTP_400_BAD_REQUEST)
