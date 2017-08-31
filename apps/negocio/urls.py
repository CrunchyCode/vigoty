from django.conf.urls import url
from .views import ListaPlatosView, PlatoView, PublicarMenuView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^platos$', login_required(ListaPlatosView.as_view()), name='platos'),
    url(r'^platos/nuevo$',
        login_required(PlatoView.as_view()), name='nuevo_plato'),
    url(r'^platos/e/(?P<id>[\d]+)$',
        login_required(PlatoView.as_view()), name='editar_plato'),
    url(r'^publicar$',
        login_required(PublicarMenuView.as_view()), name="publicar-menu"),
]
