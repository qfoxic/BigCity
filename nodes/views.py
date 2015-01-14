from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from mfs.nodes.views import NodesViewSet
from mfs.common.search import MongoSearchFilter
from nodes.managers import CategoryManager, AdvertManager, AssetManager


class CategoryViewSet(NodesViewSet):
    manager_class = CategoryManager


class AdvertViewSet(NodesViewSet):
    manager_class = AdvertManager


class AssetViewSet(NodesViewSet):
    parser_classes = (MultiPartParser, FormParser)
    manager_class = AssetManager

    def create(self, request):
        uid = request.user.pk
        return Response({})
        #um = usr.UsersManager(request)
        #gres = um.groups(uid)
        #if gres.get('error'):
        #    return Response(data=gres, status=status.HTTP_400_BAD_REQUEST)
        #elif not gres.get('result'):
        #    err = clib.jsonerror('User should be assigned to at least one group')
        #    return Response(data=err, status=status.HTTP_400_BAD_REQUEST)
        #gids = [i[0] for i in gres.get('result')]
        #res = self.manager.add(uid=uid, gid=gids[0])
        #if res.get('error'):
        #    return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        #return Response(data=res)

    def retrieve(self, request, pk=None):
        #uid = request.user.pk
        #um = usr.UsersManager(request)
        #user = um.data(pk=uid)
        #node = self.manager.data(pk=pk)
        #if not clib.check_perm(node['result'], user['result'], co.READ):
        #    return Response(
        #        data=clib.jsonerror('You do not have read permissions'),
        #        status=status.HTTP_401_UNAUTHORIZED)
        assets = self.manager.serializer.Meta.model
        asset = assets.objects.get(pk=pk)
        from django.views.static import serve as djserve
        import shutil
        import tempfile
        tmp_file = tempfile.NamedTemporaryFile()
        shutil.copyfileobj(asset.content, tmp_file)
        request = djserve(request, tmp_file.name, '/')
        request['Content-Disposition'] = 'inline;filename=123.jpg'
        return request


class AssetsListView(ListAPIView):
    paginate_by = None
    filter_backends = (MongoSearchFilter,)
    serializer_class = AssetManager.serializer

    def get_queryset(self):
        pid = self.kwargs.get('advert_id')
        content_type = self.request.get('asset_type', 'image')
        return AssetManager(self.request).assets_queryset(pid, content_type)


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


