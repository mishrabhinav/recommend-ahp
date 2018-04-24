from flask_restful import Resource, reqparse

from models import Recommendations


class History(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='username to retrieve the history for', required=True)
        self.parser = parser

    def get(self):
        args = self.parser.parse_args()

        recommendations = Recommendations.objects.raw({'user': args.username}).exclude('forecast', 'available')

        history = []
        for recommendation in recommendations:
            if not recommendation.selected:
                continue

            history.append({
                'directions': recommendation.selected.data,
                'timestamp': recommendation.created_on.timestamp() if recommendation.created_on else None,
                '_id': str(recommendation.selected._id)
            })

        return {
            'username': args.username,
            'history': history
        }
