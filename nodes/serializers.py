from django.http import Http404
from rest_framework import serializers
from mfs.nodes.serializers import NodeSerializer
from mfs.users.managers import UsersManager
from nodes.models import Category, Advert, Message
from mfs.common.utils import address_to_geo


class CategorySerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Category
        fields = ('id', 'parent', 'path', 'title', 'perm', 'uid', 'gid')


class CategoryListSerializer(CategorySerializer):
    class Meta(NodeSerializer.Meta):
        model = Category
        fields = ('id', 'parent', 'path', 'title', 'perm', 'uid', 'gid', 'kind')


class AdvertSerializer(NodeSerializer):
    owner = serializers.SerializerMethodField('_owner')

    class Meta(NodeSerializer.Meta):
        depth = 2
        model = Advert
        fields = NodeSerializer.Meta.fields + ('title', 'country', 'region',
                                               'city', 'street', 'loc',
                                               'rooms', 'square_gen', 'floor',
                                               'square_live', 'room_height',
                                               'floors', 'wall_type',
                                               'build_type', 'price',
                                               'finished', 'text', 'owner')

    def resolve_to_geo(self, *params):
        self.validated_data['loc'] = address_to_geo(*params)

    def save(self, **kwargs):
        data = self.validated_data
        country, region, city, street = (data.get('country', ''),
                                         data.get('region', ''),
                                         data.get('city', ''),
                                         data.get('street', ''))
        if not self.validated_data.get('loc'):
            self.resolve_to_geo(country, region, city, street)
        return super(AdvertSerializer, self).save(**kwargs)

    def _owner(self, obj):
        try:
            return UsersManager().data(id=obj.uid)['result']
        except Http404:
            return {}


class AdvertListSerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Advert
        depth = 2
        fields = NodeSerializer.Meta.fields + ('title', 'price', 'city', 'kind')
        read_only_fields = NodeSerializer.Meta.fields + ('title', 'price', 'city', 'kind')


class MessageSerializer(NodeSerializer):
    owner = serializers.SerializerMethodField('_owner')

    class Meta(NodeSerializer.Meta):
        model = Message
        fields = NodeSerializer.Meta.fields + ('title', 'body', 'city', 'region', 'country', 'owner')

    def _owner(self, obj):
        try:
            return UsersManager().data(id=obj.uid)['result']
        except Http404:
            return {}

    def save(self, **kwargs):
        data = self.validated_data
        country, region, city = (
            data.get('country', ''),
            data.get('region', ''),
            data.get('city', '')
        )
        lng, lat, additional = address_to_geo(country, region, city, extended=True)
        self.validated_data['country'] = additional.get('country', country.strip())
        self.validated_data['region'] = additional.get('state', region.strip())
        self.validated_data['city'] = additional.get('city', city.strip())
        return super(MessageSerializer, self).save(**kwargs)


class MessageListSerializer(NodeSerializer):
    owner = serializers.SerializerMethodField('_owner')

    class Meta(NodeSerializer.Meta):
        model = Message
        fields = NodeSerializer.Meta.fields + ('title', 'country', 'region', 'city', 'owner')

    def _owner(self, obj):
        try:
            return UsersManager().data(id=obj.uid)['result']
        except Http404:
            return {}
