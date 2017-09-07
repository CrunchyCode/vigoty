from datetime import datetime, timedelta
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from apps.inicio.models import Perfil
from apps.negocio.models import Menu
from apps.metodos_globales import getDataDireccion


class TiendaView(TemplateView):
    def get(self, request, *args, **kwargs):
        fecha = None
        if len(kwargs) > 0:
            fecha = kwargs['date']

        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.direccion == '':
                msg = (
                    'Registre una direccion en su Perfil, para mostrar ' +
                    'los menus mas cercanos a usted.'
                )
                messages.add_message(request, messages.ERROR, msg)
                return redirect('perfil')
        except ObjectDoesNotExist:
            msg = 'Perfil inexistente. Complete sus datos.'
            messages.add_message(request, messages.ERROR, msg)
            return redirect('perfil')

        menus = Menu.objects.all()

        hoy = datetime.now()
        mañana = hoy + timedelta(days=1)
        m = mañana
        fechas = []
        fechas.append(mañana)
        for x in range(1, 7):
            m = m + timedelta(days=1)
            fechas.append(m)

        if fecha is None:
            fec_filtro = mañana
        else:
            try:
                fec_filtro = datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                raise Http404()

        menus = getDataDireccion(perfil.direccion, menus, fec_filtro)

        return render(
            request,
            'tienda.html',
            {
                'menus': menus,
                'perfil': perfil,
                'fechas': fechas,
                'fec_filtro': fec_filtro
            }
        )

    def post(self, request, *args, **kwargs):
        pass
