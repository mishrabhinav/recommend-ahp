import requests
from os import environ as env

_DARKSKY_KEY = env['DARKSKY_KEY']
_URL = 'https://api.darksky.net/forecast'


def _get_single_forecast(coord):
    lat, long = coord
    url = '{url}/{key}/{lat},{long}'.format(url=_URL, key=_DARKSKY_KEY, lat=lat, long=long)

    resp = requests.get(url)

    if resp.status_code >= 400:
        return {}

    return resp.json()


def get_forecast(*coords):
    return [_get_single_forecast(coord) for coord in coords]
