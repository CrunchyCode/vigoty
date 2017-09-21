from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User)
    telefono = models.CharField(max_length=15)
    documento_identidad = models.CharField(max_length=8)
    imagen_perfil = models.ImageField(
            upload_to='img-profiles/', null=True, blank=True
        )

    def get_nombre_completo(self):
        return self.usuario.first_name + ' ' + self.usuario.last_name


class Direccion(models.Model):
    direccion_texto = models.CharField(max_length=140)
    referencia = models.TextField()
    street_number = models.CharField(max_length=6, blank=True, null=True)
    route = models.CharField(max_length=45, blank=True, null=True)
    locality = models.CharField(max_length=45, blank=True, null=True)
    administrative_area_level_2 = models.CharField(
                                        max_length=45, blank=True, null=True
                                    )
    administrative_area_level_1 = models.CharField(
                                        max_length=45, blank=True, null=True
                                    )
    country = models.CharField(max_length=45, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)
    usuario = models.ForeignKey(User)
    activo = models.BooleanField(default=True)
    seleccionada = models.BooleanField(default=False)

    def __str__(self):
        return self.direccion_texto
