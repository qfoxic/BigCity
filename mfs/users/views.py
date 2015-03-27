from rest_framework import permissions
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

import mfs.users.managers as usr
import mfs.groups.managers as grp
import mfs.common.views as vws
from mfs.common.permissions import IsAdminGroup, IsAuthenticatedCreateAllowed


#TODO Add reset password with emails.
class UserViewSet(vws.BaseViewSet):
    permission_classes = [IsAuthenticatedCreateAllowed]
    manager_class = usr.UsersManager

    def list(self, request):
        return Response(data=self.manager.ls())

    def create(self, request, pk=None):
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

    @detail_route(methods=['post'])
    def chpasswd(self, request, pk=None):
        return Response(data=self.manager.chpasswd(pk))

    @detail_route(methods=['post'])
    def addgroup(self, request, pk=None):
        gid = request.data.get('gid')
        group_manager = grp.GroupManager(request)
        res = group_manager.data(pk=gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = self.manager.data(pk=pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=self.manager.add_group(pk, gid))

    @detail_route(methods=['post'])
    def updgroups(self, request, pk=None):
        """Remove all user groups and add new ones."""
        gids = request.data.get('gids')
        group_manager = grp.GroupManager(request)
        ugids = self.manager.groups(pk)['result']
        added, failed, removed = [], [], []
        for ugid, _ in ugids:
            res = self.manager.rm_group(pk, ugid)
            if res.get('success'):
                removed.append(ugid)
        for gid in gids:
            try:
                group_manager.data(pk=gid)
            except Exception:
                failed.append(gid)
                continue
            self.manager.add_group(pk, gid)
            added.append(gid)
        res = self.manager.groups(pk)
        gids = res['result']
        res['result'] = {
            'gids': gids,
            'added': added,
            'failed': failed,
            'removed': removed
        }
        return Response(data=res)

    @detail_route(methods=['post'])
    def rmgroup(self, request, pk=None):
        gid = request.data.get('gid')
        group_manager = grp.GroupManager(request)
        res = group_manager.data(pk=gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = self.manager.data(pk=pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=self.manager.rm_group(pk, gid))

    @detail_route(methods=['get'])
    def groups(self, request, pk=None):
        return Response(data=self.manager.groups(pk))


class UserLoginView(vws.BaseViewSet):
    permission_classes = [permissions.AllowAny]
    manager_class = usr.UsersManager

    def create(self, request):
        username, password = (request.data.get('username'),
                              request.data.get('password'))
        res = self.manager.login(request, username, password)
        if 'error' in res:
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=res)


class UserLogoutView(vws.BaseViewSet):
    permission_classes = [permissions.AllowAny]
    manager_class = usr.UsersManager

    def list(self, request):
        res = self.manager.logout(request)
        if res:
            return Response(res)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


class UserTokenLoginView(views.ObtainAuthToken):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user = usr.UsersManager(request).data(pk=user.id)
        return Response({'token': token.key, 'user': user['result']})


class UserListViewSet(ListAPIView):
    permission_classes = [IsAdminGroup, permissions.IsAuthenticated]
    serializer_class = usr.UsersManager.serializer
    search_fields = ('username',)

    def get_queryset(self):
        queryset = self.serializer_class.Meta.model.objects.all()
        return queryset

