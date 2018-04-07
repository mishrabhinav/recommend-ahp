import time
from flask_restful import Resource, reqparse, abort

from utils.directions import get_all_routes
from utils.darksky import get_forecast
from models import Directions, Forecast, Recommendations


def _split_coordinates(key, coord):
    coords = coord.split(',')

    if len(coords) != 2:
        abort(400, message='{} co-ordinates incorrect'.format(key))

    return float(coords[0]), float(coords[1])


class Retrieve(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=str, help='Journey starting co-ordinates')
        parser.add_argument('to', type=str, help='Journey ending co-ordinates')
        self.parser = parser

    def get(self):
        args = self.parser.parse_args()
        to_coord = _split_coordinates('to', args['to'])
        from_coord = _split_coordinates('from', args['from'])

        gm_routes = get_all_routes(from_coord, to_coord)
        ds_forecasts = get_forecast(from_coord, to_coord)

        directions = []
        for mode, dirs in gm_routes.items():
            for d in dirs:
                directions.append(Directions(mode=mode, data=d))

        directions = Directions.objects.bulk_create(directions)

        forecasts = []
        for forecast in ds_forecasts:
            forecasts.append(Forecast(lat=forecast['latitude'], lng=forecast['longitude'], data=forecast))

        forecasts = Forecast.objects.bulk_create(forecasts)

        recommendations = Recommendations(available=directions, forecast=forecasts)
        recommendations_id = recommendations.save()

        return {
            'to': to_coord,
            'from': from_coord,
            'directions': gm_routes,
            'forecast': ds_forecasts,
            'recommendation_id': str(recommendations_id.pk)
        }
