from rest_framework import serializers
from mfs.common import constants as co
from mfs.nodes.models import Node

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


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'uid', 'gid', 'perm', 'path', 'record_type',
                  'created', 'updated', 'parent', 'shared',
                  'access_level')
