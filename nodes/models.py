from mongoengine import fields
from mfs.nodes.models import Node
from mfs.nodes.models import Resource

from mfs.common.lib import address_to_geo


WALL_TYPES = ((0, 'Ferroconcrete'), (1, 'Brick'),)
BUILD_TYPES = ((0, 'New'), (1, 'Secondary'),)


# Nodes.
class Category(Node):
    title = fields.StringField(required=True, max_length=3000)


class Advert(Node):
    title = fields.StringField(required=True, max_length=300)


# Resources.
class AddressResource(Resource):
    meta = {
        'indexes': [[("location", "2dsphere"),]]
    }

    location = fields.GeoPointField()
    country = fields.StringField(max_length=30)
    region = fields.StringField(max_length=30)
    city = fields.StringField(max_length=30)
    street = fields.StringField(max_length=100)

    def resolve_to_geo(self, *args):
        self.location = address_to_geo(*args)

    def save(self, *args, **kwargs):
        self.resolve_to_geo(self.country, self.region,
                            self.city, self.street)
        return super(AddressResource, self).save(*args, **kwargs)

    @classmethod
    def get_kind(cls):
        return 'address'


class BuildingPropertiesResource(Resource):
    rooms = fields.IntField(required=True, default=0)
    square_gen = fields.IntField(required=True, default=0)
    square_live = fields.IntField(required=True, default=0)
    room_height = fields.IntField(required=True, default=0)
    floors = fields.IntField(required=True, default=0)
    floor = fields.IntField(required=True, default=0)
    wall_type = fields.IntField(choices=WALL_TYPES,
                                required=True, default=WALL_TYPES[0][0])
    build_type = fields.IntField(choices=BUILD_TYPES,
                                 required=True, default=BUILD_TYPES[0][0])

    @classmethod
    def get_kind(cls):
        return 'building'


class PriceResource(Resource):
    price = fields.DecimalField()
    # Price per duration. For instance, one day.
    # In seconds. 0 - means doesn't have duration.
    duration = fields.IntField(default=0)

    @classmethod
    def get_kind(cls):
        return 'price'


class PosterResource(Resource):
    title = fields.StringField(max_length=500)
    text = fields.StringField(max_length=5000)

    @classmethod
    def get_kind(cls):
        return 'poster'
