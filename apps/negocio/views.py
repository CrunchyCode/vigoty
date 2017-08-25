from django.shortcuts import render, redirect
# from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from apps.inicio.models import Perfil
from .models import Plato, TipoPlato
from .forms import PlatoForm


class ListaPlatosView(TemplateView):
    def get(self, request, *args, **kwargs):
        platos = Plato.objects.filter(creador=request.user)
        return render(
            request,
            'lista_platos.html', {'platos': platos}
        )

    def post(self, request, *args, **kwargs):
        pass


class PlatoView(TemplateView):
    def get(self, request, *args, **kwargs):
        perfil = Perfil.objects.get(usuario=request.user)
        try:
            plato = get_object_or_404(Plato, pk=kwargs['id'])
        except KeyError:
            plato = None
        tipos_plato = TipoPlato.objects.all()
        return render(
            request,
            'plato.html',
            {
                'perfil': perfil,
                'tipos_plato': tipos_plato,
                'plato': plato
            }
        )

    def post(self, request, *args, **kwargs):
        try:
            # EDICION DE PLATO
            plato = get_object_or_404(
                Plato, pk=kwargs['id'], creador=request.user
            )
            try:
                plato.imagen = request.FILES['imagen']
            except Exception:
                pass
            form = PlatoForm(
                request.POST or None, request.FILES, instance=plato
            )
            if form.is_valid():
                menu = form.save()
            else:
                msg = 'Edicion invalida'
                messages.add_message(request, messages.ERROR, msg)
                print(form.errors)
                return redirect('editar_plato')
        except KeyError:
            # CREACION DE PLATO
            form = PlatoForm(request.POST, request.FILES)
            if form.is_valid():
                menu = form.save(commit=False)
                menu.creador = request.user
                menu.save()
            else:
                msg = 'Datos incorrectos'
                messages.add_message(request, messages.ERROR, msg)
                print(form.errors)
                return redirect('nuevo_plato')

        return redirect('platos')
