from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from apps.inicio.models import Perfil
from .models import Plato, TipoPlato, TipoEntrega
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


class PublicarMenuView(TemplateView):
    def get(self, request, *args, **kwargs):
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

        try:
            # EDICION DE MENU
            # pk = kwargs['id']

            menu = None
            detmen = None
            no_platos = None
            msg_estado = None

            id_product = kwargs['id']
            menu = get_object_or_404(Menu, pk=id_product, creador=request.user)
            detmen = DetalleMenuPlato.objects.filter(menu=menu, estado="1")
            # LISTA DE PLATOS DEL MENU A EDITAR
            lst = DetalleMenuPlato.objects.filter(
                menu=menu, estado="1").values_list('plato__id', flat=True)
            # LISTA DE PLATOS DEL COCINERO QUE NO ESTAN EN EL MENU
            no_platos = Plato.objects.all().exclude(id__in=lst)
            if menu.estado == "1":
                msg_estado = "Su Menu esta siendo validado para su pronta publicacion."
            elif menu.estado == "2":
                msg_estado = "Su Menu fue publicado."

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
            }
        )

    def post(self, request, *args, **kwargs):
        pass
