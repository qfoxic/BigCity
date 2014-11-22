from django.contrib.auth import authenticate, login, logout
import mfs.common.lib as clib
from mfs.users.serializers import UserSerializer


class UsersManager(clib.BaseManager):
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
            return True
        return False

    def ls(self):
        queryset = self.serializer.Meta.model.objects.all()
        return clib.jsonresult(self.serializer(queryset, many=True).data)

    def add(self):
        s = self.serializer(data=self.request.DATA)
        if s.is_valid():
            s.save()
            return clib.jsonresult(s.data)
        return clib.jsonerror(''.join([','.join(e) for e in s.errors.values()]))

    def rm(self, pk):
        res = clib.get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        res['object'].delete()
        return clib.jsonsuccess('Object id:<%s> has been removed' % (pk,))

    def upd(self, pk):
        res = clib.get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'], data=self.request.DATA, partial=True)
        if srl.is_valid():
            srl.save()
            return clib.jsonresult(srl.data)
        return clib.jsonerror(''.join([','.join([k + '-' + ''.join(v)]) for k, v in srl.errors.items()]))

    def data(self, pk):
        res = clib.get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'])
        gids = self.groups(res['object'].pk)
        srl.data['groups'] = gids['result']
        return clib.jsonresult(srl.data)

    def chpasswd(self, pk):
        res = clib.get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        user = res['object']
        try:
            user.set_password(self.request.DATA['password'])
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
        return clib.jsonresult(user.groups.values_list('id', 'name'))
