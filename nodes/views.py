from rest_framework.generics import ListAPIView
from mfs.nodes.views import NodesViewSet
from mfs.common.search import MongoSearchFilter
from nodes.managers import CategoryManager, AdvertManager



class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


class CategoryListView(ListAPIView):
    paginate_by = None
    filter_backends = (MongoSearchFilter,)
    serializer_class = CategoryManager.serializer

    def get_queryset(self):
        pid = self.kwargs.get('category_id')
        return CategoryManager(self.request).categories_queryset(pid)


class PaginatedAdvertsView(ListAPIView):
    serializer_class = AdvertManager.serializer
    filter_backends = (MongoSearchFilter,)
    search_fields = ('rooms', 'square_gen', 'square_live', 'room_height',
                     'floors', 'floor', 'wall_type', 'build_type', 'price')

    def get_queryset(self):
        data = self.request.GET
        search = data.get('search', '').split(',')
        order = data.get('order', '').split(',') # Comma separated.
        pid = self.kwargs.get('category_id')
        query = None
        if 'near' in search:
            query = AdvertManager(self.request).nearest_queryset(pid)
        elif 'within' in search:
            query = AdvertManager(self.request).within_queryset(pid)
        elif 'region' in search:
            query = AdvertManager(self.request).regions_queryset(pid)
        elif 'city' in search:
            query = AdvertManager(self.request).cities_queryset(pid)
        elif 'country' in search:
            query = AdvertManager(self.request).countries_queryset(pid)
        else:
            query = AdvertManager(self.request).all_queryset(pid)
        if order:
            query = query.order_by(*order)
        return query


