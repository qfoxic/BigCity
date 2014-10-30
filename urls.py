from django.conf.urls import url, patterns, include
from rest_framework import routers
from mfs.groups.views import GroupViewSet
from mfs.users.views import UserLoginView
from users.views import RegularUserViewSet

drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user', RegularUserViewSet, base_name='user')
drouter.register(r'login', UserLoginView, base_name='login')

urlpatterns = drouter.urls

urlpatterns += patterns('',
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
)


