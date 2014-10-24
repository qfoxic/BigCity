from rest_framework import routers
from mfs.groups.views import GroupViewSet
from users.views import RegularUserViewSet

drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user', RegularUserViewSet, base_name='user')

urlpatterns = drouter.urls
