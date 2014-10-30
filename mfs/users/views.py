from django.contrib.auth import authenticate, login

from rest_framework import permissions
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework import status

import mfs.users.managers as usr
import mfs.groups.managers as grp
import mfs.common.views as vws


class UserViewSet(vws.BaseViewSet):
    permission_classes = [permissions.IsAuthenticated]
    manager_class = usr.UsersManager

    def list(self, request):
        return Response(data=self.manager.ls())

    def create(self, request):
        res = self.manager.add()
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def retrieve(self, request, pk=None):
        return Response(data=self.manager.data(pk))

    def update(self, request, pk=None):
        res = self.manager.upd(pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def destroy(self, request, pk=None):
        return Response(data=self.manager.rm(pk))

    @action()
    def chpasswd(self, request, pk=None):
        return Response(data=self.manager.chpasswd(pk))

    @action()
    def addgroup(self, request, pk=None):
        gid = request.DATA.get('gid')
        group_manager = grp.GroupManager(request)
        res = group_manager.data(gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = self.manager.data(pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=self.manager.add_group(pk, gid))

    @action()
    def rmgroup(self, request, pk=None):
        gid = request.DATA.get('gid')
        group_manager = grp.GroupManager(request)
        res = group_manager.data(gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = self.manager.data(pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=self.manager.rm_group(pk, gid))

    @link()
    def groups(self, request, pk=None):
        return Response(data=self.manager.groups(pk))


class UserLoginView(vws.BaseViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        username, password = request.DATA.get('username'), request.DATA.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response()
        return Response(status=status.HTTP_400_BAD_REQUEST)
