from django.db.models import Sum
from rest_framework.generics import ListAPIView
from .serializers import PedidoListSerializer, VentasListSerializer
from apps.negocio.models import Menu
from ..models import Pedido


class PedidoListAPIView(ListAPIView):
    serializer_class = PedidoListSerializer

    def get_queryset(self):
        usuario = self.request.user
        queryset = Pedido.objects.filter(comprador=usuario)

        return queryset


class VentasListAPIView(ListAPIView):
    serializer_class = VentasListSerializer

    def get_queryset(self):
        usuario = self.request.user
        queryset = Menu.objects.filter(creador=usuario)

        for menu in queryset:
            cantidad = Pedido.objects.filter(
                        menu=menu).aggregate(Sum('cantidad'))['cantidad__sum']
            if cantidad:
                menu.cantidad_vendidos = cantidad
            else:
                menu.cantidad_vendidos = 0

        return queryset
