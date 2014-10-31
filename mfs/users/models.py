from mongoengine import Document, fields


class MongoUser(Document):
    resume = fields.StringField(max_length=100000)
    # User id.
    id = fields.IntField(required=True, primary_key=True)