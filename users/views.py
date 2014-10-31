from mfs.users.views import UserViewSet, UserRegisterView
from users.serializers import RegularUserManager


class RegularUserViewSet(UserViewSet):
    manager_class = RegularUserManager


class RegularUserRegisterView(UserRegisterView):
    manager_class = RegularUserManager
