from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from .models import PerfilUsuario
from .serializers import PerfilUsuarioSerializer
from rest_framework.permissions import IsAuthenticated


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
