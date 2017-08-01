from django.shortcuts import render
from django.views.generic import TemplateView


class LandingView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing.html')

    def post(self, request, *args, **kwargs):
        pass


class InicioView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

    def post(self, request, *args, **kwargs):
        pass
