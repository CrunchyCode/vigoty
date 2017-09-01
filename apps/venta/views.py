from django.shortcuts import render
from django.views.generic import TemplateView


class TiendaView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'tienda.html')

    def post(self, request, *args, **kwargs):
        pass
