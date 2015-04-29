from mongoengine import ValidationError
import mfs.common.utils as clib
from mfs.nodes.serializers import (NodeSerializer, ImageSerializer)
from mfs.common.managers import BaseManager


class NodesManager(BaseManager):
    serializer = NodeSerializer


class ImageManager(NodesManager):
    serializer = ImageSerializer

    def add(self, **kwargs):
        try:
            # TODO. MUST BE ADRESSED IN API 3.1.
            try:
                data = self.request.data.dicts[0] or self.request.data.dicts[1]
            except:
                data = self.request.data
            data['content'] = self.request.data['content']
            if kwargs:
                data.update(kwargs)
            srl = self.serializer(data=data)
            # TODO. Remove save method and use "create" instead.
            if srl.is_valid():
                srl.save()
                return clib.jsonresult(srl.data)
            return clib.jsonerror(srl.errors)
        except ValidationError as e:
            return clib.jsonerror('Error: {}'.format(e))
