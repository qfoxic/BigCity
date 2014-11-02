from rest_framework import permissions
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework import status

import mfs.nodes.managers as nds
import mfs.users.managers as usr
import mfs.common.views as vws
import mfs.common.lib as clib


class NodesViewSet(vws.BaseViewSet):
    permission_classes = [permissions.IsAuthenticated]
    manager_class = nds.NodesManager

    @link
    def show(self, request, parent=None):
        """List all nodes under parent.
        If parent wasn't specified list top level nodes.
        """
        return Response(data=self.manager.ls(parent))

    def create(self, request):
        uid = self.request.user.pk
        um = usr.UsersManager(request)
        gres = um.groups(uid)
        if gres.get('error'):
            return Response(data=gres, status=status.HTTP_400_BAD_REQUEST)
        elif not gres.get('result'):
            err = clib.jsonerror('User should be assigned to at least one group')
            return Response(data=err, status=status.HTTP_400_BAD_REQUEST)
        res = self.manager.add(uid, gres.get('result')[0]['id'])
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
