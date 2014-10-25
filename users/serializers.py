from django.contrib.auth.models import User
from rest_framework import serializers

import mfs.common.lib as clib
from mfs.users.serializers import UserSerializer


@clib.mongo_connect('city', 'user_profiles')
def mongo_save_user_profile(conn, uid, data):
    data['uid'] = uid
    return conn.update({'uid': uid}, data, upsert=True)


@clib.mongo_connect('city', 'user_profiles')
def mongo_get_user_profile(conn, uid, fields):
    cursor = conn.find({'uid': uid}, {f: 1 for f in fields})
    res = [i for i in cursor]
    if res:
        return res[0] # Dict with results.
    return {}


class MongoCharField(serializers.CharField):
    def field_to_native(self, obj, field_name):
        d = mongo_get_user_profile(obj.pk, (field_name,))
        return d.get(field_name, '')


class RegularUserSerializer(UserSerializer):
    resume = MongoCharField(max_length=100000, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'resume')
        write_only_fields = ('password',)

    def save_object(self, obj, **kwargs):
        super(RegularUserSerializer, self).save_object(obj, **kwargs)
        data = {'resume': self.data.get('resume')}
        mongo_save_user_profile(obj.pk, data)