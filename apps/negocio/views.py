from datetime import datetime, date
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from apps.inicio.models import Perfil, Direccion
from apps.venta.models import Pedido
from .models import Plato, TipoPlato, TipoEntrega, Menu, DetalleMenuPlato
from .forms import PlatoForm, MenuForm
from apps.metodos_globales import get_lat_long


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
                return redirect('editar-plato')
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
                return redirect('nuevo-plato')

        return redirect('platos')


class PublicarMenuView(TemplateView):
    def get(self, request, *args, **kwargs):
        direcciones = Direccion.objects.filter(usuario=request.user)
        tipos_entrega = TipoEntrega.objects.all()
        perfil = get_object_or_404(Perfil, usuario=request.user)

        selectHTML = ''
        selectHTML += (
            '<select name="cantidad_maxima" ' +
            'id="cantidad_maxima" class="form-control">'
        )
        for x in range(1, settings.GLOBAL_CANTIDAD_MAXIMA + 1):
            selectHTML += '<option value="%s">%s</option>' % (str(x), str(x))
        selectHTML += '</select>'

        tipos_plato = Plato.objects.filter(
            creador=request.user).values_list(
                'tipo_plato__id',
                flat=True
        ).distinct()

        if tipos_plato.count() == 0:
            divTIPO = (
                '<div class="alert alert-danger" role="alert">' +
                'NO TIENE PLATOS REGISTRADOS</div>'
            )
        else:
            divTIPO = ''
            for id_tipo_plato in tipos_plato:
                tp = TipoPlato.objects.get(id=id_tipo_plato)
                divTIPO += (
                    '<div class="col-md-12 radios" id="div_' +
                    str(tp.id) +
                    '" imagen-lista>'
                )
                divTIPO += '<h4>' + tp.nombre + '</h4>'
                divTIPO += '<div class="thumbnail col-sm-4">'
                divTIPO += (
                    '<img class="img-responsive" src="' +
                    static('img/empty.png') +
                    '" style="width:200px; height:150px;" alt="">'
                )
                divTIPO += '<div class="caption" style="text-align:center;">'
                divTIPO += '<label class="radio-inline">'
                divTIPO += (
                    '<input type="radio" name="rbt_' +
                    str(tp.id) +
                    '" value="0" checked> NINGUNO'
                )
                divTIPO += '</label>'
                divTIPO += '</div>'
                divTIPO += '</div>'
                divTIPO += '</div>'

        platos = Plato.objects.filter(creador=request.user)

        menu = None
        detmen = None
        no_platos = None
        msg_estado = None

        editable = True

        try:
            # EDICION DE MENU
            id_product = kwargs['id']
            menu = get_object_or_404(Menu, pk=id_product, creador=request.user)

            hoy = datetime.now().date()

            if hoy >= menu.fecha_disponibilidad:
                editable = False

            detmen = DetalleMenuPlato.objects.filter(menu=menu, estado='1')
            # LISTA DE PLATOS DEL MENU A EDITAR
            lst = DetalleMenuPlato.objects.filter(
                menu=menu, estado='1').values_list('plato__id', flat=True)
            # LISTA DE PLATOS DEL COCINERO QUE NO ESTAN EN EL MENU
            no_platos = Plato.objects.all().exclude(id__in=lst)
            if menu.estado == '1':
                msg_estado = (
                    'Su Menu esta siendo validado para su pronta publicacion.'
                )
            elif menu.estado == '2':
                msg_estado = 'Su Menu fue aceptado y publicado correctamente.'

        except KeyError:
            # CREACION DE MENU
            pass

        return render(
            request,
            'publicar_menu.html',
            {
                'tipos_entrega': tipos_entrega,
                'selectHTML': selectHTML,
                'divTIPO': divTIPO,
                'platos': platos,
                'detmen': detmen,
                'no_platos': no_platos,
                'msg_estado': msg_estado,
                'perfil': perfil,
                'menu': menu,
                'editable': editable,
                'direcciones': direcciones,
            }
        )

    def post(self, request, *args, **kwargs):
        try:
            menu_id = kwargs['id']
            # EDICION
            hoy = date.today()
            men = get_object_or_404(
                Menu, pk=menu_id, creador=request.user
            )
            nro_pedidos = Pedido.objects.filter(menu=men).count()
            form = MenuForm(request.POST, request.FILES, instance=men)
            if form.is_valid():
                if men.fecha_disponibilidad <= hoy or nro_pedidos > 0:
                    # NO SE PUEDE EDITAR
                    pass
                else:
                    # SI SE PUEDE EDITAR
                    menu = form.save(commit=False)
                    menu.fecha_disponibilidad = datetime.strptime(
                        request.POST.get('fecha_disponibilidad'), "%d/%m/%Y"
                    )
                    menu.rango_hora = (
                        request.POST.get('h_inicio') + ' - ' +
                        request.POST.get('h_fin')
                    )

                    try:
                        id_direccion = request.POST.get('direccion')
                        direccion = Direccion.objects.get(id=id_direccion)
                        menu.direccion = direccion

                        lat_long = get_lat_long(direccion.direccion_texto)
                        menu.lat = lat_long['lat']
                        menu.lng = lat_long['lng']
                    except ObjectDoesNotExist:
                        msg = 'Dirección no existe!'
                        messages.add_message(request, messages.ERROR, msg)
                        return redirect('publicar-menu')

                    menu.save()

                    tipos_plato = Plato.objects.filter(
                        creador=request.user).values_list(
                        'tipo_plato__id', flat=True).distinct()

                    lst_det = DetalleMenuPlato.objects.filter(menu=menu)
                    for x in lst_det:
                        x.estado = "2"
                        x.save()

                    for ti in tipos_plato:
                        id_plato = request.POST.get("rbt_"+str(ti))
                        if id_plato != "0":
                            pla = Plato.objects.get(id=id_plato)
                            try:
                                detalle = DetalleMenuPlato.objects.get(
                                    plato__id=id_plato, menu=menu
                                )
                                detalle.estado = "1"
                            except ObjectDoesNotExist:
                                detalle = DetalleMenuPlato()
                            detalle.plato = pla
                            detalle.menu = menu
                            detalle.save()
                msg = 'Menu editado correctamente!'
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect('menu')
            else:
                msg = 'Datos invalidos. Verifique la información.'
                messages.add_message(request, messages.ERROR, msg)
                print(form.errors)
                return redirect('publicar-menu')
        except KeyError:
            # CREACION
            form = MenuForm(request.POST, request.FILES)
            if form.is_valid():
                menu = form.save(commit=False)
                menu.fecha_disponibilidad = datetime.strptime(
                    request.POST.get('fecha_disponibilidad'), "%d/%m/%Y"
                )
                menu.creador = request.user
                menu.rango_hora = (
                    request.POST.get('h_inicio') + ' - ' +
                    request.POST.get('h_fin')
                )

                try:
                    id_direccion = request.POST.get('direccion')
                    direccion = Direccion.objects.get(id=id_direccion)
                    menu.direccion = direccion

                    lat_long = get_lat_long(direccion.direccion_texto)
                    menu.lat = lat_long['lat']
                    menu.lng = lat_long['lng']
                except ObjectDoesNotExist:
                    msg = 'Dirección no existe!'
                    messages.add_message(request, messages.ERROR, msg)
                    return redirect('publicar-menu')

                if menu is not None:
                    menu.save()
                else:
                    msg = (
                        'Direccion incorrecta, seleccione una ' +
                        'proporcionada por Google.'
                    )
                    messages.add_message(request, messages.ERROR, msg)
                    return redirect('publicar-menu')

                tipos_plato = Plato.objects.filter(
                    creador=request.user).values_list(
                    'tipo_plato__id', flat=True).distinct()
                for ti in tipos_plato:
                    id_plato = request.POST.get("rbt_"+str(ti))
                    if id_plato != "0":
                        pla = Plato.objects.get(id=id_plato)
                        detalle = DetalleMenuPlato()
                        detalle.plato = pla
                        detalle.menu = menu
                        detalle.save()

                msg = 'Menu creado correctamente!'
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect('menu')
            else:
                msg = 'Datos invalidos. Verifique la información.'
                messages.add_message(request, messages.ERROR, msg)
                print(form.errors)
                return redirect('publicar-menu')


class MenuView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            # LISTA DE MENUS DE UN COCINERO
            id = kwargs['id']
            menus = Menu.objects.filter(creador__id=id)
            perfil = get_object_or_404(Perfil, usuario__id=id)
        except KeyError:
            # LISTA DE MENUS DEL USUARIO LOGUEADO
            menus = Menu.objects.filter(creador=request.user)
            perfil = None

        for menu in menus:
            detalles = DetalleMenuPlato.objects.filter(menu=menu, estado='1')
            for det in detalles:
                menu.plato_mostrar = Plato.objects.get(id=det.plato.id)
                break

        return render(
            request,
            'menu.html',
            {
                'menus': menus,
                'perfil': perfil,
            }
        )

    def post(self, request, *args, **kwargs):
        return redirect('menu')
