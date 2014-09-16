from users.serializers import UserSerializer, RegularUserSerializer
import common.lib as clib
import common.constants as co


def _get_user_serializer(request):
    usr_type = request.GET.get('usr_type')
    usr_map = {co.REGULAR_USER: RegularUserSerializer}
    return usr_map.get(usr_type, UserSerializer)


def ls(request):
    srl = _get_user_serializer(request)
    queryset = srl.model().objects.all()
    return clib.jsonresult(srl(queryset, many=True).data)


def add(request):
    srl = _get_user_serializer(request)(data=request.DATA)
    if srl.is_valid():
        srl.save()
        return clib.jsonresult(srl.data)
    return clib.jsonerror(''.join([','.join(e) for e in srl.errors.values()]))


def rm(request, pk):
    res = clib.get_obj(_get_user_serializer(request), pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    res['object'].delete()
    return clib.jsonsuccess('Object id:<%s> has been removed' % (pk,))


def upd(request, pk):
    usr_srl_class = _get_user_serializer(request)
    res = clib.get_obj(usr_srl_class, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    srl = usr_srl_class(res['object'], data=request.DATA, partial=True)
    if srl.is_valid():
        srl.save()
        return clib.jsonresult(srl.data)
    return clib.jsonerror(''.join([','.join([k + '-' + ''.join(v)]) for k, v in srl.errors.items()]))


def data(request, pk):
    usr_srl_class = _get_user_serializer(request)
    res = clib.get_obj(usr_srl_class, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    srl = usr_srl_class(res['object'])
    return clib.jsonresult(srl.data)


def chpasswd(request, pk):
    res = clib.get_obj(_get_user_serializer(request), pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    user = res['object']
    try:
        user.set_password(request.DATA['password'])
        user.save()
        return clib.jsonsuccess('Password has been changed')
    except KeyError:
        return clib.jsonerror('Could not change password')


def add_group(request, uid, gid):
    srl = _get_user_serializer(request)
    try:
        user = srl.model().objects.get(pk=uid)
        user.groups.add(int(gid))
    except Exception, e:
        return clib.jsonerror(str(e))
    return clib.jsonsuccess('User has been assigned to a group %s' % gid)


def rm_group(request, uid, gid):
    srl = _get_user_serializer(request)
    try:
        user = srl.model().objects.get(pk=uid)
        user.groups.remove(int(gid))
    except Exception, e:
        return clib.jsonerror(str(e))
    return clib.jsonsuccess('User has been removed from a group %s' % gid)


def groups(request, uid):
    srl = _get_user_serializer(request)
    try:
        user = srl.model().objects.get(pk=uid)
    except Exception, e:
        return clib.jsonerror(str(e))
    return clib.jsonresult(user.groups.values_list('name', flat=True))
