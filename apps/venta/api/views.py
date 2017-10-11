from rest_framework.generics import ListAPIView
from .serializers import PedidoListSerializer
from ..models import Pedido


class PedidoListAPIView(ListAPIView):
    serializer_class = PedidoListSerializer

    def get_queryset(self):
        usuario = self.request.user
        queryset = Pedido.objects.filter(comprador=usuario)

        return queryset
