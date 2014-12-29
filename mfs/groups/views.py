from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

import mfs.groups.managers as grp
from mfs.common.views import BaseViewSet
from mfs.common.permissions import IsAdminGroup


class GroupViewSet(BaseViewSet):
    #permission_classes = [IsAdminGroup, permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]
    manager_class = grp.GroupManager

    def list(self, request):
        return Response(data=self.manager.ls())

    def create(self, request):
        res = self.manager.add()
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def retrieve(self, request, pk=None):
        return Response(data=self.manager.data(pk=pk))

    def update(self, request, pk=None):
        res = self.manager.upd(pk=pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def destroy(self, request, pk=None):
        return Response(data=self.manager.rm(pk))
