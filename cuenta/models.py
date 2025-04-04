from django.db import models
from django.contrib.auth.models import User
# Create your models here.


url_ruta = 'static/assets/imagenes'


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=f'{url_ruta}/perfil', null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    es_autor = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'