from datetime import datetime

from flask_restful import Resource, reqparse, abort

from models import Directions, Forecast, Recommendations
from utils.darksky import get_forecast
from utils.directions import get_all_routes


def _split_coordinates(key, coord):
    coords = coord.split(',')

    if len(coords) != 2:
        abort(400, message='{} co-ordinates incorrect'.format(key))

    return float(coords[0]), float(coords[1])


class Retrieve(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=str, help='Journey starting co-ordinates', required=True)
        parser.add_argument('to', type=str, help='Journey ending co-ordinates', required=True)
        parser.add_argument('username', type=str, help='Username of the logged in user', required=True)
        self.parser = parser

    def get(self):
        args = self.parser.parse_args()

        to_coord = _split_coordinates('to', args['to'])
        from_coord = _split_coordinates('from', args['from'])

        gm_routes = get_all_routes(from_coord, to_coord)
        ds_forecasts = get_forecast(from_coord, to_coord)

        directions = map(lambda x: Directions(mode=x['_mode'], data=x), gm_routes)
        directions = Directions.objects.bulk_create(list(directions))

        for idx in range(len(gm_routes)):
            gm_routes[idx]['_id'] = str(directions[idx])

        forecasts = map(lambda f: Forecast(lat=f['latitude'], lng=f['longitude'], data=f), ds_forecasts)
        forecasts = Forecast.objects.bulk_create(list(forecasts))

        recommendations = Recommendations(available=directions, forecast=forecasts, user=args.username,
                                          created_on=datetime.utcnow())
        recommendations_id = recommendations.save()

        return {
            'to': to_coord,
            'from': from_coord,
            'directions': gm_routes,
            'forecast': ds_forecasts,
            'recommendation_id': str(recommendations_id.pk)
        }
