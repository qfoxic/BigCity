from mongoengine import fields
from mfs.nodes.models import Node


WALL_TYPES = ((0, 'Ferroconcrete'), (1, 'Brick'),)
BUILD_TYPES = ((0, 'New'), (1, 'Secondary'),)


# Nodes.
class Category(Node):
    title = fields.StringField(required=True, max_length=3000)


class Advert(Node):
    title = fields.StringField(required=True, max_length=300)

    loc = fields.PointField(required=True, default=[0.0, 0.0])
    country = fields.StringField(max_length=30)
    region = fields.StringField(max_length=30)
    city = fields.StringField(max_length=30)
    street = fields.StringField(max_length=100)

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
    # TODO. Calculate it dynamically
    build_vector = fields.ListField(required=True)

    price = fields.DecimalField()
    # Price per duration. For instance, one day.
    finished = fields.DateTimeField()

    text = fields.StringField(max_length=5000)
