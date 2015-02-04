import datetime
from mongoengine import Document, fields, NULLIFY, CASCADE, queryset_manager
from mfs.common.constants import UMASK
from mfs.common.search import search_nodes, search_children


class Node(Document):
    uid = fields.IntField(required=True, min_value=1)
    #unix permission.
    perm = fields.StringField(regex='[01234567]{3}', default=UMASK)
    # dot separated path of entity's ids.
    path = fields.StringField(max_length=3000)
    kind = fields.StringField(max_length=50)
    #timestamp
    created = fields.DateTimeField()
    #timestamp
    updated = fields.DateTimeField(default=datetime.datetime.utcnow())
    # Parent record. Mongo object id.
    parent = fields.ReferenceField('self', reverse_delete_rule=NULLIFY)
    # Shared to uids.
    shared = fields.ListField()
    gid = fields.IntField(required=True, min_value=1)

    meta = {
        'allow_inheritance': True,
        'indexes': [('kind', 'uid', 'gid'),
                    ('uid', 'gid'),
                    ('kind', 'uid', 'gid', 'parent'),
                    ('kind', 'uid', 'gid', 'path')],
    }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.utcnow()
        self.kind = self.get_kind()
        super(Node, self).save(*args, **kwargs)

        path = self.path.split('.') if self.path else []
        cid = str(self.id)
        if cid not in path:
            path.insert(0, cid)
            o = self.parent
            while o:
                path.insert(0, str(o.id))
                o = o.parent
            self.path = '.'.join(path)
        return super(Node, self).save(*args, **kwargs)

    @classmethod
    def get_kind(cls):
        return cls.__name__.lower()

    @queryset_manager
    def nodes(cls, queryset, uid, gids, kind=None):
        return search_nodes(queryset, kind or cls.get_kind(), uid, gids)

    @queryset_manager
    def children(cls, queryset, uid, gids, pid, direct=True, kind=None):
        return search_children(queryset, kind or cls.get_kind(), uid, gids, pid, direct)


class Image(Node):
    parent = fields.ReferenceField('Node', reverse_delete_rule=CASCADE)
    title = fields.StringField(required=True, max_length=300)
    # image/png, application/pdf etc
    content_type = fields.StringField(required=True, max_length=100)
    # image, video etc.
    asset_type = fields.StringField(required=True, max_length=100)
    content = fields.ImageField(thumbnail_size=(100, 100, True))


