About
=====

I wrote this because I could not find a decent validation library for Python. This does precisely what the title suggests; it makes it easier to manage input validation in Python.

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

    from validator.core import *
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


Unit Tests Usage
================


Questions
=========

The best place to ask questions would be in the `Issues` section.

History
=======

 * 0.1  Initial release