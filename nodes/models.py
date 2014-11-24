from mongoengine import fields
from mfs.nodes.models import Node
from mfs.nodes.models import GeoResource, SearchVector, Resource


WALL_TYPES = ((0, 'Ferroconcrete'), (1, 'Brick'),)
BUILD_TYPES = ((0, 'New'), (1, 'Secondary'),)


class Category(Node):
    title = fields.StringField(required=True, max_length=3000)


class AddressResource(GeoResource):
    country = fields.StringField(max_length=30)
    region = fields.StringField(max_length=30)
    city = fields.StringField(max_length=30)
    street = fields.StringField(max_length=100)

    def save(self, *args, **kwargs):
        self.resolve_to_geo(self.country, self.region,
                            self.city, self.street)
        return super(AddressResource, self).save(*args, **kwargs)


class PropertiesResource(SearchVector):
    rooms = fields.IntField(required=True, default=0)
    square_gen = fields.IntField(required=True, default=0)
    square_live = fields.IntField(required=True, default=0)
    room_height = fields.IntField(required=True, default=0)
    floors = fields.IntField(required=True, default=0)
    floor = fields.IntField(required=True, default=0)
    wall_type = fields.IntField(choices=WALL_TYPES,
                                required=True, default=WALL_TYPES[0][0])
    build_type = fields.IntField(choices=WALL_TYPES,
                                 required=True, default=BUILD_TYPES[0][0])


class PriceResource(Resource):
    price = fields.DecimalField()
    # Price per duration. For instance, one day.
    # In seconds. 0 - means doesn't have duration.
    duration = fields.IntField(default=0)


class PosterResource(Resource):
    name = fields.StringField(max_length=500)
    text = fields.StringField(max_length=5000)



