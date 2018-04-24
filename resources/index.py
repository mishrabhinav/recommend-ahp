from flask_restful import Resource

from utils.auth import requires_auth


class Index(Resource):
    @staticmethod
    @requires_auth
    def get():
        return {
            'status': 'OK',
        }
