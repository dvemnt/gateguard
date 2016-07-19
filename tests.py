# coding=utf-8

import unittest

from gateguard import fields, Schema, ValidationError


class SchemaTest(unittest.TestCase):

    class TestSchema(Schema):

        pk = fields.IntegerField(min_value=1)
        name = fields.StringField(min_length=2)
        badges = fields.ArrayField(field=fields.StringField(), required=False)

    def test_validate(self):
        schema = self.TestSchema()

        data = schema.validate(
            {'pk': '1', 'name': 'Milli', 'badges': ['Beautiful']}
        )

        self.assertEqual(1, data['pk'])
        self.assertEqual('Milli', data['name'])
        self.assertEqual(['Beautiful'], data['badges'])

    def test_validate_method(self):

        class TestSchema(Schema):

            pk = fields.IntegerField(min_value=1)
            name = fields.StringField(min_length=2)
            badges = fields.ArrayField(field=fields.StringField())

            @staticmethod
            def validate_name(value):
                return value.upper()

        data = TestSchema.validate(
            {'pk': '1', 'name': 'Milli', 'badges': ['Beautiful']}
        )

        self.assertEqual(1, data['pk'])
        self.assertEqual('MILLI', data['name'])
        self.assertEqual(['Beautiful'], data['badges'])

    def test_validate__stop_on_error(self):

        def validator(value):
            if value < 2:
                raise ValidationError('error', 100)

        class TestSchema(Schema):

            pk = fields.IntegerField(min_value=1, validators=[validator])
            name = fields.StringField(min_length=2)

        with self.assertRaises(ValidationError) as context:
            TestSchema.validate({'pk': '1', 'name': 'M'}, stop_on_error=True)

        self.assertEqual(context.exception.error, {'pk': 'error'})
        self.assertEqual(context.exception.code, 100)

    def test_validate__invalid_pk(self):
        schema = self.TestSchema()

        with self.assertRaises(ValidationError) as context:
            schema.validate({'pk': 'a', 'name': 'Milli'})

        self.assertEqual(
            context.exception.error,
            {'pk': fields.IntegerField.default_error_messages['invalid']}
        )

    def test_validate__required_name(self):
        schema = self.TestSchema()

        with self.assertRaises(ValidationError) as context:
            schema.validate({'pk': '1'})

        self.assertEqual(
            context.exception.error,
            {'name': fields.Field.default_error_messages['required']}
        )

class FieldTest(unittest.TestCase):

    def test_init(self):
        field = fields.IntegerField(default='1')

        self.assertEqual(field.default, '1')
        self.assertEqual(field.validators, [])

    def test_init__empty(self):
        field = fields.IntegerField()

        self.assertEqual(field.default, None)
        self.assertEqual(field.validators, [])

    def test__validation__empty(self):
        field = fields.IntegerField(required=False)

        self.assertFalse(field.validate(None))

    def test__validation_error(self):
        field = fields.IntegerField(error_messages={'invalid': 'test'})

        with self.assertRaises(ValidationError) as context:
            field.validate('a')

        self.assertEqual(context.exception.error, 'test')

    def test__validation_error_required(self):
        field = fields.IntegerField()

        with self.assertRaises(ValidationError) as context:
            field.validate(None)

        self.assertEqual(
            context.exception.error,
            fields.Field.default_error_messages['required']
        )

    def test_is_valid(self):
        field = fields.Field()

        with self.assertRaises(NotImplementedError):
            field.is_valid(1)

    def test_to_representation(self):
        field = fields.Field()

        self.assertEqual(1, field.to_representation(1))

    def test_validate__with_validator(self):
        def validator(value):
            return 'True' if value else 'False'

        field = fields.BooleanField(validators=[validator])

        self.assertEqual('True', field.validate(True))

    def test_validate__with_validator__error(self):
        def validator(value):
            if value:
                raise ValidationError()

        field = fields.BooleanField(validators=[validator])

        with self.assertRaises(ValidationError) as context:
            field.validate(True)

        self.assertEqual(context.exception.error, None)


class BooleanFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.BooleanField()
        self.assertTrue(field.validate(True))

    def test_validate__invalid(self):
        field = fields.BooleanField()

        with self.assertRaises(ValidationError) as context:
            field.validate('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.BooleanField.default_error_messages['invalid']
        )


class StringFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.StringField()
        self.assertEqual('Test', field.validate('Test'))

    def test_validate__invalid(self):
        field = fields.StringField()

        with self.assertRaises(ValidationError) as context:
            field.validate(10)

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['invalid']
        )

    def test_validate__min_length(self):
        field = fields.StringField(min_length=5, default='test')

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['min_length'].format(
                field
            )
        )

    def test_validate__max_length(self):
        field = fields.StringField(max_length=3, default='test')

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['max_length'].format(
                field
            )
        )


class IntegerFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.IntegerField()
        self.assertEqual(10, field.validate('10'))

    def test_validate__invalid(self):
        field = fields.IntegerField()

        with self.assertRaises(ValidationError) as context:
            field.validate('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.IntegerField.default_error_messages['invalid']
        )

    def test_validate__min_value(self):
        field = fields.IntegerField(default=10, min_value=11)

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['min_value'].format(
                field
            )
        )

    def test_validate__max_value(self):
        field = fields.IntegerField(default=10, max_value=9)

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['max_value'].format(
                field
            )
        )


class FloatFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.FloatField()
        self.assertEqual(10.2, field.validate('10.2'))

    def test_validate__invalid(self):
        field = fields.FloatField()

        with self.assertRaises(ValidationError) as context:
            field.validate('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.FloatField.default_error_messages['invalid']
        )

    def test_validate__min_value(self):
        field = fields.FloatField(default=10.1, min_value=10.2)

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['min_value'].format(
                field
            )
        )

    def test_validate__max_value(self):
        field = fields.FloatField(default=10.11, max_value=10.10)

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['max_value'].format(
                field
            )
        )


class ChoiceFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.ChoiceField(choices=['a', 'b'])
        self.assertEqual('a', field.validate('a'))

    def test_validate__invalid(self):
        field = fields.ChoiceField(default='c', choices=['a', 'b'])

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ChoiceField.default_error_messages['invalid'].format(field)
        )


class MultipleChoiceFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.MultipleChoiceField(choices=['a', 'b'])
        self.assertEqual(['a'], field.validate(['a']))

    def test_validate__invalid(self):
        field = fields.MultipleChoiceField(default='c', choices=['a', 'b'])

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ArrayField.default_error_messages['invalid'].format(field)
        )

    def test_validate__choices(self):
        field = fields.MultipleChoiceField(default=['c'], choices=['a', 'b'])

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.MultipleChoiceField \
                .default_error_messages['choices'].format(field)
        )


class ArrayFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.ArrayField(field=fields.IntegerField())
        self.assertEqual([10], field.validate(['10']))

    def test_validate__invalid(self):
        field = fields.ArrayField(default='string')

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ArrayField.default_error_messages['invalid'].format(field)
        )

    def test_validate__invalid_item(self):
        field = fields.ArrayField(default=['j'], field=fields.IntegerField())

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ArrayField.default_error_messages['child'].format(
                index=0,
                message=fields.IntegerField.default_error_messages['invalid']
            )
        )


class URLFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.URLField()
        self.assertEqual(
            'https://pyvim.com/about/',
            field.validate('https://pyvim.com/about/')
        )

    def test_validate__invalid_type(self):
        field = fields.URLField(default=5)

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['invalid']
        )

    def test_validate__invalid(self):
        field = fields.URLField(default=':/wrong')

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.URLField.default_error_messages['url']
        )


class HostFieldTest(unittest.TestCase):

    def test_validate_ip(self):
        field = fields.HostField()
        self.assertEqual('144.76.78.182', field.validate('144.76.78.182'))

    def test_validate_url(self):
        field = fields.HostField()
        self.assertEqual('pyvim.com', field.validate('pyvim.com'))

    def test_validate__invalid_type(self):
        field = fields.HostField(default=5)

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['invalid']
        )

    def test_validate__invalid(self):
        field = fields.HostField(default=':/wrong')

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.HostField.default_error_messages['pattern'].format(field)
        )


class MapFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.MapField()
        self.assertEqual({'key': 'value'}, field.validate({'key': 'value'}))

    def test_validate__invalid_json(self):
        field = fields.MapField(default='wrong')

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.MapField.default_error_messages['invalid'].format(field)
        )

    def test_validate__invalid_type(self):
        field = fields.MapField(default=5)

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.MapField.default_error_messages['invalid'].format(field)
        )


class SlugFieldTest(unittest.TestCase):

    def test_validate(self):
        field = fields.SlugField()
        self.assertEqual('back-jack-100_1', field.validate('back-jack-100_1'))

    def test_validate__error(self):
        field = fields.SlugField(default='wrong slug')

        with self.assertRaises(ValidationError) as context:
            field.validate()

        self.assertEqual(
            context.exception.error,
            fields.SlugField.default_error_messages['pattern'].format(field)
        )
