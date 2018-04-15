from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern


class Directions(MongoModel):
    mode = fields.CharField(choices=('WALKING', 'DRIVING', 'BICYCLING', 'TRANSIT'), required=True)
    data = fields.DictField(required=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'recommend-ahp'
