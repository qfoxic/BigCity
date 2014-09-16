from rest_framework import routers
from groups.views import GroupViewSet
from users.views import UserViewSet

drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user', UserViewSet, base_name='user')

urlpatterns = drouter.urls
