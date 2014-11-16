from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


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


def get_obj(serializer, pk):
    try:
        instance = serializer.Meta.model.objects.get(pk=pk)
    except (ObjectDoesNotExist, ValueError):
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
