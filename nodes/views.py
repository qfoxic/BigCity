from mfs.nodes.views import NodesViewSet, ResourcesViewSet
from nodes.managers import (CategoryManager, AdvertManager,
    AddressResourceManager, BuildingPropertiesResourceManager,
    PriceResourceManager, PosterResourceManager)


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


# TODO. Get resource.
class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


class AddressResourceViewSet(ResourcesViewSet):
    manager_class = AddressResourceManager

    def get_node_manager(self, request):
        return AdvertManager(request)


class BuildingPropertiesResourceViewSet(ResourcesViewSet):
    manager_class = BuildingPropertiesResourceManager

    def get_node_manager(self, request):
        return AdvertManager(request)


class PriceResourceViewSet(ResourcesViewSet):
    manager_class = PriceResourceManager

    def get_node_manager(self, request):
        return AdvertManager(request)


class PosterResourceViewSet(ResourcesViewSet):
    manager_class = PosterResourceManager

    def get_node_manager(self, request):
        return AdvertManager(request)

