from rest_framework import serializers
from django.contrib.auth.models import make_password
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'password')
        read_only_fields = ('username',)
        write_only_fields = ('password',)

    # turn text to hashed password
    def update(self, instance, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        model = get_user_model()
        validated_data['username'] = validated_data['email']
        validated_data['password'] = make_password(validated_data['password'])
        return model.objects.create(**validated_data)

