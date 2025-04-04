from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categorias-list', CategoriaViewSet)


urlpatterns = [
    path('<slug:slug>/', detalles_entrada, name='detalles_entrada'),
    path('lista/view', lista_entradas, name='lista_entradas'),
    path('editar/<int:id>/', editar_entrada, name='editar_entrada'),
    path('eliminar/<int:id>/', eliminar_entrada, name='eliminar_entrada'),
    path('crear/view', crear_entrada, name='crear_entrada'),

    # categorias

    path('categoria/lista/view', lista_categorias, name='lista_categorias'),
    path('categoria/editar/<int:id>/', editar_categoria, name='editar_categoria'),
    path('categoria/eliminar/<int:id>/', eliminar_categoria, name='eliminar_categoria'),
    path('categoria/crear/view', crear_categoria, name='crear_categoria'),

    # DRF

    path('api/entradas/', EntradaApiView.as_view(), name='api_entradas'),
    path('api/entradas/<int:pk>/', EntradaApiUpdate.as_view(), name='api_entradas_update'),
    path('api/entradas/<slug:slug>/', EntradaPorSlugView.as_view(), name='api_entradas_slug'),

    path('api/categorias/', CategoriaApiView.as_view(), name='api_categorias'),
    path('api/categorias/<int:pk>/', CategoriaApiUpdate.as_view(), name='api_categorias_update'),


    # api a react
    path('api/', include(router.urls)) 
]