from mongoengine import fields

from mfs.nodes.models import Node

class Category(Node):
    title = fields.StringField(required=True, max_length=3000)

    @classmethod
    def get_type(cls):
        return 'category'

    @classmethod
    def get_tag(cls):
        return 'category'