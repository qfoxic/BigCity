from mfs.groups.serializers import GroupSerializer
from mfs.common.managers import BaseManager


class GroupManager(BaseManager):
    serializer = GroupSerializer


