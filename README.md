[![Build Status](https://drone.io/github.com/wilhelm-murdoch/Validator/status.png)](https://drone.io/github.com/wilhelm-murdoch/Validator/latest) [![Code Health](https://landscape.io/github/wilhelm-murdoch/Validator/master/landscape.png)](https://landscape.io/github/wilhelm-murdoch/Validator/master)

# About

I wrote this because I could not find a decent validation library for Python. This does precisely what the title suggests; it makes it easier to manage input validation in Python.

There are a handful of other validation libraries out there, but they are all either dated or require you to work your head around some strange syntax. This is the package you want to use when you don't want waste precious time thinking about how the validator should work; it's all in plain English.

# Requirements

Tested on Python 2.6 and 2.7 -- it'll probably work on earlier versions.

# Installation

Installing this package should be as easy as doing the following:

    > git clone git://github.com/wilhelm-murdoch/Validator.git && python Validator/setup.py install

Once this package gets a bit more polished, it will be submitted to PyPi and you should be able to use `pip` or `easy_install`.

# Examples

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

# Core

## Validator()
Responsible for applying rules against the specified fields. Create an instance and start attaching fields to it. Think of a validator instance as a form you want to validate; forms have fields and fields have rules that must be followed.
### Methods
#### append(field)
Attaches an instance, or a list of instances, of class Field to the current instance of a validator.

* @field object|list - A single instance of class Field, or a list of instances.

Returns the current instance of class Validator.

#### results()
Simply returns the results of the last test run in the following format:

    [{
        'field': 'field_one',
        'passed': True,
        'value': 'foo'
    }, {
        'field': 'field_two',
        'passed': False,
        'errors': [
            'Length is too short',
            'Is not a valid email address',
            'Some other error'
        ]
        'value': 'bar'
    }]

Returns a list.

#### run(return_collated_results = False)
Iterates through all the associated fields and forces them to apply rules to their values. Returns True or False depending on whether all fields validated correctly. However, if the parameter `return_collated_results` is set to True, this method will return the results as shown in the `Validator.results()` method.

* @return_collated_results bool - Returns the result list of the validation process if set to True

Returns True, False or list of results.

## Field(title, value, stop_on_first_error = True)
Represents a single field with a title and associated value. Rules are attached to a field and then applied to the field's value.

* @title str - The title of this field.  
* @value mixed - The value associated with this field.  
* @stop_on_first_error bool - Will break out of applying rules when it first encounters an error.  

### Methods
#### append(rule)
Attaches an instance, or a list of instances, of class Rule to the current instance of a field.

* @rule object|list - A single instance of class Rule, or a list of instances.

Returns the current instance of class Field.

#### run()
Iterates through all the associated rules and forces them to apply rules to their values. Returns True or False depending on whether all fields validated correctly. However, if the parameter `return_collated_results` is set to True, this method will return the results as shown in the `Validator.results()` method.

Returns True or False with list of errors.

## Rule(error = None)
Rules are assigned to fields to test field values. Rules like, "Is this value a number?", "Is this a valid credit card number" or "Does this email address already exist within my database?".

* @error str - Custom error message for a failed rule. (optional)  

### Methods
#### run
Defines the rule to apply to a field value. The only requirement is that this method returns either True or False.

# Supported Rules

### Matches(match, error = None)
Simple rule used to determine whether one value matches another. Commonly used for password confirmation.  

* @match str - The value to compare against the associated field's value.  
* @error str - Custom error message for a failed rule. (optional)  

### Regex(expression, error = None)
Applies a regular expression to a given field value.  

* @expression str - The regular expression to be applied against the associated field's value.  
* @error str - Custom error message for a failed rule. (optional)  

### Regex < IsEmail(error = None)
Regex convenience derivative class used to determine if given field value is a valid email address.  

* @error str - Custom error message for a failed rule. (optional)  

### Regex < IsNumeric(error = None)
Regex convenience derivative class used to determine if given field value is numeric-only.  

* @error str - Custom error message for a failed rule. (optional)  

### Regex < IsAlpha(error = None)
Regex convenience derivative class used to determine if given field value is alpha-only.  

* @error str - Custom error message for a failed rule. (optional)  

### Regex < IsAlphaNumeric(error = None)
Regex convenience derivative class used to determine if given field value is alpha-numeric.  

* @error str - Custom error message for a failed rule. (optional)  

### Regex < IsRequired(error = None)
Regex convenience derivative class used to determine if given field is empty.  

* @error str - Custom error message for a failed rule. (optional)  

### IsLength(length, strip = False, error = None)
Used to determine whether the given associated field value's character length equals the given maximum amount.  

* @length int - Absolute maximum character length.  
* @strip bool - Used to strip whitespace from the given field value. (optional)  
* @error str - Custom error message for a failed rule. (optional)  

### IsLengthBetween(min, max, strip = False, error = None)
Used to determine whether the given associated field value's character length is within the given range.  

* @min int - Absolute minimum character length.  
* @max int - Absolute maximum character length.  
* @strip bool - Used to strip whitespace from the given field value. (optional)  
* @error str - A user-defined error messaged for a failed rule. (optional)

### IsInList(list, strip = False, error = None)
Used to determine if the associated field's value exists within the specified list.  

* @list list - List containing values to evaluate.  
* @error str - Custom error message for a failed rule. (optional)  

### IsType(type, error = None)
Rule that compares the associated field's value against a specified data type.  

* @type mixed - The type to compare the field value against.  
* @error str - Custom error message for a failed rule. (optional)  

# Extending

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

# Unit Tests Usage

Tests have been made with the use of Nose (https://github.com/nose-devs/nose). Just navigate to the testing directory of choice run the `nosetests` command to run the entire suite.

# Questions

The best place to ask questions would be in the `Issues` section or on Twitter @wilhelm

# Contributions

A helping hand is always welcome. The current build includes a fair amount of built-in validation rules, but it could always use a few more. If you find what's available to be a bit lacking, feel free to fork and submit a pull request.

All I ask is the following:

* Consistency. Try your best to follow the same coding style in use.
* Documentation. Document all the things!
* Tests. Please write functional and unit tests where and when possible.

# History

 * 0.1  Initial release
