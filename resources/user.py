from datetime import datetime

from flask import _request_ctx_stack
from flask_restful import Resource, reqparse
from pymodm.errors import DoesNotExist

import models
from utils.auth import requires_auth
from matrix.core import DEFAULT_SETTINGS


class User(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('settings', type=dict, help='user settings')
        self.parser = parser

    @requires_auth
    def get(self):
        username = _request_ctx_stack.top.current_user['sub']

        try:
            settings = models.Settings.objects.get({'username': username})
            return settings.data
        except DoesNotExist:
            settings = models.Settings(username=username, data=DEFAULT_SETTINGS, last_modified=datetime.utcnow())
            settings.save()

            return DEFAULT_SETTINGS

    @requires_auth
    def post(self):
        username = _request_ctx_stack.top.current_user['sub']
        args = self.parser.parse_args()

        try:
            settings = models.Settings.objects.get({'username': username})
            settings.last_modified = datetime.utcnow()
            settings.data = args.settings
        except DoesNotExist:
            settings = models.Settings(username=username, data=args.settings, last_modified=datetime.utcnow())

        settings.save()

        return settings.data
