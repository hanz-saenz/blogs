from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Entrada, Categoria
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from .forms import EntradaForm, CategoriaForm

def index(request):
    entradas = Entrada.objects.all()
    categorias = Categoria.objects.all()
    # filtro una categoría

    if request.GET.getlist('categoria'):
        filtro = Q()
        for categoria_id in request.GET.getlist('categoria'):
            if categoria_id != '0':
                filtro |= Q(categoria__id=categoria_id)
        
        entradas = Entrada.objects.filter(filtro).distinct()

    context = {
        'entradas': entradas,
        'categorias': categorias
    }
    return render(request, 'index.html', context)


def detalles_entrada(request, slug):
    
    entrada = get_object_or_404(Entrada, slug=slug)
    context = {
        'entrada': entrada
    }

    return render(request, 'blogs/detalles_entrada.html', context)



@login_required
def lista_entradas(request):
    entradas = Entrada.objects.all()
    categorias = Categoria.objects.all()
    # filtro una categoría
    if request.GET.get('categoria'):
        if request.GET.get('categoria') != '0':
            entradas = Entrada.objects.filter(categoria__id=request.GET.get('categoria'))


    #filtro varias categorías
    if request.GET.getlist('categoria'):
        filtro = Q()
        for categoria_id in request.GET.getlist('categoria'):
            filtro |= Q(categoria__id=categoria_id)

        entradas = Entrada.objects.filter(filtro)


    context = {
        'entradas': entradas,
        'categorias': categorias
    }
    return render(request, 'blogs/lista_entradas.html', context)


#editar entradas

@login_required
def editar_entrada(request, id):
    entrada = get_object_or_404(Entrada, id=id)

    if request.method == 'POST':
        form = EntradaForm(request.POST, request.FILES, instance=entrada)
        print('request.FILES', request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_entradas')
        
    else:
        form = EntradaForm(instance=entrada)

    context = {
        'form': form,
        'entrada': entrada
    }
    return render(request, 'blogs/editar_entrada.html', context)

# eliminar entradas
@login_required
def eliminar_entrada(request, id):
    entrada = get_object_or_404(Entrada, id=id)
    entrada.delete()
    return redirect('lista_entradas')


#creat entradas
@login_required
def crear_entrada(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_entradas')
    else:
        form = EntradaForm()

    context = {
        'form': form
    }
    return render(request, 'blogs/crear_entrada.html', context)


#CATEGORÍAS

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()

    context = {
        'form': form
    }
    return render(request, 'blogs/categorias/crear_categoria.html', context)


@login_required
def editar_categoria(request, id):
    entrada = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
        
    else:
        form = CategoriaForm(instance=entrada)

    context = {
        'form': form,
        'categoria': entrada
    }
    return render(request, 'blogs/categorias/editar_categoria.html', context)

# eliminar entradas
@login_required
def eliminar_categoria(request, id):
    entrada = get_object_or_404(Categoria, id=id)
    entrada.delete()
    return redirect('lista_categorias')


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias
    }
    return render(request, 'blogs/categorias/lista_categorias.html', context)


# ------------------------------------- DRF ------------------------------------------

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from .serializers import EntradaSerializer, CategoriaSerializer
from rest_framework.permissions import IsAuthenticated

class EntradaApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        entradas = Entrada.objects.all()
        # entradas = self.model.objects.all()
        serializer = EntradaSerializer(entradas, many=True)

        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request):
        categorias = request.data['categorias']
        titulo = request.data['titulo']
        contenido = request.data['contenido']
        autor = request.data['autor']
        imagen = request.data['imagen']

        entrada = Entrada(titulo=titulo, contenido=contenido, autor_id=autor, imagen=imagen)
        entrada.save()

        id_categorias = categorias.split(',')
             
        for categoria_id in id_categorias:
            entrada.categoria.add(categoria_id)

        serializer = EntradaSerializer(entrada)

        return Response(serializer.data, status= status.HTTP_201_CREATED)



class EntradaApiUpdate(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        entrada = get_object_or_404(Entrada, pk=pk)
        serializer = EntradaSerializer(entrada)

        return Response(serializer.data, status= status.HTTP_200_OK)

    def put(self, request, pk):
        entrada = get_object_or_404(Entrada, pk=pk)
        print('pk', pk)

        if entrada is not None:
            print('request.data', request.data)
            categorias = request.data.get('categorias', '')
            titulo = request.data.get('titulo', entrada.titulo)
            contenido = request.data.get('contenido', entrada.contenido)
            autor = request.data.get('autor', entrada.autor_id)
            nueva_imagen = request.data.get('imagen', 'undefined')  # Obtener imagen

            # 📌 Solo actualizar la imagen si es diferente de la guardada
            if nueva_imagen != '/undefined'  or nueva_imagen != 'undefined' and nueva_imagen != str(entrada.imagen):
                entrada.imagen = nueva_imagen

       
            entrada.titulo = titulo
            entrada.contenido = contenido
            entrada.autor_id = autor
            entrada.save()

            # 📌 Actualizar categorías solo si se proporcionan
            if categorias:
                entrada.categoria.clear()  # Eliminar categorías anteriores
                id_categorias = categorias.split(',')
                entrada.categoria.add(*id_categorias)  # Agregar nuevas categorías

            serializer = EntradaSerializer(entrada)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'No existe la Entrada'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        entrada = get_object_or_404(Entrada, pk=pk)
        if entrada is not None:
            entrada.delete()
            return Response({'message': 'Entrada eliminada'}, status= status.HTTP_200_OK)

        return Response({'message': 'No existe la Entrada'}, status= status.HTTP_404_NOT_FOUND)



class CategoriaApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategoriaSerializer(data= request.data)
        print('request.data', request.data)
        print('serializer.is_valid():', serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class CategoriaApiUpdate(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        categorias = get_object_or_404(Categoria, pk=pk)
        
        serializer = CategoriaSerializer(categorias)

        return Response(serializer.data, status= status.HTTP_200_OK)

    def put(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        if categoria is not None:
            serializer = CategoriaSerializer(categoria, data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_200_OK)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No existe la categoria'}, status= status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        if categoria is not None:
            categoria.delete()
            return Response({'message': 'Categoria eliminada'}, status= status.HTTP_200_OK)

        return Response({'message': 'No existe la categoria'}, status= status.HTTP_404_NOT_FOUND)


from rest_framework import viewsets, permissions

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # permission_classes = [permissions.IsAuthenticated]


class EntradaPorSlugView(APIView):
    def get(self, request, slug):
        entrada = get_object_or_404(Entrada, slug=slug)
        serializer = EntradaSerializer(entrada)
        return Response(serializer.data, status= status.HTTP_200_OK)