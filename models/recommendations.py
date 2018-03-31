from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

from .directions import Directions
from .forecast import Forecast


class Recommendations(MongoModel):
    selected = fields.ReferenceField(Directions, blank=True)
    available = fields.ListField(fields.ReferenceField(Directions))
    forecast = fields.ListField(fields.ReferenceField(Forecast))

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'recommend-ahp'
