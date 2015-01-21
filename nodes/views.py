from django.http import StreamingHttpResponse

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

import mfs.users.managers as usr
import mfs.common.lib as clib
import mfs.common.constants as co
from rest_framework.decorators import detail_route

from mfs.nodes.views import NodesViewSet
from mfs.common.search import MongoSearchFilter
from nodes.managers import CategoryManager, AdvertManager, ImageManager


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


class ImageViewSet(NodesViewSet):
    parser_classes = (MultiPartParser, FormParser)
    manager_class = ImageManager

    @detail_route()
    def image(self, request, pk=None):
        uid = request.user.pk
        um = usr.UsersManager(request)
        user = um.data(pk=uid)
        node = self.manager.data(pk=pk)
        if not clib.check_perm(node['result'], user['result'], co.READ):
            return Response(
                data=clib.jsonerror('You do not have read permissions'),
                status=status.HTTP_401_UNAUTHORIZED)
        assets = self.manager.serializer.Meta.model
        asset = assets.objects.get(pk=pk)
        img = asset.content.thumbnail if request.GET.get('thumb') else asset.content.get()
        response = StreamingHttpResponse(img, content_type=asset.content_type)
        response['Content-Disposition'] = 'inline;filename='
        response['Content-Type'] = asset.content_type
        return response


class ImagesListView(ListAPIView):
    paginate_by = None
    filter_backends = (MongoSearchFilter,)
    serializer_class = ImageManager.serializer

    def get_queryset(self):
        pid = self.kwargs.get('advert_id')
        content_type = self.request.get('asset_type', 'image')
        return ImageManager(self.request).assets_queryset(pid, content_type)


class CategoryListView(ListAPIView):
    paginate_by = None
    filter_backends = (MongoSearchFilter,)
    serializer_class = CategoryManager.serializer
    search_fields = ('title',)

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


