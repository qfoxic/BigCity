from rest_framework import serializers
from django.contrib.auth.models import make_password
from django.contrib.auth import get_user_model

from mfs.common.utils import address_to_geo


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'password', 'date_joined')
        read_only_fields = ('username',)
        write_only_fields = ('password',)

    # turn text to hashed password
    def update(self, instance, validated_data):
        self._resolve_location(validated_data)
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

    def _resolve_location(self, validated_data):
        if not validated_data.get('address'):
            return

        lng, lat, address = address_to_geo(validated_data['address'], extended=True)
        validated_data['country'] = address.get('country') or validated_data.get('country')
        validated_data['state'] = address.get('state') or validated_data.get('state')
        validated_data['city'] = address.get('city') or validated_data.get('city')
        validated_data['street'] = address.get('street') or validated_data.get('street')
        validated_data['lng'] = lng
        validated_data['lat'] = lat

    def create(self, validated_data):
        model = get_user_model()
        self._resolve_location(validated_data)
        validated_data['username'] = validated_data['email']
        validated_data['password'] = make_password(validated_data['password'])
        return model.objects.create(**validated_data)

