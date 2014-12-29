from rest_framework.generics import ListAPIView
from mfs.nodes.views import NodesViewSet
from nodes.managers import CategoryManager, AdvertManager


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


class CategoryListView(ListAPIView):
    paginate_by = None
    serializer_class = CategoryManager.serializer

    def get_queryset(self):
        return CategoryManager(self.request).categories_queryset()


class PaginatedAdvertsByAddressView(ListAPIView):
    serializer_class = AdvertManager.serializer

    def get_queryset(self):
        data = self.request.GET
        search = data.get('search', 'near').split(',')
        order = data.get('order', '').split(',') # Comma separated.
        query = None
        if 'near' in search:
            query = AdvertManager(self.request).nearest_queryset()
        elif 'region' in search:
            query = AdvertManager(self.request).regions_queryset()
        elif 'city' in search:
            query = AdvertManager(self.request).cities_queryset()
        elif 'country' in search:
            query = AdvertManager(self.request).countries_queryset()
        if order:
            query.order_by(*order)
        return query


