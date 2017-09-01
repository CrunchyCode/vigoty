from django.db import models
from django.contrib.auth.models import User
from apps.negocio.models import Menu

'''
    ESTADOS
    1 -> por confirmar => CARRITO
    2 -> pagado
    3 -> confirmacion completa
    4 -> satisfecho
'''


class Pedido(models.Model):
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_realizado = models.DateField(auto_now=True)
    estado = models.CharField(max_length=1, default='1')
    comprador = models.ForeignKey(User)
    menu = models.ForeignKey(Menu)
