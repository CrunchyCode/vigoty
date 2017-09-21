from django.conf.urls import url, include
from .views import (
    LandingView, RegistroView, LoginView, PerfilView, DireccionView
)
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^registro$', RegistroView.as_view(), name='registro'),
    url(r'^perfil$', login_required(PerfilView.as_view()), name='perfil'),
    url(r'^direccion$',
        login_required(DireccionView.as_view()), name='direccion'),
    url('', include('social_django.urls', namespace='social')),
    url(r'^login$', LoginView.as_view(),
        kwargs={'redirect_authenticated_user': True}, name='login'),
    url(r'^logout$', logout, name='logout'),
]
