from mfs.nodes.managers import NodesManager
from nodes.serializers import CategorySerializer


class CategoryManager(NodesManager):
    serializer = CategorySerializer
