import operator

from mongoengine import Q
from rest_framework.filters import BaseFilterBackend


def search_nodes(queryset, kind, uid, gids):
    if kind:
        fltr = (Q(kind=kind) | Q(uid=uid) | Q(gid__in=gids))
    else:
        fltr = (Q(uid=uid) | Q(gid__in=gids))
    return queryset.filter(fltr
        ).where('((1*this.perm[0])&4) || ((1*this.perm[1])&4) || ((1*this.perm[2])&4)')


def search_children(queryset, kind, uid, gids, parent_id):
    return search_nodes(queryset, kind, uid, gids).filter(
        path__startswith=parent_id)


class MongoSearchFilter(BaseFilterBackend):
    def construct_search(self, field_name, field_value):
        """
        There are few rules that convert search fields to querysets.
        We have following operators for numerics:
        gt = >,gte = >=, lt = <, lte = <=, eq = ==, 
        Search for numerics are always and.
        """
        if field_value.startswith('gt'):
            return {'{}__gt'.format(field_name): field_value.strip('gt ')}
        elif field_value.startswith('gte'):
            return {'{}__gte'.format(field_name): field_value.strip('gte ')}
        elif field_value.startswith('lt'):
            return {'{}__lt'.format(field_name): field_value.strip('lt ')}
        elif field_value.startswith('lte'):
            return {'{}__lte'.format(field_name): field_value.strip('lte ')}
        elif field_value.startswith('eq'):
            return {'{}__eq'.format(field_name): field_value.strip('eq ')}

    def filter_queryset(self, request, queryset, view):
        data = request.GET
        search_fields = getattr(view, 'search_fields', None)

        if not search_fields:
            return queryset

        orm_lookups = [self.construct_search(field, data.get(field))
                       for field in search_fields if data.get(field)]

        and_queries = [Q(**orm_lookup)
                       for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.and_, and_queries))

        return queryset



































# 0 1 2 3 4 5 6 7 8 9 0 . () and or > < = <= >=
# abcdefghijklmnopqrstuvwxyz_

# expr ::= item {op-bool item}
# op-bool ::= and | or
# item ::= ident {op-sign factor}
# op-sign ::= >|<|>=|<=|=
# factor ::= number|(expr)
# number ::= digit|digit number
# ident ::= letter {letter|digit}
# digit ::= 0|1|2|3|4|5|6|7|8|9
# letter ::= a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|_
#
#
#







