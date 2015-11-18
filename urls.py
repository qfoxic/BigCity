from django.conf.urls import url, patterns, include
from rest_framework import routers
from mfs.groups.views import GroupViewSet, GroupListViewSet
from mfs.users.views import UserLoginView, UserLogoutView, UserTokenLoginView, UserListViewSet
from mfs.nodes.views import (NodesViewSet, ImageViewSet, ImagesListView, NodesListView)

from users.views import RegularUserViewSet
from nodes.views import (CategoryViewSet, AdvertViewSet, MessageViewSet)


drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user', RegularUserViewSet, base_name='user')

drouter.register(r'logout', UserLogoutView, base_name='logout')
drouter.register(r'login', UserLoginView, base_name='login')

drouter.register(r'node', NodesViewSet, base_name='node')

drouter.register(r'category', CategoryViewSet, base_name='category')
drouter.register(r'advert', AdvertViewSet, base_name='advert')
drouter.register(r'image', ImageViewSet, base_name='image')
drouter.register(r'message', MessageViewSet, base_name='message')

urlpatterns = drouter.urls

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token/', UserTokenLoginView.as_view(), name='token'),
    url(r'^images/(?P<advert_id>\w{24})/', ImagesListView.as_view(), name='images'),
    url(r'^nodes/(?P<kind>\w{2,24})/', NodesListView.as_view(), name='nodes'),
    #url(r'^admin/nodes/$', AdminNodesListView.as_view(), name='nodes'),
    url(r'^groups/', GroupListViewSet.as_view(), name='groups'),
    url(r'^users/', UserListViewSet.as_view(), name='users')
)


