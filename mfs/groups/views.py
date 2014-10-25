from rest_framework import permissions
from rest_framework.response import Response

import mfs.groups.lib as grp
from mfs.common.views import BaseViewSet
from mfs.common.permissions import IsAdminGroup


class GroupViewSet(BaseViewSet):
    permission_classes = [IsAdminGroup, permissions.IsAuthenticated]
    manager_class = grp.GroupManager

    def list(self, request):
        return Response(data=self.manager.ls())

    def create(self, request):
        return Response(data=self.manager.add())

    def retrieve(self, request, pk=None):
        return Response(data=self.manager.data(pk))

    def update(self, request, pk=None):
        return Response(data=self.manager.upd(pk))

    def destroy(self, request, pk=None):
        return Response(data=self.manager.rm(pk))
