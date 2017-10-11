from rest_framework.serializers import ModelSerializer
from ..models import Menu, Plato


class TiendaListSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'nombre',
            'precio',
        ]


class PlatoListSerializer(ModelSerializer):
    class Meta:
        model = Plato
        fields = [
            'nombre',
        ]
