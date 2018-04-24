from flask import _request_ctx_stack
from flask_restful import Resource

from models import Recommendations
from utils.auth import requires_auth


class History(Resource):
    @requires_auth
    def get(self):
        username = _request_ctx_stack.top.current_user['sub']

        recommendations = Recommendations.objects.raw({'user': username}).exclude('forecast', 'available')

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
            'username': username,
            'history': history
        }
