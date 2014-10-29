from mfs.users.views import UserViewSet
from users.serializers import RegularUserManager


class RegularUserViewSet(UserViewSet):
    manager_class = RegularUserManager

