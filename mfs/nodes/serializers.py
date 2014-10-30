from rest_framework import serializers
from mfs.common import constants as co

"""
The basic idea is that we have nodes and their resources.
Nodes can be hierarchical.

Everything is build around one record with different types. Every record
can have own data: that is python dict.

Each resource can have special field - tag. We are able to find node's resource
by tag without specifying id.

Specific node type must inherit NodeSerializer, specify it's own type, specify 
serializer for data.
"""


def unix_perm_validator(value):
    pass


class AbstractRecordSerializer(serializers.Serializer):
    # Can be of different types. Like google appengine.
    record_type = serializers.CharField(source='get_type', required=True, max_length=15)
    #timestamp
    created = serializers.DateTimeField(auto_now_add=True, read_only=True)
    #timestamp
    updated = serializers.DateTimeField(auto_now=True, read_only=True)
    #timestamp
    deleted = serializers.DateTimeField()
    # Parent record. Mongo object id.
    parent_record = serializers.CharField(max_length=24, min_length=24)
    # Shared to uids.
    shared = serializers.CharField()
    # typical access level. 0 - private, 1 - public
    access_level = serializers.IntegerField(default=co.PRIVATE_ACCESS)
    # Some name can be used to determine an object.
    name = serializers.CharField(source='get_name')

    def get_type(self):
        raise NotImplemented()

    def get_name(self):
        raise NotImplemented()


class NodeSerializer(AbstractRecordSerializer):
    uid = serializers.IntegerField(required=True, min_value=1)
    gid = serializers.IntegerField(required=True, min_value=1)
    #unix permission.
    perm = serializers.CharField(validators=[unix_perm_validator], default='666')
    # comma separated path of entity's ids.
    path = serializers.CharField(required=True, max_length=3000)

    def get_type(self):
        return 'node'

    def get_name(self):
        return 'node'


class ResourceSerializer(AbstractRecordSerializer):
    def get_type(self):
        return 'resource'

    def get_name(self):
        return 'resource'
