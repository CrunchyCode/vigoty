from rest_framework.serializers import ModelSerializer
from apps.negocio.models import Menu
from ..models import Pedido


class PedidoListSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'cantidad',
            'subtotal',
            'total',
            'fecha_realizado',
        ]


class VentasListSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'nombre',
            'precio',
        ]
