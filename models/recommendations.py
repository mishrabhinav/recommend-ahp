from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern

from .directions import Directions
from .forecast import Forecast
from .user import User


class Recommendations(MongoModel):
    user = fields.ReferenceField(User, required=True)
    selected = fields.ReferenceField(Directions, blank=True)
    available = fields.ListField(fields.ReferenceField(Directions))
    forecast = fields.ListField(fields.ReferenceField(Forecast))

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'recommend-ahp'
