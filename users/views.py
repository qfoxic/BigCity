from rest_framework import viewsets, permissions
from rest_framework.decorators import action, link
from rest_framework.response import Response
from rest_framework import status
import users.lib as usr
import groups.lib as grp


class UserViewSet(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]

    def list(self, request):
        return Response(data=usr.ls(request)) 

    def create(self, request):
        return Response(data=usr.add(request))

    def retrieve(self, request, pk=None):
        return Response(data=usr.data(request, pk))

    def update(self, request, pk=None):
        return Response(data=usr.upd(request, pk))

    def destroy(self, request, pk=None):
        return Response(data=usr.rm(request, pk))

    @action()
    def chpasswd(self, request, pk=None):
        return Response(data=usr.chpasswd(request, pk))

    @action()
    def addgroup(self, request, pk=None):
        gid = request.DATA.get('gid')
        res = grp.data(request, gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = usr.data(request, pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=usr.add_group(request, pk, gid))

    @action()
    def rmgroup(self, request, pk=None):
        gid = request.DATA.get('gid')
        res = grp.data(request, gid)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = usr.data(request, pk)
        if res.get('error'):
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=usr.rm_group(request, pk, gid))

    @link()
    def groups(self, request, pk=None):
        return Response(data=usr.groups(request, pk))

#class SellerUserViewSet(BaseUserViewSet):
#    serializer_class=SellerUserSerializer


#class AgencyUserViewSet(BaseUserViewSet):
#    serializer_class=AgencyUserSerializer


#class CompanyUserViewSet(BaseUserViewSet):
#    serializer_class=CompanyUserSerializer

