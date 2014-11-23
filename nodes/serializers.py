from mfs.nodes.serializers import NodeSerializer
from nodes.models import Category


class CategorySerializer(NodeSerializer):
    class Meta(NodeSerializer.Meta):
        model = Category
        fields = NodeSerializer.Meta.fields + ('title',)

