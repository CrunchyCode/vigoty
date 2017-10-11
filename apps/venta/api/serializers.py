from rest_framework.serializers import ModelSerializer
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
