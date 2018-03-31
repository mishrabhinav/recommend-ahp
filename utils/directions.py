import googlemaps
from os import environ as env

gmaps = googlemaps.Client(key=env['GMAPS_KEY'])

MODES = ['walking', 'driving', 'bicycling', 'transit']


def get_geocode(address):
    return gmaps.geocode(address)


def get_all_routes(from_coord, to_coord):
    return {mode: get_transit_routes(from_coord, to_coord, mode=mode) for mode in MODES}


def get_transit_routes(from_coord, to_coord, mode='walking'):
    return gmaps.directions(origin=from_coord,
                            destination=to_coord,
                            mode=mode)
