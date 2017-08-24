from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import UsuarioForm, PerfilForm
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
        if request.user.is_authenticated():
            return redirect('tienda')
        else:
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


class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('tienda')
        else:
            return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        user = authenticate(
                    username=request.POST.get('email'),
                    password=request.POST.get('password')
                )
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('tienda')
        else:
            msg = 'Usuario no existe'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('login')


class PerfilView(TemplateView):
    def get(self, request, *args, **kwargs):
        perfil = Perfil.objects.get(usuario__email=request.user.email)

        return render(request, 'perfil.html', {'perfil': perfil})

    def post(self, request, *args, **kwargs):
        obj = Perfil.objects.get(usuario=request.user)
        form = PerfilForm(request.POST, instance=obj)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            try:
                perfil.imagen_perfil = request.FILES['imagen_perfil']
            except Exception:
                print("no hay imagen")
            perfil.save()
        else:
            msg = 'Datos de Perfil incorrectos'
            messages.add_message(request, messages.ERROR, msg)
            print(form.errors)

        return redirect('perfil')
