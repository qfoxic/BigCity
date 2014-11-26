from mfs.nodes.views import NodesViewSet, ResourcesViewSet
from nodes.managers import (CategoryManager, AdvertManager,
    AddressResourceManager, BuildingPropertiesResourceManager,
    PriceResourceManager, PosterResourceManager)


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


class AddressResourceViewSet(ResourcesViewSet):
    manager_class = AddressResourceManager


class BuildingPropertiesResourceViewSet(ResourcesViewSet):
    manager_class = BuildingPropertiesResourceManager


class PriceResourceViewSet(ResourcesViewSet):
    manager_class = PriceResourceManager


class PosterResourceViewSet(ResourcesViewSet):
    manager_class = PosterResourceManager

