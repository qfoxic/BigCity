import httplib
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

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
        res = get_obj(self.serializer, **kwargs)
        if res.get('error'):
            return jsonerror(res['error'])
        srl = self.serializer(res['object'])
        return jsonresult(srl.data)

    def rm(self, pk):
        res = get_obj(self.serializer, **{'pk': pk})
        if res.get('error'):
            return jsonerror(res['error'])
        res['object'].delete()
        return jsonsuccess('Object id:<%s> has been removed' % (pk,))

    def add(self, **kwargs):
        data = self.request.DATA
        if kwargs:
            data.update(kwargs)
        s = self.serializer(data=data)
        if s.is_valid():
            s.save()
            return jsonresult(s.data)
        return jsonerror(s.errors)

    def upd(self, **kwargs):
        res = get_obj(self.serializer, **kwargs)
        if res.get('error'):
            return jsonerror(res['error'])
        srl = self.serializer(res['object'],
                              data=self.request.DATA,
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


def jsonresult(item):
    return {'result': item}


def get_obj(serializer, **kwargs):
    try:
        instance = serializer.Meta.model.objects.get(**kwargs)
    except (ObjectDoesNotExist, ValueError, serializer.Meta.model.DoesNotExist):
        raise Http404
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
    elif set(user_gids).intersection(node['access_level']):
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
        return 0.0, 0.0
    loc = converted['results'][0]['geometry']['location']
    return loc['lat'], loc['lng']
