import mfs.common.lib as clib
from mfs.groups.serializers import GroupSerializer


def ls(request):
    queryset = GroupSerializer.Meta.model.objects.all()
    return GroupSerializer(queryset, many=True).data


def add(request):
    srl = GroupSerializer(data=request.DATA)
    if srl.is_valid():
        srl.save()
        return clib.jsonresult(srl.data)
    return clib.jsonerror(''.join([','.join(e) for e in srl.errors.values()]))


def rm(request, pk):
    res = clib.get_obj(GroupSerializer, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    res['object'].delete()
    return clib.jsonsuccess('Object id:<%s> has been removed' % (pk,))


def upd(request, pk):
    res = clib.get_obj(GroupSerializer, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    srl = GroupSerializer(res['object'], data=request.DATA)
    if srl.is_valid():
        srl.save()
        return clib.jsonresult(srl.data)
    return clib.jsonerror(''.join([','.join(e) for e in srl.errors.values()]))


def data(request, pk):
    res = clib.get_obj(GroupSerializer, pk)
    if res.get('error'):
        return clib.jsonerror(res['error'])
    srl = GroupSerializer(res['object'])
    return clib.jsonresult(srl.data)

