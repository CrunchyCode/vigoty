from django.conf.urls import url
from .views import PedidoListAPIView, VentasListAPIView

urlpatterns = [
    url(r'^pedidos/$', PedidoListAPIView.as_view(), name='api_pedidos'),
    url(r'^mis-ventas/$', VentasListAPIView.as_view(), name='api_ventas'),
]
