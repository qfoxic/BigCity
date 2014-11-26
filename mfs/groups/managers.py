import mfs.common.lib as clib
from mfs.groups.serializers import GroupSerializer


class GroupManager(clib.BaseManager):
    serializer = GroupSerializer


