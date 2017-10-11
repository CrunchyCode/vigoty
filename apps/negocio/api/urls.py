from django.conf.urls import url
from .views import TiendaListAPIView, PlatoListAPIView

urlpatterns = [
    url(r'^tienda/$', TiendaListAPIView.as_view(), name='api_tienda'),
    url(r'^platos/$', PlatoListAPIView.as_view(), name='api_platos'),
]
