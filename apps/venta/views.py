from datetime import datetime, timedelta
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from apps.inicio.models import Perfil
from apps.negocio.models import Menu, DetalleMenuPlato
from apps.metodos_globales import getDataDireccion
from .models import Pedido


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


class TiendaProductoView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            id_menu = kwargs['id']

            menu = get_object_or_404(Menu, pk=id_menu)
            detalles = DetalleMenuPlato.objects.filter(menu=menu)
            nro_pedidos = Pedido.objects.filter(menu=menu).count()
            cantidad_disponible = menu.cantidad_maxima + 1 - nro_pedidos

            selectHTML = ''
            selectHTML += (
                '<select name="cantidad" id="cantidad" ' +
                'class="form-control input-sm" style="width: 60px;" ' +
                'onchange="cambiarTotal()">'
            )

            for x in range(1, cantidad_disponible):
                selectHTML += (
                    '<option value="' + str(x) + '">' + str(x) + '</option>'
                )
            selectHTML += '</select>'

            i = 0
            for det in detalles:
                det.valor_slide = i
                i = i + 1
        except KeyError:
            raise Http404()

        return render(
            request,
            'tienda_producto.html',
            {
                'menu': menu,
                'detalles': detalles,
                'selectHTML': selectHTML,
            }
        )
