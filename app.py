from flask import Flask
from flask_restful import Api

from resources import Index, Retrieve, Select


def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Index, '/', '/api')
    api.add_resource(Retrieve, '/api/retrieve')
    api.add_resource(Select, '/api/select')


if __name__ != '__main__':
    main()
