from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token


import mfs.common.utils as clib
from mfs.common.managers import BaseManager
from mfs.users.serializers import UserSerializer
from mfs.common.constants import DEFAULT_GROUP


class UsersManager(BaseManager):
    serializer = UserSerializer

    def logout(self, request):
        try:
            logout(request)
            return True
        except Exception:
            return False

    def login(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            data = self.data(pk=user.id)
            data['result']['token'] = token.key
            return data
        return clib.jsonerror('Invalid credentials')

    def add(self, **kwargs):
        res = super(UsersManager, self).add(**kwargs)
        if res.get('error'):
            return res
        grp, _ = Group.objects.get_or_create(name=DEFAULT_GROUP)
        self.add_group(res['result']['id'], grp.id)
        return self.data(pk=res['result']['id'])

    def data(self, **kwargs):
        res = clib.get_obj(self.serializer, **kwargs)
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'])
        gids = self.groups(res['object'].pk)
        resp = clib.jsonresult(srl.data)
        resp['result']['groups'] = gids['result']
        return resp

    def chpasswd(self, pk):
        res = clib.get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        user = res['object']
        try:
            user.set_password(self.request.data['password'])
            user.save()
            return clib.jsonsuccess('Password has been changed')
        except KeyError:
            return clib.jsonerror('Could not change password')

    def add_group(self, uid, gid):
        try:
            user = self.serializer.Meta.model.objects.get(pk=uid)
            user.groups.add(int(gid))
        except Exception, e:
            return clib.jsonerror(str(e))
        return clib.jsonsuccess('User has been assigned to a group %s' % gid)

    def rm_group(self, uid, gid):
        try:
            user = self.serializer.Meta.model.objects.get(pk=uid)
            user.groups.remove(int(gid))
        except Exception, e:
            return clib.jsonerror(str(e))
        return clib.jsonsuccess('User has been removed from a group %s' % gid)

    def groups(self, uid):
        try:
            user = self.serializer.Meta.model.objects.get(pk=uid)
        except Exception, e:
            return clib.jsonerror(str(e))
        return clib.jsonresult(
            [(i[0], i[1]) for i in user.groups.values_list('id', 'name')]
        )
