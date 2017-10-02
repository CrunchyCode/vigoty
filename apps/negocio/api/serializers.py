from rest_framework.serializers import ModelSerializer
from ..models import Menu


class MenuListSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'nombre',
            'precio',
        ]
