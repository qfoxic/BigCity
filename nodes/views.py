import common.lib as clib
import common.constants as co


def _get_node_serializer(request):
    pass


def ls(request, uid):
    pass
    #srl = _get_user_serializer(request)
    #queryset = srl.model().objects.all()
    #return clib.jsonresult(srl(queryset, many=True).data)


def add(request, uid):
    pass
    #srl = _get_user_serializer(request)(data=request.DATA)
    #if srl.is_valid():
    #    srl.save()
    #    return clib.jsonresult(srl.data)
    #return clib.jsonerror(''.join([','.join(e) for e in srl.errors.values()]))


def rm(request, nid):
    pass
    #res = clib.get_obj(_get_user_serializer(request), pk)
    #if res.get('error'):
    #    return clib.jsonerror(res['error'])
    #res['object'].delete()
    #return clib.jsonsuccess('Object id:<%s> has been removed' % (pk,))


def update(request, nid):
    pass
    #usr_srl_class = _get_user_serializer(request)
    #res = clib.get_obj(usr_srl_class, pk)
    #if res.get('error'):
    #    return clib.jsonerror(res['error'])
    #srl = usr_srl_class(res['object'], data=request.DATA, partial=True)
    #if srl.is_valid():
    #    srl.save()
    #    return clib.jsonresult(srl.data)
    #return clib.jsonerror(''.join([','.join([k + '-' + ''.join(v)]) for k, v in srl.errors.items()]))


def data(request, nid):
    pass
    #usr_srl_class = _get_user_serializer(request)
    #res = clib.get_obj(usr_srl_class, pk)
    #if res.get('error'):
    #    return clib.jsonerror(res['error'])
    #srl = usr_srl_class(res['object'])
    #return clib.jsonresult(srl.data)


#def chown(request, uid, gid):
#    pass
#    #srl = _get_user_serializer(request)
#    #try:
#    #    user = srl.model().objects.get(pk=uid)
#    #    user.groups.add(int(gid))
#    #except Exception, e:
#    #    return clib.jsonerror(str(e))
#    #return clib.jsonsuccess('User has been assigned to a group %s' % gid)
