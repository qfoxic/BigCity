import mfs.common.lib as clib
from mfs.nodes.serializers import NodeSerializer


class NodesManager(clib.BaseManager):
    serializer = NodeSerializer

