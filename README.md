About
=====

I wrote this because I could not find a decent validation library for Python. This does precisely what the title suggests; it makes it easier to manage input validation in Python.

There are a handful of other validation libraries out there, but they are all either dated or require you to work your head around some strange syntax. This is the package you want to use when you don't want waste precious time thinking about how the validator should work; it's all in plain English.

Requirements
============

Tested on Python 2.6 and 2.7 -- it'll probably work on earlier versions.

Installation
============

Installing this package should be as easy as doing the following:

    > git clone git://github.com/wilhelm-murdoch/Validator.git && python Validator/setup.py install

Once this package gets a bit more polished, it will be submitted to PyPi and you should be able to use `pip` or `easy_install`.

Example
=======

The following example shows how you would validate a standard user account with `username`, `email` and `password` fields using some built-in validation rules and their default error messages:

    from validator.core import Validator, Field
    from validator.rules import *

    results = Validator().append([
        Field('username', 'wilhelm').append([
            IsRequired(), IsAlphaNumeric(), IsLengthBetween(3, 10)
        ]),
        Field('email', 'wilhelm@gmail.com').append([
            IsRequired(), IsEmail()
        ]),
        Field('password', 'root').append([
            IsRequired(), IsLengthBetween(2, 10)
        ]),
        Field('password-confirm', 'root').append([
            Matches('root')
        ]),
    ]).run(True)

Here is the output of `results`:

    >>> print results

    [{
        'field': 'username',
        'passed': True,
        'value': 'wilhelm'
    }, {
        'field': 'email',
        'passed': True,
        'value': 'wilhelm.murdoch@gmail.com'
    }, {
        'field': 'password',
        'passed': True,
        'value': 'root'
    }, {
        'field': 'password-confirm',
        'passed': True,
        'value': 'root'
    }]


Usage
=========

Supported Rules
===============

Extending
=========

Writing your own rules is quite simple. You just have to make sure your own rules derive from class `validator.core.Rule`. 

Here's a simple example:

    from validator.core import Rule
    
    class IsFoo(Rule):
        def run(self, field_value):
            if field_value is 'foo':
                return True
            return False

There you go, it's as easy as that. Now, let's test it out:

    from validator.core import Validator, Field
    from some.path.in.your.app import IsFoo
    
    results = Validator().append([
        Field('field_name', 'foo').append([
            IsFoo()
        ])
    ]).run()

The validator will now check if `field_name` equals `foo`. The result of the validation is stored in `results`:

    >>> print results
    True
    
Of course, setting `return_collated_results` to `True` in `Validator.run()` will return some more useful information:

    >>> print results
    [{'field': 'field_name', 'passed': True, 'value': 'foo'}]

Unit Tests Usage
================


Questions
=========

The best place to ask questions would be in the `Issues` section.

Contributions
=============

A helping hand is always welcome. The current build includes a fair amount of built-in validation rules, but it could always use a few more. If you find what's available to be a bit lacking, feel free to fork and submit a pull request.

All I ask is the following:

* Consistency. Try your best to follow the same coding style in use.
* Documentation. Document all the things!
* Tests. Please write functional and unit tests where and when possible.

History
=======

 * 0.1  Initial release