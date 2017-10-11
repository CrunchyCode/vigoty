from django.conf.urls import url
from .views import PedidoListAPIView

urlpatterns = [
    url(r'^pedidos/$', PedidoListAPIView.as_view(), name='api_pedidos'),
]
