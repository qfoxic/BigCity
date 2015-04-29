from mfs.nodes.serializers import NodeSerializer
from nodes.models import Category, Advert
from mfs.common.utils import address_to_geo


class CategorySerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Category
        fields = ('id', 'parent', 'path', 'title', 'perm', 'uid', 'gid')

    def to_representation(self, instance):
        has_children = instance.__class__.has_children(instance.uid, [instance.gid],
                                                       instance.id)
        res = super(CategorySerializer, self).to_representation(instance)
        res['has_children'] = has_children
        return res


class CategoryListSerializer(CategorySerializer):
    class Meta(NodeSerializer.Meta):
        model = Category
        fields = ('id', 'parent', 'path', 'title', 'perm', 'uid', 'gid', 'kind')


class AdvertSerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Advert
        fields = NodeSerializer.Meta.fields + ('title', 'country', 'region',
                                               'city', 'street', 'loc',
                                               'rooms', 'square_gen', 'floor',
                                               'square_live', 'room_height',
                                               'floors', 'wall_type',
                                               'build_type', 'price',
                                               'finished', 'text')

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


class AdvertListSerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Advert
        fields = NodeSerializer.Meta.fields + ('title', 'price', 'city', 'kind')
        read_only_fields = NodeSerializer.Meta.fields + ('title', 'price', 'city', 'kind')
