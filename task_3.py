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
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
# Получаем координаты ответа.
org_hours = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
organisation_coordinates = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(organisation_coordinates[0], organisation_coordinates[1])
print('------------------------------')
print(org_address)
print(org_name)
print(org_hours)
print(get_distance_between(toponym_coodrinates, organisation_coordinates))
print('------------------------------')
map_params = {
    'l': 'map',
    'pt': '~'.join(["{0},pm2dgl".format(toponym_point), "{0},pm2dgl".format(org_point)])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
