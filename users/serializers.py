from rest_framework import serializers
from django.contrib.auth.models import User, make_password
import common.lib as clib

class MongoCharField(serializers.CharField):
    def field_to_native(self, obj, field_name):
        d = clib.mongo_get_user_profile(obj.pk, (field_name,))
        return d.get(field_name, '')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'username', 'email', 'first_name', 'last_name', 'is_active')
        write_only_fields = ('password',)

    @staticmethod
    def model():
        return User

    # turn text to hashed password
    def restore_object(self, attrs, instance=None):
        if attrs.get('password'):
            attrs['password'] = make_password(attrs['password'])
        return super(UserSerializer, self).restore_object(attrs, instance)

#TODO implement multiple types of user.
class RegularUserSerializer(UserSerializer):
    resume = MongoCharField(max_length=100000, required=False)

    class Meta:
        model=User
        fields=('id', 'username', 'email', 'first_name', 'last_name',
                'is_active', 'resume')
        write_only_fields = ('password',)

    def save_object(self, obj, **kwargs):
        super(RegularUserSerializer, self).save_object(obj, **kwargs)
        data = {'resume': self.data.get('resume')}
        clib.mongo_save_user_profile(obj.pk, data)


#class SellerUserSerializer(serializers.Serializer):
#    def save(self, **kwargs):
#        lib.user.add_seller(**kwargs)


#class AgencyUserSerializer(serializers.Serializer):
#    def save(self, **kwargs):
#        lib.user.add_agency(**kwargs)

    
#class CompanyUserSerializer(serializers.Serializer):
#    def save(self, **kwargs):
#        lib.user.add_company(**kwargs)

