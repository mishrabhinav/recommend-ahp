from datetime import datetime

from flask import _request_ctx_stack
from flask_restful import Resource, reqparse, abort

from models import Directions, Forecast, Recommendations
from utils.ahp import run_ahp
from utils.auth import requires_auth
from utils.darksky import get_forecast
from utils.directions import get_all_routes


def _split_coordinates(key, coord):
    coords = coord.split(',')

    if len(coords) != 2:
        abort(400, message='{} co-ordinates incorrect'.format(key))

    return float(coords[0]), float(coords[1])


def _prioritize(directions, forecast):
    priorities = run_ahp(directions, forecast)

    prioritized_directions = []
    for idx, dir in enumerate(directions):
        dir['_priority'] = priorities[idx]

        prioritized_directions.append(dir)

    return prioritized_directions


class Retrieve(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=str, help='Journey starting co-ordinates', required=True)
        parser.add_argument('to', type=str, help='Journey ending co-ordinates', required=True)
        self.parser = parser

    @requires_auth
    def get(self):
        args = self.parser.parse_args()

        to_coord = _split_coordinates('to', args['to'])
        from_coord = _split_coordinates('from', args['from'])
        username = _request_ctx_stack.top.current_user['sub']

        gm_routes = get_all_routes(from_coord, to_coord, limit=8)
        ds_forecasts = get_forecast(from_coord, to_coord)

        gm_routes = _prioritize(gm_routes, ds_forecasts)

        directions = map(lambda x: Directions(mode=x['_mode'], data=x, priority=x['_priority']), gm_routes)
        directions = Directions.objects.bulk_create(list(directions))

        for idx in range(len(gm_routes)):
            gm_routes[idx]['_id'] = str(directions[idx])

        forecasts = map(lambda f: Forecast(lat=f['latitude'], lng=f['longitude'], data=f), ds_forecasts)
        forecasts = Forecast.objects.bulk_create(list(forecasts))

        recommendations = Recommendations(available=directions, forecast=forecasts, user=username,
                                          created_on=datetime.utcnow())
        recommendations_id = recommendations.save()

        return {
            'to': to_coord,
            'from': from_coord,
            'directions': gm_routes,
            'forecast': ds_forecasts,
            'recommendation_id': str(recommendations_id.pk)
        }
