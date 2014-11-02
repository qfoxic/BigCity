import datetime

from mongoengine import Document, fields, NULLIFY, CASCADE
from mfs.common import constants as co
Document.save()

class Node(Document):
    meta = {
        'allow_inheritance': True
    }

    uid = fields.IntField(required=True, min_value=1)
    gid = fields.IntField(required=True, min_value=1)
    #unix permission.
    perm = fields.StringField(default='666')
    # comma separated path of entity's ids.
    path = fields.StringField(required=True, max_length=3000)
    record_type = fields.StringField(max_length=15, default=Node.get_type)
    #timestamp
    created = fields.DateTimeField()
    #timestamp
    updated = fields.DateTimeField(default=datetime.datetime.now)
    # Parent record. Mongo object id.
    parent = fields.ReferenceField('self', reverse_delete_rule=NULLIFY)
    # Shared to uids.
    shared = fields.ListField()
    # typical access level. 0 - private, 1 - public
    access_level = fields.IntField(
        choices=[co.PRIVATE_ACCESS, co.PRIVATE_ACCESS],
        default=co.PRIVATE_ACCESS)

    @classmethod
    def get_type(cls):
        return 'node'

    def save(self, *args, **kwargs):
        #self.path = 
        return super(Node, self).save(*args, **kwargs)


class Resource(Document):
    meta = {
        'allow_inheritance': True
    }

    record_type = fields.StringField(max_length=15, default=Resource.get_type)
    #timestamp
    created = fields.DateTimeField()
    #timestamp
    updated = fields.DateTimeField(default=datetime.datetime.now)
    # Parent record. Mongo object id. We don't have resource parents
    parent = fields.ReferenceField('Node', reverse_delete_rule=CASCADE)
    # Some name can be used to determine an object.
    tag = fields.StringField(default=Resource.get_tag)

    @classmethod
    def get_type(self):
        return 'resource'

    @classmethod
    def get_tag(self):
        return 'resource'


#Used for geospacial requests
class GeoResource(Resource):

    def resolve_to_geo(self, address):
        pass

    @classmethod
    def get_type(self):
        return 'geo_location'

    @classmethod
    def get_tag(self):
        return 'geo_location'


#Used for similarity search.
class SearchVector(Resource):

    def normalize(self, data):
        """Returns normal of a vector to optimize searching."""
        pass

    @classmethod
    def get_type(self):
        return 'vector'

    @classmethod
    def get_tag(self):
        return 'vector'

