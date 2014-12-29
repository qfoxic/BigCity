from mongoengine import Q


def search_nodes(queryset, kind, uid, gids):
    return queryset.filter(
            Q(kind=kind) | Q(uid=uid) | Q(gid__in=gids)
        ).where('((1*this.perm[0])&4) || ((1*this.perm[1])&4) || ((1*this.perm[2])&4)')