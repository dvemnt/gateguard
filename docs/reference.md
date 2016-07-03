title:      Reference
prev_title: Installation
prev_url:   install


# Using Gateguard #

## The Basics ##

```python
from gateguard import Schema, IntegerField, StringField


class MySchema(Schema):

    pk = IntegerField(min_value=1)
    name = StringField(required=False)
    surname = StringField(max_length=20)

data = {
    'pk': 'p',
    'name': 'Milli',
}

try:
    MySchema.validate(data)
except MySchema.ValidationError as e:
    print(e.error)

>>> {"pk": "Value must be a valid integer", "surname": "Value is required"}
```
