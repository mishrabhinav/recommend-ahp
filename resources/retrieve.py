import time
from flask_restful import Resource, reqparse, abort


def split_coordinates(key, coord):
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
        to_lat, to_long = split_coordinates('to', args['to'])
        from_lat, from_long = split_coordinates('from', args['from'])

        return {
            'timestamp': time.time(),
            'to': [to_lat, to_long],
            'from': [from_lat, from_long]
        }
