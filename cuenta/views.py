from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from .models import PerfilUsuario
from .serializers import PerfilUsuarioSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes

def login(request):

    if request.user.is_authenticated:
        return redirect('lista_entradas')

    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            print('logueado')
            auth_login(request, usuario)
            return redirect('lista_entradas')
        
    return render(request, 'cuenta/login.html')

def logouts(request):
    logout(request)
    return redirect('index')


class ListaUsuariosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios = PerfilUsuario.objects.filter(es_autor=True)
        # entradas = self.model.objects.all()
        serializer = PerfilUsuarioSerializer(usuarios, many=True)

        print('serializer.data', serializer.data)

        return Response(serializer.data, status= status.HTTP_200_OK)

class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):


        serializer = UserSerializer(data=request.data)

        if User.objects.filter(username=request.data['datos']['username']).exists():
            return Response({'error': 'El nombre de usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

        crear_usuario = User.objects.create_user(
            username=request.data['datos']['username'],
            password=request.data['datos']['password'],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated])
def editar_perfil(request):
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)

        if request.method == 'GET':
            return Response({
                "username": perfil.usuario.username,
                "first_name": perfil.usuario.first_name,  # corregido typo
                "last_name": perfil.usuario.last_name,
                "email": perfil.usuario.email,
                "avatar": perfil.avatar.url if perfil.avatar else None,
                "descripcion": perfil.descripcion,
                "es_autor": perfil.es_autor
            }, status=status.HTTP_200_OK)

        if request.method == 'PUT':
            data = request.data

            if 'descripcion' in data and data['descripcion'] != perfil.descripcion:
                perfil.descripcion = data['descripcion']

            if 'es_autor' in data:
                valor = str(data['es_autor']).lower()
                perfil.es_autor = True if valor == 'true' else False
            if 'avatar' in request.FILES:
                perfil.avatar = request.FILES['avatar']

            perfil.save()
            return Response({"mensaje": "Perfil editado correctamente"}, status=status.HTTP_200_OK)

    except PerfilUsuario.DoesNotExist:
        return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Error al editar el perfil: {e}"}, status=status.HTTP_400_BAD_REQUEST)