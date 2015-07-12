from mongoengine import ValidationError
from mfs.common.utils import jsonresult, get_obj, jsonerror, jsonsuccess
from mfs.common.serializers import cast_serializer


class BaseManager(object):
    def __init__(self, request=None, serializer=None):
        self.request = request
        if serializer:
            self.serializer = serializer

    def ls(self):
        queryset = self.serializer.Meta.model.objects.all()
        return jsonresult(self.serializer(queryset, many=True).data)

    def data(self, **kwargs):
        try:
            cast = kwargs.pop('cast')
        except KeyError:
            cast = False

        res = get_obj(self.serializer, **kwargs)
        if cast:
            self.serializer = (cast_serializer(kwargs.get('kind'))
                               or self.serializer)
        srl = self.serializer(res['object'], context={})
        return jsonresult(srl.data)

    def rm(self, pk):
        res = get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return jsonerror(res['error'])
        res['object'].delete()
        return jsonsuccess('Object id:<%s> has been removed' % (pk,))

    def add(self, **kwargs):
        try:
            # TODO. MUST BE ADRESSED IN API 3.1.
            try:
                data = self.request.data.dicts[0] or self.request.data.dicts[1]
            except:
                data = self.request.data
            if kwargs:
                data.update(kwargs)
            srl = self.serializer(data=data)
            if srl.is_valid():
                srl.save()
                return jsonresult(srl.data)
            return jsonerror(srl.errors)
        except ValidationError as e:
            return jsonerror('Error: {}'.format(e))

    def upd(self, **kwargs):
        try:
            res = get_obj(self.serializer, **kwargs)
            if res.get('error'):
                return jsonerror(res['error'])
            srl = self.serializer(res['object'],
                                  data=self.request.data,
                                  partial=True)
            if srl.is_valid():
                srl.save()
                return jsonresult(srl.data)
            return jsonerror(''.join([','.join([k + '-' + ''.join(v)])
                                      for k, v in srl.errors.items()]))
        except ValidationError as e:
            return jsonerror('Error: {}'.format(e))
