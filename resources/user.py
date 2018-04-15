import datetime

from flask_restful import Resource, reqparse

import models


class User(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Desired username of the user')
        parser.add_argument('first_name', type=str, help='First name of the user')
        parser.add_argument('last_name', type=str, help='Last name of the user')
        parser.add_argument('email', type=str, help='Email address of the user')
        self.parser = parser

    def post(self):
        args = self.parser.parse_args()
        user = models.User(username=args.username,
                           first_name=args.first_name,
                           last_name=args.last_name,
                           email=args.email,
                           created_on=datetime.datetime.now(),
                           modified_on=datetime.datetime.now())

        user.save()

        return {
            'username': args.username
        }

    def put(self):
        args = self.parser.parse_args()

        for user in models.User.objects.raw({'_id': args.username}):
            models.User(username=user.username,
                        first_name=args.first_name,
                        last_name=args.last_name,
                        email=args.email,
                        created_on=user.created_on,
                        modified_on=datetime.datetime.now()).save()

        return {
            'username': args.username
        }
