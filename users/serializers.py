from django.contrib.auth.models import User
from rest_framework import serializers

import mfs.common.lib as clib
from mfs.users.serializers import UserSerializer
from mfs.users.lib import UsersManager

from mongoengine import Document, fields


#@clib.mongo_connect('city', 'user_profiles')
#def mongo_save_user_profile(conn, uid, data):
#    raise Exception(conn, uid, data)
#    data['uid'] = uid
#    return conn.update({'uid': uid}, data, upsert=True)


#@clib.mongo_connect('city', 'user_profiles')
#def mongo_get_user_profile(conn, uid, fields):
#    cursor = conn.find({'uid': uid}, {f: 1 for f in fields})
#    res = [i for i in cursor]
#    if res:
#        return res[0] # Dict with results.
#    return {}

class MongoUser(Document):
    resume = fields.StringField(max_length=100000)
    # User id.
    id = fields.IntField(required=True, primary_key=True)


class RegularUserSerializer(UserSerializer):
    resume = serializers.CharField(max_length=100000, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'resume')
        write_only_fields = ('password',)

    def to_native(self, obj):
        return super(RegularUserSerializer, self).to_native(obj)
    #def restore_object(self, attrs, instance=None):
    #    obj = super(RegularUserSerializer, self).restore_object(attrs, instance)
    #    return obj

    def save_object(self, obj, **kwargs):
        super(RegularUserSerializer, self).save_object(obj, **kwargs)
        mu = MongoUser(**self.data)
        mu.save()


class RegularUserManager(UsersManager):
    serializer = RegularUserSerializer
