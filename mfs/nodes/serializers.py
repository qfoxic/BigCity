from mfs.nodes.models import (Node, Image)
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


class ImageSerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Image
        fields = ('id', 'parent', 'path', 'title', 'perm', 'content', 'uid',
                  'gid', 'content_type', 'asset_type')


class NodeSerializerList(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Node
        fields = ('id', 'perm', 'uid', 'kind',
                  'gid', 'parent', 'path', 'created', 'updated')


class ImageSerializerList(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Image
        fields = ('id', 'title', 'perm', 'uid',
                  'gid', 'content_type')
