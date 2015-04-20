from django.conf.urls import url, patterns, include
from rest_framework import routers
from mfs.groups.views import GroupViewSet, GroupListViewSet
from mfs.users.views import UserLoginView, UserLogoutView, UserTokenLoginView, UserListViewSet
from mfs.nodes.views import (NodesViewSet, ImageViewSet, ImagesListView, NodesListView)

from users.views import RegularUserViewSet
from nodes.views import (CategoryViewSet, AdvertViewSet, CategoryListView,
                         PaginatedAdvertsView)


drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user', RegularUserViewSet, base_name='user')

drouter.register(r'logout', UserLogoutView, base_name='logout')
drouter.register(r'login', UserLoginView, base_name='login')

drouter.register(r'node', NodesViewSet, base_name='node') # TODO. For tests only.

drouter.register(r'category', CategoryViewSet, base_name='category')
drouter.register(r'advert', AdvertViewSet, base_name='advert')
drouter.register(r'image', ImageViewSet, base_name='image')

urlpatterns = drouter.urls

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token/', UserTokenLoginView.as_view(), name='token'),
    url(r'^categories/(?P<category_id>\w{24})/', CategoryListView.as_view(), name='categories'),
    url(r'^categories/', CategoryListView.as_view(), name='root-categories'),
    url(r'^adverts/(?P<category_id>\w{24})/', PaginatedAdvertsView.as_view(), name='adverts'),
    url(r'^images/(?P<advert_id>\w{24})/', ImagesListView.as_view(), name='images'),
    url(r'^nodes/$', NodesListView.as_view(), name='nodes'),
    url(r'^groups/', GroupListViewSet.as_view(), name='groups'),
    url(r'^users/', UserListViewSet.as_view(), name='users')
)


