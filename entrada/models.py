from django.db import models
from cuenta.models import PerfilUsuario
from django.utils.text import slugify
# Create your models here.

url_ruta = 'static/assets/imagenes'

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Entrada(models.Model):
    titulo = models.CharField('Título', max_length=100)
    imagen = models.ImageField('Imagen', upload_to=f'{url_ruta}/entradas')
    contenido = models.TextField('Contenido')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    categoria = models.ManyToManyField(Categoria, verbose_name='Categorias')
    autor = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, verbose_name='Autor')


    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)

        super(Entrada, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'