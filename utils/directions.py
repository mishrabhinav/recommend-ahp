from os import environ as env

import googlemaps

gmaps = googlemaps.Client(key=env['GMAPS_KEY'])

MODES = ['walking', 'driving', 'bicycling', 'transit']


def get_geocode(address):
    return gmaps.geocode(address)


def get_all_routes(from_coord, to_coord, limit=-1):
    all_routes = []
    for mode in MODES:
        routes = []
        raw_routes = get_transit_routes(from_coord, to_coord, mode=mode)
        for route in raw_routes[:int(len(raw_routes)/2)]:
            route['_mode'] = mode.upper()
            routes.append(route)

        all_routes.extend(routes)

    if limit < 0:
        return all_routes

    return all_routes[:limit]


def get_transit_routes(from_coord, to_coord, mode='walking'):
    return gmaps.directions(origin=from_coord,
                            destination=to_coord,
                            alternatives=True,
                            mode=mode)
