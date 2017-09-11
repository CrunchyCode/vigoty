import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from apps.inicio.models import Perfil
from apps.negocio.models import Menu, DetalleMenuPlato, Plato
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
        '''
            FALTA CUANDO CANTIDAD DE PEDIDOS DEL MENU ES IGUAL A
            CANTIDAD MAXIMA QUE OFRECE EL COCINERO.
        '''
        try:
            id_menu = kwargs['id']

            menu = get_object_or_404(Menu, pk=id_menu)
            detalles = DetalleMenuPlato.objects.filter(menu=menu)

            nro_pedidos = Pedido.objects.filter(
                menu=menu).aggregate(Sum('cantidad'))['cantidad__sum']

            if not nro_pedidos:
                nro_pedidos = 0

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

    def post(self, request, *args, **kwargs):
        id_menu = kwargs['id']
        men = get_object_or_404(Menu, pk=id_menu)

        try:
            # OBTENER ALGUN PEDIDO CON EL MENU SELECCIONADO CON ESTADO '1'
            # ESTADO '1' => POR CONFIRMAR
            pedido = Pedido.objects.get(
                estado='1', comprador=request.user, menu=men
            )
        except ObjectDoesNotExist:
            pedido = Pedido()
            pedido.cantidad = 0
            pedido.subtotal = 0
            pedido.total = 0
            pedido.comprador = request.user
            pedido.menu = men
            pedido.save()

        pedido.menu = men
        pedido.cantidad = int(request.POST.get('cantidad'))
        pedido.subtotal = Decimal(pedido.cantidad * men.precio)
        '''
            FALTA CALCULAR RESTANDO COMISION DE PLATAFORMA
        '''
        pedido.total = Decimal(pedido.cantidad * men.precio)
        pedido.save()

        return redirect('venta')


class VentaView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            pedido = Pedido.objects.get(estado='1', comprador=request.user)
            detalles = DetalleMenuPlato.objects.filter(
                menu=pedido.menu, estado='1'
            )

            return render(
                request,
                'venta_detalle.html',
                {
                    'pedido': pedido,
                    'detalles': detalles,
                }
            )
        except ObjectDoesNotExist:
            return redirect('tienda')

    def post(self, request, *args, **kwargs):
        tipo = request.POST.get('tipo_operacion')

        if tipo == '1':
            # PAGAR PEDIDO (2)
            try:
                pedido = Pedido.objects.get(estado='1', comprador=request.user)
                pedido.estado = '2'
                pedido.save()

                msg = 'Su Pedido fue pagado correctamente.'
                messages.add_message(request, messages.SUCCESS, msg)
            except ObjectDoesNotExist:
                msg = 'No tiene algun Pedido pendiente.'
                messages.add_message(request, messages.ERROR, msg)
        elif tipo == '2':
            # CANCELAR PEDIDO (eliminar)
            try:
                pedido = Pedido.objects.get(estado='1', comprador=request.user)
                pedido.delete()

                msg = 'Su Pedido fue cancelado correctamente.'
                messages.add_message(request, messages.SUCCESS, msg)
            except ObjectDoesNotExist:
                msg = 'No tiene algun Pedido pendiente.'
                messages.add_message(request, messages.ERROR, msg)
        else:
            msg = (
                'Que desea hacer con su Pedido? ' +
                'Procede a pagarlo y disfruta tu Menu.'
            )
            messages.add_message(request, messages.ERROR, msg)

        return redirect('mis-pedidos')


class MisPedidosView(TemplateView):
    def get(self, request, *args, **kwargs):
        pedidos = Pedido.objects.filter(
            comprador=request.user).exclude(estado__in=['1'])

        return render(
            request,
            'mis_pedidos.html',
            {
                'pedidos': pedidos
            }
        )


class PedidoDetalleView(TemplateView):
    def get(self, request, *args, **kwargs):
        id_pedido = kwargs['id']

        try:
            pedido = Pedido.objects.filter(
                id=id_pedido, comprador=request.user).exclude(estado='1')[0]

            detalles = DetalleMenuPlato.objects.filter(
                menu=pedido.menu, estado='1'
            )
        except IndexError:
            raise Http404()

        return render(
            request,
            'pedido_detalle.html',
            {
                'pedido': pedido,
                'detalles': detalles
            }
        )


class MisVentasView(TemplateView):
    def get(self, request, *args, **kwargs):
        menus = Menu.objects.filter(creador=request.user)

        for menu in menus:
            cantidad = Pedido.objects.filter(
                        menu=menu).aggregate(Sum('cantidad'))['cantidad__sum']
            if cantidad:
                menu.cantidad_vendidos = cantidad
            else:
                menu.cantidad_vendidos = 0

        return render(
            request,
            'mis_ventas.html',
            {
                'menus': menus
            }
        )

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            id_menu = request.POST.get('menu')
            get_object_or_404(Menu, id=id_menu)

            if request.POST.get('opcion') == 'platos':
                platos = Plato.objects.filter(
                    id__in=DetalleMenuPlato.objects.filter(
                        menu__id=id_menu,
                        estado='1').values_list('plato__id', flat=True)
                )

                lst_platos = []
                for pla in platos:
                    dic = {}
                    dic['nombre'] = pla.nombre
                    dic['url_imagen'] = pla.imagen.url
                    lst_platos.append(dic)

                data = json.dumps(lst_platos)
                return HttpResponse(data, content_type='application/json')
            elif request.POST.get('opcion') == 'compradores':
                compradores = Perfil.objects.filter(
                    usuario__id__in=Pedido.objects.filter(
                        menu__id=id_menu).values_list(
                            'comprador__id', flat=True).exclude(estado='1')
                )

                lst_compradores = []
                for com in compradores:
                    dic = {}
                    dic['nombre'] = com.get_nombre_completo()
                    dic['documento'] = com.documento_identidad
                    dic['cantidad'] = Pedido.objects.get(
                                        menu__id=id_menu,
                                        comprador=com.usuario
                                    ).cantidad
                    lst_compradores.append(dic)

                data = json.dumps(lst_compradores)
                return HttpResponse(data, content_type='application/json')
            else:
                raise Http404()
        else:
            return redirect('tienda')
