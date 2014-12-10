from rest_framework.authtoken import views
from django.conf.urls import url, patterns, include
from rest_framework import routers
from mfs.groups.views import GroupViewSet
from mfs.users.views import UserLoginView, UserLogoutView
from mfs.nodes.views import NodesViewSet, ResourcesViewSet

from users.views import RegularUserViewSet, RegularUserRegisterView
from nodes.views import (CategoryViewSet, AdvertViewSet,
    BuildingPropertiesResourceViewSet, PriceResourceViewSet,
    PosterResourceViewSet, AddressResourceViewSet)


drouter = routers.DefaultRouter()
drouter.register(r'group', GroupViewSet, base_name='group')
drouter.register(r'user/register', RegularUserRegisterView, base_name='register')
drouter.register(r'user', RegularUserViewSet, base_name='user')

drouter.register(r'logout', UserLogoutView, base_name='logout')
drouter.register(r'login', UserLoginView, base_name='login')

drouter.register(r'node', NodesViewSet, base_name='node') # TODO. For tests only.
drouter.register(r'resource', ResourcesViewSet, base_name='resource') # TODO. For tests only.

# Category.
drouter.register(r'category', CategoryViewSet, base_name='category') # Node.

# Advert url.
drouter.register(r'advert', AdvertViewSet, base_name='advert') # Node.
drouter.register(r'building', BuildingPropertiesResourceViewSet, base_name='building')
drouter.register(r'address', AddressResourceViewSet, base_name='address')
drouter.register(r'price', PriceResourceViewSet, base_name='price')
drouter.register(r'poster', PosterResourceViewSet, base_name='poster')

urlpatterns = drouter.urls

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token/', views.obtain_auth_token)
)


