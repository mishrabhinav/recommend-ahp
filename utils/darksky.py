from os import environ as env

import requests

_DARKSKY_KEY = env['DARKSKY_KEY']
_URL = 'https://api.darksky.net/forecast'


def _get_single_forecast(coord):
    lat, lng = coord
    url = '{url}/{key}/{lat},{lng}?exclude=minutely,hourly,daily,alerts,flags'.format(url=_URL, key=_DARKSKY_KEY,
                                                                                      lat=lat, lng=lng)

    resp = requests.get(url)

    if resp.status_code >= 400:
        return {}

    return resp.json()


def get_forecast(*coords):
    return [_get_single_forecast(coord) for coord in coords]
