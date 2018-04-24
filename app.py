from os import environ as env

from flask import Flask
from flask_restful import Api
from pymodm import connect

from resources import Index, Retrieve, Select, User, History

connect("mongodb://{}:{}@{}:{}/{}".format(env['MONGO_USER'], env['MONGO_PASS'], env['MONGO_IP'],
                                          env['MONGO_PORT'],
                                          env['MONGO_DB']), alias="recommend-ahp")

app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/', '/api')
api.add_resource(Retrieve, '/api/retrieve')
api.add_resource(History, '/api/history')
api.add_resource(Select, '/api/select')
api.add_resource(User, '/api/user')
