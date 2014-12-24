from rest_framework.generics import ListAPIView
from mfs.nodes.views import NodesViewSet, ResourcesViewSet
from nodes.managers import (CategoryManager, AdvertManager,
                            AddressResourceManager,
                            BuildingPropertiesResourceManager,
                            PriceResourceManager, PosterResourceManager)
from nodes.filters import CategoryFilterBackend


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class PaginatedCategoriesView(ListAPIView):
    paginate_by = None
    serializer_class = CategoryManager.serializer
    filter_backends = (CategoryFilterBackend,)

    def get_queryset(self):
        return CategoryManager(self.request).categories_queryset()


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

