from mfs.nodes.managers import NodesManager
from nodes.serializers import CategorySerializer, AdvertSerializer


class CategoryManager(NodesManager):
    serializer = CategorySerializer


class AdvertManager(NodesManager):
    serializer = AdvertSerializer

