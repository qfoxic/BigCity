import httplib
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from mfs.common.serializers import cast_serializer

import mfs.common.constants as co


class BaseManager(object):
    def __init__(self, request, serializer=None):
        self.request = request
        if serializer:
            self.serializer = serializer

    def ls(self):
        queryset = self.serializer.Meta.model.objects.all()
        return jsonresult(self.serializer(queryset, many=True).data)

    def data(self, **kwargs):
        try:
            cast = kwargs.pop('cast')
            many = kwargs.pop('many')
        except KeyError:
            cast, many = False, False

        if many:
            res = get_objs(self.serializer, **kwargs)
        else:
            res = get_obj(self.serializer, **kwargs)
        if cast:
            self.serializer = (cast_serializer(kwargs.get('kind'))
                               or self.serializer)
        return jsonresult(self.serializer(res['object'], many=many).data)

    def rm(self, pk):
        res = get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return jsonerror(res['error'])
        res['object'].delete()
        return jsonsuccess('Object id:<%s> has been removed' % (pk,))

    def add(self, **kwargs):
        data = self.request.data
        if kwargs:
            data.update(kwargs)
        srl = self.serializer(data=data)
        if srl.is_valid():
            srl.save()
            return jsonresult(srl.data)
        return jsonerror(srl.errors)

    def upd(self, **kwargs):
        res = get_obj(self.serializer, **kwargs)
        if res.get('error'):
            return jsonerror(res['error'])
        srl = self.serializer(res['object'],
                              data=self.request.data,
                              partial=True)
        if srl.is_valid():
            srl.save()
            return jsonresult(srl.data)
        return jsonerror(''.join([','.join([k + '-' + ''.join(v)]) for k, v in srl.errors.items()]))


def jsonerror(error, traceback=None):
    if traceback:
        return {'error': error, 'traceback': traceback}
    return {'error': error}


def jsonsuccess(msg):
    return {'success': msg}


def jsonresult(item, direct=False):
    try:
        if direct:
            return {'result': item}
        return {'result': json.loads(json.dumps(item))}
    except TypeError:
        return {'result': []}


def get_obj(serializer, **kwargs):
    try:
        instance = serializer.Meta.model.objects.get(**kwargs)
    except (ObjectDoesNotExist, ValueError, serializer.Meta.model.DoesNotExist):
        raise Http404
    return {'object': instance}


def get_objs(serializer, **kwargs):
    instance = serializer.Meta.model.objects(**kwargs)
    return {'object': instance}


def check_perm(node, user, perm_to_check):
    perm, uid = node['perm'], user['id']
    if uid == 1:
        return True

    owner, group, other = int(perm[0]), int(perm[1]), int(perm[2])
    user_gids = [i[0] for i in user['groups']]
    # Check owner permissions.
    if uid == node['uid']:
        return bool(owner & perm_to_check)
    # If user is in at least one group the node is assigned to.
    elif node['access_level'] in user_gids:
        return bool(group & perm_to_check)
    else:
        return bool(other & perm_to_check)
    return False


def address_to_geo(*args):
    headers = {
        'User-Agent': 'python-requests/2.2.1.CPython/2.7.6.Linux/3.13.0-39-generic',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,compress'
    }
    conn = httplib.HTTPConnection(co.MAPS_HOST)
    # We have to replace whitespaces with +.
    conn.request('GET', co.MAPS_URL.format(','.join([i.strip().replace(' ', '+') for i in args])),
                 '', headers)
    resp = conn.getresponse()
    try:
        converted = json.loads(resp.read())
    except TypeError:
        return (0.0, 0.0)
    loc = converted['results'][0]['geometry']['location']
    return loc['lng'], loc['lat']
