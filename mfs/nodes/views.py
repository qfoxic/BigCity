from rest_framework import permissions
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework import status

import mfs.nodes.managers as nds
import mfs.users.managers as usr
import mfs.common.views as vws
import mfs.common.lib as clib
import mfs.common.constants as co


class NodesViewSet(vws.BaseViewSet):
    permission_classes = [permissions.IsAuthenticated]
    manager_class = nds.NodesManager

    @link()
    def show(self, request, pk=None):
        """List all nodes under a parent.
        If parent wasn't specified then list top level nodes.
        pk == parent id.
        """
        return Response(data=self.manager.ls(pk))

    def create(self, request):
        uid = self.request.user.pk
        um = usr.UsersManager(request)
        gres = um.groups(uid)
        if gres.get('error'):
            return Response(data=gres, status=status.HTTP_400_BAD_REQUEST)
        elif not gres.get('result'):
            err = clib.jsonerror('User should be assigned to at least one group')
            return Response(data=err, status=status.HTTP_400_BAD_REQUEST)
        gids = [i[0] for i in gres.get('result')]
        res = self.manager.add(uid, gids)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def retrieve(self, request, pk=None):
        uid = self.request.user.pk
        um = usr.UsersManager(request)
        user = um.data(uid)
        node = self.manager.data(pk)
        if not clib.check_perm(node['result'], user['result'], co.READ):
            return Response(
                data=clib.jsonerror('You do not have read permissions'),
                status=status.HTTP_403_FORBIDDEN)
        return Response(data=self.manager.data(pk))

    def update(self, request, pk=None):
        uid = self.request.user.pk
        um = usr.UsersManager(request)
        user = um.data(uid)
        node = self.manager.data(pk)
        if not clib.check_perm(node['result'], user['result'], co.WRITE):
            return Response(
                data=clib.jsonerror('You do not have write permissions'),
                status=status.HTTP_403_FORBIDDEN)
        res = self.manager.upd(pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def destroy(self, request, pk=None):
        return Response(data=self.manager.rm(pk))
