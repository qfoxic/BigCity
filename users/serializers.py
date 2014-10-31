from django.contrib.auth.models import User
from rest_framework import serializers

from mfs.users.serializers import UserSerializer
from mfs.users.managers import UsersManager
from mfs.users.models import MongoUser


class OneToOneMongoProxyField(serializers.CharField):
    def __init__(self, mongo_model, *args, **kwargs):
        super(OneToOneMongoProxyField, self).__init__(*args, **kwargs)
        self.mongo = mongo_model

    def field_to_native(self, obj, field_name):
        try:
            return super(OneToOneMongoProxyField, self).field_to_native(obj, field_name)
        except AttributeError:
            if not self.mongo.objects(id=obj.id):
                return ''
            return getattr(self.mongo.objects(id=obj.id)[0], field_name)


class RegularUserSerializer(UserSerializer):
    resume = OneToOneMongoProxyField(mongo_model=MongoUser, max_length=100000, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'resume', 'password')
        write_only_fields = ('password',)

    def save_object(self, obj, **kwargs):
        super(RegularUserSerializer, self).save_object(obj, **kwargs)
        mu = MongoUser(**self.data)
        mu.save()


class RegularUserManager(UsersManager):
    serializer = RegularUserSerializer
