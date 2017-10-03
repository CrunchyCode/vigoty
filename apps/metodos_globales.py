import json
from urllib.request import urlopen
from urllib.parse import urlencode
from django.db import connection
from django.db.models import Sum
from django.conf import settings
from apps.negocio.models import Plato, DetalleMenuPlato
from apps.venta.models import Pedido


# METODO PARA OBTENER UN JSON CON TODA LA INFORMACION
# DE LA DIRECCION SEGUN LA API DE GOOGLE
# Y LUEGO HACER LOS FILTROS A LOS MENUS
def getDataDireccion(direccion, menus, fecha):
    api_key = settings.GOOGLE_GEOCODE_KEY
    direccion = str(urlencode({'address': direccion}))
    url_latlng = (
        'https://maps.googleapis.com/maps/api/geocode/json?' +
        direccion +
        '&key=' +
        api_key
    )
    response = urlopen(url_latlng)
    data = response.read()
    json_lat_lng = json.loads(data.decode('utf8'))

    if json_lat_lng['status'] == 'OK':
        longitude = json_lat_lng['results'][0]['geometry']['location']['lng']
        latitude = json_lat_lng['results'][0]['geometry']['location']['lat']
        radius = settings.GLOBAL_DISTANCIA_RADIO
        near = nearby_locations(latitude, longitude, radius, use_miles=False)
        ids = [x for x in near]
        menus = menus.filter(fecha_disponibilidad=fecha)

        # SOLO MENUS VALIDADOS
        # ESTADO '2' => PUBLICADO
        menus = menus.filter(id__in=ids, estado=2)

        for menu in menus:
            nro_pedidos = Pedido.objects.filter(
                menu=menu).aggregate(Sum('cantidad'))['cantidad__sum']
            if nro_pedidos == menu.cantidad_maxima:
                menu.agotado = True
            else:
                menu.agotado = False

            detalles = DetalleMenuPlato.objects.filter(menu=menu)
            for det in detalles:
                menu.plato_mostrar = Plato.objects.get(id=det.plato.id)
                break

            # AGREGANDO PARAMETRO 'DISTANCIA' A LOS MENUS, CON LOS KM
            if near[menu.id] >= 0:
                if near[menu.id] == 0:
                    menu.distancia = ''
                else:
                    menu.distancia = str(near[menu.id]) + ' KM'
    else:
        # LA DIRECCION RECIBIDA NO ES UNA DE LAS QUE OFRECE GOOGLE
        menus = None

    return menus


def get_lat_long(direccion):
    api_key = settings.GOOGLE_GEOCODE_KEY
    address = str(urlencode({'address': direccion}))
    url_latlng = (
        'https://maps.googleapis.com/maps/api/geocode/json?' +
        address +
        '&key=' +
        api_key
    )
    response = urlopen(url_latlng)
    data = response.read()
    json_lat_lng = json.loads(data.decode('utf8'))

    obj = {}
    if len(json_lat_lng['results']) > 0:
        longitude = json_lat_lng['results'][0]['geometry']['location']['lng']
        latitude = json_lat_lng['results'][0]['geometry']['location']['lat']

        obj['lat'] = str(latitude)
        obj['lng'] = str(longitude)
    else:
        obj = None

    return obj


# SETEAR DATOS DE LOCALIZACION EN OBJETO
def set_data_obj(obj):
    api_key = settings.GOOGLE_GEOCODE_KEY
    address = str(urlencode({'address': obj.direccion_texto}))
    url_latlng = (
        'https://maps.googleapis.com/maps/api/geocode/json?' +
        address +
        '&key=' +
        api_key
    )
    response = urlopen(url_latlng)
    data = response.read()
    json_lat_lng = json.loads(data.decode('utf8'))

    if len(json_lat_lng['results']) > 0:
        longitude = json_lat_lng['results'][0]['geometry']['location']['lng']
        latitude = json_lat_lng['results'][0]['geometry']['location']['lat']

        obj.lat = str(latitude)
        obj.lng = str(longitude)
        for x in json_lat_lng['results'][0]['address_components']:
            for y in x['types']:
                if y == 'country':
                    obj.country = str(x['long_name'])
                elif y == 'administrative_area_level_2':
                    obj.administrative_area_level_2 = str(x['long_name'])
                elif y == 'administrative_area_level_1':
                    obj.administrative_area_level_1 = str(x['long_name'])
                elif y == 'locality':
                    obj.locality = str(x['long_name'])
                elif y == 'route':
                    obj.route = str(x['long_name'])
                elif y == 'street_number':
                    obj.street_number = str(x['long_name'])
                elif y == 'postal_code':
                    obj.postal_code = str(x['long_name'])
                else:
                    pass

    else:
        obj = None

    return obj


# PARA OBTENER LOS MENUS MAS CERCANOS SEGUN LATITUD Y LONGITUD
def nearby_locations(latitude, longitude, radius, use_miles=False):
    if use_miles:
        distance_unit = 3959
    else:
        distance_unit = 6371

    cursor = connection.cursor()

    sql = """ SELECT id, lat, lng, (%f * acos(cos(radians(%f)) * cos(radians(lat)) * cos(radians(lng) - radians(%f) ) + sin(radians(%f)) * sin(radians(lat)))) AS dis FROM negocio_menu WHERE (%f * acos(cos(radians(%f)) * cos(radians(lat)) * cos(radians(lng) - radians(%f) ) + sin(radians(%f)) * sin(radians(lat)))) < %d ORDER BY dis DESC """ % (distance_unit, latitude, longitude, latitude, distance_unit, latitude, longitude, latitude, int(radius))

    cursor.execute(sql)
    ids = dict((row[0], round(row[3], 2)) for row in cursor.fetchall())

    return ids
