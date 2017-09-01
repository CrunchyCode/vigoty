from django.conf.urls import url
from .views import TiendaView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^tienda$', login_required(TiendaView.as_view()), name='tienda'),
]
