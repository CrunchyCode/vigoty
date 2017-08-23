from django.conf.urls import url
from .views import LandingView, InicioView, RegistroView
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', LandingView.as_view(), name="landing"),
    url(r'^tienda$', login_required(InicioView.as_view()), name="tienda"),
    url(r'^registro$', RegistroView.as_view(), name="registro"),
    url(r'^login$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', logout, name='logout'),
]
