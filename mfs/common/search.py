import bson

from mongoengine import Q
from rest_framework.filters import BaseFilterBackend
from mfs.common import parse


def search_nodes(queryset, kind, uid, gids):
    if kind:
        fltr = Q(kind=kind) | Q(uid=uid) | Q(gid__in=gids)
    else:
        fltr = Q(uid=uid) | Q(gid__in=gids)
    return queryset.filter(fltr
        ).where('((1*this.perm[0])&4) || ((1*this.perm[1])&4) || ((1*this.perm[2])&4)')


def search_children(queryset, kind, uid, gids, pid, direct=True):
    if direct:
        try:
            pid = bson.ObjectId(pid) if pid else None
        except (TypeError, bson.errors.InvalidId):
            pid = None
        if pid:
            return search_nodes(queryset, kind, uid, gids).filter(parent=pid)
        return search_nodes(queryset, kind, uid, gids).filter(
            parent__exists=False)
    return search_nodes(queryset, kind, uid, gids).filter(
        path__startswith=pid)


class MongoExpressionFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        data = request.GET
        expr = data.get('where')
        order = data.get('order')
        parsed = parse.to_mongo(expr)
        query = queryset
        if parsed.where[0]:
            query = queryset.filter(parsed.where[0][1])
        if order:
            query = query.order_by(*order.split(','))
        return query
