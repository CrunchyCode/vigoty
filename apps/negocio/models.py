from django.db import models
from django.contrib.auth.models import User
from apps.inicio.models import Direccion


class TipoPlato(models.Model):
    nombre = models.CharField(max_length=20)
    icono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class TipoEntrega(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


# DISPONIBLE
# 1 -> disponible
# 2 -> no disponible
# ESTADO
# 1 -> por validar
# 2 -> validado
class Menu(models.Model):
    fecha_disponibilidad = models.DateField()
    cantidad_maxima = models.IntegerField()
    nombre = models.CharField(max_length=45)
    breve_descripcion = models.CharField(max_length=80)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    tipo_entrega = models.ForeignKey(TipoEntrega)
    rango_hora = models.CharField(max_length=13)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)
    creador = models.ForeignKey(User)
    direccion = models.ForeignKey(Direccion)
    disponible = models.CharField(max_length=1, default="1")
    estado = models.CharField(max_length=1, default="1")

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    nombre = models.CharField(max_length=45)
    ingredientes = models.TextField()
    imagen = models.ImageField(upload_to='img-platos/')
    tipo_plato = models.ForeignKey(TipoPlato)
    creador = models.ForeignKey(User)

    def __str__(self):
        return self.nombre


# ESTADO
# 1 => activo
# 2 => eliminado
class DetalleMenuPlato(models.Model):
    plato = models.ForeignKey(Plato)
    menu = models.ForeignKey(Menu)
    estado = models.CharField(max_length=1, default="1")

    def __str__(self):
        return self.menu.nombre + ' - ' + self.plato.nombre
