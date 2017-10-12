from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView
from .serializers import (
    TiendaListSerializer, PlatoListSerializer, MenuListSerializer
)
from ..models import Menu, Plato
from apps.inicio.models import Direccion
from apps.metodos_globales import getDataDireccion


class TiendaListAPIView(ListAPIView):
    serializer_class = TiendaListSerializer

    def get_queryset(self):
        queryset = Menu.objects.filter(disponible='1', estado='2')

        usuario = self.request.user

        try:
            direccion = Direccion.objects.get(
                usuario=usuario, activo=True, seleccionada=True
            ).direccion_texto
        except ObjectDoesNotExist:
            direccion = None

        if direccion is not None:
            hoy = datetime.now()
            mañana = hoy + timedelta(days=1)
            fec_filtro = mañana
            queryset = getDataDireccion(direccion, queryset, fec_filtro)
        else:
            queryset = None

        return queryset


class PlatoListAPIView(ListAPIView):
    serializer_class = PlatoListSerializer

    def get_queryset(self):
        usuario = self.request.user

        queryset = Plato.objects.filter(creador=usuario)

        return queryset


class MenuListAPIView(ListAPIView):
    serializer_class = MenuListSerializer

    def get_queryset(self):
        usuario = self.request.user

        queryset = Menu.objects.filter(creador=usuario)

        return queryset
