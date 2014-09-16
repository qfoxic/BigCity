import pymongo
from django.core.exceptions import ObjectDoesNotExist
import common.constants as co

client = None
def mongo_city():
    global client
    if not client:
        client = pymongo.MongoClient(co.MONGO_HOST, co.MONGO_PORT)
    return client.city

def mongo_user_profiles():
    db = mongo_city()
    return db.user_profiles

def mongo_save_user_profile(uid, data):
    usr = mongo_user_profiles()
    data['uid'] = uid
    return usr.update({'uid': uid}, data, upsert=True)

def mongo_get_user_profile(uid, fields):
    usr = mongo_user_profiles()
    cursor = usr.find({'uid': uid}, {f: 1 for f in fields})
    res =  [i for i in cursor]
    if res:
        return res[0] # Dict with results.
    return {}

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
        instance = serializer.model().objects.get(pk=pk)
    except (ObjectDoesNotExist, ValueError), e:
        return jsonerror('Object id:<%s> does not exists' % (pk), str(e))
    return {'object': instance}