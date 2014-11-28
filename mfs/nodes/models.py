import datetime

from mongoengine import Document, fields, NULLIFY, CASCADE


class Node(Document):
    uid = fields.IntField(required=True, min_value=1)
    #unix permission.
    perm = fields.StringField(default='666')
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
    # We can use access_levels instead of groups.
    access_level = fields.ListField()

    meta = {
        'allow_inheritance': True
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

    def get_kind(self):
        return self.__class__.__name__.lower()


class Resource(Document):
    kind = fields.StringField(max_length=50)
    # timestamp.
    created = fields.DateTimeField()
    # timestamp.
    updated = fields.DateTimeField(default=datetime.datetime.utcnow())
    # Parent record. Mongo object id. We don't have resource parents
    parent = fields.ReferenceField('Node', reverse_delete_rule=CASCADE,
                                   required=True)

    meta = {
        'allow_inheritance': True
    }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.utcnow()
        self.kind = self.get_kind()
        return super(Resource, self).save(*args, **kwargs)

    def get_kind(self):
        return self.__class__.__name__.lower()
