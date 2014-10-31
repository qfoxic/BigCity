import datetime

from mongoengine import Document, fields
from mfs.common import constants as co
from mfs.users.models import MongoUser


class Node(Document):
    uid = fields.IntField(required=True, min_value=1)
    gid = fields.IntField(required=True, min_value=1)
    #unix permission.
    perm = fields.StringField(default='666')
    # comma separated path of entity's ids.
    path = fields.StringField(required=True, max_length=3000)
    record_type = fields.StringField(required=True, max_length=15, default=Node.get_type)
    #timestamp
    created = fields.DateTimeField(required=True)
    #timestamp
    updated = fields.DateTimeField(required=True, default=datetime.datetime.now)
    #timestamp
    deleted = fields.DateTimeField()
    # Parent record. Mongo object id.
    parent = fields.ReferenceField('Node', reverse_delete_rule=fields.NULLIFY)
    # Shared to uids.
    shared = fields.ListField(fields.ReferenceField(MongoUser))
    # typical access level. 0 - private, 1 - public
    access_level = fields.IntField(
        choices=[co.PRIVATE_ACCESS, co.PRIVATE_ACCESS],
        default=co.PRIVATE_ACCESS)
    # Some name can be used to determine an object.
    tag = fields.StringField(default=Node.get_tag)
    title = fields.StringField(default='')

    @classmethod
    def get_type(cls):
        return 'node'

    @classmethod
    def get_tag(cls):
        return 'node'


class Resource(Document):
    record_type = fields.StringField(required=True, max_length=15, default=Resource.get_type)
    #timestamp
    created = fields.DateTimeField(required=True)
    #timestamp
    updated = fields.DateTimeField(required=True, default=datetime.datetime.now)
    # Parent record. Mongo object id. We don't have resource parents
    parent = fields.ReferenceField('Node', reverse_delete_rule=fields.CASCADE)
    # typical access level. 0 - private, 1 - public
    access_level = fields.IntField(
        choices=[co.PRIVATE_ACCESS, co.PRIVATE_ACCESS],
        default=co.PRIVATE_ACCESS)
    # Some name can be used to determine an object.
    tag = fields.StringField(default=Resource.get_tag)

    @classmethod
    def get_type(self):
        return 'resource'

    @classmethod
    def get_tag(self):
        return 'resource'
