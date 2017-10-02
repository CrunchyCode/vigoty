from django.conf.urls import url
from .views import MenuListAPIView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^menus/$',
        login_required(MenuListAPIView.as_view()), name='api_menus'),
]
