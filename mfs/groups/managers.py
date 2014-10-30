import mfs.common.lib as clib
from mfs.groups.serializers import GroupSerializer


class GroupManager(clib.BaseManager):
    serializer = GroupSerializer

    def ls(self):
        queryset = self.serializer.Meta.model.objects.all()
        return self.serializer(queryset, many=True).data

    def add(self):
        srl = self.serializer(data=self.request.DATA)
        if srl.is_valid():
            srl.save()
            return clib.jsonresult(srl.data)
        return clib.jsonerror(''.join([','.join(e) for e in srl.errors.values()]))

    def rm(self, pk):
        res = clib.get_obj(self.serializer, pk)
        if res.get('error'):
            return clib.jsonerror(res['error'])
        res['object'].delete()
        return clib.jsonsuccess('Object id:<%s> has been removed' % (pk,))

    def upd(self, pk):
        res = clib.get_obj(self.serializer, pk)
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'], data=self.request.DATA)
        if srl.is_valid():
            srl.save()
            return clib.jsonresult(srl.data)
        return clib.jsonerror(''.join([','.join(e) for e in srl.errors.values()]))

    def data(self, pk):
        res = clib.get_obj(self.serializer, pk)
        if res.get('error'):
            return clib.jsonerror(res['error'])
        srl = self.serializer(res['object'])
        return clib.jsonresult(srl.data)

