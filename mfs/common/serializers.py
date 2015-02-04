from __future__ import unicode_literals

from mongoengine.errors import ValidationError as me_ValidationError
from mongoengine import fields as me_fields
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str

from rest_framework import serializers
from bson.errors import InvalidId

from mongoengine import dereference
from mongoengine.base.document import BaseDocument
from mongoengine.document import Document
from mongoengine.fields import ObjectId
from django.db import models
from django.forms import widgets
from django.core.exceptions import ImproperlyConfigured

from collections import OrderedDict

from rest_framework import fields as drf_fields
from rest_framework_mongoengine.utils import get_field_info
import copy

kinds_registry = {}


def cast_serializer(model_kind):
    # Returns serializers class by model.
    return kinds_registry.get(model_kind)


def raise_errors_on_nested_writes(method_name, serializer, validated_data):
    """
    *** inherited from DRF 3, altered for EmbeddedDocumentSerializer to work automagically ***

    Give explicit errors when users attempt to pass writable nested data.

    If we don't do this explicitly they'd get a less helpful error when
    calling `.save()` on the serializer.

    We don't *automatically* support these sorts of nested writes because
    there are too many ambiguities to define a default behavior.

    Eg. Suppose we have a `UserSerializer` with a nested profile. How should
    we handle the case of an update, where the `profile` relationship does
    not exist? Any of the following might be valid:

    * Raise an application error.
    * Silently ignore the nested part of the update.
    * Automatically create a profile instance.
    """

    # Ensure we don't have a writable nested field. For example:
    #
    # class UserSerializer(ModelSerializer):
    #     ...
    #     profile = ProfileSerializer()
    assert not any(
        isinstance(field, serializers.BaseSerializer) and
        not isinstance(field, EmbeddedDocumentSerializer) and
        (key in validated_data)
        for key, field in serializer.fields.items()
    ), (
        'The `.{method_name}()` method does not support writable nested'
        'fields by default.\nWrite an explicit `.{method_name}()` method for '
        'serializer `{module}.{class_name}`, or set `read_only=True` on '
        'nested serializer fields.'.format(
            method_name=method_name,
            module=serializer.__class__.__module__,
            class_name=serializer.__class__.__name__
        )
    )

    # Ensure we don't have a writable dotted-source field. For example:
    #
    # class UserSerializer(ModelSerializer):
    #     ...
    #     address = serializer.CharField('profile.address')
    assert not any(
        '.' in field.source and (key in validated_data)
        for key, field in serializer.fields.items()
    ), (
        'The `.{method_name}()` method does not support writable dotted-source '
        'fields by default.\nWrite an explicit `.{method_name}()` method for '
        'serializer `{module}.{class_name}`, or set `read_only=True` on '
        'dotted-source serializer fields.'.format(
            method_name=method_name,
            module=serializer.__class__.__module__,
            class_name=serializer.__class__.__name__
        )
    )


class DocumentField(serializers.Field):
    """
    Base field for Mongoengine fields that we can not convert to DRF fields.

    To Users:
        - You can subclass DocumentField to implement custom (de)serialization
    """

    type_label = 'DocumentField'

    def __init__(self, *args, **kwargs):
        try:
            self.model_field = kwargs.pop('model_field')
        except KeyError:
            raise ValueError("%s requires 'model_field' kwarg" % self.type_label)

        super(DocumentField, self).__init__(*args, **kwargs)

    def transform_document(self, document, depth):
        data = {}

        # serialize each required field
        for field in document._fields:
            if hasattr(document, smart_str(field)):
                # finally check for an attribute 'field' on the instance
                obj = getattr(document, field)
            else:
                continue

            val = self.transform_object(obj, depth-1)

            if val is not None:
                data[field] = val

        return data

    def transform_dict(self, obj, depth):
        return dict([(key, self.transform_object(val, depth-1))
                     for key, val in obj.items()])

    def transform_object(self, obj, depth):
        """
        Models to natives
        Recursion for (embedded) objects
        """
        if isinstance(obj, BaseDocument):
            # Document, EmbeddedDocument
            if depth == 0:
                # Return primary key if exists, else return default text
                return smart_str(getattr(obj, 'pk', 'Max recursion depth exceeded'))
            return self.transform_document(obj, depth)
        elif isinstance(obj, dict):
            # Dictionaries
            return self.transform_dict(obj, depth)
        elif isinstance(obj, list):
            # List
            return [self.transform_object(value, depth) for value in obj]
        elif obj is None:
            return None
        else:
            return smart_str(obj) if isinstance(obj, ObjectId) else obj

    def to_internal_value(self, data):
        return self.model_field.to_python(data)

    def to_representation(self, value):
        return self.transform_object(value, 1)


class ReferenceField(DocumentField):
    """
    For ReferenceField.
    We always dereference DBRef object before serialization
    TODO: Maybe support DBRef too?
    """

    type_label = 'ReferenceField'

    def __init__(self, *args, **kwargs):
        self.depth = kwargs.pop('depth')
        super(ReferenceField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            dbref = self.model_field.to_python(data)
        except InvalidId:
            raise ValidationError(self.error_messages['invalid'])
        instance = dereference.DeReference()([dbref])[0]

        # Check if dereference was successful
        if not isinstance(instance, Document):
            msg = self.error_messages['invalid']
            raise ValidationError(msg)

        return instance

    def to_representation(self, value):
        return self.transform_object(value, self.depth - 1)


class ListField(DocumentField):

    type_label = 'ListField'

    def __init__(self, *args, **kwargs):
        self.depth = kwargs.pop('depth')
        super(ListField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        return self.model_field.to_python(data)

    def to_representation(self, value):
        return self.transform_object(value, self.depth - 1)


class EmbeddedDocumentField(DocumentField):

    type_label = 'EmbeddedDocumentField'

    def __init__(self, *args, **kwargs):
        try:
            self.document_type = kwargs.pop('document_type')
        except KeyError:
            raise ValueError("EmbeddedDocumentField requires 'document_type' kwarg")

        super(EmbeddedDocumentField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        if value is None:
            return None
        else:
            return self.transform_object(value, self.depth)

    def to_internal_value(self, data):
        return self.model_field.to_python(data)


class DynamicField(DocumentField):

    type_label = 'DynamicField'

    def __init__(self, field_name=None, source=None, *args, **kwargs):
        super(DynamicField, self).__init__(*args, **kwargs)
        self.field_name = field_name
        self.source = source
        if source:
            self.source_attrs = self.source.split('.')

    def to_representation(self, value):
        return self.model_field.to_python(value)


class ObjectIdField(DocumentField):

    type_label = 'ObjectIdField'

    def to_representation(self, value):
        return smart_str(value)

    def to_internal_value(self, data):
        return ObjectId(data)


class BinaryField(DocumentField):

    type_label = 'BinaryField'

    def __init__(self, **kwargs):
        try:
            self.max_bytes = kwargs.pop('max_bytes')
        except KeyError:
            raise ValueError('BinaryField requires "max_bytes" kwarg')
        super(BinaryField, self).__init__(**kwargs)

    def to_representation(self, value):
        return smart_str(value)

    def to_internal_value(self, data):
        return super(BinaryField, self).to_internal_value(smart_str(data))


class BaseGeoField(DocumentField):

    type_label = 'BaseGeoField'


class DecimalFieldProxy(drf_fields.DecimalField):

    def __init__(self, max_value=None, min_value=None, **kwargs):
        super(DecimalFieldProxy, self).__init__(1000000, 2, None, max_value, min_value, **kwargs)


class DocumentSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super(DocumentSerializer, self).__init__(instance=instance, data=data, **kwargs)
        if not hasattr(self.Meta, 'model'):
            raise AssertionError('You should set `model` attribute on %s.' % type(self).__name__)

    MAX_RECURSION_DEPTH = 5  # default value of depth
    field_mapping = {
        me_fields.FloatField: drf_fields.FloatField,
        me_fields.IntField: drf_fields.IntegerField,
        me_fields.DateTimeField: drf_fields.DateTimeField,
        me_fields.EmailField: drf_fields.EmailField,
        me_fields.URLField: drf_fields.URLField,
        me_fields.StringField: drf_fields.CharField,
        me_fields.BooleanField: drf_fields.BooleanField,
        me_fields.FileField: drf_fields.FileField,
        me_fields.ImageField: drf_fields.ImageField,
        me_fields.UUIDField: drf_fields.CharField,
        me_fields.DecimalField: DecimalFieldProxy
    }

    _drfme_field_mapping = {
        me_fields.ObjectIdField: ObjectIdField,
        me_fields.ReferenceField: ReferenceField,
        me_fields.ListField: ListField,
        me_fields.EmbeddedDocumentField: EmbeddedDocumentField,
        me_fields.DynamicField: DynamicField,
        me_fields.DictField: DocumentField,
        me_fields.BinaryField: BinaryField,
        me_fields.GeoPointField: BaseGeoField,
        me_fields.PointField: BaseGeoField,
        me_fields.PolygonField: BaseGeoField,
        me_fields.LineStringField: BaseGeoField
    }

    field_mapping.update(_drfme_field_mapping)

    embedded_document_serializer_fields = []

    def get_validators(self):
        validators = getattr(getattr(self, 'Meta', None), 'validators', [])
        return validators

    def is_valid(self, raise_exception=False):
        """
        Call super.is_valid() and then apply embedded document serializer's validations.
        """
        valid = super(DocumentSerializer, self).is_valid(raise_exception=raise_exception)

        for embedded_field in self.embedded_document_serializer_fields:
            embedded_field._initial_data = self.validated_data.pop(embedded_field.field_name, serializers.empty)
            valid &= embedded_field.is_valid(raise_exception=raise_exception)

        return valid

    def get_fields(self):
        """
        Get fields.
        Inherited mostly from DRF 3 get_fields()
        and then altered for Mongoengine compability.
        Mosts of the code could be unnecessary or irrelevant.
        Needs a lot of refactor
        """
        declared_fields = copy.deepcopy(self._declared_fields)

        ret = OrderedDict()
        model = getattr(self.Meta, 'model')
        fields = getattr(self.Meta, 'fields', None)
        exclude = getattr(self.Meta, 'exclude', None)
        depth = getattr(self.Meta, 'depth', 0)
        extra_kwargs = getattr(self.Meta, 'extra_kwargs', {})

        if fields and not isinstance(fields, (list, tuple)):
            raise TypeError(
                'The `fields` option must be a list or tuple. Got %s.' %
                type(fields).__name__
            )

        if exclude and not isinstance(exclude, (list, tuple)):
            raise TypeError(
                'The `exclude` option must be a list or tuple. Got %s.' %
                type(exclude).__name__
            )

        assert not (fields and exclude), "Cannot set both 'fields' and 'exclude'."

        extra_kwargs = self._include_additional_options(extra_kwargs)

        # # Retrieve metadata about fields & relationships on the model class.
        info = get_field_info(model)

        # Use the default set of field names if none is supplied explicitly.
        if fields is None:
            fields = self._get_default_field_names(declared_fields, info)
            exclude = getattr(self.Meta, 'exclude', None)
            if exclude is not None:
                for field_name in exclude:
                    fields.remove(field_name)

        # Determine the set of model fields, and the fields that they map to.
        # We actually only need this to deal with the slightly awkward case
        # of supporting `unique_for_date`/`unique_for_month`/`unique_for_year`.
        model_field_mapping = {}
        embedded_list = []
        for field_name in fields:
            if field_name in declared_fields:
                field = declared_fields[field_name]
                source = field.source or field_name
                if isinstance(field, EmbeddedDocumentSerializer):
                    embedded_list.append(field)
            else:
                try:
                    source = extra_kwargs[field_name]['source']
                except KeyError:
                    source = field_name
            # Model fields will always have a simple source mapping,
            # they can't be nested attribute lookups.
            if '.' not in source and source != '*':
                model_field_mapping[source] = field_name

        self.embedded_document_serializer_fields = embedded_list

        # Determine if we need any additional `HiddenField` or extra keyword
        # arguments to deal with `unique_for` dates that are required to
        # be in the input data in order to validate it.
        hidden_fields = {}

        # Now determine the fields that should be included on the serializer.
        for field_name in fields:
            if field_name in declared_fields:
                # Field is explicitly declared on the class, use that.
                ret[field_name] = declared_fields[field_name]
                continue

            elif field_name in info.fields_and_pk:
                # Create regular model fields.
                model_field = info.fields_and_pk[field_name]
                try:
                    field_cls = self.field_mapping[model_field.__class__]
                except KeyError:
                    raise KeyError('%s is not supported, yet. Please open a ticket regarding '
                                   'this issue and have it fixed asap.\n'
                                   'https://github.com/umutbozkurt/django-rest-framework-mongoengine/issues/' %
                                   type(model_field))

                kwargs = self.get_field_kwargs(model_field)
                if 'choices' in kwargs:
                    # Fields with choices get coerced into `ChoiceField`
                    # instead of using their regular typed field.
                    field_cls = drf_fields.ChoiceField
                if not issubclass(field_cls, drf_fields.CharField) and not issubclass(field_cls, drf_fields.ChoiceField):
                    # `allow_blank` is only valid for textual fields.
                    kwargs.pop('allow_blank', None)

            elif hasattr(model, field_name):
                # Create a read only field for model methods and properties.
                field_cls = drf_fields.ReadOnlyField
                kwargs = {}

            else:
                raise ImproperlyConfigured(
                    'Field name `%s` is not valid for model `%s`.' %
                    (field_name, model.__class__.__name__)
                )

            # Check that any fields declared on the class are
            # also explicitly included in `Meta.fields`.
            missing_fields = set(declared_fields.keys()) - set(fields)
            if missing_fields:
                missing_field = list(missing_fields)[0]
                raise ImproperlyConfigured(
                    'Field `%s` has been declared on serializer `%s`, but '
                    'is missing from `Meta.fields`.' %
                    (missing_field, self.__class__.__name__)
                )

            # Populate any kwargs defined in `Meta.extra_kwargs`
            extras = extra_kwargs.get(field_name, {})
            if extras.get('read_only', False):
                for attr in [
                    'required', 'default', 'allow_blank', 'allow_null',
                    'min_length', 'max_length', 'min_value', 'max_value',
                    'validators', 'queryset'
                ]:
                    kwargs.pop(attr, None)

            if extras.get('default') and kwargs.get('required') is False:
                kwargs.pop('required')

            kwargs.update(extras)
            # Create the serializer field.
            ret[field_name] = field_cls(**kwargs)

        for field_name, field in hidden_fields.items():
            ret[field_name] = field

        return ret

    def get_field_kwargs(self, model_field):
        """
        Get kwargs that will be used for validation/serialization
        """
        kwargs = {}

        if type(model_field) in self._drfme_field_mapping:
            kwargs['model_field'] = model_field

        if type(model_field) in (me_fields.ReferenceField, me_fields.GenericReferenceField,
                                 me_fields.ListField):
            kwargs['depth'] = getattr(self.Meta, 'depth', self.MAX_RECURSION_DEPTH)

        if type(model_field) is me_fields.ObjectIdField:
            kwargs['required'] = False
        else:
            kwargs['required'] = model_field.required

        if type(model_field) is me_fields.EmbeddedDocumentField:
            kwargs['document_type'] = model_field.document_type

        if model_field.default:
            kwargs['required'] = False
            kwargs['default'] = model_field.default

        if model_field.__class__ == models.TextField:
            kwargs['widget'] = widgets.Textarea

        attribute_dict = {
            me_fields.StringField: ['max_length'],
            me_fields.DecimalField: ['min_value', 'max_value'],
            me_fields.EmailField: ['max_length'],
            me_fields.FileField: ['max_length'],
            me_fields.URLField: ['max_length'],
            me_fields.BinaryField: ['max_bytes']
        }

        if model_field.__class__ in attribute_dict:
            attributes = attribute_dict[model_field.__class__]
            for attribute in attributes:
                kwargs.update({attribute: getattr(model_field, attribute)})

        return kwargs

    def create(self, validated_data):
        """
        Create an instance using queryset.create()
        Before create() on self, call EmbeddedDocumentSerializer's create() first. If exists.
        """
        raise_errors_on_nested_writes('create', self, validated_data)

        # Automagically create and set embedded documents to validated data
        for embedded_field in self.embedded_document_serializer_fields:
            embedded_doc_intance = embedded_field.create(embedded_field.validated_data)
            validated_data[embedded_field.field_name] = embedded_doc_intance

        ModelClass = self.Meta.model
        try:
            instance = ModelClass(**validated_data)
            instance.save()
        except TypeError as exc:
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception text was: %s.' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    type(self).__name__,
                    exc
                )
            )
            raise TypeError(msg)
        except me_ValidationError as exc:
            msg = (
                'Got a `ValidationError` when calling `%s.objects.create()`. '
                'This may be because request data satisfies serializer validations '
                'but not Mongoengine`s. You may need to check consistency between '
                '%s and %s.\nIf that is not the case, please open a ticket '
                'regarding this issue on https://github.com/umutbozkurt/django-rest-framework-mongoengine/issues'
                '\nOriginal exception was: %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    type(self).__name__,
                    exc
                )
            )
            raise me_ValidationError(msg)

        return instance

    def update(self, instance, validated_data):
        """
        Update embedded fields first, set relevant attributes with updated data
        And then continue regular updating
        """
        for embedded_field in self.embedded_document_serializer_fields:
            embedded_doc_intance = embedded_field.update(getattr(instance, embedded_field.field_name), embedded_field.validated_data)
            setattr(instance, embedded_field.field_name, embedded_doc_intance)

        return super(DocumentSerializer, self).update(instance, validated_data)


class DynamicDocumentSerializer(DocumentSerializer):
    """
    DocumentSerializer adjusted for DynamicDocuments.
    """
    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        After calling super, we handle dynamic data which is not handled by super class
        """
        ret = super(DocumentSerializer, self).to_internal_value(data)
        [drf_fields.set_value(ret, [k], data[k]) for k in data if k not in ret]
        return ret

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        Serialize regular + dynamic fields
        """
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if not field.write_only]
        fields += self._get_dynamic_fields(instance).values()

        for field in fields:
            attribute = field.get_attribute(instance)
            if attribute is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    def _get_dynamic_fields(self, document):
        dynamic_fields = {}
        if document is not None and document._dynamic:
            for name, field in document._dynamic_fields.items():
                dynamic_fields[name] = DynamicField(field_name=name, source=name, **self.get_field_kwargs(field))
        return dynamic_fields


class EmbeddedDocumentSerializer(DocumentSerializer):
    """
    A DocumentSerializer adjusted to have extended control over serialization and validation of EmbeddedDocuments.
    """

    def create(self, validated_data):
        """
        EmbeddedDocuments are not saved separately, so we create an instance of it.
        """
        raise_errors_on_nested_writes('create', self, validated_data)
        return self.Meta.model(**validated_data)

    def update(self, instance, validated_data):
        """
        EmbeddedDocuments are not saved separately, so we just update the instance and return it.
        """
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance

    def _get_default_field_names(self, declared_fields, model_info):
        """
        EmbeddedDocuments don't have `id`s so do not include `id` to field names
        """
        return (
            list(declared_fields.keys()) +
            list(model_info.fields.keys()) +
            list(model_info.forward_relations.keys())
        )


class MongoEngineModelSerializer(DocumentSerializer):
    """
    Model Serializer that supports Mongoengine
    """
    def __init__(self, instance=None, data=None, **kwargs):

        global kinds_registry
        kinds_registry[self.__class__.Meta.model.get_kind()] = self.__class__

        return super(MongoEngineModelSerializer, self).__init__(
            instance, data, **kwargs)

