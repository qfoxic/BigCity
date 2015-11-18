import datetime
from mongoengine import fields, NULLIFY, CASCADE, queryset_manager, Q
from mfs.common.search import search_nodes, search_children
from mfs.nodes.models import Node


WALL_TYPES = ((0, 'Ferroconcrete'), (1, 'Brick'),)
BUILD_TYPES = ((0, 'New'), (1, 'Secondary'),)


BUILDINGS = 'buildings'


class Category(Node):
    parent = fields.ReferenceField('Category', reverse_delete_rule=NULLIFY)
    title = fields.StringField(required=True, max_length=3000)
    ctype = fields.StringField(required=False, default=BUILDINGS)


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
    finished = fields.DateTimeField()

    #language field is needed for full text search.
    language = fields.StringField(default='english')
    text = fields.StringField(max_length=5000)

    meta = {
        'indexes': [('kind', 'path', 'loc', 'parent'),
                    ('kind', 'path', 'loc', 'parent', 'finished')
                    ]
    }

    @queryset_manager
    def nodes(cls, queryset, uid, gids):
        return search_nodes(queryset, cls.get_kind(), uid, gids).filter(
            Q(finished__exists=False) | Q(finished__gt=datetime.datetime.now()))

    @queryset_manager
    def nearest(cls, queryset, uid, gids, lat, lon, parent=None):
        try:
            lon, lat = float(lon), float(lat)
        except (TypeError, ValueError):
            lon, lat = 0.0, 0.0
        return search_children(
            queryset, cls.get_kind(), uid,
            gids, pid=parent, direct=False
        ).filter(
            loc__near=[lon, lat]
        ).filter(Q(finished__exists=False) | Q(finished__gt=datetime.datetime.now()))


class Message(Node):
    title = fields.StringField(required=True, max_length=300)
    body = fields.StringField(required=True, max_length=2000)
    country = fields.StringField(max_length=30)
    region = fields.StringField(max_length=30)
    city = fields.StringField(max_length=30)

    @queryset_manager
    def incoming(cls, queryset, uid, gids, country, region, city):
        geo_filter = (
            ((Q(country=country) & Q(region='') & Q(city='')) |
            (Q(country=country) & Q(region=region) & Q(city='')) |
            (Q(country=country) & Q(region=region) & Q(city=city)) |
            Q(shared__in=[uid])) & Q(uid__ne=uid)
        )
        return search_nodes(queryset, cls.get_kind(), uid, gids).filter(geo_filter)

    @queryset_manager
    def my(cls, queryset, uid, gids):
        return search_nodes(queryset, cls.get_kind(), uid, gids).filter(Q(uid=uid))
