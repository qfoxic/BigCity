from rest_framework import permissions
from django.http import StreamingHttpResponse

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route

import mfs.nodes.managers as nds
import mfs.nodes.serializers as srls
import mfs.users.managers as usr
import mfs.common.views as vws
import mfs.common.utils as clib
import mfs.common.constants as co
import mfs.common.search as srch


class NodesViewSet(vws.BaseViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    manager_class = nds.NodesManager

    def create(self, request):
        uid = request.user.pk
        um = usr.UsersManager(request)
        gres = um.groups(uid)
        if gres.get('error'):
            return Response(data=gres, status=status.HTTP_400_BAD_REQUEST)
        elif not gres.get('result'):
            err = clib.jsonerror('User should be assigned to at least one group')
            return Response(data=err, status=status.HTTP_400_BAD_REQUEST)
        gids = [i['id'] for i in gres.get('result')]
        res = self.manager.add(uid=uid, gid=gids[0])
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def retrieve(self, request, pk=None):
        uid = request.user.pk
        um = usr.UsersManager(request)
        user = um.data(pk=uid)
        node = self.manager.data(pk=pk)
        if not clib.check_perm(node['result'], user['result'], co.READ):
            return Response(
                data=clib.jsonerror('You do not have read permissions'),
                status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=self.manager.data(pk=pk))

    def update(self, request, pk=None):
        uid = request.user.pk
        um = usr.UsersManager(request)
        user = um.data(pk=uid)
        node = self.manager.data(pk=pk)
        if not clib.check_perm(node['result'], user['result'], co.WRITE):
            return Response(
                data=clib.jsonerror('You do not have write permissions'),
                status=status.HTTP_401_UNAUTHORIZED)
        res = self.manager.upd(pk=pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def destroy(self, request, pk=None):
        uid = request.user.pk
        um = usr.UsersManager(request)
        user = um.data(pk=uid)
        node = self.manager.data(pk=pk)
        if not clib.check_perm(node['result'], user['result'], co.WRITE):
            return Response(
                data=clib.jsonerror('You do not have write permissions'),
                status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=self.manager.rm(pk))


class ImageViewSet(NodesViewSet):
    parser_classes = (MultiPartParser, FormParser)
    manager_class = nds.ImageManager

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


class NodesListView(ListAPIView):
    paginate_by = None
    filter_backends = (srch.MongoSearchFilter,)
    serializer_class = srls.NodeSerializerList

    def get(self, request, *args, **kwargs):
        if not permissions.IsAdminUser():
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(NodesListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        pid = self.kwargs.get('nid')
        return nds.NodesManager(self.request).admin_queryset(pid)


class ImagesListView(ListAPIView):
    paginate_by = None
    filter_backends = (srch.MongoSearchFilter,)
    serializer_class = srls.ImageSerializerList

    def get_queryset(self):
        pid = self.kwargs.get('advert_id')
        content_type = self.request.get('asset_type', 'image')
        return nds.ImageManager(self.request).assets_queryset(pid, content_type)
