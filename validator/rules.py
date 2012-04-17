#!/usr/bin/env python

from validator.core import Rule
import re

""" Core Rules Module

Contains a comprehensive list of built-in validator rules.
"""

class Matches(Rule):
    """ Simple rule used to determine whether one value matches another. Commonly used
    for password confirmation. """

    match = ''
    """ The value to compare against the associated field's value. """

    def __init__(self, match, error = None):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        match str -- The value to compare against the associated field's value.
        error str -- A user-defined error messaged for a failed rule. (optional)
        """
        super(Matches, self).__init__(error)
        self.match = match


    def run(self, field_value):
        """ Invoked once a defined rule is ready to be validated.

        Keyword arguments:
        field_value str -- the value of the associated field to compare.
        """

        if self.match != field_value:
            if not self.error:
                self.error = "Values `%s` and `%s` do not match." % (field_value, self.match)
            return False
        return True



class Regex(Rule):
    """ Applies a regular expression to a given field value. """

    expression = ''
    """ The regular expression to apply. """

    def __init__(self, expression, error = None):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        expression str -- The regular expression to apply to the given field.
        error str      -- A user-defined error messaged for a failed rule. (optional)
        """
        super(Regex, self).__init__(error)
        self.expression = expression


    def run(self, field_value):
        """ Invoked once a defined rule is ready to be validated.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if not self.expression:
            raise ValueError, 'This rule requires a regular expression.'

        try:
            regex = re.compile(self.expression)

            if not regex.match(field_value):
                if not self.error:
                    self.error = "Expression `%s` failed when applied to `%s`" % (self.expression, field_value)
                return False
        except Exception, e:
            raise ValueError, "Expression `%s` failed with the following error: %s" % (self.expression, e)
        return True



class IsEmail(Regex):
    """ Regex convenience derivative class used to determine if given field value is a
    valid email address. """

    def __init__(self, error = None):
        super(IsEmail, self).__init__(r'^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', error)
        if not error:
            self.error = 'This is not a valid email address.'



class IsNumeric(Regex):
    """ Regex convenience derivative class used to determine if given field value is numeric-only. """

    def __init__(self, error = None):
        super(IsNumeric, self).__init__(r'^[0-9]+$', error)
        if not error:
            self.error = 'This is not a number.'



class IsAlpha(Regex):
    """ Regex convenience derivative class used to determine if given field value is alpha-only. """

    def __init__(self, error = None):
        super(IsAlpha, self).__init__(r'^[a-zA-Z]+$', error)
        if not error:
            self.error = 'This is not an alpha-only string.'



class IsAlphaNumeric(Regex):
    """ Regex convenience derivative class used to determine if given field value is alpha-numeric. """

    def __init__(self, error = None):
        super(IsAlphaNumeric, self).__init__(r'^[a-zA-Z0-9]+$', error)
        if not error:
            self.error = 'This is not an alpha-numeric string.'



class IsRequired(Rule):
    """ Used to determine if given field is empty. """

    def __init__(self, error = None):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        error str  -- A user-defined error messaged for a failed rule. (optional)
        """

        super(IsRequired, self).__init__(error)

    def run(self, field_value):
        """ Determines if field_value value is empty.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if not field_value:
            if not error:
                self.error = 'This field requires a value.'
            return False
        return True



class IsLength(Rule):
    """ Used to determine whether the given associated field value's character length equals
    the given maximum amount. """

    length = None
    """ Absolute maximum character length. """

    strip = False
    """ Determines whether to strip whitespace from either side of the given field value. """

    def __init__(self, length, strip = False, error = None):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        length int -- Absolute maximum character length.
        strip bool -- Used to strip whitespace from the given field value. (optional)
        error str  -- A user-defined error messaged for a failed rule. (optional)
        """

        super(IsLength, self).__init__(error)
        self.length = int(length)
        self.strip = bool(strip)

    def run(self, field_value):
        """ Determines if field_value character length equal self.length.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if len((field_value.strip() if self.strip else field_value)) != self.length:
            if not self.error:
                self.error = "String `%s` length does not equal `%d`" % (field_value, self.length)
            return False
        return True



class IsLengthBetween(Rule):
    """ Used to determine whether the given associated field value's character length is
    within the given range. """

    min = 0
    """ Absolute minimum character length. """

    max = 0
    """ Absolute maximum character length. """

    strip = False
    """ Determines whether to strip whitespace from either side of the given field value. """

    def __init__(self, min, max, strip = False, error = None):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        min int    -- Absolute minimum character length.
        max int    -- Absolute maximum character length.
        strip bool -- Used to strip whitespace from the given field value. (optional)
        error str  -- A user-defined error messaged for a failed rule. (optional)
        """

        super(IsLengthBetween, self).__init__(error)
        self.min = int(min)
        self.max = int(max)
        self.strip = bool(strip)

    def run(self, field_value):
        """ Determines if field_value character length is between self.min and self.max.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if self.min <= len((field_value.strip() if self.strip else field_value)) <= self.max:
            return True
        if not self.error:
            self.error = "String `%s` length is not within `%d` and `%d`" % (field_value, self.min, self.max)
        return False



class IsInList(Rule):
    """ Used to determine if the associated field's value exists within the specified list. """

    list = []
    """ A list that contains items that may, or may not, include the given field value. """

    strip = False
    """ Determines whether to strip whitespace from either side of the given field value. """

    def __init__(self, list, strip = False, error = None):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        list list  -- List containing values to evaluate.
        strip bool -- Used to strip whitespace from the given field value. (optional)
        error str  -- A user-defined error messaged for a failed rule. (optional)
        """

        super(IsInList, self).__init__(error)
        self.list = list
        self.strip = strip

    def run(self, field_value):
        """ Checks if field_value is included within self.list.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if (field_value.strip() if self.strip else field_value) not in self.list:
            if not self.error:
                self.error = "Value of `%s` is not within the list" % field_value
            return False
        return True



class IsType(Rule):
    """ Rule that compares the associated field's value against a specified data type. """

    type = None
    """ The type to compare the field value against. """

    def __init__(self, type, error = None):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        type mixed -- The type to compare the field value against.
        error str  -- A user-defined error messaged for a failed rule. (optional)
        """

        super(IsType, self).__init__(error)
        self.type = type

    def run(self, field_value):
        """ Compares field_value against self.type.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if not isinstance(field_value, self.type):
            if not self.error:
                self.error = "Type of `%s` is not of type `%s`" % (type(field_value), self.type)
            return False
        return True