from django.conf.urls import url
from .views import LandingView, InicioView
from django.contrib.auth.views import (
    login, logout
)

urlpatterns = [
    url(r'^$', LandingView.as_view(), name="landing"),
    url(r'^tienda$', InicioView.as_view(), name="inicio"),
    url(r'^login$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', logout, name='logout'),
]
