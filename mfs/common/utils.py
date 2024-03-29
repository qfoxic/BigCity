import httplib
import json
import socket

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

import mfs.common.constants as co


def user_data(request, manager):
    user = request.user
    uid, groups = 0, []
    um = manager(request)
    if user.is_authenticated():
        ures = um.data(pk=request.user.pk)
        if not ures.get('error'):
            uid, groups = user.pk, [i['id'] for i in ures['result']['groups']]
    return uid, groups


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
    user_gids = [i['id'] for i in user['groups']]
    # Check owner permissions.
    if uid == node['uid']:
        return bool(owner & perm_to_check)
    # If user is in at least one group the node is assigned to.
    elif node['gid'] in user_gids:
        return bool(group & perm_to_check)
    else:
        return bool(other & perm_to_check)
    return False


def address_to_geo(*args, **kwargs):
    headers = {
        'User-Agent': 'python-requests/2.2.1.CPython/2.7.6.Linux/3.13.0-39-generic',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,compress'
    }
    conn = httplib.HTTPConnection(co.MAPS_HOST)
    additional = {}
    ext = kwargs.get('extended')
    try:
        # We have to replace whitespaces with +.
        conn.request('GET', co.MAPS_URL.format(','.join([i.strip().replace(' ', '+') for i in args]),
                                               co.DEFAULT_LANGUAGE),
                     '', headers)
        resp = conn.getresponse()
        converted = json.loads(resp.read())
        loc = converted['results'][0]['geometry']['location']
        address = converted['results'][0]['formatted_address'].split(',')
        if ext:
            additional = {
                'country': address[-1].strip() if address else '',
                'state': address[-2].strip() if len(address) > 1 else address[-1],
                'city': address[-3].strip() if len(address) > 1 else address[-1],
                # Trick, usually address contains 3 part, sometimes 4 or 5. The very first always be street or city.
                'street': address[0].strip() if address else ''
            }

    except (TypeError, IndexError, ValueError):
        if ext:
            return 0.0, 0.0, additional
        return 0.0, 0.0
    except socket.error:
        if ext:
            return 0.0, 0.0, additional
        return 0.0, 0.0

    if ext:
        return loc['lng'], loc['lat'], additional
    return loc['lng'], loc['lat']
