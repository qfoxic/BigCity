from mfs.nodes.managers import NodesManager, ResourcesManager
from nodes.serializers import (CategorySerializer,
    AdvertSerializer, AddressResourceSerializer, BuildingPropertiesResourceSerializer,
    PriceResourceSerializer, PosterResourceSerializer)


class CategoryManager(NodesManager):
    serializer = CategorySerializer


class AdvertManager(NodesManager):
    serializer = AdvertSerializer


class AddressResourceManager(ResourcesManager):
    serializer = AddressResourceSerializer


class BuildingPropertiesResourceManager(ResourcesManager):
    serializer = BuildingPropertiesResourceSerializer


class PriceResourceManager(ResourcesManager):
    serializer = PriceResourceSerializer


class PosterResourceManager(ResourcesManager):
    serializer = PosterResourceSerializer
