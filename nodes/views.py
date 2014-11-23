from mfs.nodes.views import NodesViewSet
from nodes.managers import CategoryManager

class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager
