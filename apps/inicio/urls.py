from django.conf.urls import url
from .views import LandingView, InicioView, RegistroView, LoginView, PerfilView
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^tienda$', login_required(InicioView.as_view()), name='tienda'),
    url(r'^registro$', RegistroView.as_view(), name='registro'),
    url(r'^perfil$', login_required(PerfilView.as_view()), name='perfil'),
    url(r'^login$', LoginView.as_view(),
        kwargs={'redirect_authenticated_user': True}, name='login'),
    url(r'^logout$', logout, name='logout'),
]
