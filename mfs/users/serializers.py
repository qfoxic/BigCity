from rest_framework import serializers
from django.contrib.auth.models import User, make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active')
        write_only_fields = ('password',)

    # turn text to hashed password
    def restore_object(self, attrs, instance=None):
        if attrs.get('password'):
            attrs['password'] = make_password(attrs['password'])
        return super(UserSerializer, self).restore_object(attrs, instance)

