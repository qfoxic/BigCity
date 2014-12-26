from mfs.nodes.managers import NodesManager
from mfs.users.managers import UsersManager
from nodes.serializers import CategorySerializer, AdvertSerializer


def user_data(request):
    user = request.user
    uid, groups = 0, []
    um = UsersManager(request)
    if user.is_authenticated():
        ures = um.data(pk=request.user.pk)
        if not ures.get('error'):
            uid, groups = user.pk, ures['result']['groups']
    return uid, groups


class CategoryManager(NodesManager):
    serializer = CategorySerializer

    def categories_queryset(self):
        uid, groups = user_data(self.request)
        queryset = self.serializer.Meta.model.nodes(
            uid, groups).only('parent', 'title', 'id', 'path')
        return queryset


class AdvertManager(NodesManager):
    serializer = AdvertSerializer

    def nearest_queryset(self):
        data = self.request.GET
        try:
            lon, lat, radius = (float(data.get('lon')), float(data.get('lat')),
                                int(data.get('radius')))
        except (TypeError, ValueError):
            lon, lat, radius = 0.0, 0.0, 1000**2

        uid, groups = user_data(self.request)
        queryset = self.serializer.Meta.model.nodes(
            uid, groups).filter(
            loc__geo_within_center=[(lon or 0.0, lat or 0.0), radius or 1000**2]
        )
        return queryset

    def regions_queryset(self):
        data = self.request.GET
        regions = data.get('regions', '').split(',')
        uid, groups = user_data(self.request)
        queryset = self.serializer.Meta.model.nodes(
            uid, groups).filter(region__in=regions)
        return queryset

    def cities_queryset(self):
        data = self.request.GET
        cities = data.get('cities', '').split(',')
        uid, groups = user_data(self.request)
        queryset = self.serializer.Meta.model.nodes(
            uid, groups).filter(city__in=cities)
        return queryset

    def countries_queryset(self):
        data = self.request.GET
        countries = data.get('countries', '').split(',')
        uid, groups = user_data(self.request)
        queryset = self.serializer.Meta.model.nodes(
            uid, groups).filter(countries__in=countries)
        return queryset

