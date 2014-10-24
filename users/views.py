from mfs.users.views import UserViewSet
from users.serializers import RegularUserSerializer


class RegularUserViewSet(UserViewSet):
    serializer = RegularUserSerializer
