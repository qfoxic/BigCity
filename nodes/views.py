from mfs.nodes.views import NodesViewSet
from nodes.managers import CategoryManager, AdvertManager


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


