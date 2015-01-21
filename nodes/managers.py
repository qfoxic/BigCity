import datetime
from mongoengine import Q
from mfs.nodes.managers import NodesManager
from mfs.users.managers import UsersManager
from mfs.common.lib import jsonerror, jsonresult, ValidationError

from nodes.serializers import CategorySerializer, AdvertSerializer, ImageSerializer


def user_data(request):
    user = request.user
    uid, groups = 0, []
    um = UsersManager(request)
    if user.is_authenticated():
        ures = um.data(pk=request.user.pk)
        if not ures.get('error'):
            uid, groups = user.pk, [i[0] for i in ures['result']['groups']]
    return uid, groups


class CategoryManager(NodesManager):
    serializer = CategorySerializer

    def categories_queryset(self, pid):
        uid, groups = user_data(self.request)
        queryset = self.serializer.Meta.model.children(
            uid, groups, pid)
        return queryset


class ImageManager(NodesManager):
    serializer = ImageSerializer

    def assets_queryset(self, pid, content_type):
        uid, groups = user_data(self.request)
        queryset = self.serializer.Meta.model.children(
            uid, groups, pid).filter(content_type=content_type)
        return queryset

    def add(self, **kwargs):
        try:
            # TODO. MUST BE ADRESSED IN API 3.1.
            try:
                data = self.request.data.dicts[0] or self.request.data.dicts[1]
            except:
                data = self.request.data
            data['content'] = self.request.data['content']
            if kwargs:
                data.update(kwargs)
            srl = self.serializer(data=data)
            # TODO. Remove save method and use "create" instead.
            if srl.is_valid():
                srl.save()
                return jsonresult(srl.data)
            return jsonerror(srl.errors)
        except ValidationError as e:
            return jsonerror('Error: {}'.format(e))


class AdvertManager(NodesManager):
    serializer = AdvertSerializer

    def _bquery(self, uid, groups, pid):
        return self.serializer.Meta.model.children(
            uid, groups, pid).filter(
                Q(finished__gt=datetime.datetime.now()) | Q(finished__exists=False))

    def nearest_queryset(self, pid):
        data = self.request.GET
        try:
            lon, lat = (float(data.get('lon', 0.0)),
                        float(data.get('lat', 0.0)))
        except (TypeError, ValueError):
            lon, lat = 0.0, 0.0

        uid, groups = user_data(self.request)
        queryset = self._bquery(uid, groups, pid).filter(
            loc__near=[lon, lat]
        )
        return queryset

    def within_queryset(self, pid):
        data = self.request.GET
        try:
            lon, lat, radius = (float(data.get('lon', 0.0)),
                                float(data.get('lat', 0.0)),
                                float(data.get('radius', 10.0)))
        except (TypeError, ValueError):
            lon, lat, radius = 0.0, 0.0, 10.0

        uid, groups = user_data(self.request)
        queryset = self._bquery(uid, groups, pid).filter(
            loc__geo_within_center=[(lon, lat), radius]
        )
        return queryset

    def regions_queryset(self, pid):
        data = self.request.GET
        regions = data.get('regions', '').split(',')
        uid, groups = user_data(self.request)
        queryset = self._bquery(uid, groups, pid).filter(region__in=regions)
        return queryset

    def cities_queryset(self, pid):
        data = self.request.GET
        cities = data.get('cities', '').split(',')
        uid, groups = user_data(self.request)
        queryset = self._bquery(uid, groups, pid).filter(city__in=cities)
        return queryset

    def countries_queryset(self, pid):
        data = self.request.GET
        countries = data.get('countries', '').split(',')
        uid, groups = user_data(self.request)
        queryset = self._bquery(uid, groups, pid).filter(country__in=countries)
        return queryset

    def all_queryset(self, pid):
        uid, groups = user_data(self.request)
        queryset = self._bquery(uid, groups, pid)
        return queryset
