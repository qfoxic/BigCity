from mfs.nodes.managers import NodesManager
from nodes.serializers import CategorySerializer, AdvertSerializer, MessageSerializer


class CategoryManager(NodesManager):
    serializer = CategorySerializer


class AdvertManager(NodesManager):
    serializer = AdvertSerializer


class MessageManager(NodesManager):
    serializer = MessageSerializer
