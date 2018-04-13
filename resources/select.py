import time
from bson import ObjectId
from flask_restful import Resource, reqparse
from pymodm.context_managers import no_auto_dereference

from models import Recommendations, Directions


class Select(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('recommendation_id', type=str, help='_id of the recommendation')
        parser.add_argument('select', type=str, help='_id of the selected directions')
        self.parser = parser

    def post(self):
        args = self.parser.parse_args()
        updated = False

        recommendation = Recommendations.objects.get({'_id': ObjectId(args.recommendation_id)})

        if not recommendation.selected:
            recommendation.selected = ObjectId(args.select)
            recommendation.save()
            updated = True

        return {
            'recommendation_id': args.recommendation_id,
            'selected': args.select,
            'updated': updated
        }
