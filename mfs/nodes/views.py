from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import link
from rest_framework import status

import mfs.nodes.managers as nds
import mfs.users.managers as usr
import mfs.common.views as vws
import mfs.common.lib as clib
import mfs.common.constants as co


# TODO. Add change group functionality.
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
        gids = [i[0] for i in gres.get('result')]
        res = self.manager.add(uid, gids)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def retrieve(self, request, pk=None):
        uid = request.user.pk
        um = usr.UsersManager(request)
        user = um.data(uid)
        node = self.manager.data(pk)
        if not clib.check_perm(node['result'], user['result'], co.READ):
            return Response(
                data=clib.jsonerror('You do not have read permissions'),
                status=status.HTTP_403_FORBIDDEN)
        return Response(data=self.manager.data(pk))

    def update(self, request, pk=None):
        uid = request.user.pk
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
        uid = request.user.pk
        um = usr.UsersManager(request)
        user = um.data(uid)
        node = self.manager.data(pk)
        if not clib.check_perm(node['result'], user['result'], co.WRITE):
            return Response(
                data=clib.jsonerror('You do not have write permissions'),
                status=status.HTTP_403_FORBIDDEN)
        return Response(data=self.manager.rm(pk))

    @link()
    def reso_by_tag(self, request, pk=None):
        uid = request.user.pk
        tag = request.GET.get('tag')
        um = usr.UsersManager(request)
        user = um.data(uid)
        node = self.manager.data(pk)
        rm = nds.ResourcesManager(request)
        if not clib.check_perm(node['result'], user['result'], co.READ):
            return Response(
                data=clib.jsonerror('You do not have read permissions'),
                status=status.HTTP_403_FORBIDDEN)
        return Response(data=rm.data(parent=node['result']['id'], tag=tag))


class ResourcesViewSet(vws.BaseViewSet):
    permission_classes = [permissions.IsAuthenticated,]
    manager_class = nds.ResourcesManager

    def create(self, request):
        uid = request.user.pk
        nid = request.DATA.get('parent')
        nm = nds.NodesManager(request)
        um = usr.UsersManager(request)
        user = um.data(uid)
        node = nm.data(nid)
        if node.get('error'):
            return Response(data=node,
                            status=status.HTTP_400_BAD_REQUEST)
        if not clib.check_perm(node['result'], user['result'], co.READ):
            return Response(
                data=clib.jsonerror('You do not have read permissions to a node'),
                status=status.HTTP_403_FORBIDDEN)
        res = self.manager.add(nid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)

    def retrieve(self, request, pk=None):
        uid = self.request.user.pk
        um = usr.UsersManager(request)
        user = um.data(uid)
        resource = self.manager.data(pk=pk)
        if not clib.check_perm(resource['result']['parent'],
                               user['result'], co.READ):
            return Response(
                data=clib.jsonerror('You do not have read permissions'),
                status=status.HTTP_403_FORBIDDEN)
        return Response(data=resource)

#    def update(self, request, pk=None):
#        uid = self.request.user.pk
#        um = usr.UsersManager(request)
#        user = um.data(uid)
#        node = self.manager.data(pk)
#        if not clib.check_perm(node['result'], user['result'], co.WRITE):
#            return Response(
#                data=clib.jsonerror('You do not have write permissions'),
#                status=status.HTTP_403_FORBIDDEN)
#        res = self.manager.upd(pk)
#        if res.get('error'):
#            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
#        return Response(data=res)

#    def destroy(self, request, pk=None):
#        uid = self.request.user.pk
#        um = usr.UsersManager(request)
#        user = um.data(uid)
#        node = self.manager.data(pk)
#        if not clib.check_perm(node['result'], user['result'], co.WRITE):
#            return Response(
#                data=clib.jsonerror('You do not have write permissions'),
#                status=status.HTTP_403_FORBIDDEN)
#        return Response(data=self.manager.rm(pk))
