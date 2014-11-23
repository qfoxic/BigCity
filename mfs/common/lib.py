import urllib2
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

import mfs.common.constants as co



class BaseManager(object):
    def __init__(self, request, serializer=None):
        self.request = request
        if serializer:
            self.serializer = serializer


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
    resp = urllib2.urlopen(co.GOOGLE_MAPS.format(','.join(args))).read()
    try:
        converted = json.loads(resp)
    except TypeError:
        return 0.0, 0.0
    loc = converted['results'][0]['geometry']['location']
    return loc['lat'], loc['lng']
