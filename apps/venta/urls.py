from django.conf.urls import url, include
from .views import (
    TiendaView, TiendaProductoView, VentaView,
    MisPedidosView, MisVentasView, PedidoDetalleView
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^api/', include('apps.venta.api.urls'), name='api'),

    url(r'^tienda$',
        login_required(TiendaView.as_view()), name='tienda'),
    url(r'^tienda/(?P<id>[\d]+)$',
        login_required(TiendaProductoView.as_view()), name="tienda-detalle"),
    url(r'^tienda/f/(?P<date>\d{4}-\d{2}-\d{2})$',
        login_required(TiendaView.as_view()), name='tienda-filtro'),
    url(r'^venta$', login_required(VentaView.as_view()), name="venta"),
    url(r'^mis-pedidos$',
        login_required(MisPedidosView.as_view()), name="mis-pedidos"),
    url(r'^mis-pedidos/(?P<id>[\d]+)$',
        login_required(PedidoDetalleView.as_view()), name="pedido-detalle"),
    url(r'^mis-ventas$',
        login_required(MisVentasView.as_view()), name="mis-ventas"),
]
