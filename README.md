[![Build Status](https://drone.io/github.com/wilhelm-murdoch/Validator/status.png)](https://drone.io/github.com/wilhelm-murdoch/Validator/latest) [![Code Health](https://landscape.io/github/wilhelm-murdoch/validator/master/landscape.png)](https://landscape.io/github/wilhelm-murdoch/validator/master)

### Validator
===

I wrote this because I could not find a validation for Python that didn't require some crazy dependencies, or wasn't plain simple to work with. This does precisely what the title suggests; it makes it easier to manage input validation in Python.

There are a handful of other validation libraries out there, but they are all either dated or require you to work your head around some strange syntax. This is the package you want to use when you don't want waste precious time thinking about how the validator should work; it's all in plain English.

Say you want to validator an online form. A form is just a `collection` of `fields`. These `fields` must follow certain `rules`. This is the naming convention used throughout the library.

## Installation

### From Source

If you plan on forking and doing some local development, follow these steps.

    $: git clone git@github.com:wilhelm-murdoch/validator.git
    $: cd validator
    $: python setup.py install

Alternatively, you can use the following make targets for local development:

1. `make install` installs validator locally in development mode.
2. `make uninstall` removes validator locally
3. `make test` runs the unit test suite
4. `make clean` removes any garbage files that usage and installation generates

### Using Pip

If you have pip installed, you should be able to run the following command:

    $: pip install validator
    
Or,

    $: pip install git+ssh://git@github.com/wilhelm-murdoch/validator.git

Or, you can add the following line to your `requirements.txt` file:

    -e git+git://github.com/wilhelm-murdoch/validator.git#egg=validator

## Examples

The following example shows how you would validate a standard user account with `username`, `email` and `password` fields using some built-in validation rules and their default error messages:

```python
from validator import collection, field, rules

form = collection.Collection().append([
    field.Field('username', 'wilhelm').append([
          rules.IsRequired()
        , rules.IsAlphaNumeric()
        , rules.IsLengthBetween(3, 10)
    ]),
    field.Field('email', 'wilhelm@gmail.com').append([
          rules.IsRequired()
        , rules.IsEmail()
    ]),
    field.Field('password', 'root').append([
          rules.IsRequired()
        , rules.IsLengthBetween(2, 10)
    ]),
    field.Field('password-confirm', 'root').append([
        rules.Matches('root')
    ])
])
```

Now, to run the validator, just do:

```python
>>> print form.run()
True
```

By default, method `collection.run` will return a boolean value representing the result of the validation. If you want more detailed information, you have a few options.

Once you've run the validation process. You can do the following:

```python
>>> print form.results()
[{
    'field': 'username',
    'passed': True,
    'value': 'wilhelm',
    'errors': None
}, {
    'field': 'email',
    'passed': True,
    'value': 'wilhelm.murdoch@gmail.com',
    'errors': None
}, {
    'field': 'password',
    'passed': True,
    'value': 'root',
    'errors': None
}, {
    'field': 'password-confirm',
    'passed': True,
    'value': 'root',
    'errors': None
}]
```

Or, you can just do:

```python
>>> print form.run(True)
... same output as above ...
```

If any fields don't pass validation, the results will provide a list of relevent errors associated with the field in question. For example:

```python
>>> print form.results()
[
    ...
    {
        'field': 'email',
        'passed': False,
        'errors': [
            'Length is too short',
            'Is not a valid email address',
            'Some other error'
        ]
        'value': 'bar'
    }
    ...
]
```

You can also specify a custom error message for your validation rule. For instance:

```python
from validator import collection, field, rules

form = collection.Collection().append([
    field.Field('username', 'wilhelm').append([
          rules.IsRequired(error='heh.')
        , rules.IsAlphaNumeric(error='lolwut?')
        , rules.IsLengthBetween(3, 10, error='It is either too long or too short, man.')
    ]),
])
```

If this form generated errors, you'd get the following output:

```python
>>> print form.results()
[
    ...
    {
        'field': 'username',
        'passed': False,
        'errors': [
            'heh.',
            'lolwut?',
            'It is either too long or too short, man.'
        ]
        'value': 'wilhelm'
    }
    ...
]
```

If you want only a list of fields that failed validation and their associated error messages, you can use do:

```python
>>> print results.errors()
{
    'username': [
        'heh.',
        'lolwut?',
        'It is either too long or too short, man.'
    ]
}
```

If you want to return a JSON representation of your form, you can do the following:

```python
>>> print form.form()
{
    'username': 'wilhelm',
    'password': 'root',
    'password-confirm': 'root',
    'email': 'wilhelm@gmail.com'
}
```

Both classes `validator.collection.Collection` and `validator.rule.Rule` implement the following Python built-ins:

* __len__
* __iter__
* __getitem__

## Extending

Writing your own rules is quite simple. You just have to make sure your own rules derive from class `validator.rule.Rule`. 

Here's a simple example:

```python
from validator import rule

class IsFoo(rule.Rule):
    def run(self, field_value):
        if field_value is 'foo':
            return True
        return False
```            

There you go, it's as easy as that. Now, let's test it out:

```python
from validator import collection, field
from some.path.in.your.app import IsFoo

results = collection.Collection().append([
    field.Field('field_name', 'foo').append([
        IsFoo()
    ])
]).run()
```

The validator will now check if `field_name` equals `foo`. The result of the validation is stored in `results`:

```python
>>> print results
True
```    
    
Of course, setting `return_collated_results` to `True` in `Collection.run()` will return some more useful information:

```python
>>> print results
[{
    'field': 'field_name',
    'passed': True,
    'value': 'foo'
}]
```

## Unit Tests Usage

Tests have been made with the use of Nose (https://github.com/nose-devs/nose). Just navigate to the testing directory of choice run the `make test` command to run the entire suite.

## Questions

The best place to ask questions would be in the `Issues` section or on Twitter [@wilhelm](http://twitter.com/wilhelm)

## Contributions

A helping hand is always welcome. The current build includes a fair amount of built-in validation rules, but it could always use a few more. If you find what's available to be a bit lacking, feel free to fork and submit a pull request.

All I ask is the following:

* Consistency. Try your best to follow the same coding style in use.
* Documentation. Document all the things!
* Tests. Please write functional and unit tests where and when possible.
