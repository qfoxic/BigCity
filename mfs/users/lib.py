import mfs.common.lib as clib


def ls(request, srl):
    queryset = srl.Meta.model.objects.all()
    return clib.jsonresult(srl(queryset, many=True).data)


def add(request, srl):
    s = srl(data=request.DATA)
    if s.is_valid():
        s.save()
        return clib.jsonresult(s.data)
    return clib.jsonerror(''.join([','.join(e) for e in s.errors.values()]))


def rm(request, pk, srl):
    res = clib.get_obj(srl, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    res['object'].delete()
    return clib.jsonsuccess('Object id:<%s> has been removed' % (pk,))


def upd(request, pk, srl):
    res = clib.get_obj(srl, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    srl = srl(res['object'], data=request.DATA, partial=True)
    if srl.is_valid():
        srl.save()
        return clib.jsonresult(srl.data)
    return clib.jsonerror(''.join([','.join([k + '-' + ''.join(v)]) for k, v in srl.errors.items()]))


def data(request, pk, srl):
    res = clib.get_obj(srl, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    srl = srl(res['object'])
    return clib.jsonresult(srl.data)


def chpasswd(request, pk, srl):
    res = clib.get_obj(srl, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    user = res['object']
    try:
        user.set_password(request.DATA['password'])
        user.save()
        return clib.jsonsuccess('Password has been changed')
    except KeyError:
        return clib.jsonerror('Could not change password')


def add_group(request, uid, gid, srl):
    try:
        user = srl.Meta.model.objects.get(pk=uid)
        user.groups.add(int(gid))
    except Exception, e:
        return clib.jsonerror(str(e))
    return clib.jsonsuccess('User has been assigned to a group %s' % gid)


def rm_group(request, uid, gid, srl):
    try:
        user = srl.Meta.model.objects.get(pk=uid)
        user.groups.remove(int(gid))
    except Exception, e:
        return clib.jsonerror(str(e))
    return clib.jsonsuccess('User has been removed from a group %s' % gid)


def groups(request, uid, srl):
    try:
        user = srl.Meta.model.objects.get(pk=uid)
    except Exception, e:
        return clib.jsonerror(str(e))
    return clib.jsonresult(user.groups.values_list('name', flat=True))
