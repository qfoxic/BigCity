import datetime
from mongoengine import fields, NULLIFY, CASCADE, queryset_manager, Q
from mfs.common.search import search_nodes
from mfs.nodes.models import Node


WALL_TYPES = ((0, 'Ferroconcrete'), (1, 'Brick'),)
BUILD_TYPES = ((0, 'New'), (1, 'Secondary'),)


class Category(Node):
    parent = fields.ReferenceField('Category', reverse_delete_rule=NULLIFY)
    title = fields.StringField(required=True, max_length=3000)


class Advert(Category):
    parent = fields.ReferenceField('Category', reverse_delete_rule=CASCADE)
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
    price = fields.DecimalField()
    # Price per duration. For instance, one day.
    finished = fields.DateTimeField()

    text = fields.StringField(max_length=5000)

    meta = {
        'indexes': [('kind', 'uid', 'gid', 'loc'),
                    ('uid', 'gid', 'loc'),
                    ('kind', 'uid', 'gid', 'parent', 'loc'),
                    ('kind', 'uid', 'gid', 'path', 'loc')]
    }

    @queryset_manager
    def nodes(cls, queryset, uid, gids, kind=None):
        return search_nodes(queryset, kind or cls.get_kind(), uid, gids).filter(
            Q(finished__exists=False) | Q(finished__gt=datetime.datetime.now()))

