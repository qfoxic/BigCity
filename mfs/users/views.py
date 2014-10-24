from rest_framework import viewsets, permissions
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework import status

import mfs.users.lib as usr
import mfs.groups.lib as grp
from mfs.users.serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer = UserSerializer

    def list(self, request):
        return Response(data=usr.ls(request, self.serializer))

    def create(self, request):
        return Response(data=usr.add(request, self.serializer))

    def retrieve(self, request, pk=None):
        return Response(data=usr.data(request, pk, self.serializer))

    def update(self, request, pk=None):
        return Response(data=usr.upd(request, pk, self.serializer))

    def destroy(self, request, pk=None):
        return Response(data=usr.rm(request, pk, self.serializer))

    @action()
    def chpasswd(self, request, pk=None):
        return Response(data=usr.chpasswd(request, pk, self.serializer))

    @action()
    def addgroup(self, request, pk=None):
        gid = request.DATA.get('gid')
        res = grp.data(request, gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = usr.data(request, pk, self.serializer)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=usr.add_group(request, pk, gid, self.serializer))

    @action()
    def rmgroup(self, request, pk=None):
        gid = request.DATA.get('gid')
        res = grp.data(request, gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = usr.data(request, pk, self.serializer)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=usr.rm_group(request, pk, gid, self.serializer))

    @link()
    def groups(self, request, pk=None):
        return Response(data=usr.groups(request, pk, self.serializer))
