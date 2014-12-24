from mfs.nodes.managers import NodesManager, ResourcesManager
from mfs.users.managers import UsersManager
from nodes.serializers import (CategorySerializer,
                               AdvertSerializer, AddressResourceSerializer,
                               BuildingPropertiesResourceSerializer,
                               PriceResourceSerializer,
                               PosterResourceSerializer)


class CategoryManager(NodesManager):
    serializer = CategorySerializer

    def categories_queryset(self):
        user = self.request.user
        uid, groups = 0, []
        um = UsersManager(self.request)
        if user.is_authenticated():
            ures = um.data(pk=self.request.user.pk)
            if not ures.get('error'):
                uid, groups = user.pk, ures['result']['groups']
        queryset = self.serializer.Meta.model.nodes(
            uid, groups).only('parent', 'title', 'id', 'path')
        return queryset


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
