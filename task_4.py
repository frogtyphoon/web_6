import sys
from io import BytesIO
from util import get_distance_between

import requests
from PIL import Image

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

json_response = response.json()

toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

toponym_coodrinates = toponym["Point"]["pos"]

toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
toponym_point = "{0},{1}".format(toponym_longitude, toponym_lattitude)

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = ','.join([toponym_longitude, toponym_lattitude])

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    # ...
    pass
json_response = response.json()
# Получаем первую найденную организацию.
org_points = []
for i in range(11):
    organization = json_response["features"][i]
    organisation_coordinates = organization["geometry"]["coordinates"]
    if "TwentyFourHours" in organization["properties"]["CompanyMetaData"]["Hours"]["Availabilities"]:
        if organization["properties"]["CompanyMetaData"]["Hours"]["Availabilities"]["TwentyFourHours"]:
            org_points.append(("{0},{1}".format(organisation_coordinates[0], organisation_coordinates[1]), 'pm2gnm'))
        else:
            org_points.append(("{0},{1}".format(organisation_coordinates[0], organisation_coordinates[1]), 'pm2blm'))
    else:
        org_points.append(("{0},{1}".format(organisation_coordinates[0], organisation_coordinates[1]), 'pm2grm'))

map_params = {
    'l': 'map',
    'pt': '~'.join(list(map(lambda x: "{0},{1}".format(x[0], x[1]), org_points)))
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
