from rest_framework.generics import ListAPIView
from .serializers import MenuListSerializer
from ..models import Menu


class MenuListAPIView(ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuListSerializer
