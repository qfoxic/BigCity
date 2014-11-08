import mfs.common.lib as clib
from mfs.nodes.serializers import NodeSerializer

#TODO. Create init super user and some init group.

class NodesManager(clib.BaseManager):
    serializer = NodeSerializer

    def ls(self):
        queryset = self.serializer.Meta.model.objects.all()
        return clib.jsonresult(self.serializer(queryset, many=True).data)

    def add(self, uid, access_levels):
        data = {'uid': uid,
                'access_level': access_levels}
        data.update(self.request.DATA)
        s = self.serializer(data=data)
        if s.is_valid():
            s.save()
            return clib.jsonresult(s.data)
        return clib.jsonerror(s.errors)

    def rm(self, nid):
        pass
        #res = clib.get_obj(_get_user_serializer(request), pk)
        #if res.get('error'):
        #    return clib.jsonerror(res['error'])
        #res['object'].delete()
        #return clib.jsonsuccess('Object id:<%s> has been removed' % (pk,))

    def upd(self, nid):
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

    def data(self, nid):
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