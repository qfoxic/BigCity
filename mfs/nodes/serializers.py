from mfs.nodes.models import Node
from mfs.common.serializers import MongoEngineModelSerializer
"""
The basic idea is that we have nodes and their resources.
Nodes can be hierarchical.

Everything is build around one record with different types.
Every record can have own data: that is python dict.

Each resource can have special field - kind.
We are able to find node's resource by kind without specifying id.

Specific node type must inherit NodeSerializer, specify it's own type,
specify serializer for data.
"""


class NodeSerializer(MongoEngineModelSerializer):
    class Meta:
        depth = 1
        model = Node
        fields = ('id', 'uid', 'perm',
                  'created', 'updated', 'parent', 'shared',
                  'gid', 'path')
        read_only_fields = ('path',)

