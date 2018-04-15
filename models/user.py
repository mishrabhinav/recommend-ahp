from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern


class User(MongoModel):
    username = fields.CharField(primary_key=True, required=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    email = fields.EmailField(required=True)
    created_on = fields.DateTimeField()
    modified_on = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'recommend-ahp'
