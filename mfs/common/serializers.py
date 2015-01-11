import mongoengine

from mongoengine.errors import ValidationError
from rest_framework import serializers
from rest_framework import fields
from django.db import models
from django.forms import widgets
from django.utils.datastructures import SortedDict
from .fields import (ReferenceField, ListField, EmbeddedDocumentField,
                     DynamicField, ObjectIdField, PointField, DecimalField,
                     DateTimeField)


kinds_registry = {}


def cast_serializer(model_kind):
    # Returns serializers class by model.
    return kinds_registry.get(model_kind)


class MongoEngineModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer that supports Mongoengine
    """
    def __init__(self, instance=None, data=None, **kwargs):

        global kinds_registry
        kinds_registry[self.__class__.Meta.model.get_kind()] = self.__class__

        return super(MongoEngineModelSerializer, self).__init__(
            instance, data, **kwargs)
    #TODO. Investigate possibility to remove that function.
    def run_validation(self, attrs):
        """
        Rest Framework built-in validation + related model validations
        """
        self._errors = {}
        for field_name, field in self.fields.items():
            if field_name in self._errors:
                continue
            source = field.source or field_name
            if self.partial and source not in attrs:
                continue

            if field_name in attrs and hasattr(field, 'model_field'):
                try:
                    field.model_field.validate(attrs[field_name])
                except ValidationError as err:
                    self._errors[field_name] = str(err)
            try:
                validate_method = getattr(self, 'validate_%s' % field_name, None)
                if validate_method:
                    attrs[field_name] = validate_method(attrs[field_name])
            except serializers.ValidationError as err:
                self._errors[field_name] = self._errors.get(field_name, []) + list(err.messages)

        if not self._errors:
            try:
                attrs = self.validate(attrs)
            except serializers.ValidationError as err:
                if hasattr(err, 'message_dict'):
                    for field_name, error_messages in err.message_dict.items():
                        self._errors[field_name] = self._errors.get(field_name, []) + list(error_messages)
                elif hasattr(err, 'messages'):
                    self._errors['non_field_errors'] = err.messages

        return attrs

    def get_fields(self):
        model = getattr(self.Meta, 'model')
        fields = getattr(self.Meta, 'fields', None)
        declared_fields = model._fields

        ret = SortedDict()
        for field in fields:
            if field in declared_fields:
                ret[field] = self.get_field(declared_fields[field])

        read_only_fields = getattr(self.Meta, 'read_only_fields', None)
        if read_only_fields:
            for field_name in self.Meta.read_only_fields:
                assert field_name in ret,\
                "read_only_fields on '%s' included invalid item '%s'" %\
                (self.__class__.__name__, field_name)
                ret[field_name].read_only = True

        return ret

    def get_field(self, model_field):
        kwargs = {}

        if model_field.__class__ in (mongoengine.ReferenceField, mongoengine.EmbeddedDocumentField,
                                     mongoengine.ListField, mongoengine.DynamicField,
                                     mongoengine.ObjectIdField, mongoengine.PointField,
                                     mongoengine.DecimalField, mongoengine.DateTimeField):
            kwargs['model_field'] = model_field
            kwargs['depth'] = self.Meta.depth

        if not model_field.__class__ == mongoengine.ObjectIdField:
            kwargs['required'] = model_field.required

        if model_field.__class__ == mongoengine.EmbeddedDocumentField:
            kwargs['document_type'] = model_field.document_type

        if model_field.default:
            kwargs['required'] = False
            kwargs['default'] = model_field.default

        if model_field.__class__ == models.TextField:
            kwargs['widget'] = widgets.Textarea

        field_mapping = {
            mongoengine.FloatField: fields.FloatField,
            mongoengine.IntField: fields.IntegerField,
            mongoengine.DateTimeField: DateTimeField,
            mongoengine.EmailField: fields.EmailField,
            mongoengine.URLField: fields.URLField,
            mongoengine.StringField: fields.CharField,
            mongoengine.BooleanField: fields.BooleanField,
            mongoengine.ImageField: fields.ImageField,
            mongoengine.ObjectIdField: ObjectIdField,
            mongoengine.ReferenceField: ReferenceField,
            mongoengine.ListField: ListField,
            mongoengine.EmbeddedDocumentField: EmbeddedDocumentField,
            mongoengine.PointField: PointField,
            mongoengine.DynamicField: DynamicField,
            mongoengine.DecimalField: DecimalField,
            mongoengine.UUIDField: fields.CharField
        }

        attribute_dict = {
            mongoengine.StringField: ['max_length'],
            mongoengine.EmailField: ['max_length'],
            mongoengine.URLField: ['max_length'],
        }

        if model_field.__class__ in attribute_dict:
            attributes = attribute_dict[model_field.__class__]
            for attribute in attributes:
                kwargs.update({attribute: getattr(model_field, attribute)})
        return field_mapping[model_field.__class__](**kwargs)

    def create(self, validated_attrs):
        return self.Meta.model.objects.create(**validated_attrs)


