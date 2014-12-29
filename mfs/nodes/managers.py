import mfs.common.lib as clib
from mfs.nodes.serializers import NodeSerializer
from mfs.nodes.serializers import ResourceSerializer


class NodesManager(clib.BaseManager):
    serializer = NodeSerializer

    def chgroup(self, **kwargs):
        pass


class ResourcesManager(clib.BaseManager):
    serializer = ResourceSerializer



