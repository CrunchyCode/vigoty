import json
from urllib.request import urlopen
from urllib.parse import urlencode
from django.db import connection
from django.conf import settings
from apps.negocio.models import Plato, DetalleMenuPlato


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

        for x in json_lat_lng['results'][0]['address_components']:
            if x['types'][0] == 'country':
                menus = menus.filter(country__icontains=x['long_name'])

            if x['types'][0] == 'administrative_area_level_2':
                cadena = x['long_name'].lower().replace(
                    'province', '').replace(' ', '')
                menus = menus.filter(
                    administrative_area_level_2__icontains=cadena
                )

        # SOLO MENUS VALIDADOS
        menus = menus.filter(pk__in=ids, estado=2)

        for menu in menus:
            detalles = DetalleMenuPlato.objects.filter(menu=menu)
            for det in detalles:
                menu.plato_mostrar = Plato.objects.get(id=det.plato.id)
                break

            # AGREGANDO PARAMETRO 'DISTANCIA' A LOS MENUS, CON LOS KM
            if near[menu.id] >= 0:
                if near[menu.id] == 0:
                    menu.distancia = ''
                else:
                    menu.distancia = str((near[menu.id])) + ' KM'
    else:
        # LA DIRECCION RECIBIDA NO ES UNA DE LAS QUE OFRECE GOOGLE
        menus = None

    return menus


# SETEAR DATOS DE LOCALIZACION EN OBJETO MENU
def set_data_menu(direccion, menu):
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

    if len(json_lat_lng['results']) > 0:
        longitude = json_lat_lng['results'][0]['geometry']['location']['lng']
        latitude = json_lat_lng['results'][0]['geometry']['location']['lat']

        menu.lat = str(longitude)
        menu.lng = str(latitude)
        for x in json_lat_lng['results'][0]['address_components']:
            for y in x['types']:
                if y == 'country':
                    menu.country = str(x['long_name'])
                elif y == 'administrative_area_level_2':
                    menu.administrative_area_level_2 = str(x['long_name'])
                elif y == 'administrative_area_level_1':
                    menu.administrative_area_level_1 = str(x['long_name'])
                elif y == 'locality':
                    menu.locality = str(x['long_name'])
                elif y == 'route':
                    menu.route = str(x['long_name'])
                elif y == 'street_number':
                    menu.street_number = str(x['long_name'])
                elif y == 'postal_code':
                    menu.postal_code = str(x['long_name'])
                else:
                    pass

        menu.direccion_texto = direccion
    else:
        menu = None

    return menu


# PARA OBTENER LOS MENUS MAS CERCANOS SEGUN LATITUD Y LONGITUD
def nearby_locations(latitude, longitude, radius, use_miles=False):
    if use_miles:
        distance_unit = 3959
    else:
        distance_unit = 6371

    cursor = connection.cursor()

    sql = """ SELECT id, lat, lng, (%f * acos(cos(radians(%f)) * cos(radians(lat)) * cos(radians(lng) - radians(%f) ) + sin(radians(%f)) * sin(radians(lat)))) AS dis FROM sistema_menu WHERE (%f * acos(cos(radians(%f)) * cos(radians(lat)) * cos(radians(lng) - radians(%f) ) + sin(radians(%f)) * sin(radians(lat)))) < %d ORDER BY dis DESC """ % (distance_unit, latitude, longitude, latitude, distance_unit, latitude, longitude, latitude, int(radius))

    cursor.execute(sql)
    ids = dict((row[0], round(row[3], 2)) for row in cursor.fetchall())

    return ids
