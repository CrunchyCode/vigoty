from django.contrib import admin
from .models import TipoPlato, TipoEntrega, Menu, Plato, DetalleMenuPlato

admin.site.register(TipoPlato)
admin.site.register(TipoEntrega)
admin.site.register(Menu)
admin.site.register(Plato)
admin.site.register(DetalleMenuPlato)
