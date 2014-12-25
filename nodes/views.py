from rest_framework.generics import ListAPIView
from mfs.nodes.views import NodesViewSet, ResourcesViewSet
from nodes.managers import (CategoryManager, AdvertManager,
                            AddressResourceManager,
                            BuildingPropertiesResourceManager,
                            PriceResourceManager, PosterResourceManager)


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class CategoryListView(ListAPIView):
    paginate_by = None
    serializer_class = CategoryManager.serializer

    def get_queryset(self):
        return CategoryManager(self.request).categories_queryset()


class PaginatedAdvertsByAddressView(ListAPIView):
    serializer_class = AddressResourceManager.serializer

    def get_queryset(self):
        data = self.request.GET
        kind = data.get('search', 'nearest')
        if kind == 'nearest':
            return AddressResourceManager(self.request).nearest_queryset()
        elif kind == 'regions':
            return AddressResourceManager(self.request).regions_queryset()
        elif kind == 'cities':
            return AddressResourceManager(self.request).cities_queryset()
        elif kind == 'countries':
            return AddressResourceManager(self.request).countries_queryset()


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

