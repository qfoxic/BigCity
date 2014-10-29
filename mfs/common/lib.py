from django.core.exceptions import ObjectDoesNotExist


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
    except (ObjectDoesNotExist, ValueError), e:
        return jsonerror('Object id:<%s> does not exists' % (pk), str(e))
    return {'object': instance}