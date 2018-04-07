from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields


class Forecast(MongoModel):
    lat = fields.FloatField(required=True)
    lng = fields.FloatField(required=True)
    data = fields.DictField(required=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'recommend-ahp'
