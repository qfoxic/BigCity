from mfs.nodes.serializers import NodeSerializer
from nodes.models import Category, Advert, Asset
from mfs.common.lib import address_to_geo


class CategorySerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Category
        fields = ('id', 'parent', 'path', 'title', 'perm', 'uid', 'gid')

    def to_representation(self, instance):
        has_children = instance.__class__.children(instance.uid, [instance.gid],
                                                   instance.id).count()
        res = super(CategorySerializer, self).to_representation(instance)
        res['has_children'] = bool(has_children)
        return res


class AssetSerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Asset
        fields = ('id', 'parent', 'path', 'title', 'perm', 'content', 'uid',
                  'gid', 'content_type', 'asset_type')


class AdvertSerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Advert
        fields = NodeSerializer.Meta.fields + ('title', 'country', 'region',
                                               'city', 'street', 'loc',
                                               'rooms', 'square_gen', 'floor',
                                               'square_live', 'room_height',
                                               'floors', 'wall_type',
                                               'build_type', 'price',
                                               'finished', 'text',
                                               'build_vector')

    def resolve_to_geo(self, *params):
        self.validated_data['loc'] = address_to_geo(*params)

    def save(self, **kwargs):
        data = self.validated_data
        country, region, city, street = (data.get('country', ''),
                                         data.get('region', ''),
                                         data.get('city', ''),
                                         data.get('street', ''))
        self.resolve_to_geo(country, region, city, street)
        return super(AdvertSerializer, self).save(**kwargs)




