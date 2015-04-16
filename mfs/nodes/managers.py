from mongoengine import ValidationError
import mfs.common.utils as clib
from mfs.nodes.serializers import (NodeSerializer, ImageSerializer)
from mfs.common.managers import BaseManager
from mfs.users.managers import UsersManager
from mfs.groups.managers import GroupManager


class NodesManager(BaseManager):
    serializer = NodeSerializer

    def admin_queryset(self, pid):
        uid, _ = clib.user_data(self.request, UsersManager)
        groups = [i['id'] for i in GroupManager(None).ls()['result']]
        queryset = self.serializer.Meta.model.children(
            uid, groups, pid)
        return queryset


class ImageManager(NodesManager):
    serializer = ImageSerializer

    def assets_queryset(self, pid, content_type):
        uid, groups = clib.user_data(self.request, UsersManager)
        queryset = self.serializer.Meta.model.children(
            uid, groups, pid).filter(content_type=content_type)
        return queryset

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
