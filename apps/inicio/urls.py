from django.conf.urls import url
from .views import LandingView, InicioView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name="landing"),
    url(r'^$', InicioView.as_view(), name="inicio"),
]
