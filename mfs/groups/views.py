from rest_framework import viewsets, permissions
from rest_framework.response import Response

import mfs.groups.lib as grp
from mfs.common.permissions import IsAdminGroup


class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminGroup, permissions.IsAuthenticated]

    def list(self, request):
        return Response(data=grp.ls(request)) 

    def create(self, request):
        return Response(data=grp.add(request))

    def retrieve(self, request, pk=None):
        return Response(data=grp.data(request, pk))

    def update(self, request, pk=None):
        return Response(data=grp.upd(request, pk))

    def destroy(self, request, pk=None):
        return Response(data=grp.rm(request, pk))
