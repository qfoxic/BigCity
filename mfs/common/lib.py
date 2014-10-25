import pymongo
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


class BaseManager(object):
    def __init__(self, request, serializer=None):
        self.request = request
        if serializer:
            self.serializer = serializer


client = None
def mongo_db(dbname):
    global client
    if not client:
        client = pymongo.MongoClient(settings.MONGO_HOST,
                                     settings.MONGO_PORT)
    return client[dbname]


def mongo_connect(db, coll):
    def wrap(f):
        def wrapped(*args):
            f(mongo_db(db)[coll], *args)
        return wrapped
    return wrap


def mongo_collection(db, collection):
    return mongo_db(db)[collection]

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