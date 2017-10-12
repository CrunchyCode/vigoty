from django.conf.urls import url
from .views import TiendaListAPIView, PlatoListAPIView, MenuListAPIView

urlpatterns = [
    url(r'^tienda/$', TiendaListAPIView.as_view(), name='api_tienda'),
    url(r'^platos/$', PlatoListAPIView.as_view(), name='api_platos'),
    url(r'^menus/$', MenuListAPIView.as_view(), name='api_menus'),
]
