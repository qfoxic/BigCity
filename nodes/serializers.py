from rest_framework import serializers
from common import constants as co

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

class AbstractNodeSerializer(serializers.Serializer):
    uid = serializers.IntegerField(required=True, min_value=1)
    gid = serializers.IntegerField(required=True, min_value=1)
    # Can be of different types. Like google appengine.
    ntype = serializers.CharField(source='get_type', required=True, max_length=15)
    #timestamp
    created = serializers.DateTimeField(auto_now_add=True, read_only=True)
    #timestamp
    updated = serializers.DateTimeField(auto_now=True, read_only=True)
    #unix permission.
    perm = serializers.CharField(validators=[unix_perm_validator], default='666')
    # Parent node. Mongo object id.
    pnid = serializers.CharField(max_length=24, min_length=24)
    # typical access level. 0 - private, 1 - public
    access_level = serializers.IntegerField(default=co.PRIVATE_ACCESS)
    # Shared to uids.
    shared = serializers.CharField()
    # Some name can be used to determine an object.
    name = serializers.CharField(source='get_type')

    def get_type(self):
        raise NotImplemented()


#TODO implement specific data field.
class NodeSerializer(AbstractNodeSerializer):
    def get_type(self):
        return 'node'


class ResourceSerializer(AbstractNodeSerializer):
    def get_type(self):
        return 'resource'

