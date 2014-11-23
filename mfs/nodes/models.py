import datetime

from mongoengine import Document, fields, NULLIFY, CASCADE

from mfs.common.lib import address_to_geo


class Node(Document):
    meta = {
        'allow_inheritance': True
    }

    uid = fields.IntField(required=True, min_value=1)
    #unix permission.
    perm = fields.StringField(default='666')
    # dot separated path of entity's ids.
    path = fields.StringField(max_length=3000)
    kind = fields.StringField(max_length=15)
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

    def get_kind(self):
        return self.__class__.__name__.lower()

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


class Resource(Document):
    meta = {
        'allow_inheritance': True
    }

    kind = fields.StringField(max_length=15)
    # timestamp.
    created = fields.DateTimeField()
    # timestamp.
    updated = fields.DateTimeField(default=datetime.datetime.utcnow())
    # Parent record. Mongo object id. We don't have resource parents
    parent = fields.ReferenceField('Node', reverse_delete_rule=CASCADE,
                                   required=True)
    # Some name can be used to determine an object.
    tag = fields.StringField()

    def get_kind(self):
        return self.__class__.__name__.lower()

    def get_tag(self):
        return self.get_kind()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.utcnow()
        self.kind = self.get_kind()
        self.tag = self.tag if self.tag else self.get_tag()

        return super(Resource, self).save(*args, **kwargs)


#Used for geospacial requests
class GeoResource(Resource):
    geo_location = fields.GeoPointField()

    def resolve_to_geo(self, *args):
        self.geo_location = address_to_geo(*args)

    meta = {
        'indexes': [("location", "2dsphere"),]
    }

#Used for similarity search.
class SearchVector(Resource):

    def normalize(self, data):
        """Returns normal of a vector to optimize searching."""
        pass

