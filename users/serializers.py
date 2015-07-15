from rest_framework import fields

from mfs.users.serializers import UserSerializer
from mfs.users.managers import UsersManager
from users.models import Users


class RegularUserSerializer(UserSerializer):

    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'phone', 'gender', 'address', 'city', 'country', 'street', 'state', 'lat',
                  'lng', 'is_active', 'resume', 'password', 'date_joined')
        write_only_fields = ('password',)


class RegularUserManager(UsersManager):
    serializer = RegularUserSerializer
