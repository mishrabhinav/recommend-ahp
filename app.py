from os import environ as env

from flask import Flask
from flask_restful import Api
from pymodm import connect

import resources

connect(env['MONGODB_URI'], alias='recommend-ahp')

app = Flask(__name__)
api = Api(app)

api.add_resource(resources.Index, '/', '/api')
api.add_resource(resources.Retrieve, '/api/retrieve')
api.add_resource(resources.History, '/api/history')
api.add_resource(resources.Select, '/api/select')
api.add_resource(resources.User, '/api/user')
