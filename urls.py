from django.conf.urls import url, patterns, include
from rest_framework import routers
from mfs.groups.views import GroupViewSet
from mfs.users.views import UserLoginView, UserLogoutView
from mfs.nodes.views import NodesViewSet, ResourcesViewSet

from users.views import RegularUserViewSet, RegularUserRegisterView
from nodes.views import CategoryViewSet

drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user/register', RegularUserRegisterView, base_name='register')
drouter.register(r'user', RegularUserViewSet, base_name='user')
drouter.register(r'node', NodesViewSet, base_name='node') # TODO. For tests only.
drouter.register(r'resource', ResourcesViewSet, base_name='resource') # TODO. For tests only.
drouter.register(r'category', CategoryViewSet, base_name='category')
drouter.register(r'logout', UserLogoutView, base_name='logout')
drouter.register(r'login', UserLoginView, base_name='login')

urlpatterns = drouter.urls

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)


