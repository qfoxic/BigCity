from mfs.nodes.views import NodesViewSet
from nodes.managers import CategoryManager, AdvertManager, MessageManager


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


class MessageViewSet(NodesViewSet):
    manager_class = MessageManager

