from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    documento_identidad = models.CharField(max_length=8)
    imagen_perfil = models.ImageField(
            upload_to='img-profiles/', null=True, blank=True
        )

    def get_nombre_completo(self):
        return self.usuario.first_name + ' ' + self.usuario.last_name
