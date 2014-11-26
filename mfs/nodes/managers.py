import mfs.common.lib as clib
from mfs.nodes.serializers import NodeSerializer
from mfs.nodes.serializers import ResourceSerializer


class NodesManager(clib.BaseManager):
    serializer = NodeSerializer


class ResourcesManager(clib.BaseManager):
    serializer = ResourceSerializer



