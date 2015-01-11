from django.conf.urls import url, patterns, include
from rest_framework import routers
from mfs.groups.views import GroupViewSet
from mfs.users.views import UserLoginView, UserLogoutView, UserTokenLoginView
from mfs.nodes.views import NodesViewSet, ResourcesViewSet

from users.views import RegularUserViewSet, RegularUserRegisterView
from nodes.views import (CategoryViewSet, AdvertViewSet, CategoryListView,
                         PaginatedAdvertsView, AssetViewSet, AssetsListView)


drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user/register', RegularUserRegisterView, base_name='register')
drouter.register(r'user', RegularUserViewSet, base_name='user')

drouter.register(r'logout', UserLogoutView, base_name='logout')
drouter.register(r'login', UserLoginView, base_name='login')

drouter.register(r'node', NodesViewSet, base_name='node') # TODO. For tests only.
drouter.register(r'resource', ResourcesViewSet, base_name='resource') # TODO. For tests only.

drouter.register(r'category', CategoryViewSet, base_name='category')
drouter.register(r'advert', AdvertViewSet, base_name='advert')
drouter.register(r'asset', AssetViewSet, base_name='asset')

urlpatterns = drouter.urls

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token/', UserTokenLoginView.as_view(), name='token'),
    url(r'^categories/(?P<category_id>\w{24})/', CategoryListView.as_view(), name='categories'),
    url(r'^categories/', CategoryListView.as_view(), name='root-categories'),
    url(r'^adverts/(?P<category_id>\w{24})/', PaginatedAdvertsView.as_view(), name='adverts'),
    url(r'^assets/(?P<advert_id>\w{24})/', AssetsListView.as_view(), name='assets')
)


