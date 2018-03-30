import time
from flask_restful import Resource, reqparse


class Select(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('journey', type=dict, help='Selected journey details')
        self.parser = parser

    def post(self):
        args = self.parser.parse_args()
        return {
            'timestamp': time.time(),
            'args': args
        }
