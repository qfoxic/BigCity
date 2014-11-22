import mfs.common.lib as clib
from mfs.nodes.serializers import NodeSerializer
from mfs.nodes.serializers import ResourceSerializer


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
        res = clib.get_obj(self.serializer, **{'pk': nid})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        res['object'].delete()
        return clib.jsonsuccess('Object id:<%s> has been removed' % (nid,))

    def upd(self, nid):
        res = clib.get_obj(self.serializer, **{'pk': nid})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'],
                              data=self.request.DATA,
                              partial=True)
        if srl.is_valid():
            srl.save()
            return clib.jsonresult(srl.data)
        return clib.jsonerror(''.join([','.join([k + '-' + ''.join(v)]) for k, v in srl.errors.items()]))

    def data(self, nid):
        res = clib.get_obj(self.serializer, **{'pk': nid})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'])
        return clib.jsonresult(srl.data)


class ResourcesManager(clib.BaseManager):
    serializer = ResourceSerializer

    def ls(self):
        queryset = self.serializer.Meta.model.objects.all()
        return clib.jsonresult(self.serializer(queryset, many=True).data)

    def add(self, pid):
        s = self.serializer(data=self.request.DATA)
        if s.is_valid():
            s.save()
            return clib.jsonresult(s.data)
        return clib.jsonerror(s.errors)

    def rm(self, nid):
        res = clib.get_obj(self.serializer, **{'pk': nid})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        res['object'].delete()
        return clib.jsonsuccess('Object id:<%s> has been removed' % (nid,))

    def upd(self, nid):
        res = clib.get_obj(self.serializer, **{'pk': nid})
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'],
                              data=self.request.DATA,
                              partial=True)
        if srl.is_valid():
            srl.save()
            return clib.jsonresult(srl.data)
        return clib.jsonerror(''.join([','.join([k + '-' + ''.join(v)]) for k, v in srl.errors.items()]))

    def data(self, **kwargs):
        res = clib.get_obj(self.serializer, **kwargs)
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'])
        return clib.jsonresult(srl.data)

