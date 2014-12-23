from mfs.nodes.serializers import (NodeSerializer, ResourceSerializer)
from nodes.models import Category, Advert
from nodes.models import (AddressResource, BuildingPropertiesResource,
                          PriceResource, PosterResource)
from mfs.common.lib import address_to_geo


# Node.
class CategorySerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Category
        fields = NodeSerializer.Meta.fields + ('title',)


class AdvertSerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Advert
        fields = NodeSerializer.Meta.fields + ('title',)


# Resources
class AddressResourceSerializer(ResourceSerializer):
    class Meta(ResourceSerializer.Meta):
        model = AddressResource
        fields = ResourceSerializer.Meta.fields + ('country', 'region',
                                                   'city', 'street')

    def resolve_to_geo(self, *params):
        self.validated_data['location'] = address_to_geo(*params)

    def save(self, **kwargs):
        data = self.validated_data
        country, region, city, street = (data.get('country'), data.get('region'),
                                         data.get('city'), data.get('street'))
        self.resolve_to_geo(country, region, city, street)
        return super(AddressResourceSerializer, self).save(**kwargs)


class BuildingPropertiesResourceSerializer(ResourceSerializer):
    class Meta(ResourceSerializer.Meta):
        model = BuildingPropertiesResource
        fields = ResourceSerializer.Meta.fields + ('rooms', 'square_gen', 'floor',
                                                   'square_live', 'room_height',
                                                   'floors', 'wall_type',
                                                   'build_type')


class PriceResourceSerializer(ResourceSerializer):
    class Meta(ResourceSerializer.Meta):
        model = PriceResource
        fields = ResourceSerializer.Meta.fields + ('price', 'duration')


class PosterResourceSerializer(ResourceSerializer):
    class Meta(ResourceSerializer.Meta):
        model = PosterResource
        fields = ResourceSerializer.Meta.fields + ('title', 'text')
