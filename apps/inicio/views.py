from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import UsuarioForm
from .models import Perfil


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


class RegistroView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registro.html')

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(email=request.POST.get('email'))
                msg = 'Usuario ya existe'
                messages.add_message(request, messages.ERROR, msg)
                return redirect('registro')
            except ObjectDoesNotExist:
                user = form.save(commit=False)
                user.username = request.POST.get('email')
                user.password = make_password(request.POST.get('password'))
                user.save()

                perfil = Perfil()
                perfil.usuario = user
                perfil.save()

                user = authenticate(
                    username=request.POST.get('email'),
                    password=request.POST.get('password')
                )
                login(request, user)

            return redirect('tienda')
        else:
            print(form.errors)
            msg = 'Datos incorrectos'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('registro')
