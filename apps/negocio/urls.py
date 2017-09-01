from django.conf.urls import url
from .views import ListaPlatosView, PlatoView, PublicarMenuView, MenuView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^platos$', login_required(ListaPlatosView.as_view()), name='platos'),
    url(r'^platos/nuevo$',
        login_required(PlatoView.as_view()), name='nuevo-plato'),
    url(r'^platos/e/(?P<id>[\d]+)$',
        login_required(PlatoView.as_view()), name='editar-plato'),
    url(r'^publicar$',
        login_required(PublicarMenuView.as_view()), name="publicar-menu"),
    url(r'^publicar/e/(?P<id>[\d]+)$',
        login_required(PublicarMenuView.as_view()), name="editar-menu"),
    url(r'^menu$', login_required(MenuView.as_view()), name="menu"),
]
