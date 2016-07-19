# coding=utf-8

import collections

from .fields import Field
from .exceptions import ValidationError


class MetaSchema(type):

    @classmethod
    def __prepare__(mcs, *args, **kwargs):
        return collections.OrderedDict()

    def __new__(mcs, name, bases, attributes):
        fields = collections.OrderedDict()

        for parent in bases:
            if hasattr(parent, '__fields__'):
                fields.update(parent.__fields__)

        for name, field in attributes.items():
            if isinstance(field, Field):
                fields[name] = field

        for field in fields:
            attributes.pop(field, None)

        cls = type.__new__(mcs, name, bases, attributes)

        cls.__fields__ = fields
        cls.ValidationError = ValidationError

        return cls


class Schema(object, metaclass=MetaSchema):

    @classmethod
    def validate(cls, data, stop_on_error=False):
        errors = {}

        for name, field in cls.__fields__.items():
            try:
                value = data.get(name, field.default)
                value = field.validate(value)

                method = getattr(cls, 'validate_{}'.format(name), None)

                if method:
                    value = method(cls, value)

                data[name] = value

            except ValidationError as e:
                errors[name] = e.error

                if stop_on_error:
                    raise ValidationError(errors, e.code)

        if errors:
            raise ValidationError(errors)

        return data
