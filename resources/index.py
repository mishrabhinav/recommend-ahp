from flask_restful import Resource


class Index(Resource):
    @staticmethod
    def get():
        return {
            'status': 'OK',
        }
