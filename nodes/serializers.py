from mfs.nodes.serializers import (NodeSerializer, ResourceSerializer)
from nodes.models import Category, Advert
from nodes.models import (AddressResource, BuildingPropertiesResource,
                          PriceResource, PosterResource)


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
                                                   'city', 'street', 'location')


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


