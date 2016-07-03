# Gateguard #
*Schema-based validation package*

[![Build Status](https://travis-ci.org/pyvim/gateguard.svg)](https://travis-ci.org/pyvim/gateguard)
[![Coverage Status](https://coveralls.io/repos/github/pyvim/gateguard/badge.svg?branch=master)](https://coveralls.io/github/pyvim/gateguard?branch=master)
[![PyPI](http://img.shields.io/pypi/v/gateguard.svg?style=flat)](https://pypi.python.org/pypi/gateguard)
[![Documentation Status](http://readthedocs.org/projects/gateguard/badge/?version=latest)](http://gateguard.readthedocs.org/en/latest/?badge=latest)

## Installation ##

`pip install gateguard`

## Usage ##

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

## Documentation ##
[Read the Docs](http://gateguard.readthedocs.org/)

## Tests ##
```bash
tox
```

## Changelog ##
See [releases](https://github.com/pyvim/gateguard/releases)

## License ##
See [LICENSE](https://github.com/pyvim/gateguard/blob/master/LICENSE)
