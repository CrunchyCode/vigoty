from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Perfil


def guardar_perfil(backend, user, response, details, *args, **kwargs):
    if backend.name == 'facebook':
        existe = User.objects.filter(email=user.email).exists()
        if not existe:
            user.username = user.email
            user.save()

        try:
            Perfil.objects.get(usuario__email=user.email)
        except ObjectDoesNotExist:
            per = Perfil()
            per.usuario = user
            per.save()
