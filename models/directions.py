from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class Directions(MongoModel):
    mode = fields.CharField(choices=('walking', 'driving', 'bicycling', 'transit'), required=True)
    data = fields.DictField(required=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'recommend-ahp'
