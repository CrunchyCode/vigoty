from django.conf.urls import url
from .views import MenuListAPIView

urlpatterns = [
    url(r'^menus/$', MenuListAPIView.as_view(), name='api_menus'),
]
